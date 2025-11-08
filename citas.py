import json
import time
from typing import Optional

class Cita:
    def __init__(self, cliente_nombre: str, servicios: list, fecha: str, hora: str, empleado: Optional[str]=None):
        self.cliente_nombre = cliente_nombre
        self.servicios = servicios[:]
        self.fecha = fecha
        self.hora = hora
        self.empleado = empleado
        self.id = f"CITA_{int(time.time()*1000)}"
        self.siguiente = None

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
    def __init__(self):
        self.cabeza = None
        self.cargar_json()  # CARGAR CITAS AL INICIAR

    def agregar_cita(self, cliente_nombre: str, servicios: list, fecha: str, hora: str, empleado: Optional[str]=None):
        nueva = Cita(cliente_nombre, servicios, fecha, hora, empleado)
        if self.cabeza is None:
            self.cabeza = nueva
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nueva
        
        self.guardar_json()  # GUARDAR DESPUÉS DE AGREGAR
        print(f"Cita registrada: {nueva.cliente_nombre} - {nueva.fecha} {nueva.hora} (id: {nueva.id})")
        return nueva

    def eliminar_cita(self, id_cita: str):
        actual = self.cabeza
        previo = None
        while actual:
            if actual.id == id_cita:
                if previo:
                    previo.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                
                self.guardar_json()  # GUARDAR DESPUÉS DE ELIMINAR
                print(f"Cita {id_cita} eliminada.")
                return True
            previo = actual
            actual = actual.siguiente
        print("Cita no encontrada.")
        return False

    # ... (los otros métodos se mantienen igual)

    def obtener_todas_citas(self):
        citas = []
        actual = self.cabeza
        while actual:
            citas.append(actual)
            actual = actual.siguiente
        return citas

    def buscar_por_fecha(self, fecha: str):
        resultados = []
        actual = self.cabeza
        while actual:
            if actual.fecha == fecha:
                resultados.append(actual)
            actual = actual.siguiente
        return resultados

    def to_list_of_dicts(self):
        salida = []
        actual = self.cabeza
        while actual:
            salida.append(actual.to_dict())
            actual = actual.siguiente
        return salida

    def from_list_of_dicts(self, lista_dicts):
        self.cabeza = None
        for d in lista_dicts:
            nodo = Cita.from_dict(d)
            if self.cabeza is None:
                self.cabeza = nodo
            else:
                actual = self.cabeza
                while actual.siguiente:
                    actual = actual.siguiente
                actual.siguiente = nodo

    def guardar_json(self, ruta="citas.json"):
        try:
            datos = self.to_list_of_dicts()
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            print(f"Citas guardadas en {ruta}")
            return True
        except Exception as e:
            print("Error guardando citas:", e)
            return False

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
            print("Error cargando citas:", e)
            return False