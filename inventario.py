from db_inventario import crear_tabla, agregar_producto, actualizar_cantidad, obtener_productos

# ---------------------------------------------------
# Nodo de producto con tipo
# ---------------------------------------------------
class NodoProducto:
    def __init__(self, nombre, cantidad, precio, tipo="unidad"):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.tipo = tipo  # "unidad" o "ml"
        self.siguiente = None

# ---------------------------------------------------
# Lista enlazada de inventario
# ---------------------------------------------------
class Inventario_lista:
    def __init__(self):
        self.cabeza = None
        self.stack = []  # Entradas
        self.cola = []   # Salidas
        crear_tabla()    # Crear tabla si no existe
        self.cargar_desde_db()

    # Cargar productos desde DB
    def cargar_desde_db(self):
        productos = obtener_productos()
        for nombre, cantidad, precio in productos:
            self.agregar_producto_memoria(nombre, cantidad, precio)

    # Agregar producto en memoria
    def agregar_producto_memoria(self, nombre, cantidad, precio, tipo="unidad"):
        nuevo = NodoProducto(nombre, cantidad, precio, tipo)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    # Agregar producto nuevo o actualizar existente
    def agregar_producto(self, nombre, cantidad, precio, tipo="unidad"):
        nodo = self.busqueda_secuencial(nombre)
        if nodo:
            nodo.cantidad += cantidad
            nodo.precio = precio
            nodo.tipo = tipo
            print(f"Producto {nombre} actualizado: {nodo.cantidad} {tipo}, Q{precio}")
        else:
            self.agregar_producto_memoria(nombre, cantidad, precio, tipo)
            print(f"Producto {nombre} agregado: {cantidad} {tipo}, Q{precio}")
        # Guardar/actualizar en DB
        agregar_producto(nombre, nodo.cantidad if nodo else cantidad, nodo.precio if nodo else precio)

    # Mostrar inventario completo
    def mostrar_inventario(self):
        if self.cabeza is None:
            print("Inventario vacío")
            return
        print("\n=== Inventario ===")
        actual = self.cabeza
        while actual:
            estado = "Disponible" if actual.cantidad > 0 else "Agotado"
            print(f"{actual.nombre} | Cantidad: {actual.cantidad} {actual.tipo} | Precio: Q{actual.precio} | Estado: {estado}")
            actual = actual.siguiente

    # Registrar entrada de producto
    def registrar_entrada(self, nombre, cantidad):
        nodo = self.busqueda_secuencial(nombre)
        if nodo:
            nodo.cantidad += cantidad
            self.stack.append((nombre, cantidad, nodo.tipo))
            actualizar_cantidad(nombre, nodo.cantidad)
            print(f"Entrada registrada: {cantidad} {nodo.tipo} de {nombre}")
            return True
        print("Producto no encontrado")
        return False

    # Registrar salida de producto
    def registrar_salida(self, nombre, cantidad):
        nodo = self.busqueda_secuencial(nombre)
        if nodo:
            if nodo.cantidad >= cantidad:
                nodo.cantidad -= cantidad
                self.cola.append((nombre, cantidad, nodo.tipo))
                actualizar_cantidad(nombre, nodo.cantidad)
                print(f"Salida registrada: {cantidad} {nodo.tipo} de {nombre}")
                return True
            else:
                print("Stock insuficiente")
                return False
        print("Producto no encontrado")
        return False

    # Buscar producto en memoria
    def busqueda_secuencial(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre.lower() == nombre.lower():
                return actual
            actual = actual.siguiente
        return None

    # Mostrar historial de entradas y salidas
    def mostrar_movimientos(self):
        print("\n=== Movimientos de Inventario ===")
        if self.stack:
            print("\n-- Entradas --")
            for nombre, cant, tipo in self.stack:
                print(f"{nombre}: +{cant} {tipo}")
        if self.cola:
            print("\n-- Salidas --")
            for nombre, cant, tipo in self.cola:
                print(f"{nombre}: -{cant} {tipo}")
