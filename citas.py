
import json
import time
from typing import Optional

# ---------------------------------------------------------------------
# NOTAS DE MEMORIA (comentadas para tu documentación)
# - Cada objeto Cita (nodo) vive en el HEAP (memoria dinámica).
# - Las variables locales de las funciones (ej. 'actual') se almacenan
#   temporalmente en el STACK mientras la función corre.
# - El campo `siguiente` actúa como un PUNTERO (referencia a otro nodo
#   en el HEAP). Cuando reasignas `actual.siguiente` cambias enlaces.
# ---------------------------------------------------------------------

class Cita:
    """
    Nodo que representa una cita.
    Campos:
      - cliente_nombre: str
      - servicios: list of strings (ej: ["Corte", "Tinte completo - corto"])
      - fecha: str "YYYY-MM-DD"
      - hora: str "HH:MM"
      - empleado: str (nombre del trabajador que atenderá) - opcional
      - id: str (identificador único simple)
      - siguiente: referencia (puntero) al siguiente nodo (Cita) en la lista
    """
    def __init__(self, cliente_nombre: str, servicios: list, fecha: str, hora: str, empleado: Optional[str]=None):
        self.cliente_nombre = cliente_nombre
        self.servicios = servicios[:]  # copia a HEAP
        self.fecha = fecha
        self.hora = hora
        self.empleado = empleado
        # id simple usando timestamp + cliente para unicidad local
        self.id = f"CITA_{int(time.time()*1000)}"
        self.siguiente = None  # puntero a otro nodo Cita (None = fin de lista)

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_nombre": self.cliente_nombre,
            "servicios": self.servicios,
            "fecha": self.fecha,
            "hora": self.hora,
            "empleado": self.empleado
        }

    @staticmethod
    def from_dict(d):
        c = Cita(d["cliente_nombre"], d.get("servicios", []), d.get("fecha", ""), d.get("hora", ""), d.get("empleado"))
        c.id = d.get("id", c.id)
        return c


