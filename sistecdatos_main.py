# sistecdatos_main.py
"""
SIS-TEC-DATOS FEMA – Sistema Técnico de Datos de la Fiscalía de Medio Ambiente

Desarrollado para la Fiscalía Especial de Medio Ambiente (FEMA)
para la gestión eficiente de dictámenes técnico-ambientales y datos técnicos.

POR INGENIERO: FERNANDO ARDON, SECCION TECNICA AMBIENTAL, Y ANTIGRAVITY AI @ 2025

Copyright © 2025 Fiscalía Especial de Medio Ambiente (FEMA)
Todos los derechos reservados.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
import os
from datetime import datetime
from PIL import Image, ImageTk
from tkcalendar import Calendar
import logging

logger = logging.getLogger("sistecdatos.main")

# Importar módulos SISTECDATOSFEMA
from sistecdatos_ui import SISTECDATOSFEMAUIStyles
from sistecdatos_db import SISTECDATOSFEMADatabase
from sistecdatos_export import SISTECDATOSFEMAExportManager
from sistecdatos_login import mostrar_ventana_login
from sistecdatos_i18n import _ as translation_func, i18n
from sistecdatos_logic import (
    SISTECDATOSFEMALogic,
    TIPOS_DECOMISO, TIPOS_OPCIONES, CAMPOS_DICTAMEN,
)

def _(clave, **kwargs):
    """Función de conveniencia para traducción"""
    return translation_func(clave, **kwargs)

APP_NAME = "SIS-TEC-DATOS FEMA – Sistema Técnico de Datos de la Fiscalía de Medio Ambiente"
SHORT_NAME = "SIS-TEC-DATOS FEMA"
APP_VERSION = "v2.0 Professional"
ORG_NAME = "Fiscalía Especial de Medio Ambiente (FEMA)"

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Estados del dictamen según flujo de trabajo FEMA (requieren i18n en tiempo de carga)
ESTADOS_DICTAMEN = [
    _("revision_documental"),
    _("programado_inspeccion"),
    _("en_inspeccion"),
    _("analisis_resultados"),
    _("proceso_redaccion"),
    _("revision_interna"),
    _("finalizado_no_entregado"),
    _("finalizado_entregado")
]


class SISTECDATOSFEMAApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Inicializar Base de Datos unificada (Advanced Features)
        self.db = SISTECDATOSFEMADatabase()
        
        # Iniciar con Login antes de construir la interfaz principal
        self.withdraw()
        mostrar_ventana_login(self, self.db, self._on_login_success)

    # Tiempo de inactividad antes de cerrar sesión (30 minutos)
    SESSION_TIMEOUT_MS = 30 * 60 * 1000

    def _on_login_success(self):
        """Callback tras login exitoso"""
        self.deiconify()
        self.title(f"{_('app_title')} | {APP_VERSION}")

        self.export_manager = SISTECDATOSFEMAExportManager(self.db)
        self.styles = SISTECDATOSFEMAUIStyles()
        self.logic = SISTECDATOSFEMALogic(self.db)
        self.mode = "light"  # o "dark"

        self._setup_window()
        self._init_vars()
        self._build_interface()
        self._load_data()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Iniciar vigilancia de inactividad
        self._session_timer_id = None
        self._reset_session_timer()
        self.bind_all("<Motion>", self._reset_session_timer)
        self.bind_all("<KeyPress>", self._reset_session_timer)

    def _reset_session_timer(self, event=None):
        """Reinicia el contador de inactividad cada vez que el usuario actúa."""
        if self._session_timer_id:
            self.after_cancel(self._session_timer_id)
        self._session_timer_id = self.after(self.SESSION_TIMEOUT_MS, self._session_expired)

    def _session_expired(self):
        """Cierra la aplicación por inactividad tras mostrar aviso."""
        logger.info(f"Sesión expirada por inactividad para usuario '{getattr(self.db.current_user, 'username', '?') if self.db.current_user else '?'}'.")
        self.db.registrar_accion('SESSION_TIMEOUT', 'usuarios',
                                 self.db.current_user['id'] if self.db.current_user else None,
                                 nivel='WARNING')
        messagebox.showwarning(
            "Sesión expirada",
            "La sesión se ha cerrado por inactividad.\nEl sistema se cerrará."
        )
        self.on_close()


    def _setup_window(self):
        self.after(0, lambda: self.state("zoomed")) # Workaround para ctk zoomed
        self.iconbitmap(os.path.join(ASSETS_DIR, "icon_sistecdatos.ico"))
        
        # CustomTkinter maneja el fondo automáticamente con set_appearance_mode

    def _init_vars(self):
        # Variables principales para campos
        fields = [
            "dictamen", "denuncia", "imputado", "ofendido", "delito", "sitio",
            "antecedentes", "tecnico", "fecha", "fiscal", "agente", "decomiso",
            "tipo", "cantidad", "otro", "unidad", "estado_dictamen", "fecha_estado", "entregado_a"
        ]
        # Mapeamos internamente las claves de traducción pero mostramos el valor traducido en la UI
        self.campos_vars = {k: tk.StringVar() for k in fields}
        
        # Variables adicionales para campos condicionales
        self.campos_vars["fecha_entrega"] = tk.StringVar()
        
        # Valores por defecto
        self.campos_vars["dictamen"].set("DT-SISTECDATOSFEMA N°-")
        self.campos_vars["fecha"].set(datetime.now().strftime(i18n.formatos_fecha[i18n.idioma_actual]['fecha']))
        self.campos_vars["fecha_estado"].set(datetime.now().strftime(i18n.formatos_fecha[i18n.idioma_actual]['fecha']))
        self.campos_vars["decomiso"].set("NO")
        self.campos_vars["tipo"].set(_("otro").upper())
        self.campos_vars["unidad"].set(_("unidades").upper())
        self.campos_vars["estado_dictamen"].set(_("revision_documental"))

        self.datos = []
        # Diccionario para almacenar referencias a widgets
        self.campos_widgets = {}

        # Referencias para widgets condicionales
        self.widgets_entrega = {}

        # Paginación y búsqueda
        self._page_size = 50
        self._current_page = 0
        self._current_search = ""

    def _build_interface(self):
        # Configurar el grid principal para responsividad
        self.grid_rowconfigure(0, weight=0)  # Header fijo
        self.grid_rowconfigure(1, weight=1)  # Contenido principal expandible
        self.grid_rowconfigure(2, weight=0)  # Barra de estado fija
        self.grid_columnconfigure(0, weight=1)
        
        # ------ MENÚ TRADICIONAL DE WINDOWS ------
        self._crear_menu()
        
        # ------ HEADER CENTRADO ------
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Logo y títulos centrados
        logo_path = os.path.join(ASSETS_DIR, "logo_sistecdatos.png")
        try:
            img = Image.open(logo_path)
            self.logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(160, 160))
            ctk.CTkLabel(header_frame, image=self.logo_img, text="").grid(row=0, column=0, pady=(0, 8))
        except (FileNotFoundError, OSError) as e:
            logger.warning(f"Logo no encontrado en '{logo_path}': {e}")
            ctk.CTkLabel(header_frame, text="🏛️", font=ctk.CTkFont(size=48)).grid(row=0, column=0, pady=(0, 8))
        
        ctk.CTkLabel(header_frame, text=APP_NAME, font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
                     text_color=self.styles.get_colors()["accent"]).grid(row=1, column=0, pady=(0, 5))
        ctk.CTkLabel(header_frame, text=ORG_NAME, font=ctk.CTkFont(family="Segoe UI", size=14)).grid(row=2, column=0, pady=(0, 10))

        # ------ CONTENIDO PRINCIPAL ------
        main_content = ctk.CTkFrame(self, fg_color="transparent")
        main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        main_content.grid_rowconfigure(0, weight=1)
        main_content.grid_columnconfigure(0, weight=1)
        
        self.tabview = ctk.CTkTabview(main_content)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        
        self.tabview.add("Ingreso y Edición")
        self.tabview.add("Directorio de Expedientes (Búsqueda)")
        
        tab_form = self.tabview.tab("Ingreso y Edición")
        tab_form.grid_rowconfigure(0, weight=1)
        tab_form.grid_rowconfigure(1, weight=0)
        tab_form.grid_columnconfigure(0, weight=1)
        
        tab_list = self.tabview.tab("Directorio de Expedientes (Búsqueda)")
        tab_list.grid_rowconfigure(0, weight=1)
        tab_list.grid_columnconfigure(0, weight=1)

        # ------ FORMULARIO COMPACTO ------
        form_frame = ctk.CTkFrame(tab_form)
        form_frame.grid(row=0, column=0, sticky="nsew", pady=10)
        
        # Etiqueta de título del formulario
        ctk.CTkLabel(form_frame, text=_("informacion_dictamen"), font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")).grid(row=0, column=0, columnspan=3, pady=(10, 5), padx=15, sticky="w")
        
        # Configurar grid del formulario para tres columnas más compactas
        form_frame.grid_columnconfigure(0, weight=1)  # Columna izquierda
        form_frame.grid_columnconfigure(1, weight=1)  # Columna central
        form_frame.grid_columnconfigure(2, weight=1)  # Columna derecha
        
        self.form_container = form_frame
        self.entries = {}
        
        # Dividir campos en tres columnas para mayor compacidad
        campos_lista = list(self.campos_vars.items())
        campos_filtrados = [(k, v) for k, v in campos_lista if k != "fecha_entrega"]
        
        # Dividir en tres columnas
        tercio = len(campos_filtrados) // 3
        campos_izquierda = campos_filtrados[:tercio]
        campos_centro = campos_filtrados[tercio:tercio*2]
        campos_derecha = campos_filtrados[tercio*2:]
        
        # Crear las tres columnas
        left_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(15, 5), pady=(0, 10))
        left_frame.grid_columnconfigure(1, weight=1)
        
        center_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        center_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=(0, 10))
        center_frame.grid_columnconfigure(1, weight=1)
        
        right_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        right_frame.grid(row=1, column=2, sticky="nsew", padx=(5, 15), pady=(0, 10))
        right_frame.grid_columnconfigure(1, weight=1)
        
        # Llenar las columnas
        self._crear_campos_columna_compacta(left_frame, campos_izquierda, 1)
        self._crear_campos_columna_compacta(center_frame, campos_centro, 1)
        self._crear_campos_columna_compacta(right_frame, campos_derecha, 1)
        
        # Crear campos adicionales para entrega (ocultos por defecto)
        self._crear_campos_entrega()

        # ------ PANEL DE BOTONES COMPACTO ------
        btn_frame = ctk.CTkFrame(tab_form, fg_color="transparent")
        btn_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        btn_frame.grid_columnconfigure(0, weight=1)
        
        # Frame interno para centrar botones en una sola fila
        btn_inner = ctk.CTkFrame(btn_frame, fg_color="transparent")
        btn_inner.grid(row=0, column=0)
        
        # Todos los botones en una fila para ahorrar espacio
        ctk.CTkButton(btn_inner, text="➕ " + _("add"), command=self.add_record, 
                     width=100, height=32, corner_radius=8).grid(row=0, column=0, padx=6, pady=5)
        ctk.CTkButton(btn_inner, text="📊 Excel", command=self.export_excel, 
                     width=90, height=32, corner_radius=8, fg_color="#28a745", hover_color="#218838").grid(row=0, column=1, padx=6, pady=5)
        ctk.CTkButton(btn_inner, text="📄 PDF", command=self.export_pdf, 
                     width=90, height=32, corner_radius=8, fg_color="#dc3545", hover_color="#c82333").grid(row=0, column=2, padx=6, pady=5)
        ctk.CTkButton(btn_inner, text="🗑️ " + _("clear"), command=self.clear_form, 
                     width=90, height=32, corner_radius=8, fg_color="#6c757d", hover_color="#5a6268").grid(row=0, column=3, padx=6, pady=5)
        ctk.CTkButton(btn_inner, text="🌓 " + _("tema_visual"), command=self.toggle_theme, 
                     width=100, height=32, corner_radius=8, fg_color="#6200ee", hover_color="#3700b3").grid(row=0, column=4, padx=6, pady=5)
        ctk.CTkButton(btn_inner, text="❌ " + _("close"), command=self.on_close, 
                     width=90, height=32, corner_radius=8, fg_color="#343a40", hover_color="#23272b").grid(row=0, column=5, padx=6, pady=5)

        # ------ LISTA DE DICTÁMENES CON SCROLL ------
        list_frame = ctk.CTkFrame(tab_list)
        list_frame.grid(row=0, column=0, sticky="nsew", pady=10)
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Frame superior de la lista (Título y Buscador)
        list_header_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        list_header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        list_header_frame.grid_columnconfigure(1, weight=1)  # Espacio flexible
        
        ctk.CTkLabel(list_header_frame, text=_("decomisos_registrados"), font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        
        # Búsqueda
        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(list_header_frame, textvariable=self.search_var, placeholder_text="Buscar dictamen, sitio, etc...", width=250, height=28)
        search_entry.grid(row=0, column=2, padx=(10, 5), sticky="e")
        search_entry.bind('<Return>', self._perform_search)
        
        ctk.CTkButton(list_header_frame, text="🔍 Buscar", width=80, height=28, command=self._perform_search).grid(row=0, column=3, padx=2)
        ctk.CTkButton(list_header_frame, text="✖", width=28, height=28, command=self._clear_search, fg_color="#6c757d", hover_color="#5a6268").grid(row=0, column=4, padx=2)
        
        # Frame para lista y scrollbar
        list_container = ctk.CTkFrame(list_frame, fg_color="transparent")
        list_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        list_container.grid_rowconfigure(0, weight=1)
        list_container.grid_columnconfigure(0, weight=1)
        
        # Lista con scrollbars (Vertical y Horizontal)
        self.lista = tk.Listbox(list_container, font=('Segoe UI', 10), 
                                relief="flat", borderwidth=0, highlightthickness=0,
                                height=8)
        self.lista.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar vertical
        scrollbar_v = ctk.CTkScrollbar(list_container, orientation="vertical", command=self.lista.yview)
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        
        # Scrollbar horizontal
        scrollbar_h = ctk.CTkScrollbar(list_container, orientation="horizontal", command=self.lista.xview)
        scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        self.lista.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Context menu y doble-clic
        self.lista.bind("<Button-3>", self.show_context_menu)
        self.lista.bind("<Double-Button-1>", self.visualizar_seleccionado)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="👁️ " + _("ver_detalles", default="Ver Detalles"), command=self.visualizar_seleccionado)
        self.context_menu.add_command(label="✏️ " + _("edit"), command=self.edit_selected)
        self.context_menu.add_command(label="🗑️ " + _("delete"), command=self.delete_selected)

        # ------ CONTROLES DE PAGINACIÓN ------
        pag_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        pag_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))

        self.btn_prev = ctk.CTkButton(pag_frame, text="◀ Anterior", width=90, height=26,
                                      command=self._pagina_anterior, state="disabled")
        self.btn_prev.pack(side="left", padx=(0, 6))

        self.lbl_pagina = ctk.CTkLabel(pag_frame, text="Pág. 1 / 1", font=ctk.CTkFont(size=11))
        self.lbl_pagina.pack(side="left", padx=6)

        self.btn_next = ctk.CTkButton(pag_frame, text="Siguiente ▶", width=90, height=26,
                                      command=self._pagina_siguiente, state="disabled")
        self.btn_next.pack(side="left", padx=6)

        self.lbl_total_items = ctk.CTkLabel(pag_frame, text="", font=ctk.CTkFont(size=11))
        self.lbl_total_items.pack(side="left", padx=10)

        # ------ BARRA DE ESTADO ------
        self.statusbar = ctk.CTkLabel(self, text="✅ " + _("refresh") + " - SISTECDATOSFEMA " + APP_VERSION, 
                                     font=ctk.CTkFont(family="Segoe UI", size=12),
                                     anchor='w', padx=20, pady=5)
        self.statusbar.grid(row=2, column=0, sticky="ew")
        
        # Inicializar el comportamiento del Combobox Unidad basado en el tipo por defecto
        self.actualizar_unidad_categoria()

    def _crear_menu(self):
        """Crea el menú tradicional de Windows"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("menu_file"), menu=archivo_menu)
        archivo_menu.add_command(label=_("add"), command=self.clear_form, accelerator="Ctrl+N")
        archivo_menu.add_command(label=_("save"), command=self.add_record, accelerator="Ctrl+S")
        archivo_menu.add_separator()
        archivo_menu.add_command(label=_("export") + " Excel", command=self.export_excel, accelerator="Ctrl+E")
        archivo_menu.add_command(label=_("export") + " PDF", command=self.export_pdf, accelerator="Ctrl+P")
        archivo_menu.add_separator()
        archivo_menu.add_command(label=_("close"), command=self.on_close, accelerator="Alt+F4")
        
        # Menú Edición
        edicion_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("menu_edit"), menu=edicion_menu)
        edicion_menu.add_command(label=_("edit"), command=self.edit_selected, accelerator="F2")
        edicion_menu.add_command(label=_("delete"), command=self.delete_selected, accelerator="Del")
        edicion_menu.add_separator()
        edicion_menu.add_command(label=_("clear"), command=self.clear_form, accelerator="Ctrl+L")
        
        # Menú Ver
        ver_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=ver_menu)
        ver_menu.add_command(label="Cambiar Tema", command=self.toggle_theme, accelerator="Ctrl+T")
        ver_menu.add_command(label="Actualizar Lista", command=self._load_data, accelerator="F5")
        
        # Menú Herramientas
        herramientas_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("menu_tools"), menu=herramientas_menu)
        herramientas_menu.add_command(label=_("decomisos_title"), command=self.mostrar_info_tipos)
        herramientas_menu.add_command(label=_("fecha"), command=lambda: self.abrir_calendario("fecha"))
        
        # Menú Ayuda
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("menu_help"), menu=ayuda_menu)
        ayuda_menu.add_command(label=_("acerca_de"), command=self.mostrar_acerca_de)
        ayuda_menu.add_command(label=_("manual_usuario"), command=self.mostrar_manual)
        
        # Configurar atajos de teclado
        self.bind('<Control-n>', lambda e: self.clear_form())
        self.bind('<Control-s>', lambda e: self.add_record())
        self.bind('<Control-e>', lambda e: self.export_excel())
        self.bind('<Control-p>', lambda e: self.export_pdf())
        self.bind('<Control-l>', lambda e: self.clear_form())
        self.bind('<Control-t>', lambda e: self.toggle_theme())
        self.bind('<F2>', lambda e: self.edit_selected())
        self.bind('<Delete>', lambda e: self.delete_selected())
        self.bind('<F5>', lambda e: self._load_data())

    def _crear_campos_columna_compacta(self, parent_frame, campos_lista, offset_row):
        """Crea los campos de una columna específica con diseño compacto usando CustomTkinter"""
        for row, (field, var) in enumerate(campos_lista):
            # Label alineado a la derecha
            ctk.CTkLabel(parent_frame, text=_(field)+":", font=ctk.CTkFont(family="Segoe UI", size=12)).grid(
                row=row, column=0, sticky="e", pady=5, padx=(2, 8))
            
            # Caso especial para el campo "tipo" - usar CTKComboBox
            if field == "tipo":
                tipo_cb = ctk.CTkComboBox(parent_frame, variable=var, values=TIPOS_OPCIONES, 
                                        command=lambda x: self.actualizar_unidad_categoria(),
                                        width=200, height=28)
                tipo_cb.grid(row=row, column=1, sticky="ew", pady=5)
                self.campos_widgets["tipo"] = tipo_cb
                self.entries[field] = tipo_cb
                
                # Botón de información para tipos
                ctk.CTkButton(parent_frame, text="ℹ️", width=30, height=28, 
                             command=self.mostrar_info_tipos).grid(row=row, column=2, sticky="w", padx=(5, 0))
                
            # Caso especial para el campo "unidad"
            elif field == "unidad":
                unidad_cb = ctk.CTkComboBox(parent_frame, variable=var, values=[], width=200, height=28)
                unidad_cb.grid(row=row, column=1, sticky="ew", pady=5)
                self.campos_widgets["unidad"] = unidad_cb
                self.entries[field] = unidad_cb
                
            # Caso especial para el campo "decomiso"
            elif field == "decomiso":
                decomiso_cb = ctk.CTkComboBox(parent_frame, variable=var, values=["SI", "NO"], 
                                           width=100, height=28)
                decomiso_cb.grid(row=row, column=1, sticky="w", pady=5)
                self.campos_widgets["decomiso"] = decomiso_cb
                self.entries[field] = decomiso_cb
                
            # Caso especial para el campo "fecha"
            elif field == "fecha":
                f = ctk.CTkFrame(parent_frame, fg_color="transparent")
                f.grid(row=row, column=1, sticky="ew", pady=5)
                f.grid_columnconfigure(0, weight=1)
                
                fecha_entry = ctk.CTkEntry(f, textvariable=var, height=28)
                fecha_entry.grid(row=0, column=0, sticky="ew")
                self.entries[field] = fecha_entry
                self.campos_widgets[field] = fecha_entry
                
                ctk.CTkButton(f, text="📅", width=30, height=28,
                             command=lambda f=field: self.abrir_calendario(f)).grid(row=0, column=1, padx=(5, 0))
                          
            # Caso especial para el campo "estado_dictamen"
            elif field == "estado_dictamen":
                estado_cb = ctk.CTkComboBox(parent_frame, variable=var, values=ESTADOS_DICTAMEN,
                                         command=lambda x: self.actualizar_campos_entrega(),
                                         width=200, height=28)
                estado_cb.grid(row=row, column=1, sticky="ew", pady=5)
                self.campos_widgets["estado_dictamen"] = estado_cb
                self.entries[field] = estado_cb
                self.estado_row = offset_row + row
                
            # Caso especial para el campo "fecha_estado"
            elif field == "fecha_estado":
                f = ctk.CTkFrame(parent_frame, fg_color="transparent")
                f.grid(row=row, column=1, sticky="ew", pady=5)
                f.grid_columnconfigure(0, weight=1)
                
                fecha_estado_entry = ctk.CTkEntry(f, textvariable=var, height=28)
                fecha_estado_entry.grid(row=0, column=0, sticky="ew")
                self.entries[field] = fecha_estado_entry
                self.campos_widgets[field] = fecha_estado_entry
                
                ctk.CTkButton(f, text="📅", width=30, height=28,
                             command=lambda f=field: self.abrir_calendario(f)).grid(row=0, column=1, padx=(5, 0))

            # Caso especial para el campo "antecedentes"
            elif field == "antecedentes":
                widget = ctk.CTkTextbox(parent_frame, height=80, font=("Segoe UI", 11), border_width=2)
                widget.grid(row=row, column=1, columnspan=2, sticky="ew", pady=5)
                self.text_antecedentes = widget
                self.entries[field] = widget
                self.campos_widgets[field] = widget
                
                # Sincronización StringVar -> CTKTextbox
                def sync_var_to_text(*args):
                    current = self.text_antecedentes.get("1.0", tk.END).strip()
                    new = var.get()
                    if current != new:
                        self.text_antecedentes.delete("1.0", tk.END)
                        self.text_antecedentes.insert("1.0", new)
                
                var.trace_add('write', sync_var_to_text)
                
                # Sincronización CTKTextbox -> StringVar (vía evento o método save)
                # Nota: CTKTextbox no tiene textvariable, actualizaremos var al guardar o perder foco
                widget.bind('<FocusOut>', lambda e: var.set(self.text_antecedentes.get("1.0", tk.END).strip()))
                
            else:
                entry = ctk.CTkEntry(parent_frame, textvariable=var, height=28)
                entry.grid(row=row, column=1, sticky="ew", pady=5)
                self.entries[field] = entry
                self.campos_widgets[field] = entry

    def _crear_campos_columna(self, parent_frame, campos_lista, offset_row):
        """Crea los campos de una columna específica con alineación profesional usando CustomTkinter"""
        for row, (field, var) in enumerate(campos_lista):
            # Label alineado a la derecha
            ctk.CTkLabel(parent_frame, text=_(field)+":", font=ctk.CTkFont(family="Segoe UI", size=13)).grid(
                row=row, column=0, sticky="e", pady=8, padx=(5, 12))
            
            # Caso especial para el campo "tipo"
            if field == "tipo":
                tipo_cb = ctk.CTkComboBox(parent_frame, variable=var, values=TIPOS_OPCIONES, 
                                        command=lambda x: self.actualizar_unidad_categoria(),
                                        width=250, height=32)
                tipo_cb.grid(row=row, column=1, sticky="ew", pady=8)
                self.campos_widgets["tipo"] = tipo_cb
                self.entries[field] = tipo_cb
                
                ctk.CTkButton(parent_frame, text="ℹ️", width=40, height=32, 
                             command=self.mostrar_info_tipos).grid(row=row, column=2, sticky="w", padx=(8, 0))
                
            # Caso especial para el campo "unidad"
            elif field == "unidad":
                unidad_cb = ctk.CTkComboBox(parent_frame, variable=var, values=[], width=250, height=32)
                unidad_cb.grid(row=row, column=1, sticky="ew", pady=8)
                self.campos_widgets["unidad"] = unidad_cb
                self.entries[field] = unidad_cb
                
            # Caso especial para el campo "decomiso"
            elif field == "decomiso":
                decomiso_cb = ctk.CTkComboBox(parent_frame, variable=var, values=["SI", "NO"], 
                                           width=120, height=32)
                decomiso_cb.grid(row=row, column=1, sticky="w", pady=8)
                self.campos_widgets["decomiso"] = decomiso_cb
                self.entries[field] = decomiso_cb
                
            # Caso especial para el campo "fecha"
            elif field == "fecha":
                f = ctk.CTkFrame(parent_frame, fg_color="transparent")
                f.grid(row=row, column=1, sticky="ew", pady=8)
                f.grid_columnconfigure(0, weight=1)
                
                fecha_entry = ctk.CTkEntry(f, textvariable=var, height=32)
                fecha_entry.grid(row=0, column=0, sticky="ew")
                self.entries[field] = fecha_entry
                self.campos_widgets[field] = fecha_entry
                
                ctk.CTkButton(f, text="📅", width=40, height=32,
                             command=lambda f=field: self.abrir_calendario(f)).grid(row=0, column=1, padx=(8, 0))
                          
            # Caso especial para el campo "estado_dictamen"
            elif field == "estado_dictamen":
                estado_cb = ctk.CTkComboBox(parent_frame, variable=var, values=ESTADOS_DICTAMEN,
                                         command=lambda x: self.actualizar_campos_entrega(),
                                         width=250, height=32)
                estado_cb.grid(row=row, column=1, sticky="ew", pady=8)
                self.campos_widgets["estado_dictamen"] = estado_cb
                self.entries[field] = estado_cb
                self.estado_row = offset_row + row
                
            # Caso especial para el campo "fecha_estado"
            elif field == "fecha_estado":
                f = ctk.CTkFrame(parent_frame, fg_color="transparent")
                f.grid(row=row, column=1, sticky="ew", pady=8)
                f.grid_columnconfigure(0, weight=1)
                
                fecha_estado_entry = ctk.CTkEntry(f, textvariable=var, height=32)
                fecha_estado_entry.grid(row=0, column=0, sticky="ew")
                self.entries[field] = fecha_estado_entry
                self.campos_widgets[field] = fecha_estado_entry
                
                ctk.CTkButton(f, text="📅", width=40, height=32,
                             command=lambda f=field: self.abrir_calendario(f)).grid(row=0, column=1, padx=(8, 0))
            else:
                entry = ctk.CTkEntry(parent_frame, textvariable=var, height=32)
                entry.grid(row=row, column=1, sticky="ew", pady=8)
                self.entries[field] = entry
                self.campos_widgets[field] = entry

    def _crear_campos_entrega(self):
        """Crea los campos adicionales para entrega (ocultos por defecto)"""
        form_container = self.form_container
        
        # Etiquetas
        self.widgets_entrega["lbl_entregado"] = ctk.CTkLabel(form_container, text=_("entregado_a")+":")
        self.widgets_entrega["lbl_fecha_entrega"] = ctk.CTkLabel(form_container, text=_("fecha_entrega")+":")
        
        # Entradas
        self.widgets_entrega["entry_entregado"] = ctk.CTkEntry(form_container, textvariable=self.campos_vars["entregado_a"], width=200)
        self.widgets_entrega["entry_fecha_entrega"] = ctk.CTkEntry(form_container, textvariable=self.campos_vars["fecha_entrega"], 
                                                                 width=150)
        self.widgets_entrega["btn_fecha_entrega"] = ctk.CTkButton(form_container, text="📅", width=40,
                                                               command=self.abrir_calendario_fecha_entrega)
        
        # Por defecto, ocultar estos widgets
        for widget in self.widgets_entrega.values():
            widget.grid_remove()

    def actualizar_campos_entrega(self, event=None):
        """Muestra u oculta campos adicionales según el estado seleccionado"""
        estado = self.campos_vars["estado_dictamen"].get()
        
        if estado == _("finalizado_entregado"):
            # Mostrar campos adicionales
            row_entregado = self.estado_row + 1
            row_fecha_entrega = self.estado_row + 2
            
            self.widgets_entrega["lbl_entregado"].grid(row=row_entregado, column=0, sticky="e", padx=4, pady=4)
            self.widgets_entrega["entry_entregado"].grid(row=row_entregado, column=1, sticky="w", padx=4, pady=4)
            
            self.widgets_entrega["lbl_fecha_entrega"].grid(row=row_fecha_entrega, column=0, sticky="e", padx=4, pady=4)
            self.widgets_entrega["entry_fecha_entrega"].grid(row=row_fecha_entrega, column=1, sticky="w", padx=(0, 5), pady=4)
            self.widgets_entrega["btn_fecha_entrega"].grid(row=row_fecha_entrega, column=2, sticky="w", padx=2, pady=4)
            
            self.statusbar['text'] = _("refresh") + " - " + _("campos_incompletos")
        else:
            # Ocultar campos adicionales
            for widget in self.widgets_entrega.values():
                widget.grid_remove()
            
            # Limpiar valores
            self.campos_vars["entregado_a"].set("")
            self.campos_vars["fecha_entrega"].set("")
            
            self.statusbar['text'] = f"Estado cambiado a: {estado}"

    def abrir_calendario_fecha_entrega(self):
        """Abre calendario específico para fecha de entrega"""
        top = tk.Toplevel(self)
        top.title("Seleccionar fecha de entrega")
        top.grab_set()
        
        # Usar fecha actual por defecto
        today = datetime.today()
        cal = Calendar(top, selectmode='day', year=today.year, month=today.month, day=today.day, date_pattern='dd/MM/yyyy')
        cal.pack(padx=15, pady=15)
        
        def seleccionar():
            fecha = cal.get_date()
            self.campos_vars["Fecha de Entrega"].set(fecha)
            top.destroy()
            
        ttk.Button(top, text="Seleccionar", command=seleccionar).pack(pady=8)

    def validar_guardado(self):
        """Valida que los campos obligatorios estén completos antes de guardar"""
        estado = self.campos_vars["estado_dictamen"].get()
        
        if estado == _("finalizado_entregado"):
            if not self.campos_vars["entregado_a"].get().strip():
                messagebox.showwarning(_("campos_incompletos"), _("campo_obligatorio", campo=_("entregado_a")))
                return False
            if not self.campos_vars["fecha_entrega"].get().strip():
                messagebox.showwarning(_("campos_incompletos"), _("campo_obligatorio", campo=_("fecha_entrega")))
                return False
        
        return True

    def _load_data(self):
        """Carga la página actual de dictámenes en la lista."""
        rows, total, page = self.logic.cargar_pagina(self._current_page, self._page_size, self._current_search)
        self._current_page = page
        self.datos = rows
        total_pages = max(1, -(-total // self._page_size))

        self.lista.delete(0, tk.END)
        for item in rows:
            item_str = [str(f) if f is not None else "" for f in item]
            self.lista.insert(tk.END, " | ".join(item_str))

        pagina_actual = self._current_page + 1
        self.lbl_pagina.configure(text=f"Pág. {pagina_actual} / {total_pages}")
        self.lbl_total_items.configure(text=f"({total} registros)")
        self.btn_prev.configure(state="normal" if self._current_page > 0 else "disabled")
        self.btn_next.configure(state="normal" if pagina_actual < total_pages else "disabled")

    def _perform_search(self, event=None):
        self._current_search = self.search_var.get().strip()
        self._current_page = 0
        self._load_data()

    def _clear_search(self):
        self.search_var.set("")
        self._current_search = ""
        self._current_page = 0
        self._load_data()

    def _pagina_anterior(self):
        self._current_page -= 1
        self._load_data()

    def _pagina_siguiente(self):
        self._current_page += 1
        self._load_data()

    def _leer_campos(self) -> dict:
        """Lee todos los campos del formulario como dict plano."""
        return {k: v.get() for k, v in self.campos_vars.items()}

    # --------- ACCIONES PRINCIPALES ----------
    def _validar_inputs(self) -> bool:
        """Delega validación a la capa de lógica y muestra mensajes en UI."""
        campos = self._leer_campos()
        formato = i18n.formatos_fecha[i18n.idioma_actual]['fecha']
        valido, error = self.logic.validar_campos(campos, formato)
        if not valido:
            campo_foco, mensaje = error
            messagebox.showwarning(_("campos_incompletos"), mensaje)
            if campo_foco in self.entries:
                self.entries[campo_foco].focus()
            return False
        return True

    def validar_guardado(self) -> bool:
        """Delega validación de estado de entrega a la capa de lógica."""
        campos = self._leer_campos()
        valido, error = self.logic.validar_estado_entrega(
            estado=campos.get("estado_dictamen", ""),
            entregado_a=campos.get("entregado_a", ""),
            fecha_entrega=campos.get("fecha_entrega", ""),
            estado_entregado=_("finalizado_entregado"),
        )
        if not valido:
            campo_foco, mensaje = error
            messagebox.showwarning(_("campos_incompletos"), mensaje)
            return False
        return True

    def add_record(self):
        if not self._validar_inputs():
            return
        if not self.validar_guardado():
            return

        try:
            self.logic.guardar_dictamen(self._leer_campos())
        except Exception as e:
            logger.error(f"Error al guardar dictamen: {e}")
            messagebox.showerror("Error", f"No se pudo guardar el dictamen:\n{e}")
            return
        self.statusbar['text'] = _("dictamen_guardado")
        self._load_data()
        self.clear_form()

    def export_excel(self):
        self._abrir_dialogo_exportacion("excel")

    def export_pdf(self):
        self._abrir_dialogo_exportacion("pdf")

    def _abrir_dialogo_exportacion(self, tipo_export):
        """Abre un diálogo para seleccionar parámetros de exportación y procesa la exportación"""
        win = ctk.CTkToplevel(self)
        win.title(f"Opciones de Exportación ({tipo_export.upper()})")
        win.geometry("450x380")
        win.grab_set()
        
        # Opciones de Fecha
        ctk.CTkLabel(win, text="Rango de Fechas (Opcional):", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")).pack(pady=(15, 10))
        
        date_frame = ctk.CTkFrame(win, fg_color="transparent")
        date_frame.pack(fill="x", padx=20)
        
        # Fecha Inicio
        ctk.CTkLabel(date_frame, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
        var_inicio = tk.StringVar()
        entry_inicio = ctk.CTkEntry(date_frame, textvariable=var_inicio, width=120)
        entry_inicio.grid(row=0, column=1, padx=5, pady=5)
        
        def cal_inicio():
            top = ctk.CTkToplevel(win)
            top.title("Seleccionar Fecha")
            top.geometry("300x350")
            top.grab_set()
            
            cal = Calendar(top, selectmode='day', date_pattern=i18n.formatos_fecha[i18n.idioma_actual]['fecha'].replace('%d','dd').replace('%m','MM').replace('%Y','yyyy'))
            cal.pack(padx=15, pady=15)
            
            def set_date():
                var_inicio.set(cal.get_date())
                top.destroy()
            ctk.CTkButton(top, text="Aceptar", command=set_date).pack(pady=10)
            
        ctk.CTkButton(date_frame, text="📅", width=30, command=cal_inicio).grid(row=0, column=2, padx=5, pady=5)
        
        # Fecha Fin
        ctk.CTkLabel(date_frame, text="Hasta:").grid(row=1, column=0, padx=5, pady=5)
        var_fin = tk.StringVar()
        entry_fin = ctk.CTkEntry(date_frame, textvariable=var_fin, width=120)
        entry_fin.grid(row=1, column=1, padx=5, pady=5)
        
        def cal_fin():
            top = ctk.CTkToplevel(win)
            top.title("Seleccionar Fecha")
            top.geometry("300x350")
            top.grab_set()
            
            cal = Calendar(top, selectmode='day', date_pattern=i18n.formatos_fecha[i18n.idioma_actual]['fecha'].replace('%d','dd').replace('%m','MM').replace('%Y','yyyy'))
            cal.pack(padx=15, pady=15)
            
            def set_date():
                var_fin.set(cal.get_date())
                top.destroy()
            ctk.CTkButton(top, text="Aceptar", command=set_date).pack(pady=10)
            
        ctk.CTkButton(date_frame, text="📅", width=30, command=cal_fin).grid(row=1, column=2, padx=5, pady=5)
        
        # Texto Libre (Fiscal/Agente)
        ctk.CTkLabel(win, text="Filtro (ej. nombre de Fiscal, Agente o Sitio):", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")).pack(pady=(20, 10))
        var_texto = tk.StringVar()
        ctk.CTkEntry(win, textvariable=var_texto, width=280).pack(pady=5)
        
        def ejecutar_exportacion():
            inicio = var_inicio.get().strip()
            fin = var_fin.get().strip()
            texto = var_texto.get().strip()
            
            fecha_inicio_obj = None
            fecha_fin_obj = None
            
            if inicio and fin:
                try:
                    fecha_inicio_obj = datetime.strptime(inicio, "%d/%m/%Y").date()
                    fecha_fin_obj = datetime.strptime(fin, "%d/%m/%Y").date()
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Use el calendario o dd/mm/yyyy.")
                    return
            elif inicio or fin:
                messagebox.showerror("Error", "Si usa filtro de fechas debe indicar Desde y Hasta.")
                return
                
            win.destroy()
            self.statusbar['text'] = "Preparando exportación..."
            
            # Consultar BD con los filtros
            datos_filtrados = self.db.fetch_dictamenes_para_exportar(
                fecha_inicio=fecha_inicio_obj,
                fecha_fin=fecha_fin_obj,
                buscar_texto=texto
            )
            
            if tipo_export == "excel":
                self.export_manager.export_to_excel(datos_filtrados)
                self.statusbar['text'] = "Filtro aplicado. Archivo de Excel generado."
            else:
                self.export_manager.export_to_pdf(datos_filtrados)
                self.statusbar['text'] = "Filtro aplicado. Archivo PDF generado."
                
        # Botones
        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Exportar Todos" if not (var_inicio.get() or var_texto.get()) else "Exportar Filtrados", command=ejecutar_exportacion, width=150).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", command=win.destroy, fg_color="#6c757d", hover_color="#5a6268", width=120).pack(side="right", padx=10)

    def mostrar_info_tipos(self):
        """Muestra una guía de los tipos de decomiso disponibles"""
        texto = self.logic.guia_tipos()
        win = ctk.CTkToplevel(self)
        win.title("Guía de Tipos de Decomiso")
        win.geometry("500x400")
        
        txt = ctk.CTkTextbox(win, width=480, height=300, font=("Segoe UI", 11))
        txt.pack(padx=10, pady=10)
        txt.insert("1.0", texto)
        txt.configure(state="disabled")
        
        ctk.CTkButton(win, text=_("close"), command=win.destroy).pack(pady=10)

    def abrir_calendario(self, nombre_var):
        """Abre un diálogo de calendario para seleccionar fecha"""
        top = ctk.CTkToplevel(self)
        top.title(_("fecha"))
        top.geometry("300x350")
        top.grab_set()
        
        try:
            actual = datetime.strptime(self.campos_vars[nombre_var].get(), 
                                     i18n.formatos_fecha[i18n.idioma_actual]['fecha'])
        except Exception:
            actual = datetime.now()
            
        cal = Calendar(top, selectmode='day', year=actual.year, month=actual.month, day=actual.day, 
                       date_pattern=i18n.formatos_fecha[i18n.idioma_actual]['fecha'].replace('%d','dd').replace('%m','MM').replace('%Y','yyyy'))
        cal.pack(padx=15, pady=15)

        def seleccionar():
            fecha_sel = cal.get_date()
            self.campos_vars[nombre_var].set(fecha_sel)
            top.destroy()
        ctk.CTkButton(top, text=_("seleccionar"), command=seleccionar).pack(pady=10)

    def actualizar_unidad_categoria(self, event=None):
        """Actualiza automáticamente la unidad cuando se selecciona un tipo de decomiso."""
        tipo = self.campos_vars["tipo"].get()
        unidad_widget = self.campos_widgets.get("unidad")
        if not unidad_widget:
            return

        if tipo not in TIPOS_OPCIONES:
            unidad_widget.configure(state="readonly")
            self.statusbar.configure(text="Seleccione un tipo de decomiso válido")
            return

        categoria_key = self.logic.obtener_categoria_para_tipo(tipo).lower()
        categoria = _(categoria_key)
        unidades = self.logic.obtener_unidades_para_tipo(tipo)

        if self.logic.tipo_permite_unidad_libre(tipo):
            self.campos_vars["unidad"].set("")
            unidad_widget.configure(state="normal", values=unidades)
            self.statusbar.configure(
                text=f"{_('tipo')}: {tipo} | {_('categoria_ambiental')}: {categoria} | {_('unidad')}: EDITABLE"
            )
        else:
            unidad = unidades[0] if unidades else ""
            self.campos_vars["unidad"].set(unidad)
            unidad_widget.configure(state="readonly", values=[unidad])
            self.statusbar.configure(
                text=f"{_('tipo')}: {tipo} | {_('categoria_ambiental')}: {categoria} | {_('unidad')}: {unidad}"
            )

    def clear_form(self):
        """Limpia todos los campos del formulario"""
        for var in self.campos_vars.values():
            var.set("")
        
        # Limpiar específicamente el widget CTKTextbox de Antecedentes
        if hasattr(self, 'text_antecedentes'):
            self.text_antecedentes.delete("1.0", tk.END)
        
        # Restaurar valores por defecto
        self.campos_vars["dictamen"].set("DT-SISTECDATOSFEMA N°-")
        self.campos_vars["fecha"].set(datetime.now().strftime(i18n.formatos_fecha[i18n.idioma_actual]['fecha']))
        self.campos_vars["fecha_estado"].set(datetime.now().strftime(i18n.formatos_fecha[i18n.idioma_actual]['fecha']))
        self.campos_vars["decomiso"].set("NO")
        self.campos_vars["tipo"].set(_("otro").upper())
        self.campos_vars["unidad"].set(_("unidades").upper())
        self.campos_vars["estado_dictamen"].set(_("revision_documental"))
        
        # Ocultar campos de entrega
        self.actualizar_campos_entrega()
        
        self.statusbar['text'] = _("refresh")

    def show_context_menu(self, event):
        try:
            self.lista.selection_clear(0, tk.END)
            self.lista.selection_set(self.lista.nearest(event.y))
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def edit_selected(self):
        idx = self.lista.curselection()
        if not idx:
            return
        fila = self.datos[idx[0]]
        for k, var in zip(self.campos_vars.keys(), fila):
            self.campos_vars[k].set(var)
        
        # Actualizar campos de entrega si es necesario
        self.actualizar_campos_entrega()
        
        self.statusbar.configure(text=_("edit") + " - " + _("save"))
        
        try:
            self.tabview.set("Ingreso y Edición")
        except Exception:
            pass

    def delete_selected(self):
        idx = self.lista.curselection()
        if not idx:
            return
        dictamen_num = self.datos[idx[0]][0]
        if messagebox.askyesno(_("delete"), _("confirmar_eliminar")):
            self.logic.eliminar_dictamen(dictamen_num)
            self._load_data()
            self.statusbar.configure(text=_("delete") + f" {dictamen_num}")

    def visualizar_seleccionado(self, event=None):
        """Muestra una ventana detallada con la información del dictamen seleccionado"""
        idx = self.lista.curselection()
        if not idx:
            return
            
        fila = self.datos[idx[0]]
        # Mapeamos los datos a un diccionario
        campos_dict = dict(zip(self.campos_vars.keys(), fila))
        
        # Crear la ventana toplevel usando CTk
        win = ctk.CTkToplevel(self)
        win.title("Detalles del Expediente: " + str(campos_dict.get('dictamen', '')))
        win.geometry("600x650")
        win.grab_set()  # Hacerla modal
        
        # Frame scrollable para poder ver todos los detalles si son muchos
        main_frame = ctk.CTkScrollableFrame(win, width=580, height=550)
        main_frame.pack(padx=10, pady=(10, 5), fill="both", expand=True)
        
        # Título
        ctk.CTkLabel(main_frame, text="Información Detallada del Expediente", 
                     font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")).pack(pady=(10, 20))
        
        # Recorremos CAMPOS_DICTAMEN para mostrarlos en orden
        for key in CAMPOS_DICTAMEN:
            val = campos_dict.get(key, "")
            if val and str(val).strip():
                # Obtenemos la etiqueta formateada o traducida
                try:
                    label_text = _(key).replace("_", " ").title() + ":"
                except:
                    label_text = key.replace("_", " ").title() + ":"
                    
                row_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=4, padx=10)
                
                # Nombre del campo (columna izq)
                ctk.CTkLabel(row_frame, text=label_text, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
                             width=160, anchor="e").pack(side="left", padx=(0, 15))
                
                # Valor del campo (columna der)
                if key == "antecedentes":
                    val_text = ctk.CTkTextbox(row_frame, height=120, width=380, font=("Segoe UI", 12))
                    val_text.pack(side="left", fill="both", expand=True)
                    val_text.insert("1.0", str(val))
                    val_text.configure(state="disabled")
                else:
                    ctk.CTkLabel(row_frame, text=str(val), font=ctk.CTkFont(family="Segoe UI", size=13), 
                                 justify="left", wraplength=380, anchor="w").pack(side="left", fill="x", expand=True)
                                 
        # Botones de acción inferiores
        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10, padx=20)
        
        def do_edit():
            win.destroy()
            self.edit_selected()
            
        ctk.CTkButton(btn_frame, text="✏️ " + _("edit"), command=do_edit, width=120).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="❌ " + _("close"), command=win.destroy, fg_color="#6c757d", hover_color="#5a6268", 
                      width=120).pack(side="right", padx=10)


    def mostrar_acerca_de(self):
        """Muestra información acerca del sistema SISTECDATOSFEMA con estilo CustomTkinter"""
        acerca_win = ctk.CTkToplevel(self)
        acerca_win.title(_("acerca_de"))
        acerca_win.geometry("500x550")
        acerca_win.resizable(False, False)
        acerca_win.grab_set()
        
        # Logo
        try:
            logo_path = os.path.join(ASSETS_DIR, "logo_sistecdatos.png")
            img = Image.open(logo_path)
            img = img.resize((240, 240), Image.Resampling.LANCZOS)
            logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(240, 240))
            ctk.CTkLabel(acerca_win, image=logo_img, text="").pack(pady=20)
            acerca_win.logo_img = logo_img
        except (FileNotFoundError, OSError):
            ctk.CTkLabel(acerca_win, text="🏛️", font=ctk.CTkFont(size=64)).pack(pady=20)
        
        # Info
        ctk.CTkLabel(acerca_win, text=APP_NAME, font=ctk.CTkFont(size=18, weight="bold"), wraplength=450).pack(padx=20)
        ctk.CTkLabel(acerca_win, text=f"Versión {APP_VERSION}", font=ctk.CTkFont(size=14)).pack(pady=5)
        ctk.CTkLabel(acerca_win, text=ORG_NAME, font=ctk.CTkFont(size=12)).pack()
        
        descripcion = f"""SIS-TEC-DATOS FEMA – Sistema Técnico de Datos de la Fiscalía de Medio Ambiente.
        
Optimizado para el análisis forense, gestión de dictámenes y control de evidencia ambiental.
        
Desarrollado para la FEMA por Ing. Fernando Ardon y Antigravity AI @ 2025.
        
Copyright © 2025 FEMA. Todos los derechos reservados."""
        
        txt = ctk.CTkTextbox(acerca_win, width=440, height=180, font=("Segoe UI", 11))
        txt.pack(padx=20, pady=20)
        txt.insert("1.0", descripcion)
        txt.configure(state="disabled")
        
        ctk.CTkButton(acerca_win, text=_("close"), command=acerca_win.destroy).pack(pady=10)
        


    def mostrar_manual(self):
        """Muestra el manual de usuario con estilo CustomTkinter"""
        manual_win = ctk.CTkToplevel(self)
        manual_win.title(f"Manual de Usuario - {SHORT_NAME}")
        manual_win.geometry("800x700")
        manual_win.grab_set()
        
        txt = ctk.CTkTextbox(manual_win, width=760, height=600, font=("Segoe UI", 11), border_width=2)
        txt.pack(padx=20, pady=20, fill='both', expand=True)
        
        manual_content = f"""MANUAL DE USUARIO - {SHORT_NAME} {APP_VERSION}
Sistema Técnico de Datos de la Fiscalía de Medio Ambiente

═══════════════════════════════════════════════════════════════

ÍNDICE
1. Introducción
2. Interfaz Principal
3. Gestión de Dictámenes
4. Funcionalidad del Campo "Unidad"
5. Exportación de Datos (Excel/PDF)
6. Atajos de Teclado
7. Seguridad y Acceso

═══════════════════════════════════════════════════════════════

1. INTRODUCCIÓN

{SHORT_NAME} es una herramienta profesional diseñada para la Seccion Técnica de FEMA 
para gestionar dictámenes técnico-ambientales con rigor y eficiencia.

2. INTERFAZ PRINCIPAL

La interfaz Premium se divide en:
• Header: Identidad institucional y título dinámico.
• Formulario: Captura de datos en 3 columnas optimizadas.
• Acciones: Botones de acceso rápido para gestión y exportación.
• Visor: Lista sincronizada con la base de datos centralizada.
• Status: Información en tiempo real sobre el estado del sistema.

3. GESTIÓN DE DICTÁMENES

Proceso de Registro:
1. Complete los campos (Dictamen, Denuncia, Imputado, etc.).
2. Use el botón "➕ Agregar" o Ctrl+S.
3. El sistema valida campos obligatorios y duplicados.

Edición y Borrado:
• Use el menú contextual (Clic derecho) sobre cualquier registro en la lista.
• O use F2 para editar y Delete para eliminar tras seleccionar.

4. FUNCIONALIDAD DEL CAMPO "UNIDAD"

Inteligencia de Datos:
• Catálogo: Para tipos forestales o mineros, la unidad se bloquea automáticamente.
• Flexibilidad: Al elegir "OTROS", el campo se vuelve editable con 24 unidades comunes.

5. ATAJOS DE TECLADO (Productividad)

• Ctrl+S: Guardar / Actualizar
• Ctrl+E/P: Exportar Excel / PDF
• Ctrl+N/L: Limpiar Formulario
• Ctrl+T: Alternar Tema (Claro/Oscuro)
• F5: Recargar datos desde la BD

6. SEGURIDAD

El acceso está protegido por credenciales institucionales. El sistema registra 
auditoría de cambios y previene la alteración accidental de dictámenes finalizados.

═══════════════════════════════════════════════════════════════

© 2025 Fiscalía Especial de Medio Ambiente (FEMA)
{SHORT_NAME} {APP_VERSION} - Todos los derechos reservados."""
        
        txt.insert('1.0', manual_content)
        txt.configure(state='disabled')
        
        ctk.CTkButton(manual_win, text=_("close"), command=manual_win.destroy).pack(pady=(0, 20))

    def toggle_theme(self):
        self.mode = "dark" if self.mode == "light" else "light"
        self.styles.apply_theme(self.mode)
        self.statusbar.configure(text=f"Tema {self.mode.capitalize()} activado.")

    def on_close(self):
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = SISTECDATOSFEMAApp()
    app.mainloop()
