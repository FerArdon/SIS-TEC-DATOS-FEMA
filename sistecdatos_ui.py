# sistecdatos_ui.py
import customtkinter as ctk

class SISTECDATOSFEMAUIStyles:
    """Gestor de estética premium para SISTECDATOSFEMA usando CustomTkinter."""
    
    def __init__(self):
        # Configuraciones globales de CustomTkinter
        ctk.set_appearance_mode("light")  # Opciones: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"
        
        # Paleta de colores Premium (Inspirada en software institucional moderno)
        self.colors = {
            "light": {
                "bg": "#F5F7FA",
                "fg": "#1A1C1E",
                "accent": "#005FB8",
                "surface": "#FFFFFF",
                "border": "#D1D9E0"
            },
            "dark": {
                "bg": "#1A1C1E",
                "fg": "#E2E2E6",
                "accent": "#7ABCFF",
                "surface": "#2D2F31",
                "border": "#43474E"
            }
        }
        self.current_theme = "light"

    def apply_theme(self, mode):
        """Aplica el modo (light/dark) de manera directa."""
        self.current_theme = mode
        ctk.set_appearance_mode(mode)
        return self.current_theme

    def toggle_theme(self):
        """Alterna entre tema claro y oscuro."""
        if self.current_theme == "light":
            self.apply_theme("dark")
        else:
            self.apply_theme("light")
        return self.current_theme

    def get_colors(self):
        """Retorna la paleta de colores del tema actual."""
        return self.colors[self.current_theme]
