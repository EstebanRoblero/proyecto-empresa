class Reportes:
    def __init__(self):
        self.ventas=[]  # lista de tuplas= cliente, servicio, precio

    def registrar_venta(self,cliente,servicio,precio):
        self.ventas.append((cliente,servicio,precio))

    def mostrar_reporte_del_dia(self,fecha=None):
        print("\n-- REPORTE DEL DIA --")
        total=0
        for v in self.ventas:
            c,s,p=v
            print(f"{c} === {s} === Q{p}")
            total+=p
        print(f"Total del día: Q{total}")

    def mostrar_reporte_del_mes(self,mes=None):
        print("\n-- REPORTE DEL MES --")
        total=0
        for v in self.ventas:
            c,s,p=v
            print(f"{c} == {s} == Q{p}")
            total+=p
        print(f"Total del mes: Q{total}")