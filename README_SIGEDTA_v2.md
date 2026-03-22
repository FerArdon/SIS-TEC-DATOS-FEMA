# SIGEDTA v2.0 Professional
## Sistema Integrado de Gestión y Expedientes de Dictámenes Técnico-Ambientales

### 🏛️ Fiscalía Especial de Medio Ambiente (FEMA)

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Características Principales](#características-principales)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Guía de Usuario](#guía-de-usuario)
6. [Módulos del Sistema](#módulos-del-sistema)
7. [Seguridad y Auditoría](#seguridad-y-auditoría)
8. [Exportación e Importación](#exportación-e-importación)
9. [Internacionalización](#internacionalización)
10. [Mantenimiento y Backup](#mantenimiento-y-backup)
11. [Desarrollo y Extensión](#desarrollo-y-extensión)
12. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Descripción General

SIGEDTA v2.0 Professional es un sistema integral de gestión de dictámenes técnico-ambientales desarrollado específicamente para la Fiscalía Especial de Medio Ambiente (FEMA). El sistema permite el registro, seguimiento y gestión completa de dictámenes periciales, incluyendo la gestión detallada de decomisos asociados.

### Objetivos del Sistema

- **Centralización**: Unificar el registro y seguimiento de dictámenes técnico-ambientales
- **Trazabilidad**: Mantener un historial completo de todas las acciones realizadas
- **Eficiencia**: Automatizar procesos y reducir tiempos de gestión
- **Seguridad**: Garantizar la integridad y confidencialidad de la información
- **Cumplimiento**: Facilitar el cumplimiento de normativas legales y procedimentales

---

## ✨ Características Principales

### 🔐 Sistema de Autenticación Avanzado
- Login seguro con hash de contraseñas (PBKDF2 + SHA256)
- Control de intentos fallidos y bloqueo temporal
- Gestión de sesiones con timeout configurable
- Roles de usuario (Admin, Técnico, Consulta)

### 📊 Gestión Integral de Dictámenes
- Formulario completo con validaciones automáticas
- Estados de dictamen según flujo FEMA
- Campos condicionales para entrega
- Calendario integrado para fechas
- Combobox inteligente para unidades (editable solo para "OTROS")

### 🏛️ Módulo de Decomisos Forense
- Gestión detallada de decomisos por dictamen
- Categorización ambiental automática
- Tipos predefinidos con unidades específicas
- Descripción detallada y trazabilidad completa

### 📈 Sistema de Auditoría Completo
- Registro automático de todas las acciones
- Niveles de criticidad (INFO, WARNING, ERROR)
- Trazabilidad de cambios con datos anteriores/nuevos
- Reportes de auditoría exportables

### 🌐 Internacionalización
- Soporte para múltiples idiomas (Español, Inglés)
- Formatos regionales de fecha y números
- Interfaz completamente traducible

### 📤 Exportación Avanzada
- Excel con múltiples hojas y formato profesional
- PDF con gráficos y análisis estadístico
- JSON estructurado para intercambio de datos
- Exportación de auditoría y estadísticas

### 🔄 Backup Automático
- Backup automático al cerrar aplicación
- Backup programado por intervalos
- Historial de backups con metadatos
- Restauración desde backup

---

## 🏗️ Arquitectura del Sistema

### Estructura de Archivos

```
SIGEDTA_v2/
├── sigedta_main.py              # Aplicación principal
├── sigedta_db_advanced.py       # Gestor de base de datos avanzado
├── sigedta_login.py             # Sistema de autenticación
├── sigedta_ui.py                # Estilos y temas visuales
├── sigedta_decomisos.py         # Módulo de gestión de decomisos
├── sigedta_export_advanced.py   # Sistema de exportación avanzado
├── sigedta_i18n.py              # Sistema de internacionalización
├── requirements.txt             # Dependencias del proyecto
├── README_SIGEDTA_v2.md         # Documentación completa
├── assets/                      # Recursos gráficos
│   ├── icon_sigedta.ico
│   └── logo_sigedta.png
├── data/                        # Base de datos
│   ├── sigedta_dictamenes.db
│   └── backups/
└── exports/                     # Archivos exportados
```

### Base de Datos

#### Tablas Principales

1. **dictamenes** - Información principal de dictámenes
2. **decomisos** - Decomisos asociados a dictámenes
3. **usuarios** - Usuarios del sistema con roles
4. **auditoria** - Log completo de acciones
5. **sesiones** - Sesiones activas de usuarios
6. **configuracion** - Configuración del sistema
7. **backups** - Historial de backups realizados
8. **decomisos_temporales** - Decomisos en proceso de creación

#### Relaciones

```sql
dictamenes (1) ←→ (N) decomisos
usuarios (1) ←→ (N) sesiones
usuarios (1) ←→ (N) auditoria
```

---

## 🚀 Instalación y Configuración

### Requisitos del Sistema

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows 10/11, Linux, macOS
- **RAM**: Mínimo 4GB, recomendado 8GB
- **Espacio en Disco**: 500MB para instalación + espacio para datos

### Dependencias

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
tkinter>=8.6
pandas>=1.3.0
openpyxl>=3.0.9
reportlab>=3.6.0
matplotlib>=3.5.0
seaborn>=0.11.0
Pillow>=8.3.0
tkcalendar>=1.6.0
```

### Instalación

1. **Clonar o descargar el proyecto**
```bash
git clone [repository_url]
cd SIGEDTA_v2
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
python sigedta_main.py
```

### Primera Configuración

1. **Usuario Administrador por Defecto**
   - Usuario: `admin`
   - Contraseña: `admin123`
   - **¡IMPORTANTE!** Cambiar la contraseña en el primer acceso

2. **Configuración Inicial**
   - El sistema creará automáticamente la base de datos
   - Se configurarán los valores por defecto
   - Se creará la estructura de directorios necesaria

---

## 👤 Guía de Usuario

### Inicio de Sesión

1. **Ejecutar la aplicación**
2. **Introducir credenciales**
   - Usuario y contraseña
   - Opción para mostrar contraseña
3. **Información del sistema**
   - Estadísticas básicas
   - Versión del sistema

### Interfaz Principal

#### Formulario de Dictámenes

**Campos Obligatorios:**
- Dictamen (único)
- Fecha
- Estado del Dictamen

**Campos Especiales:**
- **Tipo**: Combobox con botón de ayuda "?"
- **Unidad**: Editable solo para "OTROS"
- **Decomiso**: SI/NO con tooltip
- **Fechas**: Con calendario integrado
- **Estado**: Con campos condicionales para entrega

#### Botones de Acción

- **Agregar**: Guarda nuevo dictamen
- **🏛️ Gestión Decomisos**: Abre módulo de decomisos
- **Exportar Excel/PDF**: Exportación avanzada
- **Limpiar**: Limpia formulario
- **Tema Claro/Oscuro**: Cambia tema visual

### Módulo de Decomisos

#### Características

- **Formulario Detallado**: Tipo, cantidad, unidad, descripción
- **Categorización Automática**: Según tipo seleccionado
- **Validaciones**: Campos obligatorios y formatos
- **Lista Visual**: TreeView con información completa
- **Menú Contextual**: Editar, eliminar, copiar

#### Tipos de Decomiso Predefinidos

| Tipo | Unidad | Categoría |
|------|--------|-----------|
| MADERA EN ROLLO | m³ | Forestal |
| MADERA ASERRADA | PT | Forestal |
| LEÑA | Cargas | Forestal |
| FAUNA SILVESTRE | Unidades | Fauna |
| SUELO CONTAMINADO | Toneladas | Suelo |
| OTROS | Editable | Otro |

---

## 🔒 Seguridad y Auditoría

### Sistema de Autenticación

#### Características de Seguridad

- **Hash de Contraseñas**: PBKDF2 con SHA256 (100,000 iteraciones)
- **Salt Único**: Cada contraseña tiene su salt aleatorio
- **Control de Intentos**: Máximo 3 intentos fallidos
- **Bloqueo Temporal**: 15 minutos tras intentos fallidos
- **Timeout de Sesión**: 30 minutos de inactividad

#### Roles de Usuario

1. **Admin**
   - Acceso completo al sistema
   - Gestión de usuarios
   - Configuración del sistema
   - Acceso a auditoría completa

2. **Técnico**
   - Gestión de dictámenes y decomisos
   - Exportación de datos
   - Acceso limitado a auditoría

3. **Consulta**
   - Solo lectura de dictámenes
   - Exportación básica
   - Sin acceso a auditoría

### Sistema de Auditoría

#### Eventos Registrados

- **LOGIN/LOGOUT**: Inicio y cierre de sesión
- **CREATE/UPDATE/DELETE**: Operaciones CRUD
- **EXPORT/IMPORT**: Operaciones de datos
- **CONFIG**: Cambios de configuración
- **BACKUP/RESTORE**: Operaciones de backup

#### Niveles de Criticidad

- **INFO**: Operaciones normales
- **WARNING**: Situaciones de atención
- **ERROR**: Errores del sistema

#### Información Registrada

- Usuario responsable
- Fecha y hora exacta
- Acción realizada
- Datos anteriores y nuevos
- Dirección IP
- Detalles adicionales

---

## 📊 Exportación e Importación

### Exportación Excel Avanzada

#### Hojas Incluidas

1. **Dictámenes**: Datos completos con formato profesional
2. **Decomisos**: Información detallada de decomisos
3. **Estadísticas**: Métricas y análisis
4. **Resumen**: Resumen por dictamen
5. **Metadatos**: Información de la exportación

#### Características

- **Formato Profesional**: Colores, fuentes, alineación
- **Columnas Ajustadas**: Ancho automático
- **Encabezados Fijos**: Primera fila congelada
- **Filtros Aplicados**: Documentación de filtros

### Exportación PDF Profesional

#### Secciones

1. **Portada**: Logo, título, información del reporte
2. **Resumen Ejecutivo**: Estadísticas principales
3. **Dictámenes por Estado**: Tabla y análisis
4. **Detalle de Dictámenes**: Tabla principal (limitada a 50)
5. **Análisis de Decomisos**: Por categoría
6. **Gráficos**: Visualizaciones estadísticas

#### Características

- **Formato A4**: Márgenes profesionales
- **Estilos Personalizados**: Colores corporativos
- **Tablas Formateadas**: Encabezados destacados
- **Gráficos Integrados**: Matplotlib embebido

### Exportación JSON Estructurada

```json
{
  "metadata": {
    "version": "2.0",
    "export_date": "2024-01-01T12:00:00",
    "exported_by": "usuario",
    "total_records": 100
  },
  "dictamenes": [...],
  "decomisos": [...],
  "estadisticas": {...}
}
```

### Importación

#### Desde Excel
- Validación de columnas requeridas
- Procesamiento por lotes
- Reporte de errores detallado
- Registro en auditoría

#### Desde JSON
- Validación de estructura
- Importación de dictámenes y decomisos
- Manejo de errores por registro
- Preservación de relaciones

---

## 🌐 Internacionalización

### Idiomas Soportados

- **Español (es)**: Idioma por defecto
- **Inglés (en)**: Traducción completa

### Características

#### Traducción Completa
- Interfaz de usuario
- Mensajes del sistema
- Etiquetas de campos
- Estados y categorías

#### Formatos Regionales
- **Fechas**: dd/mm/yyyy (ES) vs mm/dd/yyyy (EN)
- **Números**: 1.234,56 (ES) vs 1,234.56 (EN)
- **Moneda**: Q 1.234,56 (ES) vs $1,234.56 (EN)

#### Uso

```python
from sigedta_i18n import _, formatear_fecha, formatear_numero

# Traducir texto
titulo = _('app_title')

# Formatear fecha
fecha_formateada = formatear_fecha(datetime.now())

# Formatear número
numero_formateado = formatear_numero(1234.56)
```

### Agregar Nuevo Idioma

1. **Editar sigedta_i18n.py**
2. **Agregar diccionario de traducciones**
3. **Configurar formatos regionales**
4. **Probar todas las funcionalidades**

---

## 🔄 Mantenimiento y Backup

### Backup Automático

#### Configuración

- **Al Cerrar**: Backup automático al cerrar aplicación
- **Por Intervalos**: Cada 60 minutos (configurable)
- **Ubicación**: `data/backups/`
- **Formato**: `sigedta_backup_YYYYMMDD_HHMMSS.db`

#### Tipos de Backup

1. **Manual**: Solicitado por usuario
2. **Automático**: Por intervalo de tiempo
3. **Cierre**: Al cerrar aplicación
4. **Pre-restauración**: Antes de restaurar

#### Gestión de Backups

- **Historial Completo**: Tabla de backups en BD
- **Metadatos**: Fecha, usuario, tamaño, tipo
- **Limpieza Automática**: Mantiene últimos 10 backups automáticos
- **Verificación**: Integridad de archivos

### Mantenimiento de Base de Datos

#### Operaciones Automáticas

- **VACUUM**: Optimización de espacio
- **ANALYZE**: Actualización de estadísticas
- **Limpieza**: Datos temporales antiguos
- **Verificación**: Integridad de datos

#### Comandos de Mantenimiento

```python
# Optimizar base de datos
db.optimizar_base_datos()

# Verificar integridad
integridad_ok, resultado = db.verificar_integridad()

# Limpiar datos temporales
eliminados = db.limpiar_datos_temporales()
```

---

## 🛠️ Desarrollo y Extensión

### Arquitectura Modular

#### Principios de Diseño

- **Separación de Responsabilidades**: Cada módulo tiene una función específica
- **Bajo Acoplamiento**: Módulos independientes
- **Alta Cohesión**: Funcionalidades relacionadas agrupadas
- **Extensibilidad**: Fácil agregar nuevas funcionalidades

#### Módulos Principales

1. **sigedta_main.py**: Interfaz principal y coordinación
2. **sigedta_db_advanced.py**: Acceso a datos y lógica de negocio
3. **sigedta_ui.py**: Estilos y temas visuales
4. **sigedta_decomisos.py**: Gestión específica de decomisos
5. **sigedta_export_advanced.py**: Exportación e importación
6. **sigedta_i18n.py**: Internacionalización
7. **sigedta_login.py**: Autenticación y seguridad

### Agregar Nuevos Campos

#### 1. Modificar Base de Datos

```python
# En sigedta_db_advanced.py
cursor.execute('''
    ALTER TABLE dictamenes 
    ADD COLUMN nuevo_campo TEXT
''')
```

#### 2. Actualizar Interfaz

```python
# En sigedta_main.py
self.campos_vars["Nuevo Campo"] = tk.StringVar()

# Agregar widget en _build_interface()
nuevo_entry = ttk.Entry(form_container, textvariable=self.campos_vars["Nuevo Campo"])
```

#### 3. Actualizar Exportación

```python
# En sigedta_export_advanced.py
columns.append('Nuevo Campo')
```

#### 4. Agregar Traducciones

```python
# En sigedta_i18n.py
"nuevo_campo": "Nuevo Campo",
```

### Agregar Nuevo Tipo de Decomiso

```python
# En sigedta_main.py y sigedta_decomisos.py
TIPOS_DECOMISO_SIGEDTA["NUEVO TIPO"] = {
    "unidad": "Nueva Unidad", 
    "categoria": "Nueva Categoría"
}
```

### Personalizar Estilos

```python
# En sigedta_ui.py
def apply_custom_theme(self):
    self.style.configure('Custom.TButton',
                        background='#custom_color',
                        foreground='white')
```

---

## 🔧 Solución de Problemas

### Problemas Comunes

#### 1. Error de Conexión a Base de Datos

**Síntomas**: "Error de conexión con la base de datos"

**Soluciones**:
- Verificar permisos de escritura en directorio `data/`
- Comprobar espacio disponible en disco
- Verificar que no haya otro proceso usando la BD

```bash
# Verificar permisos
ls -la data/
chmod 755 data/
```

#### 2. Error de Importación de Módulos

**Síntomas**: "ModuleNotFoundError: No module named 'X'"

**Soluciones**:
- Instalar dependencias faltantes
- Verificar versión de Python
- Usar entorno virtual

```bash
pip install -r requirements.txt
python --version  # Debe ser 3.8+
```

#### 3. Problemas de Rendimiento

**Síntomas**: Aplicación lenta, timeouts

**Soluciones**:
- Optimizar base de datos
- Limpiar datos temporales
- Verificar tamaño de BD

```python
db.optimizar_base_datos()
db.limpiar_datos_temporales()
```

#### 4. Error en Exportación PDF

**Síntomas**: "Error generando PDF"

**Soluciones**:
- Verificar instalación de ReportLab
- Comprobar permisos de escritura
- Verificar espacio en disco

```bash
pip install --upgrade reportlab
```

#### 5. Problemas de Autenticación

**Síntomas**: No puede iniciar sesión

**Soluciones**:
- Verificar credenciales
- Comprobar si usuario está bloqueado
- Resetear contraseña desde BD

```sql
-- Desbloquear usuario
UPDATE usuarios SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE username = 'usuario';
```

### Logs y Diagnóstico

#### Habilitar Logs Detallados

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Verificar Integridad del Sistema

```python
# Verificar BD
integridad_ok, resultado = db.verificar_integridad()

# Verificar archivos
import os
archivos_requeridos = ['sigedta_main.py', 'sigedta_db_advanced.py', ...]
for archivo in archivos_requeridos:
    if not os.path.exists(archivo):
        print(f"Archivo faltante: {archivo}")
```

#### Información del Sistema

```python
import sys, platform
print(f"Python: {sys.version}")
print(f"Plataforma: {platform.platform()}")
print(f"Arquitectura: {platform.architecture()}")
```

---

## 📞 Soporte y Contacto
frardonr@hotmail.com
+504 33527444

### Información de Soporte

- **Versión**: 2.0 Professional
- **Desarrollado para**: Fiscalía Especial de Medio Ambiente (FEMA)
- **Fecha de Lanzamiento**: 2025

### Documentación Adicional

- **Manual de Usuario**: Incluido en la aplicación (Menú Ayuda)
- **Guía de Administrador**: Este documento
- **API Documentation**: Comentarios en código fuente

### Actualizaciones

Para mantener el sistema actualizado:

1. **Backup Completo**: Antes de cualquier actualización
2. **Verificar Compatibilidad**: Revisar requisitos
3. **Probar en Entorno de Desarrollo**: Antes de producción
4. **Documentar Cambios**: Mantener registro de modificaciones

---

## 📄 Licencia y Términos de Uso

Este software ha sido desarrollado específicamente para la Fiscalía Especial de Medio Ambiente (FEMA) y está sujeto a los términos y condiciones establecidos en el contrato de desarrollo correspondiente.

### Restricciones

- Uso exclusivo para FEMA
- Prohibida la redistribución sin autorización
- Modificaciones solo por personal autorizado
- Backup y seguridad responsabilidad del usuario

### Garantía

El software se proporciona "tal como está" con garantía limitada según los términos del contrato de desarrollo.

---

**© 2024 - Sistema SIGEDTA v2.0 Professional**  
**Fiscalía Especial de Medio Ambiente (FEMA)**

---

*Documento actualizado: Enero 2024*  
*Versión del documento: 2.0*
