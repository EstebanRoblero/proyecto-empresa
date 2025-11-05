# usario.py

class Lista_de_usuarios:
    def __init__(self):
        # Usuarios por defecto
        self.usuarios = {
            "jefe": {"password": "1234", "rol": "jefe"},
            "trabajador": {"password": "0000", "rol": "trabajador"},
        }

    def autenticar(self, username, password):
        """Verifica usuario y contraseña y devuelve el rol si es correcto."""
        username = username.strip().lower()
        if username in self.usuarios:
            if self.usuarios[username]["password"] == password:
                return self.usuarios[username]["rol"]
        return None

    def agregar_usuario(self, username, password, rol):
        """Agrega un nuevo usuario al sistema."""
        username = username.strip().lower()
        if username in self.usuarios:
            return False
        self.usuarios[username] = {"password": password, "rol": rol}
        return True

