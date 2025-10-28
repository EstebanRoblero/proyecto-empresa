#clases dentro de la lista de nodos 

class cliente:
    #dento de la clase cliente es un nodo ya que contiene los datos  
    def __init__(self, nombre, telefono, edad):
        self.nombre=nombre
        self.telefono=telefono
        self.edad=edad
        self.siguiente=None #aqui se establce el fin de la de lista si no hay nada 

    
    class Listadeclienetes:
        def __init__(self):
            # donde la lista se va enlazar 
            self.cabeza=None
            # cabeza de la lista enlazada

        def agregarcliente(self,nombre,telefono,edad):
            nuevo=cliente(nombre,telefono,edad)
            if self.cabeza is None:# si la lista llegue a estar vacia el nodo empieza hacer la nueva cabeza 
                self.cabeza=nuevo 
            else:
                actual=self.cabeza
                while actual.siguiente:
                    actual=actual.siguiente #aqui esta recorriendo hasta llegar al final de la cabeza
                actual.siguiente=nuevo #luego lo conecta con el nodo nuevo al final del puntero 
            print(f"Cliente agragado {cliente} ")
        
        def mostarclientes(self): 
            if self.cabeza is None:
                print("No hay clientes registrados.") #aqui itera al usar punteros en el nodo 
                return 
            actual=self.cabeza
            print("\n--Lista de clientes--")
            while actual:
                print(f"{actual.nombre} == Telefono:{actual.telefono} == Edad: {actual.edad}")
                actual=actual.siguiente
        
        def buscarcliente(self,nombre):
            actual=self.cabeza 
            while actual:
                if actual.nombre.lower() == nombre.lower():
                    return actual
                actual=actual.siguiente
            return None 
        
        def bucleordenado(self):
            if not self.cabeza:
                return
            cambiado=True
            while cambiado:
                cambiado=False
                actual=self.cabeza
                while actual.siguiente:
                    if actual.nombre > actual.siguiente.nombre:
                        actual.nombre, actual.siguiente.nombre = actual.siguiente.nombre, actual.nombre
                        actual.telefono, actual.siguiente.telefono = actual.siguiente.telefono, actual.telefono
                        actual.edad, actual.siguiente.edad = actual.siguiente.edad, actual.edad
                        actual.genero, actual.siguiente.genero = actual.siguiente.genero, actual.genero
                        cambiado=True
                    actual=actual.siguiente
        
        def quicksort_ordenar(self):
            def quicksort(lista):
                if len(lista) <=1:
                    return lista
                soporte=lista[len (lista)//2]
                izquierda=[x for x in lista if x.nombre < soporte.nombre]
                centro=[x for x in lista if x.nombre== soporte.nombre]
                derecha=[x for x in lista if x.nombre > soporte.nombre]
                return quicksort(izquierda)+centro+quicksort(derecha)
            
            ordenados =quicksort(self.obtenerlista())
            self.cabeza=None
            for a in ordenados:
                self.agregarcliente(a.nombre, )
       

            
        




    
        
        


