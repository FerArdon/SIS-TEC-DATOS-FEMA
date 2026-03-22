# test_sistecdatos.py
"""
Suite de tests para SISTECDATOSFEMA.
Cubre: CRUD básico, autenticación, cambio de contraseña,
paginación, auditoría, validaciones y condiciones de error.
"""
import unittest
import os
import glob
import sqlite3
import itertools

from sistecdatos_db import SISTECDATOSFEMADatabase

_counter = itertools.count(1)

# ── Datos de prueba ──────────────────────────────────────────────────────────
FILA_BASE = [
    "DT-TEST-001", "DEN-001", "Imputado A", "Ofendido B",
    "Tala ilegal", "Sitio X", "Antecedentes test",
    "Tec. García", "01/01/2025", "Fiscal López", "Agente Pérez",
    "SI", "MADERA EN ROLLO", "10.5", "", "m³",
    "Revisión Documental", "01/01/2025", "", "",
]


def _fila(dictamen="DT-TEST-001", **overrides):
    fila = FILA_BASE.copy()
    fila[0] = dictamen
    return fila


class BaseTestCase(unittest.TestCase):
    """Clase base: crea/destruye una BD temporal en cada test."""

    def setUp(self):
        # Nombre único por test para evitar colisiones de archivo en Windows
        self.db = SISTECDATOSFEMADatabase(f"_test_{next(_counter):05d}.db")

    def tearDown(self):
        db_path = self.db.db_path
        self.db.close()
        # Elimina el .db y archivos WAL/SHM que SQLite puede dejar en Windows
        for f in glob.glob(db_path + "*"):
            try:
                os.remove(f)
            except OSError:
                pass


# ── Tests de CRUD ─────────────────────────────────────────────────────────────

class TestCRUD(BaseTestCase):

    def test_insert_y_fetch(self):
        self.db.insert_dictamen(_fila())
        rows = self.db.fetch_all_dictamenes()
        self.assertTrue(any(r[0] == "DT-TEST-001" for r in rows))

    def test_insert_multiple(self):
        for i in range(5):
            self.db.insert_dictamen(_fila(f"DT-TEST-{i:03d}"))
        rows = self.db.fetch_all_dictamenes()
        self.assertEqual(len(rows), 5)

    def test_delete_logico(self):
        self.db.insert_dictamen(_fila("DT-DEL-001"))
        self.db.delete_dictamen("DT-DEL-001")
        rows = self.db.fetch_all_dictamenes()
        self.assertFalse(any(r[0] == "DT-DEL-001" for r in rows))

    def test_delete_no_afecta_otros(self):
        self.db.insert_dictamen(_fila("DT-KEEP"))
        self.db.insert_dictamen(_fila("DT-DEL"))
        self.db.delete_dictamen("DT-DEL")
        rows = self.db.fetch_all_dictamenes()
        self.assertTrue(any(r[0] == "DT-KEEP" for r in rows))

    def test_insert_reemplaza_existente(self):
        """INSERT OR REPLACE actualiza el registro si el dictamen ya existe."""
        self.db.insert_dictamen(_fila())
        fila_mod = _fila()
        fila_mod[2] = "Imputado Nuevo"
        self.db.insert_dictamen(fila_mod)
        rows = self.db.fetch_all_dictamenes()
        # Debe existir sólo un registro con ese número
        matches = [r for r in rows if r[0] == "DT-TEST-001"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][2], "Imputado Nuevo")

    def test_delete_inexistente_no_falla(self):
        """Borrar un dictamen que no existe no debe lanzar excepción."""
        try:
            self.db.delete_dictamen("DT-NOEXISTE-999")
        except Exception as e:
            self.fail(f"delete_dictamen lanzó excepción inesperada: {e}")


# ── Tests de paginación ───────────────────────────────────────────────────────