class ListaCitas:
    """
    Lista enlazada simple para manejar las citas.
    - self.cabeza es la referencia (puntero) al primer nodo en HEAP.
    """
    def __init__(self):
        self.cabeza = None

    # ---------------------------
    # Agregar cita (al final)
    # ---------------------------
    def agregar_cita(self, cliente_nombre: str, servicios: list, fecha: str, hora: str, empleado: Optional[str]=None):
        nueva = Cita(cliente_nombre, servicios, fecha, hora, empleado)
        if self.cabeza is None:
            # Cabeza pasa a apuntar al nuevo nodo (referencia en el HEAP)
            self.cabeza = nueva
        else:
            actual = self.cabeza
            # recorrer la lista siguiendo punteros (variables locales en STACK)
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nueva  # se enlaza el nuevo nodo
        print(f"Cita registrada: {nueva.cliente_nombre} - {nueva.fecha} {nueva.hora} (id: {nueva.id})")
        return nueva

    # ---------------------------
    # Mostrar todas las citas
    # ---------------------------
    def mostrar_citas(self):
        if self.cabeza is None:
            print("No hay citas registradas.")
            return
        print("\n-- Citas registradas --")
        actual = self.cabeza
        i = 1
        while actual:
            servicios_txt = ", ".join(actual.servicios) if actual.servicios else "Sin servicios"
            empleado_txt = actual.empleado if actual.empleado else "No asignado"
            print(f"{i}. ID: {actual.id} | {actual.cliente_nombre} | {actual.fecha} {actual.hora} | {servicios_txt} | Empleado: {empleado_txt}")
            actual = actual.siguiente
            i += 1

    # ---------------------------
    # Buscar cita por cliente (retorna primer nodo que coincida)
    # ---------------------------
    def buscar_por_cliente(self, nombre: str):
        actual = self.cabeza
        while actual:
            if actual.cliente_nombre.lower() == nombre.lower():
                return actual
            actual = actual.siguiente
        return None

    # ---------------------------
    # Buscar citas por fecha (retorna lista de nodos)
    # ---------------------------
    def buscar_por_fecha(self, fecha: str):
        resultados = []
        actual = self.cabeza
        while actual:
            if actual.fecha == fecha:
                resultados.append(actual)
            actual = actual.siguiente
        return resultados

    # ---------------------------
    # Buscar cita por ID
    # ---------------------------
    def buscar_por_id(self, id_cita: str):
        actual = self.cabeza
        while actual:
            if actual.id == id_cita:
                return actual
            actual = actual.siguiente
        return None

    # ---------------------------
    # Editar una cita (por id)
    # ---------------------------
    def editar_cita(self, id_cita: str, cliente_nombre: Optional[str]=None, servicios: Optional[list]=None, fecha: Optional[str]=None, hora: Optional[str]=None, empleado: Optional[str]=None):
        nodo = self.buscar_por_id(id_cita)
        if not nodo:
            print("Cita no encontrada.")
            return False
        # Actualizamos los campos si vienen no-None
        if cliente_nombre is not None:
            nodo.cliente_nombre = cliente_nombre
        if servicios is not None:
            nodo.servicios = servicios[:]
        if fecha is not None:
            nodo.fecha = fecha
        if hora is not None:
            nodo.hora = hora
        if empleado is not None:
            nodo.empleado = empleado
        print(f"Cita {id_cita} actualizada.")
        return True

    # ---------------------------
    # Eliminar cita (por id)
    # ---------------------------
    def eliminar_cita(self, id_cita: str):
        actual = self.cabeza
        previo = None
        while actual:
            if actual.id == id_cita:
                if previo:
                    previo.siguiente = actual.siguiente
                else:
                    # eliminando la cabeza
                    self.cabeza = actual.siguiente
                print(f"Cita {id_cita} eliminada.")
                return True
            previo = actual
            actual = actual.siguiente
        print("Cita no encontrada.")
        return False

    # ---------------------------
    # Convertir toda la lista a lista de dicts (útil para guardar en JSON)
    # ---------------------------
    def to_list_of_dicts(self):
        salida = []
        actual = self.cabeza
        while actual:
            salida.append(actual.to_dict())
            actual = actual.siguiente
        return salida

    # ---------------------------
    # Reconstruir lista desde lista de dicts (cargar JSON)
    # ---------------------------
    def from_list_of_dicts(self, lista_dicts):
        self.cabeza = None
        for d in lista_dicts:
            nodo = Cita.from_dict(d)
            # agregar al final reusando agregar logic pero sin imprimir
            if self.cabeza is None:
                self.cabeza = nodo
            else:
                actual = self.cabeza
                while actual.siguiente:
                    actual = actual.siguiente
                actual.siguiente = nodo

    # ---------------------------
    # Guardar en JSON
    # ---------------------------
    def guardar_json(self, ruta="citas.json"):
        datos = self.to_list_of_dicts()
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            print(f"Citas guardadas en {ruta}")
            return True
        except Exception as e:
            print("Error guardando JSON:", e)
            return False

    # ---------------------------
    # Cargar desde JSON
    # ---------------------------
    def cargar_json(self, ruta="citas.json"):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
            self.from_list_of_dicts(datos)
            print(f"Citas cargadas desde {ruta}")
            return True
        except FileNotFoundError:
            print("Archivo de citas no encontrado; iniciando con lista vacía.")
            return False
        except Exception as e:
            print("Error cargando JSON:", e)
            return False

    # ---------------------------
    # Utilidad: mostrar citas de un cliente en formato amigable
    # ---------------------------
    def mostrar_citas_cliente(self, nombre: str):
        actual = self.cabeza
        found = False
        while actual:
            if actual.cliente_nombre.lower() == nombre.lower():
                servicios_txt = ", ".join(actual.servicios) if actual.servicios else "Sin servicios"
                print(f"ID: {actual.id} | {actual.fecha} {actual.hora} | Servicios: {servicios_txt} | Empleado: {actual.empleado}")
                found = True
            actual = actual.siguiente
        if not found:
            print("No se encontraron citas para ese cliente.")

# ---------------------------
# Ejemplo rápido (solo corre si ejecutas este archivo directamente)
# ---------------------------
if __name__ == "__main__":
    lc = ListaCitas()
    lc.agregar_cita("Juan Perez", ["Corte hombre"], "2025-11-10", "14:00", "Luis")
    lc.agregar_cita("Ana Lopez", ["Tinte completo - corto"], "2025-11-11", "09:30", None)
    lc.mostrar_citas()
    # guardar y cargar demo
    lc.guardar_json("demo_citas.json")
    nueva = ListaCitas()
    nueva.cargar_json("demo_citas.json")
    nueva.mostrar_citas()
