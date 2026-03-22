# sistecdatos_login.py
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import os
from datetime import datetime
from PIL import Image
import logging

logger = logging.getLogger("sistecdatos.login")

class SISTECDATOSFEMALogin:
    """Sistema de login avanzado para SISTECDATOSFEMA usando CTkToplevel."""
    
    def __init__(self, parent, db_manager, on_login_success=None):
        self.parent = parent
        self.db = db_manager
        self.on_login_success = on_login_success
        self.login_window = None
        self.intentos_fallidos = 0
        self.max_intentos = 3
        
    def mostrar_login(self):
        """Muestra la ventana de login como Toplevel vinculado al root."""
        self.login_window = ctk.CTkToplevel(self.parent)
        self.login_window.title("SISTECDATOSFEMA - Inicio de Sesión")
        self.login_window.geometry("450x720")
        self.login_window.resizable(False, False)
        
        # Hacerla modal
        self.login_window.grab_set()
        self.login_window.focus_force()
        
        # Centrar relativo al padre o pantalla
        self.login_window.update_idletasks()
        x = (self.login_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.login_window.winfo_screenheight() // 2) - (720 // 2)
        self.login_window.geometry(f"450x720+{x}+{y}")
        
        # Asegurar que si cierran la ventana de login, se cierra todo si no han logueado
        self.login_window.protocol("WM_DELETE_WINDOW", self._cerrar_aplicacion)
        
        self._crear_interfaz_login()
        
        # Configurar eventos
        self.login_window.bind('<Return>', lambda e: self._intentar_login())

    def _crear_interfaz_login(self):
        """Crea la interfaz de login moderna"""
        # (Se mantiene la misma estructura pero usando self.login_window)
        try:
            logo_path = os.path.join("assets", "logo_sistecdatos.png")
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                self.logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200)) # Reducido de 240 a 200
                logo_label = ctk.CTkLabel(self.login_window, image=self.logo_img, text="")
                logo_label.pack(pady=(15, 5)) # PAD reducido
            else:
                raise FileNotFoundError
        except Exception:
            logo_label = ctk.CTkLabel(self.login_window, text="🏛️", font=ctk.CTkFont(size=64))
            logo_label.pack(pady=(15, 5))
        
        container = ctk.CTkFrame(self.login_window, fg_color="transparent")
        container.pack(fill="x", padx=40)
        
        ctk.CTkLabel(container, text="Iniciar Sesión", 
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(container, text="Usuario:", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(0, 5))
        self.usuario_entry = ctk.CTkEntry(container, placeholder_text="Nombre de usuario", height=35)
        self.usuario_entry.pack(fill="x", padx=2, pady=(0, 15))
        self.usuario_entry.focus()
        
        ctk.CTkLabel(container, text="Contraseña:", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(0, 5))
        self.password_entry = ctk.CTkEntry(container, placeholder_text="Contraseña", show="*", height=35)
        self.password_entry.pack(fill="x", padx=2, pady=(0, 15))
        
        self.mostrar_password_var = tk.BooleanVar()
        self.mostrar_check = ctk.CTkCheckBox(container, text="Mostrar contraseña",
                                            variable=self.mostrar_password_var,
                                            command=self._toggle_password_visibility,
                                            font=ctk.CTkFont(size=12))
        self.mostrar_check.pack(anchor="w", pady=(0, 15))
        
        self.login_btn = ctk.CTkButton(container, text="Iniciar Sesión",
                                      command=self._intentar_login,
                                      height=40, font=ctk.CTkFont(size=14, weight="bold"))
        self.login_btn.pack(fill="x", pady=(0, 10))
        
        self.change_pass_btn = ctk.CTkButton(container, text="Cambiar Contraseña",
                                             command=self._abrir_dialogo_cambio_password,
                                             fg_color="transparent", border_width=1, text_color=("#333", "#ccc"),
                                             height=30, font=ctk.CTkFont(size=12))
        self.change_pass_btn.pack(fill="x", pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(container, text="", 
                                        font=ctk.CTkFont(size=12),
                                        text_color="#d13438")
        self.status_label.pack(pady=(5, 10))
        
        info_frame = ctk.CTkFrame(self.login_window, height=60)
        info_frame.pack(fill="x", padx=40, pady=(10, 0))
        
        try:
            stats = self.db.get_estadisticas_generales()
            info_text = f"Dictámenes: {stats.get('total_dictamenes', 0)} | Decomisos: {stats.get('total_decomisos', 0)}\nVersión: 2.0 Professional"
        except Exception as e:
            logger.warning(f"Error estadísticas login: {e}")
            info_text = "SISTECDATOSFEMA v2.0 Professional\nInicializando base de datos..."
        
        info_label = ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=11), text_color="#666666")
        info_label.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.login_window, text="© 2025 Fiscalía Especial de Medio Ambiente (FEMA)",
                     font=ctk.CTkFont(size=10), text_color="#999999").pack(side="bottom", pady=15)

    def _toggle_password_visibility(self):
        if self.mostrar_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
    
    def _intentar_login(self):
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get()
        
        if not usuario:
            self._mostrar_error("Ingrese su usuario")
            return
        
        self.login_btn.configure(state="disabled", text="Verificando...")
        self.login_window.update()
        
        try:
            if self.db.verificar_usuario(usuario, password):
                self._login_exitoso()
            else:
                self._mostrar_error("Usuario o contraseña incorrectos")
        except Exception as e:
            self._mostrar_error(f"Error: {e}")
        finally:
            self.login_btn.configure(state="normal", text="Iniciar Sesión")
    
    def _login_exitoso(self):
        self.status_label.configure(text="✓ Acceso concedido", text_color="#28a745")
        self.login_window.update()
        if self.db.current_user and self.db.current_user.get('debe_cambiar_password'):
            self.login_window.after(400, self._solicitar_cambio_password)
        else:
            self.login_window.after(600, self._finalizar_login)

    def _solicitar_cambio_password(self):
        win = ctk.CTkToplevel(self.login_window)
        win.title("Cambio de contraseña")
        win.geometry("380x320")
        win.grab_set()
        win.protocol("WM_DELETE_WINDOW", lambda: None)

        ctk.CTkLabel(win, text="Cambio de contraseña requerido", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)
        new_pass = ctk.CTkEntry(win, show="*", placeholder_text="Nueva contraseña", height=35)
        new_pass.pack(fill="x", padx=40, pady=10)
        confirm_pass = ctk.CTkEntry(win, show="*", placeholder_text="Confirmar", height=35)
        confirm_pass.pack(fill="x", padx=40, pady=10)
        
        err_lbl = ctk.CTkLabel(win, text="", text_color="#d13438")
        err_lbl.pack()

        def confirmar():
            p1, p2 = new_pass.get(), confirm_pass.get()
            if len(p1) < 6 or p1 != p2:
                err_lbl.configure(text="Contraseñas no coinciden o muy cortas")
                return
            self.db.cambiar_password(self.db.current_user['username'], p1)
            win.destroy()
            self._finalizar_login()

        ctk.CTkButton(win, text="Guardar y continuar", command=confirmar).pack(pady=20)

    def _finalizar_login(self):
        self.login_window.destroy()
        if self.on_login_success:
            self.on_login_success()
    
    def _mostrar_error(self, mensaje):
        self.status_label.configure(text=f"✗ {mensaje}")
        orig = self.login_window.cget("fg_color")
        self.login_window.configure(fg_color="#ffe6e6")
        self.login_window.after(200, lambda: self.login_window.configure(fg_color=orig))

    def _abrir_dialogo_cambio_password(self):
        win = ctk.CTkToplevel(self.login_window)
        win.title("Cambiar Mi Contraseña")
        win.geometry("400x420")
        win.grab_set()
        
        ctk.CTkLabel(win, text="Actualizar Contraseña", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        user_entry = ctk.CTkEntry(win, placeholder_text="Usuario", height=35)
        user_entry.pack(fill="x", padx=40, pady=10)
        
        old_pass = ctk.CTkEntry(win, show="*", placeholder_text="Contraseña actual", height=35)
        old_pass.pack(fill="x", padx=40, pady=10)
        
        new_pass = ctk.CTkEntry(win, show="*", placeholder_text="Nueva contraseña", height=35)
        new_pass.pack(fill="x", padx=40, pady=10)
        
        confirm_pass = ctk.CTkEntry(win, show="*", placeholder_text="Confirmar nueva", height=35)
        confirm_pass.pack(fill="x", padx=40, pady=10)
        
        err_lbl = ctk.CTkLabel(win, text="", text_color="#d13438")
        err_lbl.pack()
        
        def procesar_cambio():
            u = user_entry.get().strip()
            op = old_pass.get()
            np = new_pass.get()
            cp = confirm_pass.get()
            
            if not u or not op or not np:
                err_lbl.configure(text="Llene todos los campos")
                return
            if np != cp:
                err_lbl.configure(text="Las contraseñas nuevas no coinciden")
                return
            if len(np) < 6:
                err_lbl.configure(text="La contraseña debe tener al menos 6 caracteres")
                return
                
            if self.db.verificar_usuario(u, op):
                try:
                    self.db.cambiar_password(u, np)
                    messagebox.showinfo("Éxito", "Contraseña cambiada exitosamente. Por favor, inicie sesión.")
                    win.destroy()
                except Exception as e:
                    err_lbl.configure(text=f"Error: {e}")
            else:
                err_lbl.configure(text="Credenciales actuales incorrectas")
                
        ctk.CTkButton(win, text="Actualizar", command=procesar_cambio, height=35).pack(pady=15)

    def _cerrar_aplicacion(self):
        self.parent.destroy()

def mostrar_ventana_login(parent, db_manager, on_success_callback):
    login_system = SISTECDATOSFEMALogin(parent, db_manager, on_success_callback)
    login_system.mostrar_login()
