# comprobante.py
# Generación de comprobantes de pago (PDF o TXT) + registro de ventas en memoria
import os
import time

# Lista RAM donde se guardan todas las ventas realizadas
ventas_ram = []

class Comprobante:
    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []  # (descripcion, precio)
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

    def guardar_txt(self, carpeta="comprobantes"):
        # Crear carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        filename_base = f"comprobante_{self.cliente.nombre.replace(' ', '_')}_{int(time.time())}"
        file_path = os.path.join(carpeta, filename_base + ".txt")

        # Crear el comprobante en formato texto
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("        💈 COMPROBANTE DE PAGO 💈\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Cliente: {self.cliente.nombre}\n")
            f.write(f"Fecha: {self.fecha_emision}\n")
            f.write("-" * 50 + "\n")

            for desc, precio in self.items:
                f.write(f"{desc:<40} Q{precio:>7.2f}\n")

            f.write("-" * 50 + "\n")
            f.write(f"TOTAL:{'':<36} Q{self.total():>7.2f}\n")
            f.write("=" * 50 + "\n")

        # Guardar en memoria RAM
        ventas_ram.append(self.to_dict())

        return file_path


def generar_comprobante(cliente, servicios=None, inventario=None):
    """
    Crea un comprobante vacío (los servicios se agregan después).
    """
    return Comprobante(cliente)