class TestPaginacion(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Inserción en batch usando una sola transacción para velocidad
        user = "sistema"
        query = (
            "INSERT OR REPLACE INTO dictamenes "
            "(dictamen, denuncia, imputado, ofendido, delito, sitio, antecedentes, tecnico, "
            "fecha, fiscal, agente, decomiso, tipo, cantidad, otro, unidad, estado_dictamen, "
            "fecha_estado, entregado_a, fecha_entrega, usuario_creacion, usuario_modificacion) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        )
        rows = [
            (f"DT-PAG-{i:04d}", "D", "I", "O", "De", "S", "A", "T",
             "01/01/2025", "F", "Ag", "NO", "OTROS", "1", "", "Unidades",
             "Revisión Documental", "01/01/2025", "", "", user, user)
            for i in range(120)
        ]
        self.db.cursor.executemany(query, rows)
        self.db.conn.commit()

    def test_count_dictamenes(self):
        self.assertEqual(self.db.count_dictamenes(), 120)

    def test_pagina_primera(self):
        rows = self.db.fetch_dictamenes_paginados(offset=0, limit=50)
        self.assertEqual(len(rows), 50)

    def test_pagina_segunda(self):
        rows = self.db.fetch_dictamenes_paginados(offset=50, limit=50)
        self.assertEqual(len(rows), 50)

    def test_pagina_ultima_parcial(self):
        rows = self.db.fetch_dictamenes_paginados(offset=100, limit=50)
        self.assertEqual(len(rows), 20)

    def test_offset_mayor_que_total(self):
        rows = self.db.fetch_dictamenes_paginados(offset=200, limit=50)
        self.assertEqual(len(rows), 0)

    def test_sin_duplicados_entre_paginas(self):
        p1 = {r[0] for r in self.db.fetch_dictamenes_paginados(offset=0, limit=50)}
        p2 = {r[0] for r in self.db.fetch_dictamenes_paginados(offset=50, limit=50)}
        self.assertEqual(len(p1 & p2), 0)


# ── Tests de autenticación ────────────────────────────────────────────────────

class TestAutenticacion(BaseTestCase):

    def test_login_admin_default_correcto(self):
        """El usuario admin creado por defecto con 'admin123' debe autenticar."""
        resultado = self.db.verificar_usuario("admin", "admin123")
        self.assertTrue(resultado)
        self.assertIsNotNone(self.db.current_user)
        self.assertEqual(self.db.current_user["username"], "admin")

    def test_login_password_incorrecta(self):
        resultado = self.db.verificar_usuario("admin", "wrongpass")
        self.assertFalse(resultado)

    def test_login_usuario_inexistente(self):
        resultado = self.db.verificar_usuario("noexiste", "pass")
        self.assertFalse(resultado)

    def test_admin_debe_cambiar_password(self):
        """El admin por defecto debe tener debe_cambiar_password=1."""
        self.db.verificar_usuario("admin", "admin123")
        self.assertTrue(self.db.current_user.get("debe_cambiar_password"))

    def test_cambiar_password(self):
        self.db.verificar_usuario("admin", "admin123")
        self.db.cambiar_password("admin", "nueva_clave_123")
        # Login con contraseña vieja debe fallar
        self.assertFalse(self.db.verificar_usuario("admin", "admin123"))
        # Login con contraseña nueva debe funcionar
        self.assertTrue(self.db.verificar_usuario("admin", "nueva_clave_123"))

    def test_cambiar_password_resetea_flag(self):
        self.db.verificar_usuario("admin", "admin123")
        self.db.cambiar_password("admin", "nueva_clave_456")
        self.db.verificar_usuario("admin", "nueva_clave_456")
        self.assertFalse(self.db.current_user.get("debe_cambiar_password"))

    def test_login_actualiza_ultimo_acceso(self):
        self.db.verificar_usuario("admin", "admin123")
        self.db.cursor.execute("SELECT ultimo_acceso FROM usuarios WHERE username='admin'")
        ultimo = self.db.cursor.fetchone()[0]
        self.assertIsNotNone(ultimo)


# ── Tests de auditoría ────────────────────────────────────────────────────────

class TestAuditoria(BaseTestCase):

    def test_insert_registra_auditoria(self):
        self.db.insert_dictamen(_fila("DT-AUDIT-001"))
        self.db.cursor.execute("SELECT COUNT(*) FROM auditoria WHERE accion='CREATE/UPDATE'")
        count = self.db.cursor.fetchone()[0]
        self.assertGreater(count, 0)

    def test_delete_registra_auditoria(self):
        self.db.insert_dictamen(_fila("DT-AUDIT-DEL"))
        self.db.delete_dictamen("DT-AUDIT-DEL")
        self.db.cursor.execute("SELECT COUNT(*) FROM auditoria WHERE accion='DELETE'")
        count = self.db.cursor.fetchone()[0]
        self.assertGreater(count, 0)

    def test_login_registra_auditoria(self):
        self.db.verificar_usuario("admin", "admin123")
        self.db.cursor.execute("SELECT COUNT(*) FROM auditoria WHERE accion='LOGIN'")
        count = self.db.cursor.fetchone()[0]
        self.assertGreater(count, 0)

    def test_cambio_password_registra_auditoria(self):
        self.db.verificar_usuario("admin", "admin123")
        self.db.cambiar_password("admin", "pass_nueva")
        self.db.cursor.execute("SELECT COUNT(*) FROM auditoria WHERE accion='PASSWORD_CHANGE'")
        count = self.db.cursor.fetchone()[0]
        self.assertGreater(count, 0)


# ── Tests de condiciones de error ─────────────────────────────────────────────

class TestErrores(BaseTestCase):

    def test_insert_fila_incompleta_lanza_error(self):
        """Una fila con menos de 20 campos genera sqlite3.Error (bindings incorrectos)."""
        fila_mala = ["DT-ERR-001", "solo_dos_campos"]
        with self.assertRaises(sqlite3.Error):
            self.db.insert_dictamen(fila_mala)

    def test_insert_dictamen_none_lanza_error(self):
        """Un dictamen con valor None viola la restricción NOT NULL de SQLite."""
        fila_mala = [None] + ["X"] * 19
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.insert_dictamen(fila_mala)

    def test_bd_no_corrompe_tras_error(self):
        """Tras un error de inserción (fila incompleta), la BD sigue funcionando."""
        try:
            self.db.insert_dictamen(["DT-ERR", "solo_dos"])  # 2 campos → error bindings
        except Exception:
            pass
        # Inserción válida posterior debe funcionar
        self.db.insert_dictamen(_fila("DT-POST-ERROR"))
        rows = self.db.fetch_all_dictamenes()
        self.assertTrue(any(r[0] == "DT-POST-ERROR" for r in rows))


# ── Tests de estadísticas ─────────────────────────────────────────────────────

class TestEstadisticas(BaseTestCase):

    def test_estadisticas_iniciales(self):
        stats = self.db.get_estadisticas_generales()
        self.assertIn("total_dictamenes", stats)
        self.assertIn("total_decomisos", stats)
        self.assertEqual(stats["total_dictamenes"], 0)

    def test_estadisticas_tras_insert(self):
        self.db.insert_dictamen(_fila())
        stats = self.db.get_estadisticas_generales()
        self.assertEqual(stats["total_dictamenes"], 1)

    def test_estadisticas_tras_delete(self):
        self.db.insert_dictamen(_fila("DT-STAT"))
        self.db.delete_dictamen("DT-STAT")
        stats = self.db.get_estadisticas_generales()
        self.assertEqual(stats["total_dictamenes"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
