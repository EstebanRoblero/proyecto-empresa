from db_usuarios import crear_tabla_usuarios, insertar_usuario, cargar_usuarios

# Crear tabla si no existe
crear_tabla_usuarios()

class ListaDeUsuarios:
    def __init__(self):
        # Usuarios por defecto en RAM
        self.usuarios = {
            "jefe": {"password": "1234", "rol": "jefe"},
            "trabajador": {"password": "0000", "rol": "trabajador"},
        }
        # Cargar usuarios desde DB y fusionar con los por defecto
        usuarios_db = cargar_usuarios()
        self.usuarios.update(usuarios_db)

        # Guardar los usuarios por defecto en DB si no existen
        for username, data in self.usuarios.items():
            insertar_usuario(username, data["password"], data["rol"])

    def autenticar(self, username, password):
        username = username.strip().lower()
        if username in self.usuarios:
            if self.usuarios[username]["password"] == password:
                return self.usuarios[username]["rol"]
        return None

    def agregar_usuario(self, username, password, rol):
        username = username.strip().lower()
        if username in self.usuarios:
            return False
        self.usuarios[username] = {"password": password, "rol": rol}
        # Guardar en DB
        insertar_usuario(username, password, rol)
        return True
