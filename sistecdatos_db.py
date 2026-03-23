# sistecdatos_db.py
# UNIFIED DATABASE MANAGER FOR SISTECDATOSFEMA
# Combines basic functionality with advanced security and auditing.

import sqlite3
import os
import sys
from datetime import datetime, timedelta
import shutil
import hashlib
import json
import threading
import time
import logging
from logging.handlers import RotatingFileHandler

# ---- Resolución de ruta base compatible con PyInstaller (one-file y dev) ----
def _get_base_dir():
    """Retorna el directorio base correcto tanto en modo script como en exe compilado."""
    if getattr(sys, 'frozen', False):
        # Exe instalado: usar %APPDATA%\SISTECDATOSFEMA (siempre escribible por el usuario)
        return os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'SISTECDATOSFEMA')
    else:
        # Modo desarrollo: usar directorio del script
        return os.path.dirname(os.path.abspath(__file__))

_BASE_DIR = _get_base_dir()

# ---- Configuración de logging centralizado ----
_log_dir = os.path.join(_BASE_DIR, "data", "logs")
os.makedirs(_log_dir, exist_ok=True)
_log_file = os.path.join(_log_dir, "sistecdatos.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        RotatingFileHandler(_log_file, maxBytes=2_000_000, backupCount=3, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("sistecdatos.db")

PBKDF2_ITERATIONS = 100_000

class SISTECDATOSFEMADatabase:
    """Gestor unificado de base de datos SQLite para SISTECDATOSFEMA."""

    def __init__(self, db_name="sistecdatos_dictamenes.db"):
        # Carpeta de datos y backups
        self.data_dir = os.path.join(_BASE_DIR, "data")
        self.backup_dir = os.path.join(self.data_dir, "backups")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        self.db_path = os.path.join(self.data_dir, db_name)

        # Migración automática: copiar BD existente de la carpeta del exe si aún no existe
        if getattr(sys, 'frozen', False) and not os.path.exists(self.db_path):
            old_db = os.path.join(os.path.dirname(sys.executable), 'data', db_name)
            if os.path.exists(old_db):
                shutil.copy2(old_db, self.db_path)

        self.current_user = None
        self.session_start = None
        self.backup_timer = None
        
        self._connect()
        self._create_tables()
        self._init_default_data()
        self._start_backup_timer()

    def _connect(self):
        """Establece conexión con la base de datos"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self._lock = threading.Lock()

    def _create_tables(self):
        """Crea todas las tablas necesarias del sistema"""
        
        # Tabla principal de dictámenes (Versión Profesional unificada)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dictamenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dictamen TEXT NOT NULL UNIQUE,
                denuncia TEXT,
                imputado TEXT,
                ofendido TEXT,
                delito TEXT,
                sitio TEXT,
                antecedentes TEXT,
                tecnico TEXT,
                fecha TEXT NOT NULL,
                fiscal TEXT,
                agente TEXT,
                decomiso TEXT,
                tipo TEXT,
                cantidad TEXT,
                otro TEXT,
                unidad TEXT,
                estado_dictamen TEXT NOT NULL,
                fecha_estado TEXT,
                entregado_a TEXT,
                fecha_entrega TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_creacion TEXT,
                usuario_modificacion TEXT,
                activo INTEGER DEFAULT 1
            )
        ''')
        
        # Tabla de decomisos detallados
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS decomisos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dictamen_numero TEXT NOT NULL,
                tipo TEXT NOT NULL,
                cantidad REAL NOT NULL,
                unidad TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                categoria TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_modificacion TIMESTAMP,
                usuario_creacion TEXT,
                usuario_modificacion TEXT,
                activo INTEGER DEFAULT 1,
                FOREIGN KEY (dictamen_numero) REFERENCES dictamenes (dictamen)
            )
        ''')
        
        # Tabla de usuarios
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                nombre_completo TEXT,
                email TEXT,
                rol TEXT DEFAULT 'tecnico',
                activo INTEGER DEFAULT 1,
                intentos_fallidos INTEGER DEFAULT 0,
                bloqueado_hasta TIMESTAMP,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acceso TIMESTAMP,
                ultimo_cambio_password TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de auditoría
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT,
                accion TEXT NOT NULL,
                tabla_afectada TEXT,
                registro_id TEXT,
                datos_anteriores TEXT,
                datos_nuevos TEXT,
                fecha_accion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                detalles TEXT,
                nivel_criticidad TEXT DEFAULT 'INFO'
            )
        ''')
        
        # Tabla de sesiones
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sesiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                token_sesion TEXT UNIQUE,
                fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_ultimo_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                activa INTEGER DEFAULT 1,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Tabla de configuración
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                clave TEXT PRIMARY KEY,
                valor TEXT,
                tipo_dato TEXT DEFAULT 'string',
                descripcion TEXT,
                categoria TEXT DEFAULT 'general',
                fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_modificacion TEXT
            )
        ''')
        
        # Tabla de backups
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_archivo TEXT,
                ruta_completa TEXT,
                tamaño_bytes INTEGER,
                fecha_backup TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo_backup TEXT DEFAULT 'manual',
                usuario TEXT,
                exitoso INTEGER DEFAULT 1,
                observaciones TEXT
            )
        ''')

        # Columna debe_cambiar_password (se agrega si no existe para BDs antiguas)
        try:
            self.cursor.execute("ALTER TABLE usuarios ADD COLUMN debe_cambiar_password INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        # Índices para rendimiento
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_dictamenes_dictamen ON dictamenes (dictamen)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_dictamenes_activo ON dictamenes (activo)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_decomisos_dictamen ON decomisos (dictamen_numero)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_auditoria_usuario ON auditoria (usuario)")

        self.conn.commit()

    def _init_default_data(self):
        """Inicializa datos por defecto"""
        # Usuario admin (debe_cambiar_password=1 obliga a cambiar en primer acceso)
        self.cursor.execute('SELECT COUNT(*) FROM usuarios WHERE username = ?', ('admin',))
        if self.cursor.fetchone()[0] == 0:
            salt = self._generate_salt()
            password_hash = self._hash_password('admin123', salt)
            self.cursor.execute('''
                INSERT INTO usuarios (username, password_hash, salt, nombre_completo, rol, debe_cambiar_password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('admin', password_hash, salt, 'Administrador del Sistema', 'admin', 1))
        
        # Configuraciones default
        configuraciones = [
            ('backup_automatico', 'true', 'boolean', 'Backup automático al cerrar', 'sistema'),
            ('idioma', 'es', 'string', 'Idioma por defecto', 'interfaz'),
            ('separador_miles', ',', 'string', 'Separador de miles (Fer Rule)', 'formato'),
            ('separador_decimal', '.', 'string', 'Separador decimal (Fer Rule)', 'formato')
        ]
        for c in configuraciones:
            self.cursor.execute('INSERT OR IGNORE INTO configuracion VALUES (?,?,?,?,?, CURRENT_TIMESTAMP, "sistema")', c)
        
        self.conn.commit()

    def _generate_salt(self):
        import secrets
        return secrets.token_hex(32)

    def _hash_password(self, password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), PBKDF2_ITERATIONS).hex()

    def _start_backup_timer(self, interval_seconds=3600):
        """Programa un backup automático cada `interval_seconds` (default: 1 hora)."""
        def _do_backup():
            try:
                self._hacer_backup(tipo='automatico')
            except Exception as e:
                logger.error(f"Error en backup automático: {e}")
            finally:
                # Re-programar solo si la conexión sigue abierta
                if self.conn:
                    self.backup_timer = threading.Timer(interval_seconds, _do_backup)
                    self.backup_timer.daemon = True
                    self.backup_timer.start()

        self.backup_timer = threading.Timer(interval_seconds, _do_backup)
        self.backup_timer.daemon = True
        self.backup_timer.start()
        logger.info(f"Backup automático programado cada {interval_seconds // 60} minutos.")

    def _hacer_backup(self, tipo='manual'):
        """Copia la base de datos al directorio de backups."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre = f"backup_{tipo}_{timestamp}.db"
        destino = os.path.join(self.backup_dir, nombre)
        shutil.copy2(self.db_path, destino)
        tamaño = os.path.getsize(destino)
        user = self.current_user['username'] if self.current_user else 'sistema'
        try:
            self.cursor.execute('''
                INSERT INTO backups (nombre_archivo, ruta_completa, tamaño_bytes, tipo_backup, usuario)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, destino, tamaño, tipo, user))
            self.conn.commit()
        except sqlite3.Error as e:
            logger.warning(f"No se pudo registrar el backup en BD: {e}")
        logger.info(f"Backup '{nombre}' creado ({tamaño} bytes).")
        return destino

    # ---------- MÉTODOS DE COMPATIBILIDAD Y CRUD ----------

    def insert_dictamen(self, fila):
        """
        Inserta un dictamen.
        Compatibilidad: Si recibe una lista de 20 elementos, la mapea a los 21 campos.
        """
        try:
            if len(fila) == 20:
                # Mapear lista básica a campos profesionales
                # dictamen, denuncia, imputado, ofendido, delito, sitio,
                # antecedentes, tecnico, fecha, fiscal, agente, decomiso,
                # tipo, cantidad, otro, unidad, estado_dictamen, fecha_estado, entregado_a, fecha_entrega
                data = list(fila)
            else:
                data = fila

            query = "INSERT OR REPLACE INTO dictamenes (dictamen, denuncia, imputado, ofendido, delito, sitio, antecedentes, tecnico, fecha, fiscal, agente, decomiso, tipo, cantidad, otro, unidad, estado_dictamen, fecha_estado, entregado_a, fecha_entrega, usuario_creacion, usuario_modificacion) VALUES (" + ",".join("?" for _ in range(22)) + ")"
            
            user = self.current_user['username'] if self.current_user else 'sistema'
            full_data = list(data) + [user, user]
            
            with self._lock:
                self.cursor.execute(query, full_data)
                self.conn.commit()

            self.registrar_accion('CREATE/UPDATE', 'dictamenes', data[0], datos_nuevos={'dictamen': data[0]})
        except sqlite3.Error as e:
            logger.error(f"Error insertando dictamen '{data[0] if data else '?'}': {e}")
            raise

    def fetch_all_dictamenes(self):
        """Retorna todos los dictámenes activos (sin paginación, para compatibilidad con export)."""
        self.cursor.execute('''
            SELECT dictamen, denuncia, imputado, ofendido, delito, sitio,
                   antecedentes, tecnico, fecha, fiscal, agente, decomiso,
                   tipo, cantidad, otro, unidad, estado_dictamen, fecha_estado,
                   entregado_a, fecha_entrega
            FROM dictamenes WHERE activo = 1 ORDER BY fecha_creacion DESC
        ''')
        return self.cursor.fetchall()

    def fetch_dictamenes_para_exportar(self, fecha_inicio=None, fecha_fin=None, buscar_texto=""):
        """Retorna dictámenes activos aplicando filtros de fecha o búsqueda de texto para exportar."""
        # Se obtienen todos y se filtran en python debido al formato de fecha dd/mm/yyyy no estándar de SQLite
        datos_todos = self.fetch_all_dictamenes()
        resultado = []
        
        from datetime import datetime
        
        # Parse text search
        texto_lower = buscar_texto.lower() if buscar_texto else ""
        
        for fila in datos_todos:
            # fila[8] es 'fecha'
            str_fecha = fila[8]
            pasa_fecha = True
            
            if fecha_inicio and fecha_fin and str_fecha:
                try:
                    fecha_obj = datetime.strptime(str_fecha, "%d/%m/%Y").date()
                    if not (fecha_inicio <= fecha_obj <= fecha_fin):
                        pasa_fecha = False
                except ValueError:
                    # Formato de fecha inválido o vacío
                    pass

            if pasa_fecha:
                pasa_texto = True
                if texto_lower:
                    # Unir todos los campos de texto para buscar coincidencias
                    contenido = " ".join([str(x).lower() for x in fila if x is not None])
                    if texto_lower not in contenido:
                        pasa_texto = False
                        
                if pasa_texto:
                    resultado.append(fila)
                    
        return resultado

    def count_dictamenes(self, search_query=""):
        """Retorna el número total de dictámenes activos."""
        if search_query:
            q = f"%{search_query}%"
            self.cursor.execute('''
                SELECT COUNT(*) FROM dictamenes 
                WHERE activo = 1 AND (
                    dictamen LIKE ? OR denuncia LIKE ? OR imputado LIKE ? OR 
                    sitio LIKE ? OR fecha LIKE ? OR antecedentes LIKE ?
                )
            ''', (q, q, q, q, q, q))
        else:
            self.cursor.execute("SELECT COUNT(*) FROM dictamenes WHERE activo = 1")
        return self.cursor.fetchone()[0]

    def fetch_dictamenes_paginados(self, offset=0, limit=50, search_query=""):
        """Retorna una página de dictámenes. Usar esta en la UI para no cargar todo en memoria."""
        if search_query:
            q = f"%{search_query}%"
            self.cursor.execute('''
                SELECT dictamen, denuncia, imputado, ofendido, delito, sitio,
                       antecedentes, tecnico, fecha, fiscal, agente, decomiso,
                       tipo, cantidad, otro, unidad, estado_dictamen, fecha_estado,
                       entregado_a, fecha_entrega
                FROM dictamenes 
                WHERE activo = 1 AND (
                    dictamen LIKE ? OR denuncia LIKE ? OR imputado LIKE ? OR 
                    sitio LIKE ? OR fecha LIKE ? OR antecedentes LIKE ?
                )
                ORDER BY fecha_creacion DESC
                LIMIT ? OFFSET ?
            ''', (q, q, q, q, q, q, limit, offset))
        else:
            self.cursor.execute('''
                SELECT dictamen, denuncia, imputado, ofendido, delito, sitio,
                       antecedentes, tecnico, fecha, fiscal, agente, decomiso,
                       tipo, cantidad, otro, unidad, estado_dictamen, fecha_estado,
                       entregado_a, fecha_entrega
                FROM dictamenes WHERE activo = 1
                ORDER BY fecha_creacion DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
        return self.cursor.fetchall()

    def delete_dictamen(self, dictamen_num):
        """Borrado lógico de dictamen"""
        with self._lock:
            self.cursor.execute("UPDATE dictamenes SET activo = 0 WHERE dictamen = ?", (dictamen_num,))
            self.conn.commit()
        self.registrar_accion('DELETE', 'dictamenes', dictamen_num)

    # ---------- SEGURIDAD Y AUDITORÍA ----------

    def verificar_usuario(self, username, password, ip_address=None):
        """Verifica credenciales. Retorna dict con resultado o False."""
        self.cursor.execute(
            'SELECT id, password_hash, salt, nombre_completo, rol, debe_cambiar_password '
            'FROM usuarios WHERE username = ? AND activo = 1',
            (username,)
        )
        res = self.cursor.fetchone()
        if res and self._hash_password(password, res[2]) == res[1]:
            self.current_user = {
                'id': res[0], 'username': username,
                'nombre_completo': res[3], 'rol': res[4],
                'debe_cambiar_password': bool(res[5]),
            }
            self.cursor.execute("UPDATE usuarios SET ultimo_acceso = CURRENT_TIMESTAMP WHERE id = ?", (res[0],))
            self.conn.commit()
            self.registrar_accion('LOGIN', 'usuarios', res[0], detalles=f"IP: {ip_address}")
            return True
        return False

    def cambiar_password(self, username, nueva_password):
        """Cambia la contraseña de un usuario y resetea el flag debe_cambiar_password."""
        salt = self._generate_salt()
        password_hash = self._hash_password(nueva_password, salt)
        with self._lock:
            self.cursor.execute(
                'UPDATE usuarios SET password_hash=?, salt=?, debe_cambiar_password=0, '
                'ultimo_cambio_password=CURRENT_TIMESTAMP WHERE username=?',
                (password_hash, salt, username)
            )
            self.conn.commit()
        self.registrar_accion('PASSWORD_CHANGE', 'usuarios', username)
        logger.info(f"Contraseña cambiada para usuario '{username}'.")

    def registrar_accion(self, accion, tabla=None, reg_id=None, datos_anteriores=None, datos_nuevos=None, detalles=None, nivel='INFO'):
        user = self.current_user['username'] if self.current_user else 'sistema'
        try:
            self.cursor.execute('''
                INSERT INTO auditoria (usuario, accion, tabla_afectada, registro_id, datos_anteriores, datos_nuevos, detalles, nivel_criticidad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user, accion, tabla, str(reg_id), json.dumps(datos_anteriores), json.dumps(datos_nuevos), detalles, nivel))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error registrando auditoría [{accion}] en tabla '{tabla}': {e}")

    def get_estadisticas_generales(self):
        self.cursor.execute("SELECT COUNT(*) FROM dictamenes WHERE activo = 1")
        total_d = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM decomisos WHERE activo = 1")
        total_de = self.cursor.fetchone()[0]
        return {'total_dictamenes': total_d, 'total_decomisos': total_de}

    def close(self):
        if self.backup_timer:
            self.backup_timer.cancel()
        if self.conn:
            try:
                self.conn.commit()
                self.conn.close()
            except sqlite3.Error as e:
                logger.error(f"Error cerrando la base de datos: {e}")
            finally:
                self.conn = None
