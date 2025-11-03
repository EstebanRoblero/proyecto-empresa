class NodoProducto:
    def __init__(self,nombre,cantidad,precio):
        self.nombre=nombre
        self.cantidad=cantidad
        self.precio=precio
        self.siguiente=None

class Inventario_lista:
    def __init__(self):
        self.cabeza=None
        self.stack=[]
        self.cola=[]

    def agregar_producto(self,nombre,cantidad,precio):
        nuevo=NodoProducto(nombre,cantidad,precio)
        if self.cabeza is None:
            self.cabeza=nuevo
        else:
            actual=self.cabeza
            while actual.siguiente:
                actual=actual.siguiente
            actual.siguiente=nuevo
        print(f"El producto: {nombre}  ha sido agregado con éxito.")

    def mostrar_inventario(self):
        if self.cabeza is None:
            print("El inventario esta vacío.")
            return
        actual=self.cabeza
        print("\n === Inventario === ")
        while actual:
            estado="Disponible" if actual.cantidad>0 else "Agotado"
            print(f"{actual.nombre} === Cantidad: {actual.cantidad} === Precio Q{actual.precio} === Estado: {estado}")
            actual=actual.siguiente

    def salidas(self,nombre,cantidad):
        actual=self.cabeza
        while actual:
            if actual.nombre==nombre:
                if actual.cantidad>=cantidad:
                    actual.cantidad-=cantidad
                    self.cola.append((nombre,cantidad))
                    print(f"La salida registrada es: {cantidad} unidades de: {nombre}")
                    return True
                else:
                    print("El stock  es insuficiente")
                    return False
            actual=actual.siguiente
        print("El producto no ha sido encontrado")
        return False

    def entradas(self,nombre,cantidad):
        actual=self.cabeza
        while actual:
            if actual.nombre==nombre:
                actual.cantidad+=cantidad
                self.stack.append((nombre,cantidad))
                print(f"la entrada registrada de : {cantidad} unidades de {nombre}")
                return True
            actual=actual.siguiente
        print("Producto no encontrado")
        return False

    def busqueda_secuencial(self,nombre):
        actual=self.cabeza
        while actual:
            if actual.nombre.lower()==nombre.lower():
                print(f"{nombre} encontrado === Cantidad: {actual.cantidad} === Precio Q{actual.precio}")
                return actual
            actual=actual.siguiente
        print("Producto no encontrado")
        return None

    def arreglo_de_lista(self):
        arreglo=[]
        actual=self.cabeza
        while actual:
            arreglo.append((actual.nombre,actual.cantidad,actual.precio))
            actual=actual.siguiente
        return arreglo

    def bubble_sort(self):
        lista=self.arreglo_lista()
        n=len(lista)
        for i in range(n):
            for j in range(0,n-i-1):
                if lista[j][0]>lista[j+1][0]:
                    lista[j],lista[j+1]=lista[j+1],lista[j]
        print("Inventario ordenado")
        return lista

    def hash_buscar(self,nombre):
        tabla={}
        actual=self.cabeza
        while actual:
            clave=sum(ord(c) for c in actual.nombre)%10
            tabla[clave]=actual
            actual=actual.siguiente
        clave=sum(ord(c) for c in nombre)%10
        return tabla.get(clave,None)




    





                 
                



        
    


