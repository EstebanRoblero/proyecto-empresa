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
        