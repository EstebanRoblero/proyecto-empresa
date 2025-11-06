import sqlite3

DB_NAME = "clientes.db"

def crear_tabla_clientes():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            edad INTEGER,
            genero TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

def insertar_cliente(cliente):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO clientes (nombre, telefono, edad, genero)
        VALUES (?, ?, ?, ?)
    ''', (cliente.nombre, cliente.telefono, cliente.edad, cliente.genero))
    conexion.commit()
    conexion.close()

def actualizar_cliente(cliente, id_cliente):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE clientes
        SET nombre=?, telefono=?, edad=?, genero=?
        WHERE id=?
    ''', (cliente.nombre, cliente.telefono, cliente.edad, cliente.genero, id_cliente))
    conexion.commit()
    conexion.close()

def eliminar_cliente_db(id_cliente):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM clientes WHERE id=?', (id_cliente,))
    conexion.commit()
    conexion.close()

def cargar_todos_clientes():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM clientes')
    filas = cursor.fetchall()
    conexion.close()
    return filas
