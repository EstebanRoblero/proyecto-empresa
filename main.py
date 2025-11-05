# main.py
import sys
from Clientes import ListaClientes
from servicios import atender_servicios_para_cliente, pila_historial
from inventario import Inventario_lista
from citas import ListaCitas
from comprobante import generar_comprobante
from usario import Lista_de_usuarios
import reportes

# Instancias globales (RAM)
lista_clientes = ListaClientes()
inventario = Inventario_lista()
lista_citas = ListaCitas()
usuarios = Lista_de_usuarios()  # contiene admin/1234 por defecto

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
def login_prompt():
    print("\n=== LOGIN ===")
    user = input("Usuario: ").strip()
    pwd = input("Contraseña: ").strip()
    rol = usuarios.autenticar(user, pwd)
    if rol:
        print(f"Acceso concedido. Rol: {rol}")
    else:
        print("Credenciales inválidas.")
    return rol

# ---------------------------------------------------
# FLUJO TRABAJADOR
# ---------------------------------------------------
def flujo_trabajador(username):
    while True:
        print("\n=== MENÚ TRABAJADOR ===")
        print("1. Registrar cliente y cita")
        print("2. Registrar servicios prestados (y generar comprobante)")
        print("3. Registrar uso de producto (descontar inventario)")
        print("4. Generar comprobante manual para cliente")
        print("5. Cerrar sesión")
        op = input("Opción: ").strip()

        if op == "1":
            nombre = input("Nombre completo: ").strip()
            tel = input("Teléfono: ").strip()
            edad = int(input("Edad: ").strip())
            genero = input("Género (H/M): ").strip().upper()
            cliente = lista_clientes.agregar_cliente(nombre, tel, edad, genero)
            fecha = input("Fecha cita (YYYY-MM-DD): ").strip()
            hora = input("Hora (HH:MM): ").strip()
            lista_citas.agregar_cita(cliente.nombre, fecha, hora)
            print(f"✅ Cita registrada para {cliente.nombre} - {fecha} {hora}")

        elif op == "2":
            nombre = input("Nombre del cliente (registrado): ").strip()
            cliente = lista_clientes.busqueda_secuencial(nombre)
            if not cliente:
                print("Cliente no encontrado. Regístralo primero.")
                continue

            comp = generar_comprobante(cliente, None, None)
            atender_servicios_para_cliente(cliente, comp.agregar_item)

            # Generar comprobante en TXT (sin PDF)
            fname = comp.guardar_txt()

            from comprobante import ventas_ram
            if ventas_ram:
                ventas_ram[-1] = comp.to_dict()

            print(f"✅ Comprobante generado y guardado en {fname}")

        elif op == "3":
            prod = input("Nombre del producto usado: ").strip()
            cantidad = float(input("Cantidad usada (unidades/ml): ").strip())
            ok = inventario.registrar_salida(prod, cantidad)
            if not ok:
                print("⚠️ No se pudo registrar la salida (producto faltante).")
            else:
                print("✅ Salida registrada en inventario.")

        elif op == "4":
            nombre = input("Nombre del cliente: ").strip()
            cliente = lista_clientes.busqueda_secuencial(nombre)
            if not cliente:
                print("Cliente no encontrado.")
                continue

            comp = generar_comprobante(cliente, None, None)
            while True:
                desc = input("Descripción del servicio (enter para terminar): ").strip()
                if desc == "":
                    break
                precio = float(input("Precio Q: ").strip())
                comp.agregar_item(desc, precio)

            fname = comp.guardar_txt()
            from comprobante import ventas_ram
            if ventas_ram:
                ventas_ram[-1] = comp.to_dict()

            print(f"✅ Comprobante guardado en {fname}")

        elif op == "5":
            print("👋 Cerrando sesión trabajador.")
            break

        else:
            print("Opción inválida.")

# ---------------------------------------------------
# FLUJO JEFE
# ---------------------------------------------------
def flujo_jefe(username):
    while True:
        print("\n=== MENÚ JEFE ===")
        print("1. Ver inventario")
        print("2. Reabastecer inventario (entrada)")
        print("3. Ver reporte mensual (TXT)")
        print("4. Ver historial de inventario")
        print("5. Registrar nuevo usuario del sistema")
        print("6. Cerrar sesión")
        op = input("Opción: ").strip()

        if op == "1":
            inventario.mostrar_inventario()

        elif op == "2":
            prod = input("Nombre del producto: ").strip()
            cantidad = float(input("Cantidad a ingresar: ").strip())
            ok = inventario.registrar_entrada(prod, cantidad)
            if not ok:
                precio = float(input("Producto no existe. Indica precio unitario Q: ").strip())
                inventario.agregar_producto(prod, cantidad, precio)
            print("✅ Inventario actualizado correctamente.")

        elif op == "3":
            yyyy_mm = input("Mes a reportar (YYYY-MM): ").strip()
            fname, text = reportes.generar_reporte_mensual_txt(
                yyyy_mm, inventario_obj=inventario, carpeta="reportes"
            )
            print(f"📄 Reporte mensual guardado en: {fname}")

        elif op == "4":
            inventario.mostrar_movimientos()

        elif op == "5":
            user = input("Nuevo usuario (username): ").strip()
            pwd = input("Contraseña: ").strip()
            rol = input("Rol (jefe/trabajador): ").strip().lower()
            ok = usuarios.agregar_usuario(user, pwd, rol)
            if ok:
                print("✅ Usuario agregado con éxito.")
            else:
                print("⚠️ No se pudo agregar (usuario ya existe).")

        elif op == "6":
            print("👋 Cerrando sesión jefe.")
            break

        else:
            print("Opción inválida.")

# ---------------------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------------------
def main_menu():
    print("=== SISTEMA PELUQUERÍA (CON ROLES) ===")
    while True:
        print("""
1. Iniciar como TRABAJADOR (login)
2. Iniciar como JEFE (login)
0. Salir
""")
        op = input("Elección: ").strip()

        if op == "0":
            print("👋 Saliendo del programa.")
            sys.exit(0)

        elif op in ("1", "2"):
            rol_esperado = "trabajador" if op == "1" else "jefe"
            print(f"Ingrese credenciales para rol {rol_esperado.upper()}:")
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            rol = usuarios.autenticar(username, password)

            if not rol:
                print("Credenciales inválidas.")
                continue

            if rol != rol_esperado:
                print(f"⚠️ El usuario no tiene permisos de {rol_esperado}. (rol actual: {rol})")
                continue

            if rol == "trabajador":
                flujo_trabajador(username)
            elif rol == "jefe":
                flujo_jefe(username)

        else:
            print("Opción inválida.")

# ---------------------------------------------------
# EJECUCIÓN
# ---------------------------------------------------
if __name__ == "__main__":
    main_menu()
