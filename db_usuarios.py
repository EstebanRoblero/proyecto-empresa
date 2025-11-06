import sqlite3

DB_NAME = "usuarios.db"

def crear_tabla_usuarios():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

def insertar_usuario(username, password, rol):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuarios (username, password, rol)
            VALUES (?, ?, ?)
        ''', (username.lower(), password, rol))
        conexion.commit()
    except sqlite3.IntegrityError:
        # Usuario ya existe
        pass
    conexion.close()

def cargar_usuarios():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('SELECT username, password, rol FROM usuarios')
    usuarios = cursor.fetchall()
    conexion.close()
    return {u[0]: {"password": u[1], "rol": u[2]} for u in usuarios}
