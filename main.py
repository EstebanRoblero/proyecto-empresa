import sys
import datetime
from servicios import atender_servicios_para_cliente
from inventario import Inventario_lista
from citas import ListaCitas
from comprobante import generar_comprobante
from usuario import ListaDeUsuarios
from reportes import Reportes
from Clientes import ListaClientes
from interfaz_grafica import iniciar_interfaz

# Inicialización de listas y clases
lista_clientes = ListaClientes()
inventario = Inventario_lista()
lista_citas = ListaCitas()
usuarios = ListaDeUsuarios()  # admin/1234 por defecto
reportes_obj = Reportes()

# ==========================
# LOGIN
# ==========================
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

# ==========================
# FLUJO CLIENTE
# ==========================
def flujo_cliente():
    while True:
        print("\n=== MENÚ CLIENTE ===")
        print("1. Agendar cita")
        print("2. Ver mis citas")
        print("3. Cancelar una cita")
        print("4. Volver al menú principal")
        op = input("Opción: ").strip()

        if op == "1":
            nombre = input("Nombre completo: ").strip()
            tel = input("Teléfono: ").strip()

            cliente = lista_clientes.busqueda_secuencial(nombre)
            if not cliente:
                print("No estabas registrado, te agregamos al sistema.")
                try:
                    edad = int(input("Edad: ").strip())
                    if edad < 0:
                        print("La edad no puede ser negativa.")
                        continue
                except ValueError:
                    print("Ingresa una edad válida.")
                    continue

                while True:
                    genero = input("Género (H/M): ").strip().upper()
                    if genero in ["H", "M"]:
                        break
                    print("Por favor, ingresa H o M solamente.")

                cliente = lista_clientes.agregar_cliente(nombre, tel, edad, genero)

            fecha = input("Fecha de la cita (DD-MM-YYYY): ").strip()
            try:
                datetime.datetime.strptime(fecha, "%d-%m-%Y")
            except ValueError:
                print("Formato de fecha inválido. Usa DD-MM-YYYY.")
                continue

            hora = input("Hora cita (HH:MM AM/PM): ").strip().lower()
            if not hora.endswith(("am", "pm")):
                print("Por favor incluya AM o PM (ejemplo: 11:00 am).")
                continue

            citas_mismo_dia = lista_citas.buscar_por_fecha(fecha)
            for c in citas_mismo_dia:
                if c.hora.lower() == hora.lower():
                    print("Ya existe una cita a esa hora. Elige otra.")
                    break
            else:
                def dummy_agregar(desc, precio):
                    print(f"Servicio agregado: {desc} Q{precio}")

                servicios = atender_servicios_para_cliente(cliente, dummy_agregar, genero=cliente.genero)

                if servicios:
                    lista_citas.agregar_cita(cliente.nombre, [s[0] for s in servicios], fecha, hora)
                    print(f"\nCita agendada para {cliente.nombre} el {fecha} a las {hora}")
                    total = sum(s[1] for s in servicios)
                    print("Servicios seleccionados:")
                    for s in servicios:
                        print(f"- {s[0]} Q{s[1]}")
                    print(f"Total a pagar: Q{total}")
                else:
                    print("No se registró ninguna cita porque no se seleccionaron servicios.")

        elif op == "2":
            nombre = input("Ingresa tu nombre para ver tus citas: ").strip()
            lista_citas.mostrar_citas_cliente(nombre)

        elif op == "3":
            nombre = input("Tu nombre: ").strip()
            lista_citas.mostrar_citas_cliente(nombre)
            id_cita = input("ID de la cita que deseas cancelar: ").strip()
            lista_citas.eliminar_cita(id_cita)

        elif op == "4":
            break
        else:
            print("Opción inválida.")

