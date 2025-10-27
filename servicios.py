class servicio:
    def __init__(self,nombre,precio):
        self.nombre=nombre
        self.precio=precio


class listadeservicios:
    def __init__(self):
        self.servicios= [
            servicio("Corte de cabello", 30),
            servicio("Tinte de cabello largo", 500),
            servicio("Tinte de cabello coro, 300"),
            servicio("Tinte de cabello (colores vivos), 500"),
            servicio("Lavado y secado", 40),
            servicio("Pedicure", 20),
            servicio("Base cabello corto y largo",150)
        ]
    