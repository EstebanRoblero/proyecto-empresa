import sqlite3

DB_NAME = "citas.db"

def crear_tabla_citas():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id TEXT PRIMARY KEY,
            cliente_nombre TEXT NOT NULL,
            servicios TEXT,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            empleado TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

def insertar_cita(cita):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    servicios_str = ",".join(cita.servicios)  # lista a string
    cursor.execute('''
        INSERT INTO citas (id, cliente_nombre, servicios, fecha, hora, empleado)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (cita.id, cita.cliente_nombre, servicios_str, cita.fecha, cita.hora, cita.empleado))
    conexion.commit()
    conexion.close()

def actualizar_cita(cita):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    servicios_str = ",".join(cita.servicios)
    cursor.execute('''
        UPDATE citas
        SET cliente_nombre=?, servicios=?, fecha=?, hora=?, empleado=?
        WHERE id=?
    ''', (cita.cliente_nombre, servicios_str, cita.fecha, cita.hora, cita.empleado, cita.id))
    conexion.commit()
    conexion.close()

def eliminar_cita_db(id_cita):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM citas WHERE id=?', (id_cita,))
    conexion.commit()
    conexion.close()

def cargar_todas_citas():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM citas')
    filas = cursor.fetchall()
    conexion.close()
    return filas
