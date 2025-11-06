import sqlite3
DB_FILE = "inventario.db"

def crear_tabla():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            cantidad REAL NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def agregar_producto(nombre, cantidad, precio):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, cantidad, precio)
        VALUES (?, ?, ?)
        ON CONFLICT(nombre) DO UPDATE SET cantidad=excluded.cantidad, precio=excluded.precio
    ''', (nombre, cantidad, precio))
    conn.commit()
    conn.close()

def actualizar_cantidad(nombre, cantidad):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE productos
        SET cantidad = ?
        WHERE nombre = ?
    ''', (cantidad, nombre))
    conn.commit()
    conn.close()

def obtener_productos():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, cantidad, precio FROM productos')
    filas = cursor.fetchall()
    conn.close()
    return filas
