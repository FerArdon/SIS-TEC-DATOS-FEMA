# sigedta_i18n.py
"""
Sistema de internacionalización para SIS-TEC-DATOS FEMA
Soporte para múltiples idiomas y configuración regional
"""

import json
import os
from datetime import datetime
import logging

logger = logging.getLogger("sistecdatos.i18n")

class SISTECDATOSFEMAInternationalization:
    """Gestor de internacionalización para SIS-TEC-DATOS FEMA"""
    
    def __init__(self, idioma_default='es'):
        self.idioma_actual = idioma_default
        self.traducciones = {}
        self.formatos_fecha = {}
        self.formatos_numero = {}
        self._cargar_traducciones()
        self._configurar_formatos()
    
    def _cargar_traducciones(self):
        """Carga las traducciones desde archivos JSON"""
        
        # Traducciones en español (por defecto)
        self.traducciones['es'] = {
            # Interfaz principal
            "app_title": "SIS-TEC-DATOS FEMA - Sistema Integrado de Gestión y Expedientes de Dictámenes Técnico-Ambientales",
            "app_subtitle": "Fiscalía Especial de Medio Ambiente (FEMA)",
            
            # Login
            "login_title": "Iniciar Sesión",
            "username": "Usuario",
            "password": "Contraseña",
            "show_password": "Mostrar contraseña",
            "login_button": "Iniciar Sesión",
            "login_success": "Login exitoso",
            "login_failed": "Usuario o contraseña incorrectos",
            "max_attempts": "Máximo de intentos alcanzado",
            
            # Menú principal
            "menu_file": "Archivo",
            "menu_edit": "Editar",
            "menu_view": "Ver",
            "menu_tools": "Herramientas",
            "menu_help": "Ayuda",
            
            # Botones principales
            "add": "Agregar",
            "edit": "Editar",
            "delete": "Eliminar",
            "save": "Guardar",
            "cancel": "Cancelar",
            "close": "Cerrar",
            "search": "Buscar",
            "filter": "Filtrar",
            "export": "Exportar",
            "import": "Importar",
            "backup": "Backup",
            "restore": "Restaurar",
            "clear": "Limpiar",
            "refresh": "Actualizar",
            
            # Campos del formulario
            "dictamen": "Dictamen",
            "denuncia": "Denuncia",
            "imputado": "Imputado",
            "ofendido": "Ofendido",
            "delito": "Delito",
            "sitio": "Sitio",
            "antecedentes": "Antecedentes",
            "tecnico": "Técnico",
            "fecha": "Fecha",
            "fiscal": "Fiscal",
            "agente": "Agente",
            "decomiso": "Decomiso",
            "tipo": "Tipo",
            "cantidad": "Cantidad",
            "unidad": "Unidad",
            "estado_dictamen": "Estado del Dictamen",
            "fecha_estado": "Fecha del Estado",
            "entregado_a": "Entregado A",
            "fecha_entrega": "Fecha de Entrega",
            
            # Estados del dictamen
            "revision_documental": "Revisión documental",
            "programado_inspeccion": "Programado para inspección",
            "en_inspeccion": "En inspección de campo",
            "analisis_resultados": "En análisis de resultados",
            "proceso_redaccion": "En proceso de redacción",
            "revision_interna": "En revisión interna",
            "finalizado_no_entregado": "Finalizado (no entregado)",
            "finalizado_entregado": "Finalizado y entregado",
            
            # Decomisos
            "decomisos_title": "Gestión de Decomisos",
            "decomisos_subtitle": "Módulo Forense - Dictámenes Técnico-Ambientales",
            "tipo_decomiso": "Tipo de Decomiso",
            "cantidad_decomiso": "Cantidad",
            "unidad_decomiso": "Unidad",
            "categoria_ambiental": "Categoría Ambiental",
            "descripcion_detallada": "Descripción Detallada",
            "agregar_decomiso": "Agregar Decomiso",
            "actualizar_decomiso": "Actualizar",
            "limpiar_formulario": "Limpiar Formulario",
            "exportar_json": "Exportar JSON",
            "decomisos_registrados": "Decomisos Registrados",
            
            # Categorías ambientales
            "forestal": "Forestal",
            "minero": "Minero",
            "suelo": "Suelo",
            "agua": "Agua",
            "aire": "Aire",
            "fauna": "Fauna",
            "flora": "Flora",
            "quimico": "Químico",
            "otro": "Otro",
            
            # Mensajes de validación
            "campo_obligatorio": "El campo '{campo}' es obligatorio",
            "dictamen_duplicado": "El número de dictamen '{numero}' ya existe",
            "cantidad_invalida": "La cantidad debe ser un número válido mayor a cero",
            "fecha_invalida": "Formato de fecha inválido",
            "campos_incompletos": "Complete todos los campos obligatorios",
            
            # Mensajes de confirmación
            "confirmar_eliminar": "¿Está seguro de eliminar este registro?",
            "confirmar_salir": "¿Está seguro de salir de la aplicación?",
            "cambios_no_guardados": "Hay cambios sin guardar. ¿Desea continuar?",
            
            # Mensajes de éxito
            "dictamen_guardado": "Dictamen guardado correctamente",
            "decomiso_agregado": "Decomiso agregado exitosamente",
            "exportacion_exitosa": "Exportación completada exitosamente",
            "backup_creado": "Backup creado correctamente",
            
            # Mensajes de error
            "error_conexion": "Error de conexión con la base de datos",
            "error_exportacion": "Error durante la exportación",
            "error_importacion": "Error durante la importación",
            "error_backup": "Error al crear el backup",
            "error_permisos": "No tiene permisos para realizar esta acción",
            
            # Auditoría
            "auditoria_title": "Registro de Auditoría",
            "usuario_auditoria": "Usuario",
            "accion_auditoria": "Acción",
            "fecha_auditoria": "Fecha",
            "detalles_auditoria": "Detalles",
            "nivel_criticidad": "Nivel de Criticidad",
            
            # Configuración
            "configuracion_title": "Configuración del Sistema",
            "configuracion_general": "General",
            "configuracion_seguridad": "Seguridad",
            "configuracion_interfaz": "Interfaz",
            "configuracion_exportacion": "Exportación",
            "idioma_sistema": "Idioma del Sistema",
            "tema_visual": "Tema Visual",
            "backup_automatico": "Backup Automático",
            "intervalo_backup": "Intervalo de Backup (minutos)",
            "timeout_sesion": "Tiempo de Sesión (minutos)",
            
            # Estadísticas
            "estadisticas_title": "Estadísticas del Sistema",
            "total_dictamenes": "Total de Dictámenes",
            "total_decomisos": "Total de Decomisos",
            "dictamenes_por_estado": "Dictámenes por Estado",
            "decomisos_por_categoria": "Decomisos por Categoría",
            "actividad_reciente": "Actividad Reciente",
            
            # Ayuda
            "ayuda_title": "Ayuda del Sistema",
            "manual_usuario": "Manual de Usuario",
            "acerca_de": "Acerca de SIS-TEC-DATOS FEMA",
            "version": "Versión",
            "contacto_soporte": "Contacto de Soporte",
            
            # Formatos de fecha y hora
            "formato_fecha": "%d/%m/%Y",
            "formato_fecha_hora": "%d/%m/%Y %H:%M",
            "formato_hora": "%H:%M",
            
            # Unidades de medida
            "metros_cubicos": "m³",
            "pies_tablares": "PT",
            "cargas": "Cargas",
            "tonelada_metrica": "Tonelada métrica",
            "sacos": "Sacos",
            "toneladas": "Toneladas",
            "litros": "Litros",
            "unidades": "Unidades",
            "libras": "Libras",
            "kilogramos": "Kilogramos",
            "galones": "Galones",
            "metros": "Metros"
        }
        
        # Traducciones en inglés
        self.traducciones['en'] = {
            # Interfaz principal
            "app_title": "SIS-TEC-DATOS FEMA - Integrated Management System for Technical-Environmental Reports",
            "app_subtitle": "Special Environmental Prosecutor's Office (FEMA)",
            
            # Login
            "login_title": "Login",
            "username": "Username",
            "password": "Password",
            "show_password": "Show password",
            "login_button": "Login",
            "login_success": "Login successful",
            "login_failed": "Incorrect username or password",
            "max_attempts": "Maximum attempts reached",
            
            # Menú principal
            "menu_file": "File",
            "menu_edit": "Edit",
            "menu_view": "View",
            "menu_tools": "Tools",
            "menu_help": "Help",
            
            # Botones principales
            "add": "Add",
            "edit": "Edit",
            "delete": "Delete",
            "save": "Save",
            "cancel": "Cancel",
            "close": "Close",
            "search": "Search",
            "filter": "Filter",
            "export": "Export",
            "import": "Import",
            "backup": "Backup",
            "restore": "Restore",
            "clear": "Clear",
            "refresh": "Refresh",
            
            # Campos del formulario
            "dictamen": "Report",
            "denuncia": "Complaint",
            "imputado": "Accused",
            "ofendido": "Victim",
            "delito": "Crime",
            "sitio": "Site",
            "antecedentes": "Background",
            "tecnico": "Technician",
            "fecha": "Date",
            "fiscal": "Prosecutor",
            "agente": "Agent",
            "decomiso": "Seizure",
            "tipo": "Type",
            "cantidad": "Quantity",
            "unidad": "Unit",
            "estado_dictamen": "Report Status",
            "fecha_estado": "Status Date",
            "entregado_a": "Delivered To",
            "fecha_entrega": "Delivery Date",
            
            # Estados del dictamen
            "revision_documental": "Document review",
            "programado_inspeccion": "Scheduled for inspection",
            "en_inspeccion": "Field inspection",
            "analisis_resultados": "Results analysis",
            "proceso_redaccion": "Writing process",
            "revision_interna": "Internal review",
            "finalizado_no_entregado": "Finished (not delivered)",
            "finalizado_entregado": "Finished and delivered",
            
            # Decomisos
            "decomisos_title": "Seizure Management",
            "decomisos_subtitle": "Forensic Module - Technical-Environmental Reports",
            "tipo_decomiso": "Seizure Type",
            "cantidad_decomiso": "Quantity",
            "unidad_decomiso": "Unit",
            "categoria_ambiental": "Environmental Category",
            "descripcion_detallada": "Detailed Description",
            "agregar_decomiso": "Add Seizure",
            "actualizar_decomiso": "Update",
            "limpiar_formulario": "Clear Form",
            "exportar_json": "Export JSON",
            "decomisos_registrados": "Registered Seizures",
            
            # Categorías ambientales
            "forestal": "Forest",
            "minero": "Mining",
            "suelo": "Soil",
            "agua": "Water",
            "aire": "Air",
            "fauna": "Fauna",
            "flora": "Flora",
            "quimico": "Chemical",
            "otro": "Other",
            
            # Mensajes de validación
            "campo_obligatorio": "Field '{campo}' is required",
            "dictamen_duplicado": "Report number '{numero}' already exists",
            "cantidad_invalida": "Quantity must be a valid number greater than zero",
            "fecha_invalida": "Invalid date format",
            "campos_incompletos": "Complete all required fields",
            
            # Mensajes de confirmación
            "confirmar_eliminar": "Are you sure you want to delete this record?",
            "confirmar_salir": "Are you sure you want to exit the application?",
            "cambios_no_guardados": "There are unsaved changes. Do you want to continue?",
            
            # Mensajes de éxito
            "dictamen_guardado": "Report saved successfully",
            "decomiso_agregado": "Seizure added successfully",
            "exportacion_exitosa": "Export completed successfully",
            "backup_creado": "Backup created successfully",
            
            # Mensajes de error
            "error_conexion": "Database connection error",
            "error_exportacion": "Error during export",
            "error_importacion": "Error during import",
            "error_backup": "Error creating backup",
            "error_permisos": "You don't have permissions for this action",
            
            # Auditoría
            "auditoria_title": "Audit Log",
            "usuario_auditoria": "User",
            "accion_auditoria": "Action",
            "fecha_auditoria": "Date",
            "detalles_auditoria": "Details",
            "nivel_criticidad": "Criticality Level",
            
            # Configuración
            "configuracion_title": "System Configuration",
            "configuracion_general": "General",
            "configuracion_seguridad": "Security",
            "configuracion_interfaz": "Interface",
            "configuracion_exportacion": "Export",
            "idioma_sistema": "System Language",
            "tema_visual": "Visual Theme",
            "backup_automatico": "Automatic Backup",
            "intervalo_backup": "Backup Interval (minutes)",
            "timeout_sesion": "Session Timeout (minutes)",
            
            # Estadísticas
            "estadisticas_title": "System Statistics",
            "total_dictamenes": "Total Reports",
            "total_decomisos": "Total Seizures",
            "dictamenes_por_estado": "Reports by Status",
            "decomisos_por_categoria": "Seizures by Category",
            "actividad_reciente": "Recent Activity",
            
            # Ayuda
            "ayuda_title": "System Help",
            "manual_usuario": "User Manual",
            "acerca_de": "About SIS-TEC-DATOS FEMA",
            "version": "Version",
            "contacto_soporte": "Support Contact",
            
            # Formatos de fecha y hora
            "formato_fecha": "%m/%d/%Y",
            "formato_fecha_hora": "%m/%d/%Y %I:%M %p",
            "formato_hora": "%I:%M %p",
            
            # Unidades de medida
            "metros_cubicos": "m³",
            "pies_tablares": "BF",  # Board Feet
            "cargas": "Loads",
            "tonelada_metrica": "Metric ton",
            "sacos": "Bags",
            "toneladas": "Tons",
            "litros": "Liters",
            "unidades": "Units",
            "libras": "Pounds",
            "kilogramos": "Kilograms",
            "galones": "Gallons",
            "metros": "Meters"
        }
    
    def _configurar_formatos(self):
        """Configura formatos regionales"""
        
        # Formatos para español (Guatemala)
        self.formatos_fecha['es'] = {
            'fecha': '%d/%m/%Y',
            'fecha_hora': '%d/%m/%Y %H:%M',
            'hora': '%H:%M',
            'separador_decimal': ',',
            'separador_miles': '.',
            'moneda': 'Q',
            'formato_numero': '{:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        }
        
        # Formatos para inglés (Estados Unidos)
        self.formatos_fecha['en'] = {
            'fecha': '%m/%d/%Y',
            'fecha_hora': '%m/%d/%Y %I:%M %p',
            'hora': '%I:%M %p',
            'separador_decimal': '.',
            'separador_miles': ',',
            'moneda': '$',
            'formato_numero': '{:,.2f}'
        }
    
    def cambiar_idioma(self, nuevo_idioma):
        """Cambia el idioma actual del sistema"""
        if nuevo_idioma in self.traducciones:
            self.idioma_actual = nuevo_idioma
            return True
        return False
    
    def obtener_idiomas_disponibles(self):
        """Retorna lista de idiomas disponibles"""
        return list(self.traducciones.keys())
    
    def t(self, clave, **kwargs):
        """Traduce una clave al idioma actual"""
        traduccion = self.traducciones.get(self.idioma_actual, {}).get(clave, clave)
        
        # Reemplazar variables en la traducción
        if kwargs:
            try:
                traduccion = traduccion.format(**kwargs)
            except KeyError:
                pass  # Si falta alguna variable, devolver sin formatear
        
        return traduccion
    
    def formatear_fecha(self, fecha, tipo='fecha'):
        """Formatea una fecha según el idioma actual"""
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    fecha = datetime.strptime(fecha, '%d/%m/%Y')
                except ValueError:
                    return fecha  # Retornar sin formatear si no se puede parsear
        
        formato = self.formatos_fecha.get(self.idioma_actual, {}).get(tipo, '%d/%m/%Y')
        return fecha.strftime(formato)
    
    def formatear_numero(self, numero, decimales=2):
        """Formatea un número según el idioma actual"""
        try:
            formato_config = self.formatos_fecha.get(self.idioma_actual, {})
            
            if self.idioma_actual == 'es':
                # Formato solicitado por Fer: 1,234.56 (coma para miles, punto para decimales)
                return f"{numero:,.{decimales}f}"
            else:
                # Formato inglés: 1,234.56
                return f"{numero:,.{decimales}f}"
        except (ValueError, TypeError):
            return str(numero)
    
    def formatear_moneda(self, cantidad):
        """Formatea una cantidad como moneda"""
        formato_config = self.formatos_fecha.get(self.idioma_actual, {})
        simbolo_moneda = formato_config.get('moneda', '$')
        numero_formateado = self.formatear_numero(cantidad, 2)
        
        if self.idioma_actual == 'es':
            return f"{simbolo_moneda} {numero_formateado}"
        else:
            return f"{simbolo_moneda}{numero_formateado}"
    
    def exportar_traducciones(self, archivo_salida):
        """Exporta las traducciones a un archivo JSON"""
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(self.traducciones, f, ensure_ascii=False, indent=2)
            return True
        except (OSError, IOError) as e:
            logger.error(f"Error exportando traducciones a '{archivo_salida}': {e}")
            return False
    
    def importar_traducciones(self, archivo_entrada):
        """Importa traducciones desde un archivo JSON"""
        try:
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                nuevas_traducciones = json.load(f)
            
            # Validar estructura
            for idioma, traducciones in nuevas_traducciones.items():
                if isinstance(traducciones, dict):
                    self.traducciones[idioma] = traducciones
            
            return True
        except (OSError, IOError, json.JSONDecodeError) as e:
            logger.error(f"Error importando traducciones desde '{archivo_entrada}': {e}")
            return False
    
    def validar_traduccion_completa(self, idioma):
        """Valida que un idioma tenga todas las traducciones necesarias"""
        if idioma not in self.traducciones:
            return False, ["Idioma no encontrado"]
        
        claves_base = set(self.traducciones['es'].keys())
        claves_idioma = set(self.traducciones[idioma].keys())
        
        claves_faltantes = claves_base - claves_idioma
        claves_extra = claves_idioma - claves_base
        
        errores = []
        if claves_faltantes:
            errores.append(f"Claves faltantes: {', '.join(claves_faltantes)}")
        if claves_extra:
            errores.append(f"Claves extra: {', '.join(claves_extra)}")
        
        return len(errores) == 0, errores


# Instancia global del sistema de internacionalización
i18n = SISTECDATOSFEMAInternationalization()

# Función de conveniencia para traducir
def _(clave, **kwargs):
    """Función de conveniencia para traducir"""
    return i18n.t(clave, **kwargs)

# Funciones de conveniencia para formateo
def formatear_fecha(fecha, tipo='fecha'):
    """Función de conveniencia para formatear fechas"""
    return i18n.formatear_fecha(fecha, tipo)

def formatear_numero(numero, decimales=2):
    """Función de conveniencia para formatear números"""
    return i18n.formatear_numero(numero, decimales)

def formatear_moneda(cantidad):
    """Función de conveniencia para formatear moneda"""
    return i18n.formatear_moneda(cantidad)


if __name__ == "__main__":
    # Pruebas del sistema de internacionalización
    print("=== Pruebas de Internacionalización ===")
    
    # Prueba en español
    print(f"Español: {_('app_title')}")
    print(f"Botón agregar: {_('add')}")
    print(f"Campo obligatorio: {_('campo_obligatorio', campo='Dictamen')}")
    
    # Cambiar a inglés
    i18n.cambiar_idioma('en')
    print(f"\nInglés: {_('app_title')}")
    print(f"Add button: {_('add')}")
    print(f"Required field: {_('campo_obligatorio', campo='Report')}")
    
    # Pruebas de formateo
    from datetime import datetime
    fecha_actual = datetime.now()
    
    print(f"\nFormatos de fecha:")
    i18n.cambiar_idioma('es')
    print(f"Español: {formatear_fecha(fecha_actual)}")
    
    i18n.cambiar_idioma('en')
    print(f"Inglés: {formatear_fecha(fecha_actual)}")
    
    # Pruebas de números
    numero = 1234.56
    print(f"\nFormatos de número:")
    i18n.cambiar_idioma('es')
    print(f"Español: {formatear_numero(numero)}")
    print(f"Moneda: {formatear_moneda(numero)}")
    
    i18n.cambiar_idioma('en')
    print(f"Inglés: {formatear_numero(numero)}")
    print(f"Currency: {formatear_moneda(numero)}")
