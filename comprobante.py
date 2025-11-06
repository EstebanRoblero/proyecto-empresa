# comprobante.py
# Generación de comprobantes de pago (PDF o TXT) + registro de ventas en memoria
# comprobante.py
# comprobante.py
from fpdf import FPDF
import os
import time

ventas_ram = []

class Comprobante:
    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []  # (descripcion, precio)
        self.fecha_emision = time.strftime("%d-%m-%Y %H:%M:%S")  # Formato amigable

    def agregar_item(self, descripcion, precio):
        self.items.append((descripcion, float(precio)))

    def total(self):
        return sum(p for _, p in self.items)

    def to_dict(self):
        return {
            "cliente": self.cliente.nombre,
            "fecha_emision": self.fecha_emision,
            "items": self.items,
            "total": self.total()
        }

    # --- PDF ---
    def guardar_pdf(self, carpeta="comprobantes"):
        # Crear carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        filename_base = f"comprobante_{self.cliente.nombre.replace(' ', '_')}_{int(time.time())}.pdf"
        file_path = os.path.join(carpeta, filename_base)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "💈 COMPROBANTE DE PAGO 💈", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Cliente: {self.cliente.nombre}", ln=True)
        pdf.cell(0, 10, f"Fecha emisión: {self.fecha_emision}", ln=True)
        pdf.ln(5)
        pdf.cell(0, 0, "-"*60, ln=True)
        pdf.ln(5)

        for desc, precio in self.items:
            pdf.cell(140, 10, desc, border=0)
            pdf.cell(0, 10, f"Q{precio:.2f}", ln=True, align="R")

        pdf.ln(5)
        pdf.cell(140, 10, "TOTAL", border=0)
        pdf.cell(0, 10, f"Q{self.total():.2f}", ln=True, align="R")

        pdf.output(file_path)

        # Guardar en memoria RAM
        ventas_ram.append(self.to_dict())

        return file_path
