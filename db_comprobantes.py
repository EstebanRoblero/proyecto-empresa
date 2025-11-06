import sqlite3

DB_NAME = "comprobantes.db"

def crear_tabla_comprobantes():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comprobantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            fecha_emision TEXT,
            total REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comprobante_id INTEGER,
            descripcion TEXT,
            precio REAL,
            FOREIGN KEY(comprobante_id) REFERENCES comprobantes(id)
        )
    ''')
    conexion.commit()
    conexion.close()

def insertar_comprobante(comprobante):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO comprobantes (cliente, fecha_emision, total)
        VALUES (?, ?, ?)
    ''', (comprobante.cliente.nombre, comprobante.fecha_emision, comprobante.total()))
    id_comprobante = cursor.lastrowid
    for desc, precio in comprobante.items:
        cursor.execute('''
            INSERT INTO items (comprobante_id, descripcion, precio)
            VALUES (?, ?, ?)
        ''', (id_comprobante, desc, precio))
    conexion.commit()
    conexion.close()

def cargar_todos_comprobantes():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM comprobantes')
    comprobantes = cursor.fetchall()
    resultados = []
    for comp in comprobantes:
        id_comp, cliente, fecha_emision, total = comp
        cursor.execute('SELECT descripcion, precio FROM items WHERE comprobante_id=?', (id_comp,))
        items = cursor.fetchall()
        resultados.append({
            "id": id_comp,
            "cliente": cliente,
            "fecha_emision": fecha_emision,
            "items": items,
            "total": total
        })
    conexion.close()
    return resultados
