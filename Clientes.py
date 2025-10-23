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
    
    def mostrar_primero(self):
        print(" esta es la pila de clientes recientes:")
        for cliente in reversed(self.items[-3:]): # de los ultimos 3 clientes recientes
            print(f"{cliente.nombre}")
        

#seccion de la cola

class  Clientescola:
    def __init__(self):
        self.items = []

    
    def encolar_cliente(self, cliente):
        self.items().append(cliente)

    
    def desencolar_cliente(self,cliente):
        if self.items:
            return self.items.popleft()
        return None
    
    def mostar(self):
        print(" Esta es la cola de los clientes en espera:")
        for cliente in self.items:
            print(f"{cliente.nombre}")

lista_enlazada=Enlazadalista_declientes()
pila_clientes= Clientespila()
cola_clientes=Clientescola()

#funvion principal 

def registro_declientes():
    print("resgistar al cliente")

    nombre=input("Escriba su nombre: ")
    email=input(" Escriba su Email: ")
    telefono=input("Coloque su numero de telefono: ")
    edad= input("Coloque su edad")



    cliente_nuevo=clientes(nombre, email,telefono,edad)


