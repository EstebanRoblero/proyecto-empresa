#clases 

class clientes: 
    def __init__(self, nombre, telefono, edad, email):
        self.nombre=nombre
        self.telefono=telefono
        self.edad=edad
        self.email=email


#arreglo udimensional 

lista_clientesarray=[]

#listas enlazadas y punteros 

class Nodocliente:
    def __init__(self,cliente):
        self.cliente=cliente
        self.siguiente=None #no hay nada en la cabeza pasa al siguiente 


class Enlazadalista_declientes:
    def __init__(self):
        self.cabeza=None # pasa a puntear el primero  de la cabeza del nodo 


def agregar_cliente(self,cliente):
    nodo_nuevo=Nodocliente(cliente)
    if not self.cabeza:
        self.cabeza=nodo_nuevo
    else:
        actual=self.cabeza
        while actual.siguiente:
            actual=actual.siguiente
        actual.siguiente=nodo_nuevo


def mostrar_cliente(self):
    actual= self.cabeza
    print("Esta es la lista enlaza de los clientes: ")
    while actual:
        print(f"cliente: {actual.cliente.nombre}")
        actual=actual.siguiente #segue el puntero 


#seccion de la pila 

class Clientespila:
    def __init__(self):
        self.items=[]
    

    def apilar_clientes(self, cliente):
        self.items.append(cliente)

    def desapilar(self):
        if self.items:
            return self.items.pop()
        return None
