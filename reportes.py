from fpdf import FPDF
import os

class Reportes:
    def __init__(self):
        self.ventas = []  # lista de tuplas (cliente, servicio, precio)

    def registrar_venta(self, cliente, servicio, precio):
        self.ventas.append((cliente, servicio, precio))

    def mostrar_reporte_del_dia(self, fecha=None):
        print("\n-- REPORTE DEL DÍA --")
        total = 0
        for c, s, p in self.ventas:
            print(f"{c} === {s} === Q{p}")
            total += p
        print(f"Total del día: Q{total}")

    def mostrar_reporte_del_mes(self, mes=None):
        print("\n-- REPORTE DEL MES --")
        total = 0
        for c, s, p in self.ventas:
            print(f"{c} == {s} == Q{p}")
            total += p
        print(f"Total del mes: Q{total}")

    def generar_reporte_mensual_pdf(self, yyyy_mm, inventario_obj=None, carpeta="reportes"):
        """Genera un reporte mensual en PDF usando fpdf."""
        os.makedirs(carpeta, exist_ok=True)
        fname = os.path.join(carpeta, f"reporte_{yyyy_mm}.pdf")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Reporte Mensual - {yyyy_mm}", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        total = 0
        for c, s, p in self.ventas:
            pdf.cell(0, 8, f"{c} - {s} - Q{p}", ln=True)
            total += p

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"TOTAL GENERAL: Q{total}", ln=True)

        if inventario_obj:
            pdf.ln(10)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Resumen de Inventario", ln=True)
            pdf.set_font("Arial", "", 12)
            for nodo in inventario_obj:
                pdf.cell(0, 8, f"{nodo.nombre} - {nodo.cantidad} {nodo.tipo} - Q{nodo.precio}", ln=True)

        pdf.output(fname)
        self.ventas.clear()
        return fname