# ==========================
# FLUJO TRABAJADOR
# ==========================
def flujo_trabajador(username):
    while True:
        print("\n=== MENÚ TRABAJADOR ===")
        print("1. Registrar cliente y cita")
        print("2. Registrar servicios prestados (y generar comprobante)")
        print("3. Registrar uso de producto (descontar inventario)")
        print("4. Agregar producto al inventario")
        print("5. Generar comprobante manual para cliente")
        print("6. Cerrar sesión")
        op = input("Opción: ").strip()

        if op == "1":
            nombre = input("Nombre completo: ").strip()
            tel = input("Teléfono: ").strip()
            try:
                edad = int(input("Edad: ").strip())
                if edad < 0:
                    print("La edad no puede ser negativa.")
                    continue
            except ValueError:
                print("Edad inválida.")
                continue
            while True:
                genero = input("Género (H/M): ").strip().upper()
                if genero in ["H", "M"]:
                    break
                print("Por favor, ingresa H o M solamente.")
            cliente = lista_clientes.agregar_cliente(nombre, tel, edad, genero)
            fecha = input("Fecha cita (DD-MM-YYYY): ").strip()
            hora = input("Hora (HH:MM AM/PM): ").strip().lower()
            lista_citas.agregar_cita(cliente.nombre, [], fecha, hora)
            print(f"Cita registrada para {cliente.nombre} - {fecha} {hora}")

        elif op == "2":
            nombre = input("Nombre del cliente (registrado): ").strip()
            cliente = lista_clientes.busqueda_secuencial(nombre)
            if not cliente:
                print("Cliente no encontrado. Regístralo primero.")
                continue
            comp = generar_comprobante(cliente)
            servicios = atender_servicios_para_cliente(cliente, comp.agregar_item, genero=cliente.genero)
            fname = comp.guardar_pdf()
            print(f"Comprobante PDF generado y guardado en {fname}")

        elif op == "3":
            prod = input("Nombre del producto usado: ").strip()
            entrada = input("Cantidad usada (unidades/ml): ").strip()
            tipo = input("Tipo (unidad/ml): ").strip().lower()
            try:
                cantidad = float(''.join(c for c in entrada if c.isdigit() or c == '.'))
                if cantidad < 0:
                    print("No se permiten cantidades negativas.")
                    continue
            except ValueError:
                print("Cantidad inválida.")
                continue
            ok = inventario.registrar_salida(prod, cantidad)
            if not ok:
                print("No se pudo registrar la salida (producto faltante o insuficiente).")
            else:
                print("Salida registrada en inventario.")

        elif op == "4":
            prod = input("Nombre del producto: ").strip()
            try:
                cant = float(input("Cantidad: ").strip())
                if cant < 0:
                    print("No se permiten cantidades negativas.")
                    continue
            except ValueError:
                print("Cantidad inválida.")
                continue
            tipo = input("Tipo de producto (unidad/ml): ").strip().lower()
            nodo = inventario.busqueda_secuencial(prod)
            if nodo:
                inventario.registrar_entrada(prod, cant)
            else:
                try:
                    precio = float(input("Producto nuevo. Precio unitario Q: ").strip())
                    if precio < 0:
                        print("No se permiten precios negativos.")
                        continue
                except ValueError:
                    print("Precio inválido.")
                    continue
                inventario.agregar_producto(prod, cant, precio)
            print("Inventario actualizado.")

        elif op == "5":
            nombre = input("Nombre del cliente: ").strip()
            cliente = lista_clientes.busqueda_secuencial(nombre)
            if not cliente:
                print("Cliente no encontrado.")
                continue
            comp = generar_comprobante(cliente)
            while True:
                desc = input("Descripción del servicio (enter para terminar): ").strip()
                if desc == "":
                    break
                try:
                    precio = float(input("Precio Q: ").strip())
                    if precio < 0:
                        print("No se permiten precios negativos.")
                        continue
                except ValueError:
                    print("Precio inválido.")
                    continue
                comp.agregar_item(desc, precio)
            fname = comp.guardar_pdf()
            print(f"Comprobante PDF guardado en {fname}")

        elif op == "6":
            print("Cerrando sesión trabajador.")
            break
        else:
            print("Opción inválida.")

# ==========================
# FLUJO JEFE
# ==========================
def flujo_jefe(username):
    while True:
        print("\n=== MENÚ JEFE ===")
        print("1. Ver inventario")
        print("2. Reabastecer inventario")
        print("3. Generar reporte mensual (PDF)")
        print("4. Ver historial de inventario")
        print("5. Registrar nuevo usuario")
        print("6. Cerrar sesión")
        op = input("Opción: ").strip()

        if op == "1":
            inventario.mostrar_inventario()
        elif op == "2":
            prod = input("Producto: ").strip()
            try:
                cant = float(input("Cantidad: ").strip())
                if cant < 0:
                    print("No se permiten cantidades negativas.")
                    continue
            except ValueError:
                print("Cantidad inválida.")
                continue
            tipo = input("Tipo de producto (unidad/ml): ").strip().lower()
            nodo = inventario.busqueda_secuencial(prod)
            if nodo:
                inventario.registrar_entrada(prod, cant)
            else:
                try:
                    precio = float(input("Producto nuevo. Precio unitario Q: ").strip())
                    if precio < 0:
                        print("No se permiten precios negativos.")
                        continue
                except ValueError:
                    print("Precio inválido.")
                    continue
                inventario.agregar_producto(prod, cant, precio)
            print("Inventario actualizado.")

        elif op == "3":
            yyyy_mm = input("Mes a reportar (YYYY-MM): ").strip()
            fname = reportes_obj.generar_reporte_mensual_pdf(
                yyyy_mm, inventario_obj=inventario, carpeta="reportes"
            )
            print(f"✅ Reporte mensual PDF generado: {fname}")

        elif op == "4":
            inventario.mostrar_movimientos()

        elif op == "5":
            user = input("Nuevo usuario: ").strip()
            pwd = input("Contraseña: ").strip()
            rol = input("Rol (jefe/trabajador): ").strip().lower()
            ok = usuarios.agregar_usuario(user, pwd, rol)
            if ok:
                print("Usuario agregado.")
            else:
                print("Usuario ya existe.")

        elif op == "6":
            print("Cerrando sesión jefe.")
            break
        else:
            print("Opción inválida.")

# ==========================
# MENÚ PRINCIPAL
# ==========================
def main_menu():
    print("=== SISTEMA PELUQUERÍA ===")
    while True:
        print("""
1. Iniciar como CLIENTE
2. Iniciar como TRABAJADOR (login)
3. Iniciar como JEFE (login)
0. Salir
""")
        op = input("Elección: ").strip()

        if op == "0":
            print("Saliendo del sistema.")
            sys.exit(0)
        elif op == "1":
            flujo_cliente()
        elif op == "2":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            rol = usuarios.autenticar(username, password)
            if rol == "trabajador":
                flujo_trabajador(username)
            else:
                print("Usuario sin permisos de trabajador.")
        elif op == "3":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            rol = usuarios.autenticar(username, password)
            if rol == "jefe":
                flujo_jefe(username)
            else:
                print("Usuario sin permisos de jefe.")
        else:
            print("Opción inválida.")

# ==========================
# EJECUCIÓN
# ==========================
if __name__ == "__main__":
    iniciar_interfaz()
