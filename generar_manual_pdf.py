"""
Generador del Manual de Usuario PDF para SIS-TEC-DATOS FEMA v2.0
Ejecutar con: python generar_manual_pdf.py
Requiere: reportlab, Pillow
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from datetime import datetime

# ─── RUTAS ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BRAIN_DIR  = r"C:\Users\frard\.gemini\antigravity\brain\da5b59a8-0eb4-45a1-bcd2-68508f4c418f"
OUTPUT_PDF = os.path.join(BASE_DIR, "Manual_SIS-TEC-DATOS-FEMA_v2.pdf")

# ─── PALETA INSTITUCIONAL ──────────────────────────────────────────────────────
VERDE_FEMA   = HexColor("#1a4a2e")   # Verde oscuro institucional
VERDE_MED    = HexColor("#2e7d52")   # Verde medio
VERDE_LIGHT  = HexColor("#e8f5ee")   # Verde muy claro (fondos)
DORADO       = HexColor("#c8a84b")   # Dorado accent
GRIS_TEXTO   = HexColor("#2c2c2c")   # Gris texto
GRIS_CLARO   = HexColor("#f0f0f0")   # Gris muy claro
ROJO_ACCION  = HexColor("#c0392b")   # Rojo (botón eliminar)
AZUL_ACCION  = HexColor("#2471a3")   # Azul (botón Excel)

# ─── ESTILOS ──────────────────────────────────────────────────────────────────
def crear_estilos():
    styles = getSampleStyleSheet()

    estilos = {
        "titulo_principal": ParagraphStyle(
            "titulo_principal", fontName="Helvetica-Bold",
            fontSize=22, textColor=VERDE_FEMA, spaceAfter=6,
            alignment=TA_CENTER, leading=28),

        "subtitulo": ParagraphStyle(
            "subtitulo", fontName="Helvetica",
            fontSize=13, textColor=GRIS_TEXTO, spaceAfter=4,
            alignment=TA_CENTER, leading=18),

        "h1": ParagraphStyle(
            "h1", fontName="Helvetica-Bold",
            fontSize=16, textColor=VERDE_FEMA, spaceBefore=18,
            spaceAfter=8, borderPad=4, leading=22),

        "h2": ParagraphStyle(
            "h2", fontName="Helvetica-Bold",
            fontSize=13, textColor=VERDE_MED, spaceBefore=12,
            spaceAfter=6, leading=18),

        "h3": ParagraphStyle(
            "h3", fontName="Helvetica-Bold",
            fontSize=11, textColor=GRIS_TEXTO, spaceBefore=8,
            spaceAfter=4, leading=16),

        "cuerpo": ParagraphStyle(
            "cuerpo", fontName="Helvetica",
            fontSize=10, textColor=GRIS_TEXTO, spaceAfter=5,
            alignment=TA_JUSTIFY, leading=15),

        "bullet": ParagraphStyle(
            "bullet", fontName="Helvetica",
            fontSize=10, textColor=GRIS_TEXTO, spaceAfter=4,
            leftIndent=16, bulletIndent=4, leading=15),

        "nota": ParagraphStyle(
            "nota", fontName="Helvetica-Oblique",
            fontSize=9, textColor=AZUL_ACCION, spaceAfter=4,
            leftIndent=12, leading=13),

        "campo_nombre": ParagraphStyle(
            "campo_nombre", fontName="Helvetica-Bold",
            fontSize=10, textColor=VERDE_FEMA, leading=14),

        "campo_desc": ParagraphStyle(
            "campo_desc", fontName="Helvetica",
            fontSize=10, textColor=GRIS_TEXTO, leading=14),

        "pie": ParagraphStyle(
            "pie", fontName="Helvetica",
            fontSize=8, textColor=HexColor("#888888"),
            alignment=TA_CENTER, leading=12),

        "indice_titulo": ParagraphStyle(
            "indice_titulo", fontName="Helvetica-Bold",
            fontSize=12, textColor=VERDE_FEMA, spaceBefore=4,
            spaceAfter=2, leading=18),

        "indice_item": ParagraphStyle(
            "indice_item", fontName="Helvetica",
            fontSize=10, textColor=GRIS_TEXTO, spaceAfter=2,
            leftIndent=12, leading=15),

        "caption": ParagraphStyle(
            "caption", fontName="Helvetica-Oblique",
            fontSize=8.5, textColor=HexColor("#555555"),
            alignment=TA_CENTER, spaceBefore=2, spaceAfter=8),
    }
    return estilos

# ─── HELPER: imagen segura ─────────────────────────────────────────────────────
def img_safe(filename, width, height, brain=True):
    """Retorna una imagen ReportLab o None si no existe."""
    folder = BRAIN_DIR if brain else ASSETS_DIR
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        return RLImage(path, width=width, height=height)
    return None

def img_assets(filename, width, height):
    return img_safe(filename, width, height, brain=False)

# ─── NUMERACIÓN DE PÁGINAS ────────────────────────────────────────────────────
class PaginaConPie(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_pie(num_pages)
            super().showPage()
        super().save()

    def _draw_pie(self, total):
        page_num = self._pageNumber
        w, _ = A4
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor("#888888"))
        # Línea separadora
        self.setStrokeColor(HexColor("#cccccc"))
        self.line(2*cm, 1.8*cm, w - 2*cm, 1.8*cm)
        # Texto izquierda
        self.drawString(2*cm, 1.2*cm, "SIS-TEC-DATOS FEMA v2.0 — Manual de Usuario")
        # Texto derecha
        self.drawRightString(w - 2*cm, 1.2*cm, f"Página {page_num} de {total}")
        self.restoreState()

# ─── SECCIÓN: PORTADA ─────────────────────────────────────────────────────────
def seccion_portada(st):
    items = []
    # Imagen de portada generada
    cover = img_safe("manual_cover_fema_1774274892809.png", 14*cm, 10*cm)
    if cover:
        cover.hAlign = "CENTER"
        items.append(cover)
        items.append(Spacer(1, 0.5*cm))

    # Logo institucional desde assets
    logo = img_assets("logo_sistecdatos.png", 5*cm, 5*cm)
    if logo:
        logo.hAlign = "CENTER"
        items.append(logo)
        items.append(Spacer(1, 0.4*cm))

    items += [
        Paragraph("MANUAL DE USUARIO", st["titulo_principal"]),
        Paragraph("SIS-TEC-DATOS FEMA — v2.0 Professional", st["subtitulo"]),
        Spacer(1, 0.3*cm),
        HRFlowable(width="80%", thickness=2, color=DORADO, hAlign="CENTER"),
        Spacer(1, 0.4*cm),
        Paragraph("Sistema Técnico de Datos de la Fiscalía de Medio Ambiente", st["subtitulo"]),
        Paragraph("Fiscalía Especial de Medio Ambiente (FEMA)", st["subtitulo"]),
        Spacer(1, 0.5*cm),
        Paragraph(f"Sección Técnica Ambiental · Versión 2025", st["pie"]),
        Paragraph(f"Fecha de emisión: {datetime.now().strftime('%d/%m/%Y')}", st["pie"]),
        Paragraph("Desarrollado por Ing. Fernando Ardón · Antigravity AI © 2025", st["pie"]),
        PageBreak()
    ]
    return items

# ─── SECCIÓN: ÍNDICE ──────────────────────────────────────────────────────────
def seccion_indice(st):
    items = [
        Paragraph("ÍNDICE DE CONTENIDOS", st["h1"]),
        HRFlowable(width="100%", thickness=1.5, color=VERDE_FEMA),
        Spacer(1, 0.3*cm),
    ]
    secciones = [
        ("1.", "Introducción al Sistema", "3"),
        ("2.", "Inicio de Sesión", "4"),
        ("3.", "Interfaz Principal", "5"),
        ("4.", "Formulario de Ingreso — Campos Detallados", "6"),
        ("5.", "Acciones del Formulario (Botones)", "10"),
        ("6.", "Menú de la Aplicación", "11"),
        ("7.", "Directorio de Expedientes y Búsqueda", "12"),
        ("8.", "Exportación de Datos (Excel / PDF)", "13"),
        ("9.", "Estados del Dictamen y Flujo de Trabajo", "14"),
        ("10.", "Tipos de Decomiso y Unidades", "15"),
        ("11.", "Atajos de Teclado", "16"),
        ("12.", "Seguridad y Gestión de Sesión", "17"),
    ]
    for num, titulo, pag in secciones:
        data = [[
            Paragraph(f"<b>{num}</b>", st["indice_item"]),
            Paragraph(titulo, st["indice_item"]),
            Paragraph(f"{pag}", st["indice_item"]),
        ]]
        t = Table(data, colWidths=[1.2*cm, 12.5*cm, 1.5*cm])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LINEBELOW", (0, 0), (-1, 0), 0.3, HexColor("#dddddd")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        items.append(t)
    items.append(PageBreak())
    return items

# ─── SECCIÓN 1: INTRODUCCIÓN ──────────────────────────────────────────────────
def seccion_introduccion(st):
    return [
        Paragraph("1. INTRODUCCIÓN AL SISTEMA", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "SIS-TEC-DATOS FEMA es el Sistema Técnico de Datos de la Fiscalía Especial de "
            "Medio Ambiente (FEMA) de Honduras. Fue desarrollado para la Sección Técnica "
            "Ambiental con el fin de centralizar, gestionar y controlar los dictámenes "
            "técnico-ambientales generados en el marco de procesos judiciales y de "
            "investigación forense ambiental.", st["cuerpo"]),
        Spacer(1, 0.3*cm),
        Paragraph("<b>Objetivos del sistema:</b>", st["h3"]),
        Paragraph("▸  Registrar dictámenes técnicos con todos sus datos asociados.", st["bullet"]),
        Paragraph("▸  Controlar el estado de avance de cada expediente.", st["bullet"]),
        Paragraph("▸  Gestionar decomisos ambientales (madera, fauna, minerales, etc.).", st["bullet"]),
        Paragraph("▸  Exportar informes en formato Excel y PDF para uso institucional.", st["bullet"]),
        Paragraph("▸  Garantizar la trazabilidad y auditoría de cambios.", st["bullet"]),
        Paragraph("▸  Proteger el acceso mediante credenciales institucionales.", st["bullet"]),
        Spacer(1, 0.4*cm),
        Paragraph("<b>Requisitos del sistema:</b>", st["h3"]),
        _tabla_simple([
            ["Elemento", "Requerimiento"],
            ["Sistema Operativo", "Windows 10 / 11"],
            ["Versión", "SIS-TEC-DATOS FEMA v2.0 Professional"],
            ["Resolución mínima", "1280 × 720 píxeles"],
            ["Almacenamiento", "Base de datos SQLite local (incluida)"],
        ], st),
        Spacer(1, 0.3*cm),
        Paragraph(
            "ℹ  El sistema opera completamente fuera de línea. La base de datos SQLite "
            "se almacena localmente en el equipo institucional. No requiere conexión a internet.",
            st["nota"]),
        PageBreak(),
    ]

# ─── SECCIÓN 2: LOGIN ─────────────────────────────────────────────────────────
def seccion_login(st):
    items = [
        Paragraph("2. INICIO DE SESIÓN", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "Al iniciar la aplicación, el sistema muestra automáticamente la ventana de "
            "inicio de sesión. El acceso está protegido por credenciales institucionales "
            "asignadas por el administrador.", st["cuerpo"]),
        Spacer(1, 0.3*cm),
    ]
    img = img_safe("manual_login_screen_1774274908755.png", 9*cm, 13*cm)
    if img:
        img.hAlign = "CENTER"
        items.append(img)
        items.append(Paragraph("Figura 1 — Ventana de inicio de sesión del sistema.", st["caption"]))
    items += [
        Paragraph("Elementos de la ventana de login:", st["h2"]),
        _tabla_campos([
            ("Usuario", "Campo de texto donde se ingresa el nombre de usuario institucional asignado."),
            ("Contraseña", "Campo de contraseña (enmascarada con asteriscos). Al marcar 'Mostrar contraseña' se revela el texto."),
            ("Mostrar contraseña", "Casilla de verificación que alterna la visibilidad de la contraseña ingresada."),
            ("Botón 'Iniciar Sesión'", "Valida las credenciales. Si son correctas, abre la interfaz principal. Máximo 3 intentos."),
            ("Botón 'Cambiar Contraseña'", "Permite actualizar la contraseña del usuario actual ingresando la contraseña anterior y la nueva."),
            ("Panel de estadísticas", "Muestra en tiempo real el total de dictámenes y decomisos registrados, así como la versión del sistema."),
        ], st),
        Spacer(1, 0.3*cm),
        Paragraph(
            "⚠  Al alcanzar 3 intentos fallidos consecutivos, el sistema muestra una "
            "advertencia. Si un usuario debe cambiar su contraseña en el próximo ingreso, "
            "el sistema lo solicitará automáticamente antes de mostrar la interfaz principal.",
            st["nota"]),
        Spacer(1, 0.2*cm),
        Paragraph(
            "ℹ  Si un usuario recién creado inicia sesión por primera vez con contraseña "
            "temporal, el sistema pedirá establecer una contraseña nueva de al menos 6 caracteres.",
            st["nota"]),
        PageBreak(),
    ]
    return items

# ─── SECCIÓN 3: INTERFAZ PRINCIPAL ────────────────────────────────────────────
def seccion_interfaz(st):
    items = [
        Paragraph("3. INTERFAZ PRINCIPAL", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "Tras el inicio de sesión exitoso, la ventana principal se despliega en modo "
            "maximizado. La interfaz se divide en cuatro zonas funcionales claramente "
            "diferenciadas:", st["cuerpo"]),
        Spacer(1, 0.3*cm),
    ]
    img = img_safe("manual_main_interface_1774274923714.png", 15*cm, 8*cm)
    if img:
        img.hAlign = "CENTER"
        items.append(img)
        items.append(Paragraph("Figura 2 — Interfaz principal con sus zonas funcionales.", st["caption"]))
    items += [
        Paragraph("Zonas de la interfaz:", st["h2"]),
        _tabla_campos([
            ("Barra de Menú", "Menú tradicional de Windows en la parte superior: Archivo, Editar, Ver, Herramientas y Ayuda. Cada menú contiene comandos con atajos de teclado."),
            ("Encabezado (Header)", "Muestra el logo institucional de la FEMA, el nombre completo del sistema 'SIS-TEC-DATOS FEMA' y el nombre de la organización como identidad visual."),
            ("Panel de Pestañas", "Contiene dos pestañas: (1) 'Ingreso y Edición' — para captura y modificación de datos; (2) 'Directorio de Expedientes (Búsqueda)' — para consulta y búsqueda de registros."),
            ("Barra de Estado", "Franja inferior que muestra mensajes de retroalimentación en tiempo real: confirmaciones, errores, estado del tema visual y otras notificaciones del sistema."),
        ], st),
        PageBreak(),
    ]
    return items

# ─── SECCIÓN 4: CAMPOS DEL FORMULARIO ────────────────────────────────────────
def seccion_campos(st):
    items = [
        Paragraph("4. FORMULARIO DE INGRESO — CAMPOS DETALLADOS", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.2*cm),
        Paragraph(
            "La pestaña 'Ingreso y Edición' contiene el formulario principal distribuido en "
            "tres columnas para optimizar el espacio. A continuación se detalla cada campo, "
            "su propósito y cómo usarlo correctamente.", st["cuerpo"]),
        Spacer(1, 0.4*cm),
        Paragraph("4.1 — Columna Izquierda", st["h2"]),
    ]
    # Campos columna izquierda
    items.append(_tabla_campos([
        ("Dictamen",
         "Número único de identificación del dictamen técnico. Formato predeterminado: "
         "'DT-SISTECDATOSFEMA N°-XXX'. Editar el número correlativo al final. "
         "⚑ Campo OBLIGATORIO. No se permiten números duplicados."),
        ("Denuncia",
         "Número o código del expediente de denuncia penal asociado al dictamen "
         "(ej. DEN-2025-001). Es el vínculo con el expediente judicial. "
         "⚑ Campo OBLIGATORIO."),
        ("Imputado",
         "Nombre completo del imputado (persona acusada) en el proceso. "
         "Si hay múltiples imputados, separar con coma. Campo de texto libre."),
        ("Ofendido",
         "Nombre del ofendido, víctima o entidad afectada por el delito ambiental. "
         "Puede ser una persona, comunidad o el Estado de Honduras."),
        ("Delito",
         "Descripción del tipo de delito ambiental investigado (ej. 'Aprovechamiento "
         "ilegal de madera', 'Extracción ilegal de fauna silvestre'). "
         "⚑ Campo OBLIGATORIO."),
        ("Sitio",
         "Ubicación geográfica donde ocurrió el hecho investigado. Incluir municipio, "
         "departamento y referencias de ubicación precisas."),
        ("Antecedentes",
         "Área de texto multilínea para ingresar el contexto histórico, "
         "expedientes previos relacionados, denuncias anteriores u otros antecedentes "
         "relevantes del caso. Permite texto extenso."),
    ], st))

    items += [Spacer(1, 0.4*cm), Paragraph("4.2 — Columna Central", st["h2"])]
    items.append(_tabla_campos([
        ("Técnico",
         "Nombre del técnico ambiental responsable de elaborar el dictamen. "
         "Debe coincidir con el firmante del documento oficial. "
         "⚑ Campo OBLIGATORIO."),
        ("Fecha",
         "Fecha de elaboración del dictamen en formato DD/MM/AAAA. "
         "Se pre-llena automáticamente con la fecha actual. "
         "Usar el botón 📅 para abrir el calendario visual y seleccionar una fecha."),
        ("Fiscal",
         "Nombre del Fiscal a cargo del caso penal ante quien se presenta el dictamen. "
         "Es el operador de justicia solicitante del peritaje técnico."),
        ("Agente",
         "Nombre del Agente del Ministerio Público o autoridad policial involucrada "
         "en la cadena de custodia o en el acompañamiento de la inspección."),
        ("Decomiso",
         "Indica si existe material decomisado asociado al expediente. "
         "Seleccionar 'SI' o 'NO' del menú desplegable. "
         "Si se elige 'SI', los campos Tipo, Cantidad y Unidad se vuelven relevantes."),
        ("Tipo",
         "Categoría del material decomisado. Seleccionar del menú desplegable:\n"
         "MADERA EN ROLLO, MADERA ASERRADA, LEÑA, ASERRÍN, CARBÓN VEGETAL, "
         "MATERIAL MINERÍA, SUELO CONTAMINADO, AGUA CONTAMINADA, FAUNA SILVESTRE, "
         "FLORA SILVESTRE, EMISIONES AIRE, MAQUINARIA PESADA, EQUIPO FORESTAL, "
         "EQUIPO MINERO, PRODUCTOS QUÍMICOS, OTROS. "
         "El botón ℹ️ muestra la guía completa de tipos y unidades."),
    ], st))

    items += [Spacer(1, 0.4*cm), Paragraph("4.3 — Columna Derecha", st["h2"])]
    items.append(_tabla_campos([
        ("Cantidad",
         "Cantidad numérica del material decomisado. Usar punto (.) como separador "
         "decimal (ej. 15.5). No incluir la unidad en este campo."),
        ("Unidad",
         "Unidad de medida del decomiso. Se asigna automáticamente según el tipo:\n"
         "• Madera en Rollo → m³   • Madera Aserrada → PT (pies tablares)\n"
         "• Leña → Cargas   • Carbón Vegetal → Sacos   • Fauna / Flora → Unidades\n"
         "• Minería → Toneladas   • Agua → Litros   • Químicos → Libras\n"
         "Al seleccionar OTROS, el campo se habilita para edición libre con "
         "24 unidades comunes disponibles en el desplegable."),
        ("Otro",
         "Campo de descripción adicional del decomiso cuando el tipo es OTROS "
         "o cuando se necesita especificar detalles no capturados por los campos anteriores."),
        ("Estado del Dictamen",
         "Estado actual del dictamen dentro del flujo de trabajo de la Sección Técnica. "
         "Ver Sección 9 para la descripción completa de cada estado del flujo."),
        ("Fecha del Estado",
         "Fecha en que el dictamen alcanzó el estado actual. Se pre-llena con la fecha "
         "actual. Usar el botón 📅 para seleccionar del calendario."),
        ("Entregado A",
         "Visible solo cuando el Estado es 'Finalizado y entregado'. "
         "Registra el nombre o cargo de quien recibió el dictamen físicamente "
         "(ej. Fiscal, Juzgado, Secretaría). ⚑ Obligatorio en ese estado."),
        ("Fecha de Entrega",
         "Visible solo cuando el Estado es 'Finalizado y entregado'. "
         "Fecha en que se realizó la entrega formal del dictamen. "
         "⚑ Campo OBLIGATORIO cuando el estado es 'Finalizado y entregado'."),
    ], st))
    items.append(PageBreak())
    return items

# ─── SECCIÓN 5: BOTONES DE ACCIÓN ─────────────────────────────────────────────
def seccion_botones(st):
    items = [
        Paragraph("5. ACCIONES DEL FORMULARIO (BOTONES)", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "En la parte inferior de la pestaña 'Ingreso y Edición' se encuentran los "
            "botones de acción principal, dispuestos en una sola fila para acceso rápido:",
            st["cuerpo"]),
        Spacer(1, 0.3*cm),
        _tabla_campos([
            ("➕ Agregar  (Ctrl+S)",
             "Guarda el dictamen actualmente en el formulario. El sistema valida que los "
             "campos obligatorios (Dictamen, Denuncia, Delito, Técnico) estén completos "
             "y que el número de dictamen no esté duplicado. Si el formulario contiene un "
             "registro existente en edición, lo actualiza. Al finalizar, limpia el formulario."),
            ("📊 Excel  (Ctrl+E)",
             "Abre el diálogo de opciones de exportación para generar un archivo .XLSX "
             "con los registros de la base de datos. Permite filtrar por rango de fechas "
             "y/o por texto libre antes de exportar."),
            ("📄 PDF  (Ctrl+P)",
             "Abre el diálogo de opciones de exportación para generar un informe PDF "
             "con los dictámenes registrados. Soporta los mismos filtros que la exportación Excel."),
            ("🗑️ Limpiar  (Ctrl+L)",
             "Borra todos los valores del formulario y restaura los campos a sus valores "
             "predeterminados (número de dictamen con prefijo, fecha actual, "
             "estado inicial 'Revisión documental'). No borra registros de la base de datos."),
            ("🌓 Tema  (Ctrl+T)",
             "Alterna el tema visual de la aplicación entre el modo Claro y el modo Oscuro "
             "para mayor comodidad según las condiciones de iluminación del entorno de trabajo."),
            ("❌ Cerrar  (Alt+F4)",
             "Cierra la sesión activa y finaliza la aplicación correctamente, "
             "guardando y cerrando la conexión con la base de datos."),
        ], st),
        PageBreak(),
    ]
    return items

# ─── SECCIÓN 6: MENÚ ──────────────────────────────────────────────────────────
def seccion_menu(st):
    items = [
        Paragraph("6. MENÚ DE LA APLICACIÓN", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "La barra de menú tradicional de Windows presenta cinco menús con acceso a "
            "todas las funciones del sistema:", st["cuerpo"]),
        Spacer(1, 0.3*cm),
        Paragraph("Menú Archivo", st["h2"]),
        _tabla_simple([
            ["Opción", "Función", "Atajo"],
            ["Agregar", "Limpia el formulario para nuevo ingreso", "Ctrl+N"],
            ["Guardar", "Guarda el registro actual", "Ctrl+S"],
            ["Exportar Excel", "Exporta datos a hoja de cálculo", "Ctrl+E"],
            ["Exportar PDF", "Exporta datos a documento PDF", "Ctrl+P"],
            ["Cerrar", "Cierra la aplicación", "Alt+F4"],
        ], st),
        Spacer(1, 0.3*cm),
        Paragraph("Menú Editar", st["h2"]),
        _tabla_simple([
            ["Opción", "Función", "Atajo"],
            ["Editar", "Carga el registro seleccionado para edición", "F2"],
            ["Eliminar", "Elimina el registro seleccionado (con confirmación)", "Supr"],
            ["Limpiar", "Limpia el formulario", "Ctrl+L"],
        ], st),
        Spacer(1, 0.3*cm),
        Paragraph("Menú Ver", st["h2"]),
        _tabla_simple([
            ["Opción", "Función", "Atajo"],
            ["Cambiar Tema", "Alterna modo claro / oscuro", "Ctrl+T"],
            ["Actualizar Lista", "Recarga los datos desde la base de datos", "F5"],
        ], st),
        Spacer(1, 0.3*cm),
        Paragraph("Menú Herramientas", st["h2"]),
        _tabla_simple([
            ["Opción", "Función", "Atajo"],
            ["Gestión de Decomisos", "Muestra guía de tipos de decomiso y unidades", "—"],
            ["Fecha", "Abre el selector de calendario para el campo Fecha", "—"],
        ], st),
        Spacer(1, 0.3*cm),
        Paragraph("Menú Ayuda", st["h2"]),
        _tabla_simple([
            ["Opción", "Función", "Atajo"],
            ["Manual de Usuario", "Muestra el manual interno de la aplicación", "—"],
            ["Acerca de", "Información del sistema, versión y créditos", "—"],
        ], st),
        PageBreak(),
    ]
    return items

# ─── SECCIÓN 7: DIRECTORIO Y BÚSQUEDA ────────────────────────────────────────
def seccion_directorio(st):
    items = [
        Paragraph("7. DIRECTORIO DE EXPEDIENTES Y BÚSQUEDA", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "La pestaña 'Directorio de Expedientes (Búsqueda)' presenta todos los "
            "dictámenes registrados en forma de lista navegable con soporte de búsqueda "
            "y paginación.", st["cuerpo"]),
        Spacer(1, 0.3*cm),
    ]
    img = img_safe("manual_search_directory_1774274950596.png", 15*cm, 7*cm)
    if img:
        img.hAlign = "CENTER"
        items.append(img)
        items.append(Paragraph("Figura 3 — Directorio de expedientes con buscador y paginación.", st["caption"]))

    items += [
        Paragraph("Funciones del Directorio:", st["h2"]),
        _tabla_campos([
            ("Buscador",
             "Campo de texto para filtrar registros en tiempo real. Busca en todos los "
             "campos: número de dictamen, sitio, imputado, fiscal, agente, tipo de decomiso, etc. "
             "Presionar Enter o el botón 'Buscar' para ejecutar. El botón ✖ limpia el filtro."),
            ("Lista de registros",
             "Muestra los expedientes en formato de texto separado por ' | '. "
             "Cada fila incluye: Dictamen | Denuncia | Imputado | Delito | Técnico | Fecha | Estado. "
             "Soporta scroll horizontal y vertical para ver todos los datos."),
            ("Paginación",
             "Navega entre páginas de 50 registros. Los botones '◀ Anterior' y 'Siguiente ▶' "
             "avanzan entre páginas. El contador muestra la página actual, el total de páginas "
             "y el total de registros en la base de datos."),
            ("Doble clic",
             "Al hacer doble clic sobre un registro, se abre la ventana 'Detalles del Expediente' "
             "con toda la información del dictamen en formato detallado y legible."),
            ("Clic derecho (Menú contextual)",
             "Sobre cualquier registro seleccionado, el clic derecho despliega tres opciones:\n"
             "• 👁️ Ver Detalles — abre ventana completa de visualización\n"
             "• ✏️ Editar — carga los datos en el formulario de la pestaña 'Ingreso y Edición'\n"
             "• 🗑️ Eliminar — borra el registro previa confirmación del usuario"),
        ], st),
    ]
    img2 = img_safe("manual_context_menu_1774274979227.png", 12*cm, 6*cm)
    if img2:
        img2.hAlign = "CENTER"
        items.append(Spacer(1, 0.3*cm))
        items.append(img2)
        items.append(Paragraph("Figura 4 — Menú contextual con opciones sobre un registro seleccionado.", st["caption"]))
    items.append(PageBreak())
    return items

# ─── SECCIÓN 8: EXPORTACIÓN ───────────────────────────────────────────────────
def seccion_exportacion(st):
    items = [
        Paragraph("8. EXPORTACIÓN DE DATOS (EXCEL / PDF)", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "El sistema permite exportar los dictámenes a dos formatos de salida. "
            "Ambas opciones abren el mismo diálogo de configuración de exportación.",
            st["cuerpo"]),
        Spacer(1, 0.3*cm),
    ]
    img = img_safe("manual_export_dialog_1774274966402.png", 10*cm, 8*cm)
    if img:
        img.hAlign = "CENTER"
        items.append(img)
        items.append(Paragraph("Figura 5 — Diálogo de opciones de exportación filtrada.", st["caption"]))

    items += [
        Paragraph("Opciones del diálogo de exportación:", st["h2"]),
        _tabla_campos([
            ("Desde / Hasta (Rango de fechas)",
             "Permite filtrar los registros por un rango de fechas específico. "
             "Se puede usar el botón 📅 para abrir el selector de calendario. "
             "Ambas fechas deben estar completas si se usa el filtro de fecha. "
             "Si se dejan vacíos, se exportan todos los registros."),
            ("Filtro de texto",
             "Campo adicional para filtrar por el nombre de un Fiscal, Agente o Sitio. "
             "Compatible con el filtro de fechas (se pueden combinar ambos)."),
            ("Botón 'Exportar Todos'",
             "Genera el archivo sin filtros (cuando no se ingresaron parámetros), "
             "o 'Exportar Filtrados' si se aplicaron criterios de búsqueda."),
            ("Botón 'Cancelar'",
             "Cierra el diálogo sin realizar ninguna exportación."),
        ], st),
        Spacer(1, 0.3*cm),
        Paragraph(
            "ℹ  Al exportar, el sistema abre el explorador de archivos para que el usuario "
            "elija la ubicación y nombre del archivo de destino. Los archivos Excel tienen "
            "extensión .xlsx y los PDF tienen extensión .pdf.",
            st["nota"]),
        PageBreak(),
    ]
    return items

# ─── SECCIÓN 9: ESTADOS DEL DICTAMEN ─────────────────────────────────────────
def seccion_estados(st):
    items = [
        Paragraph("9. ESTADOS DEL DICTAMEN Y FLUJO DE TRABAJO", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "Cada dictamen tiene un Estado que refleja su fase dentro del proceso "
            "técnico-jurídico. El estado debe actualizarse cada vez que el expediente "
            "avance a la siguiente etapa del flujo de trabajo de la Sección Técnica:",
            st["cuerpo"]),
        Spacer(1, 0.3*cm),
        _tabla_simple([
            ["#", "Estado", "Descripción"],
            ["1", "Revisión documental",
             "El expediente fue recibido y se revisan los documentos de la denuncia."],
            ["2", "Programado para inspección",
             "Se tiene fecha agendada para la inspección de campo."],
            ["3", "En inspección de campo",
             "El técnico se encuentra realizando la visita al sitio del hecho."],
            ["4", "En análisis de resultados",
             "La información de campo está siendo procesada y analizada."],
            ["5", "En proceso de redacción",
             "El técnico está redactando el documento del dictamen."],
            ["6", "En revisión interna",
             "El borrador es revisado por el coordinador o jefe de sección."],
            ["7", "Finalizado (no entregado)",
             "El dictamen está concluido pero aún no se ha entregado al fiscal."],
            ["8", "Finalizado y entregado",
             "El dictamen fue entregado formalmente. Requiere completar 'Entregado A' y 'Fecha de Entrega'."],
        ], st),
        Spacer(1, 0.4*cm),
        Paragraph(
            "⚠  Al seleccionar el estado 'Finalizado y entregado', el sistema muestra "
            "automáticamente los campos adicionales 'Entregado A' y 'Fecha de Entrega', "
            "los cuales son obligatorios para poder guardar el registro.",
            st["nota"]),
        PageBreak(),
    ]
    return items

# ─── SECCIÓN 10: TIPOS DE DECOMISO ────────────────────────────────────────────
def seccion_decomisos(st):
    items = [
        Paragraph("10. TIPOS DE DECOMISO Y UNIDADES", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "El sistema maneja un catálogo técnico de tipos de decomiso con sus unidades "
            "de medida estandarizadas. Al seleccionar un tipo, la unidad se asigna "
            "automáticamente:", st["cuerpo"]),
        Spacer(1, 0.3*cm),
        _tabla_simple([
            ["Tipo de Decomiso", "Unidad", "Categoría"],
            ["MADERA EN ROLLO", "m³ (metros cúbicos)", "Forestal"],
            ["MADERA ASERRADA", "PT (pies tablares)", "Forestal"],
            ["LEÑA", "Cargas", "Forestal"],
            ["ASERRÍN", "Tonelada métrica", "Forestal"],
            ["CARBÓN VEGETAL", "Sacos", "Forestal"],
            ["MATERIAL MINERÍA", "Toneladas", "Minero"],
            ["SUELO CONTAMINADO", "Toneladas", "Suelo"],
            ["AGUA CONTAMINADA", "Litros", "Agua"],
            ["FAUNA SILVESTRE", "Unidades", "Fauna"],
            ["FLORA SILVESTRE", "Unidades", "Flora"],
            ["EMISIONES AIRE", "m³", "Aire"],
            ["MAQUINARIA PESADA", "Unidades", "Forestal"],
            ["EQUIPO FORESTAL", "Unidades", "Forestal"],
            ["EQUIPO MINERO", "Unidades", "Minero"],
            ["PRODUCTOS QUÍMICOS", "Libras", "Químico"],
            ["OTROS", "Editable (libre)", "Otro"],
        ], st),
        Spacer(1, 0.3*cm),
        Paragraph(
            "ℹ  Para el tipo OTROS, el campo Unidad se activa y permite seleccionar "
            "entre: Unidades, Piezas, Kilogramos, Libras, m³, PT, Cargas, Litros, Galones. "
            "El botón ℹ️ en el campo Tipo abre la guía completa dentro de la aplicación.",
            st["nota"]),
        PageBreak(),
    ]
    return items

# ─── SECCIÓN 11: ATAJOS ───────────────────────────────────────────────────────
def seccion_atajos(st):
    items = [
        Paragraph("11. ATAJOS DE TECLADO", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "Los atajos de teclado permiten ejecutar las funciones más comunes sin "
            "usar el ratón, aumentando significativamente la productividad:",
            st["cuerpo"]),
        Spacer(1, 0.3*cm),
        _tabla_simple([
            ["Atajo", "Función"],
            ["Ctrl + S", "Guardar / Agregar el dictamen actual"],
            ["Ctrl + N", "Nuevo registro (limpiar formulario)"],
            ["Ctrl + L", "Limpiar formulario"],
            ["Ctrl + E", "Exportar a Excel"],
            ["Ctrl + P", "Exportar a PDF"],
            ["Ctrl + T", "Alternar tema claro / oscuro"],
            ["F2", "Editar el registro seleccionado en la lista"],
            ["Supr (Delete)", "Eliminar el registro seleccionado"],
            ["F5", "Actualizar / Recargar datos desde la base de datos"],
            ["Alt + F4", "Cerrar la aplicación"],
            ["Enter (en login)", "Intentar inicio de sesión"],
        ], st),
        PageBreak(),
    ]
    return items

# ─── SECCIÓN 12: SEGURIDAD ────────────────────────────────────────────────────
def seccion_seguridad(st):
    items = [
        Paragraph("12. SEGURIDAD Y GESTIÓN DE SESIÓN", st["h1"]),
        HRFlowable(width="100%", thickness=1, color=VERDE_MED),
        Spacer(1, 0.3*cm),
        Paragraph(
            "SIS-TEC-DATOS FEMA implementa múltiples capas de seguridad para proteger "
            "la integridad de los expedientes:", st["cuerpo"]),
        Spacer(1, 0.3*cm),
        _tabla_campos([
            ("Control de acceso",
             "Solo usuarios registrados por el administrador pueden acceder al sistema. "
             "Las contraseñas se almacenan de forma segura con hash criptográfico."),
            ("Bloqueo por intentos fallidos",
             "Tras 3 intentos de inicio de sesión fallidos, el sistema muestra una "
             "advertencia y registra el evento de seguridad."),
            ("Cierre de sesión por inactividad",
             "El sistema cierra automáticamente la sesión si detecta inactividad "
             "durante 30 minutos (sin movimiento de ratón ni pulsaciones de teclado). "
             "Muestra advertencia antes de cerrar."),
            ("Registro de auditoría",
             "Todas las acciones sensibles (creación, edición, eliminación de registros, "
             "cambios de sesión, errores) son registradas en el log de auditoría de la "
             "base de datos con usuario, fecha/hora y descripción del evento."),
            ("Cambio de contraseña",
             "El usuario puede cambiar su contraseña desde el botón 'Cambiar Contraseña' "
             "en la pantalla de login. Requiere la contraseña actual válida. "
             "La nueva contraseña debe tener al menos 6 caracteres."),
            ("Cambio forzado",
             "Si el administrador marca un usuario para 'cambio obligatorio de contraseña', "
             "el sistema lo solicitará inmediatamente tras el primer inicio de sesión válido."),
        ], st),
        Spacer(1, 0.4*cm),
        HRFlowable(width="100%", thickness=1.5, color=DORADO),
        Spacer(1, 0.3*cm),
        Paragraph(
            "© 2025 Fiscalía Especial de Medio Ambiente (FEMA) — "
            "SIS-TEC-DATOS FEMA v2.0 Professional\n"
            "Desarrollado por Ing. Fernando Ardón · Sección Técnica Ambiental · "
            "Antigravity AI © 2025\n"
            "Todos los derechos reservados. Documento de uso institucional interno.",
            st["pie"]),
    ]
    return items

# ─── HELPERS TABLAS ───────────────────────────────────────────────────────────
def _tabla_campos(filas, st):
    """Tabla de dos columnas: nombre del campo y descripción."""
    tdata = []
    for nombre, desc in filas:
        tdata.append([
            Paragraph(f"<b>{nombre}</b>", st["campo_nombre"]),
            Paragraph(desc, st["campo_desc"]),
        ])
    t = Table(tdata, colWidths=[4.5*cm, 11.5*cm])
    t.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND",   (0, 0), (0, -1), VERDE_LIGHT),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [VERDE_LIGHT, colors.white]),
        ("GRID",         (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t

def _tabla_simple(filas, st):
    """Tabla genérica con cabecera verde."""
    tdata = []
    for i, fila in enumerate(filas):
        tdata.append([Paragraph(str(cell), st["campo_nombre"] if i == 0 else st["campo_desc"]) for cell in fila])
    ncols = len(filas[0])
    ancho_disponible = 16*cm
    col_w = [ancho_disponible / ncols] * ncols
    t = Table(tdata, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), VERDE_FEMA),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [VERDE_LIGHT, colors.white]),
        ("GRID",         (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t

# ─── MAIN: CONSTRUIR EL PDF ───────────────────────────────────────────────────
def generar_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2.2*cm, bottomMargin=2.5*cm,
        title="Manual de Usuario — SIS-TEC-DATOS FEMA v2.0",
        author="Ing. Fernando Ardón — FEMA",
        subject="Manual de Usuario Institucional",
    )

    st = crear_estilos()
    story = []

    story += seccion_portada(st)
    story += seccion_indice(st)
    story += seccion_introduccion(st)
    story += seccion_login(st)
    story += seccion_interfaz(st)
    story += seccion_campos(st)
    story += seccion_botones(st)
    story += seccion_menu(st)
    story += seccion_directorio(st)
    story += seccion_exportacion(st)
    story += seccion_estados(st)
    story += seccion_decomisos(st)
    story += seccion_atajos(st)
    story += seccion_seguridad(st)

    doc.build(story, canvasmaker=PaginaConPie)
    print(f"\n✅  Manual generado exitosamente:\n   {OUTPUT_PDF}")

if __name__ == "__main__":
    generar_pdf()
