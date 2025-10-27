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

    #USAMOS BUBBLE SORT
    def mostrarservicio(self):
        e=len(self.servicios)
        for i in range(e):
            for j in range (0, e - i -1):
                if self.servicios[j].precio>self.servicios[j + 1].precio:
                    self.servicios[j], self.servicios[j + 1] =self.servicios[j + 1],self.servicios[j]
        print("Servicios ordenados por precio")


    