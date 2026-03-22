# sigedta_export.py
import os
from tkinter import filedialog, messagebox
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import datetime

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo_sistecdatos.png")

class SISTECDATOSFEMAExportManager:
    def __init__(self, db_manager):
        self.db = db_manager

    def export_to_excel(self, datos=None):
        if datos is None:
            datos = self.db.fetch_all_dictamenes()
            
        if not datos:
            messagebox.showwarning("Advertencia", "No hay datos para exportar a Excel.")
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("Todos los archivos", "*.*")],
            title="Guardar archivo Excel"
        )
        if archivo:
            try:
                wb = Workbook()
                ws = wb.active
                ws.title = "Dictámenes"

                headers = [
                    "Dictamen", "Denuncia", "Imputado", "Ofendido", "Delito", "Sitio",
                    "Antecedentes", "Técnico", "Fecha", "Fiscal", "Agente", "Decomiso",
                    "Tipo", "Cantidad", "Otro", "Unidad", "Estado del Dictamen", "Fecha del Estado", "Entregado A"
                ]
                ws.append(headers)
                for fila in datos:
                    ws.append(fila)

                # Ajustar ancho de columnas
                for idx, col in enumerate(headers):
                    ws.column_dimensions[chr(65 + idx)].width = max(15, len(col) + 2)

                wb.save(archivo)
                messagebox.showinfo("Éxito", f"Archivo Excel guardado en:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def export_to_pdf(self, datos=None):
        if datos is None:
            datos = self.db.fetch_all_dictamenes()
            
        if not datos:
            messagebox.showwarning("Advertencia", "No hay datos para exportar a PDF.")
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("Todos los archivos", "*.*")],
            title="Guardar archivo PDF"
        )
        if archivo:
            try:
                doc = SimpleDocTemplate(archivo, pagesize=letter)
                story = []
                styles = getSampleStyleSheet()
                styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=13, fontName="Helvetica-Bold"))
                styles.add(ParagraphStyle(name='NormalLeft', alignment=TA_LEFT, fontSize=10))

                # Logo
                if os.path.exists(LOGO_PATH):
                    story.append(RLImage(LOGO_PATH, width=1.2*inch, height=1.2*inch))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph("SISTECDATOSFEMA - Dictámenes Técnico-Ambientales", styles['Center']))
                story.append(Paragraph("Fiscalía Especial de Medio Ambiente (FEMA)", styles['Center']))
                story.append(Spacer(1, 0.18 * inch))
                story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['NormalLeft']))
                story.append(Spacer(1, 0.18 * inch))

                headers = [
                    "Dictamen", "Denuncia", "Imputado", "Ofendido", "Delito", "Sitio",
                    "Antecedentes", "Técnico", "Fecha", "Fiscal", "Agente", "Decomiso",
                    "Tipo", "Cantidad", "Otro", "Unidad", "Estado del Dictamen", "Fecha del Estado", "Entregado A"
                ]
                for fila in datos:
                    story.append(Spacer(1, 0.10 * inch))
                    for head, value in zip(headers, fila):
                        story.append(Paragraph(f"<b>{head}:</b> {value}", styles['NormalLeft']))
                    story.append(Spacer(1, 0.14 * inch))
                    story.append(Paragraph("-" * 100, styles['NormalLeft']))

                doc.build(story)
                messagebox.showinfo("Éxito", f"Archivo PDF guardado en:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo PDF:\n{e}")
