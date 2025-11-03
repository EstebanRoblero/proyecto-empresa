class Cita:
    def __init__(self,cliente_nombre,fecha,hora):
        self.cliente_nombre=cliente_nombre
        self.fecha=fecha
        self.hora=hora
        self.siguiente=None

class ListaCitas:
    def __init__(self):
        self.cabeza=None

    def agregar_cita(self,cliente_nombre,fecha,hora):
        nueva=Cita(cliente_nombre,fecha,hora)
        if self.cabeza is None:
            self.cabeza=nueva
        else:
            actual=self.cabeza
            while actual.siguiente:
                actual=actual.siguiente
            actual.siguiente=nueva
        print(f"Cita registrada: {cliente_nombre} {fecha} {hora}")
    
    def mostrar_citas(self):
        if self.cabeza is None:
            print("No hay citas registradas.")
            return
        actual=self.cabeza
        print("\n=== Citas Registradas ===")
        while actual:
            print(f"{actual.cliente_nombre} == {actual.fecha} == {actual.hora}")
            actual=actual.siguiente