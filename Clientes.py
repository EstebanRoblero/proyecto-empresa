from db_clientes import crear_tabla_clientes, insertar_cliente, actualizar_cliente, eliminar_cliente_db, cargar_todos_clientes

crear_tabla_clientes()

class Cliente:
    def __init__(self, nombre, telefono, edad, genero):
        self.nombre = nombre
        self.telefono = telefono
        self.edad = edad
        self.genero = genero.upper()  # 'H' o 'M'
        self.siguiente = None
        self.id_db = None  # opcional: referencia a DB

class ListaClientes:
    def __init__(self):
        self.cabeza = None
        self.cargar_desde_db()

    # ---------------------------
    # Agregar cliente
    # ---------------------------
    def agregar_cliente(self, nombre, telefono, edad, genero):
        nuevo = Cliente(nombre, telefono, edad, genero)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        insertar_cliente(nuevo)
        return nuevo

    # ---------------------------
    # Mostrar clientes
    # ---------------------------
    def mostrar_clientes(self):
        actual = self.cabeza
        if actual is None:
            print("No hay clientes registrados.")
            return
        idx = 1
        print("\n== Lista de Clientes ==")
        while actual:
            print(f"{idx}. {actual.nombre} == Tel: {actual.telefono} == Edad: {actual.edad} == Genero: {actual.genero}")
            actual = actual.siguiente
            idx += 1

    # ---------------------------
    # Búsqueda secuencial
    # ---------------------------
    def busqueda_secuencial(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre.lower() == nombre.lower():
                return actual
            actual = actual.siguiente
        return None

    # ---------------------------
    # Ordenamiento por selección
    # ---------------------------
    def selection_sort(self):
        arreglo = self.obtener_lista()
        n = len(arreglo)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arreglo[j].nombre.lower() < arreglo[min_idx].nombre.lower():
                    min_idx = j
            if min_idx != i:
                arreglo[i], arreglo[min_idx] = arreglo[min_idx], arreglo[i]
        self.reconstruir_desde_lista(arreglo)
        print("Lista de clientes ordenada.")

    # ---------------------------
    # Obtener lista en arreglo
    # ---------------------------
    def obtener_lista(self):
        arreglo = []
        actual = self.cabeza
        while actual:
            arreglo.append(actual)
            actual = actual.siguiente
        return arreglo

    # ---------------------------
    # Reconstruir lista desde arreglo
    # ---------------------------
    def reconstruir_desde_lista(self, arreglo):
        if not arreglo:
            self.cabeza = None
            return
        self.cabeza = arreglo[0]
        actual = self.cabeza
        actual.siguiente = None
        for nodo in arreglo[1:]:
            actual.siguiente = nodo
            actual = actual.siguiente
            actual.siguiente = None

    # ---------------------------
    # Cargar todos los clientes desde DB
    # ---------------------------
    def cargar_desde_db(self):
        filas = cargar_todos_clientes()
        self.cabeza = None
        for fila in filas:
            id_db, nombre, telefono, edad, genero = fila
            nodo = Cliente(nombre, telefono, edad, genero)
            nodo.id_db = id_db
            if self.cabeza is None:
                self.cabeza = nodo
            else:
                actual = self.cabeza
                while actual.siguiente:
                    actual = actual.siguiente
                actual.siguiente = nodo


    
        
        


