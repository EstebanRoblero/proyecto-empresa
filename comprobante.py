# comprobante.py
# Generación de comprobantes de pago (PDF o TXT) + registro de ventas en memoria
# comprobante.py
# comprobante.py
# comprobante.py
# Generación de comprobantes de pago en PDF + registro en memoria
import os
import time
from fpdf import FPDF  # asegúrate de tener fpdf2 instalado

# Lista RAM donde se guardan todas las ventas realizadas
ventas_ram = []

class Comprobante:
    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []  # lista de tuples (descripcion, precio)
        self.fecha_emision = time.strftime("%Y-%m-%d %H:%M:%S")

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

    # -------------------------------
    # Guardar como PDF
    # -------------------------------
    def guardar_pdf(self, carpeta="comprobantes"):
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        nombre_archivo = f"comprobante_{self.cliente.nombre.replace(' ', '_')}_{int(time.time())}.pdf"
        ruta = os.path.join(carpeta, nombre_archivo)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, " COMPROBANTE DE PAGO ", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Cliente: {self.cliente.nombre}", ln=True)
        pdf.cell(0, 8, f"Fecha de emisión: {self.fecha_emision}", ln=True)
        pdf.ln(5)
        pdf.cell(0, 8, "-"*50, ln=True)

        for desc, precio in self.items:
            pdf.cell(0, 8, f"{desc:<40} Q{precio:>7.2f}", ln=True)

        pdf.cell(0, 8, "-"*50, ln=True)
        pdf.cell(0, 8, f"TOTAL:{'':<36} Q{self.total():>7.2f}", ln=True)
        pdf.output(ruta)

        # Guardar en RAM
        ventas_ram.append(self.to_dict())
        return ruta

# -------------------------------
# Función para crear comprobante
# -------------------------------
def generar_comprobante(cliente, servicios=None, inventario=None):
    return Comprobante(cliente)
