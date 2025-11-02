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
        
    
    def registode_entradas(self,cantidad,nombre):
        self.cola.append(nombre,cantidad)
        actual=actual.siguiente
        while actual:
            if actual.nombre==nombre:
                actual.cantidad += cantidad
                print(f"Entrada de producto registrado: {cantidad}  == unidades de: {nombre}")
                return
            actual=actual.siguiente
        print("El producto no se ha encontrado intente de nuevo.")
    

    def registrode_salidas(self,cantidad,nombre):
        self.cola.append(nombre,cantidad)
        actual=actual.siguiente
        while actual:
            if actual.nombre==nombre:
                if actual.cantidad >= cantidad:
                    actual.cantidad-= cantidad
                    print(f"Ha salido el producto registrado: {cantidad} == unidade de: {nombre}")
                
                else:
                    print("No hay suficiente producto en el stock.")
                
                return
            actual=actual.siguiente
        print("El prodcuto no se ha encontrado intente de nuevo.")
    

    def secuencial_buscar(self,nombre):
        actual=actual.cabeza
        while actual:
            if actual.nombre==nombre:
                print(f"Se ha encontrado el producto: {nombre} con la cantidad de: {actual.cantidad} con el precio de: Q{actual.precio}")
                return actual
            actual=actual.siguiente
        print("El producto no se ha encontrado intente de nuevo.")
        return None

    def arreglo_lista(self):
        arreglo=[]
        actual=self.cabeza
        while actual:
            arreglo.append((actual.nombre, actual.cantidad, actual.precio))
            actual=actual.siguiente
        return arreglo
    
    def hashing(self,nombre):
        clave=sum(ord(c) for c in nombre) % 10
        print(f"hash de {nombre}: {clave}")
        return clave


    def bubble_sort(self, lista):
        n=len(lista)
        for i in range(n):
            for j in range(0, n-i-1):
                if lista[j][0] > lista[j+1][0]:
                    lista[j], lista[j+1] = lista[j + 1], lista[j]
        print("la lista esta ordenada:")
        return lista
    
    

    





                 
                



        
    


