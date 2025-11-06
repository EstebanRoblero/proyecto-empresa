
import os
import time
from fpdf import FPDF
from db_comprobantes import crear_tabla_comprobantes, insertar_comprobante

# Inicializar DB
crear_tabla_comprobantes()

ventas_ram = []

class Comprobante:
    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []
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

        # Guardar en RAM y DB
        ventas_ram.append(self.to_dict())
        insertar_comprobante(self)
        return ruta

def generar_comprobante(cliente):
    return Comprobante(cliente)
