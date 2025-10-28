class Nododelproducto:
    def __init__(self,nombre, cantidad,precio):
        self.nombre=nombre
        self.cantidad=cantidad
        self.precio=precio
        self.siguiente=None


class Inventariolista:
    def __init__(self):
        self.cabeza=None
        self.stack=[]
        self.cola=[]

    

    def agregar_producto(self,nombre,cantidad, precio ):
        nuevo=Nododelproducto(nombre,cantidad,precio)
        if self.cabeza is None:
            self.cabeza=nuevo

        else:
            actual=self.cabeza
            while actual.siguiente:
                actual=actual.siguiente
            actual.siguiente=nuevo
        print(f"El producto {nombre} ha sido agregado exitosamente.")

    
    def mostrar_elinventario(self):
        if self.cabeza is None:
            print("El inventario esta vacio.")
            return
        actual=self.cabeza
        while actual:
            estado= "Hay Disponible" if actual.cantidad > 0 else "Esta Agotado"
            print(f"{actual.nombre} == Cantidad: {actual.cantidad} == Precio Q{actual.precio} == Estado {actual.estado}")
            actual= actual.siguiente
            
        
    


