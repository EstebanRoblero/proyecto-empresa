#clases dentro de la lista de nodos 

class cliente:
    #dento de la clase cliente es un nodo ya que contiene los datos  
    def __init__(self, nombre, telefono, edad, genero):
        self.nombre=nombre
        self.telefono=telefono
        self.edad=edad
        self.genero=genero
        self.siguiente=None #aqui se establce el fin de la de lista si no hay nada 

    
    class Listadeclieentes:
        def __init__(self):
            # donde la lista se va enlazar 
            self.cabeza=None
            # cabeza de la lista enlazada

        def agregarcliente(self,nombre,telefono,edad,genero):
            nuevo=cliente(nombre,telefono,edad,genero)
            if not self.cabeza:
                self.cabeza=nuevo 
            else:
                actual=self.cabeza
                while actual.siguiente:
                    actual=actual.siguiente
                actual.siguiente=nuevo
            return nuevo
           
        def mostar_clientes(self):
            actual=self.cabeza 
            if not actual:
                print("No hay clientes registrados.") #aqui itera al usar punteros en el nodo 
                return 
            
            idz=1
            print("\n--Lista de clientes--")
            while actual:
                print(f"{idz}. {actual.nombre} == Telefono:{actual.telefono} == Edad: {actual.edad} == Genero {actual.genero}")
                actual=actual.siguiente
                idz+=1

        
        def busqueda_secuencial(self,nombre):
            actual=self.cabeza 
            while actual:
                if actual.nombre.lower() == nombre.lower():
                    return actual
                actual=actual.siguiente
            return None 
        
        def lista_obtener(self):
            arreglo=[]
            actual=self.cabeza
            while actual:
                arreglo.append(actual)
                actual=actual.siguiente
            return arreglo       
        
        def lista_reconstruida(self, arreglo):
            if not arreglo:
                self.cabeza=None
                return
            self.cabeza=arreglo[0]
            actual=self.cabeza
            actual.siguiente=None
            for nodo in arreglo[1:]:
                actual.siguiente=nodo
                actual=actual.siguiente
                actual.siguiente=None

        def selection_sort(self):
            arreglo= self.lista_obtener
            n=len(arreglo)
            for i in range(n):
                min_idz=i
                for j in range( i +1, n):
                    if arreglo[j].nombre.lower() < arreglo[min_idz].nombre.lower():
                        min_idz=j
                if min_idz != i:
                    arreglo[i], arreglo[min_idz]= arreglo[min_idz], arreglo[i]
            self.lista_reconstruida(arreglo)
            print("Lista de los clientess ordenada por nombre. ")        

        
        def eliminar_cliente(self, nombre):
            actual=self.cabeza
            previo=None
            while actual:
                if actual.nombre.lower()==nombre.lower():
                    if previo:
                        previo.sitguiente=actual.siguiente
                    else:
                        self.cabeza= actual.siguiente
                    return True
                previo=actual
                actual=actual.siguiente
            return False
        
        def lista_clientes(self):
            salida=[]
            actual=self.cabeza
            while actual:
                salida.append({
                    "nombre": actual.nombre,
                    "telefono": actual.telefono,
                    "edad": actual.edad,
                    "genero": actual.genero
               })
                actual=actual.siguiente
            return salida
        




    
        
        


