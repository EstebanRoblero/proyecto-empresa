class Usuario:
    def __init__(self,nombre,rol):
        self.nombre=nombre
        self.rol=rol  # 'jefe' o 'trabajador'

class Lista_de_usuarios:
    def __init__(self):
        self.usuarios=[]

    def agregar_usuario(self,nombre,rol):
        self.usuarios.append(Usuario(nombre,rol))

    def mostrar_usuarios(self):
        print("\n== Usuarios del sistema ==")
        for u in self.usuarios:
            print(f"{u.nombre} | Rol: {u.rol}")