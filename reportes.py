# reportes.py
import os
from datetime import datetime
from fpdf import FPDF

class Reportes:
    def __init__(self):
        self.ventas = []  # lista de tuplas = (cliente, servicio, precio, fecha)

    def registrar_venta(self, cliente, servicio, precio, fecha=None):
        """Registra una venta con fecha opcional (datetime.date o str 'YYYY-MM-DD')."""
        if fecha is None:
            fecha = datetime.today().date()
        elif isinstance(fecha, str):
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        self.ventas.append((cliente, servicio, precio, fecha))

    def mostrar_reporte_del_dia(self, fecha=None):
        if fecha is None:
            fecha = datetime.today().date()
        elif isinstance(fecha, str):
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

        print(f"\n-- REPORTE DEL DIA {fecha} --")
        total = 0
        for v in self.ventas:
            c, s, p, f = v
            if f == fecha:
                print(f"{c} === {s} === Q{p}")
                total += p
        print(f"Total del día: Q{total}")

    def mostrar_reporte_del_mes(self, mes=None):
        if mes is None:
            mes = datetime.today().strftime("%Y-%m")
        print(f"\n-- REPORTE DEL MES {mes} --")
        total = 0
        for v in self.ventas:
            c, s, p, f = v
            if f.strftime("%Y-%m") == mes:
                print(f"{c} === {s} === Q{p}")
                total += p
        print(f"Total del mes: Q{total}")

# -------------------------------
# Función para generar PDF mensual con FPDF
# -------------------------------
def generar_reporte_mensual_pdf(mes_yyyy_mm, reportes_obj=None, inventario_obj=None, carpeta="reportes"):
    """
    Genera un PDF con todas las ventas registradas en reportes_obj para el mes especificado,
    y opcionalmente con el inventario.
    """
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    fname = os.path.join(carpeta, f"reporte_{mes_yyyy_mm}.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Reporte Mensual: {mes_yyyy_mm}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "=== VENTAS DEL MES ===", ln=True)
    pdf.set_font("Arial", '', 12)

    total_ventas = 0
    if reportes_obj:
        for v in reportes_obj.ventas:
            cte, serv, precio, fecha = v
            if fecha.strftime("%Y-%m") == mes_yyyy_mm:
                pdf.cell(0, 8, f"{fecha} = {cte} = {serv} = Q{precio}", ln=True)
                total_ventas += precio

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"TOTAL VENTAS: Q{total_ventas}", ln=True)

    # Inventario (opcional)
    if inventario_obj and hasattr(inventario_obj, "productos"):
        pdf.ln(5)
        pdf.cell(0, 10, "=== INVENTARIO ACTUAL ===", ln=True)
        pdf.set_font("Arial", '', 12)
        for prod in inventario_obj.productos:
            pdf.cell(0, 8, f"{prod.nombre} | {prod.cantidad} {prod.tipo} | Q{prod.precio}", ln=True)

    pdf.output(fname)
    return fname, f"Reporte PDF generado en {fname}"
