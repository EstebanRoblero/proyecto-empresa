import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
from comprobante import generar_comprobante, ventas_ram

def iniciar_interfaz_gui(lista_clientes, lista_citas, inventario, usuarios):
    root = tk.Tk()
    root.title("Sistema Peluquería")
    root.geometry("900x700")

    current_frame = None
    servicios_disponibles = [("Corte de cabello", 50), ("Manicura", 30), ("Pedicura", 35), ("Tinte", 80)]

    def cambiar_frame(frame):
        nonlocal current_frame
        if current_frame:
            current_frame.destroy()
        current_frame = frame
        current_frame.pack(fill="both", expand=True)

    # ==========================
    # MENÚ PRINCIPAL
    # ==========================
    def main_menu_gui():
        frame = tk.Frame(root)
        tk.Label(frame, text="=== SISTEMA PELUQUERÍA ===", font=("Arial", 24)).pack(pady=30)
        tk.Button(frame, text="Iniciar como CLIENTE", width=40, command=flujo_cliente_gui).pack(pady=10)
        tk.Button(frame, text="Iniciar como TRABAJADOR", width=40, command=lambda: login_window("trabajador", flujo_trabajador_gui)).pack(pady=10)
        tk.Button(frame, text="Iniciar como JEFE", width=40, command=lambda: login_window("jefe", flujo_jefe_gui)).pack(pady=10)
        tk.Button(frame, text="Salir", width=40, command=root.quit).pack(pady=20)
        cambiar_frame(frame)

    # ==========================
    # LOGIN
    # ==========================
    def login_window(role_required, callback):
        frame = tk.Frame(root)
        tk.Label(frame, text=f"Login {role_required.upper()}", font=("Arial", 18)).pack(pady=20)
        tk.Label(frame, text="Usuario:").pack()
        entry_user = tk.Entry(frame)
        entry_user.pack()
        tk.Label(frame, text="Contraseña:").pack()
        entry_pass = tk.Entry(frame, show="*")
        entry_pass.pack()

        def verificar():
            username = entry_user.get().strip()
            password = entry_pass.get().strip()
            rol = usuarios.autenticar(username, password)
            if rol == role_required:
                messagebox.showinfo("Login", f"Acceso concedido como {rol}")
                callback(username)
            else:
                messagebox.showerror("Login", "Usuario o rol incorrecto")

        tk.Button(frame, text="Ingresar", command=verificar).pack(pady=10)
        tk.Button(frame, text="Volver", command=main_menu_gui).pack(pady=5)
        cambiar_frame(frame)

    # ==========================
    # FLUJO CLIENTE
    # ==========================
    def flujo_cliente_gui():
        frame = tk.Frame(root)
        tk.Label(frame, text="Menú Cliente", font=("Arial", 18)).pack(pady=10)
        tk.Button(frame, text="Agendar cita", width=40, command=lambda: agendar_cita_gui("cliente")).pack(pady=5)
        tk.Button(frame, text="Ver mis citas", width=40, command=ver_citas_cliente_gui).pack(pady=5)
        tk.Button(frame, text="Cancelar cita", width=40, command=cancelar_cita_cliente_gui).pack(pady=5)
        tk.Button(frame, text="Volver", width=40, command=main_menu_gui).pack(pady=10)
        cambiar_frame(frame)

    # ==========================
    # AGENDAR CITA
    # ==========================
    def agendar_cita_gui(rol):
        frame = tk.Frame(root)
        tk.Label(frame, text="Agendar Cita", font=("Arial", 18)).pack(pady=10)

        tk.Label(frame, text="Nombre completo:").pack()
        entry_nombre = tk.Entry(frame)
        entry_nombre.pack()

        tk.Label(frame, text="Teléfono:").pack()
        entry_tel = tk.Entry(frame)
        entry_tel.pack()

        tk.Label(frame, text="Edad:").pack()
        entry_edad = tk.Entry(frame)
        entry_edad.pack()

        tk.Label(frame, text="Género (H/M):").pack()
        entry_genero = tk.Entry(frame)
        entry_genero.pack()

        tk.Label(frame, text="Fecha (DD-MM-YYYY):").pack()
        entry_fecha = tk.Entry(frame)
        entry_fecha.pack()

        tk.Label(frame, text="Hora (HH:MM AM/PM):").pack()
        entry_hora = tk.Entry(frame)
        entry_hora.pack()

        tk.Label(frame, text="Selecciona servicios:").pack()
        vars_check = []
        for desc, precio in servicios_disponibles:
            var = tk.IntVar()
            chk = tk.Checkbutton(frame, text=f"{desc} Q{precio}", variable=var)
            chk.pack(anchor="w")
            vars_check.append((var, desc, precio))

        def registrar():
            nombre = entry_nombre.get().strip()
            tel = entry_tel.get().strip()
            try:
                edad = int(entry_edad.get())
                if edad < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Edad inválida")
                return
            genero = entry_genero.get().strip().upper()
            fecha = entry_fecha.get().strip()
            hora = entry_hora.get().strip().lower()
            try:
                datetime.datetime.strptime(fecha, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Error", "Fecha inválida")
                return
            if not hora.endswith(("am", "pm")):
                messagebox.showerror("Error", "Hora debe incluir AM/PM")
                return

            cliente = lista_clientes.busqueda_secuencial(nombre)
            if not cliente:
                cliente = lista_clientes.agregar_cliente(nombre, tel, edad, genero)

            servicios_seleccionados = [(desc, precio) for var, desc, precio in vars_check if var.get() == 1]
            if not servicios_seleccionados:
                messagebox.showwarning("Aviso", "No se seleccionó ningún servicio")
                return

            # Validación de hora
            citas_mismo_dia = lista_citas.buscar_por_fecha(fecha)
            for c in citas_mismo_dia:
                if c.hora.lower() == hora.lower():
                    messagebox.showwarning("Aviso", "Ya existe una cita a esa hora")
                    return

            lista_citas.agregar_cita(cliente.nombre, [s[0] for s in servicios_seleccionados], fecha, hora)
            total = sum(s[1] for s in servicios_seleccionados)
            msg = f"Cita agendada para {cliente.nombre} el {fecha} a las {hora}\n"
            msg += "Servicios:\n" + "\n".join([f"- {s[0]} Q{s[1]}" for s in servicios_seleccionados])
            msg += f"\nTotal: Q{total}"
            messagebox.showinfo("Cita registrada", msg)
            flujo_cliente_gui()

        tk.Button(frame, text="Registrar cita", command=registrar).pack(pady=10)
        tk.Button(frame, text="Volver", command=flujo_cliente_gui).pack()
        cambiar_frame(frame)

    # ==========================
    # VER CITAS CLIENTE
    # ==========================
    def ver_citas_cliente_gui():
        nombre = simpledialog.askstring("Cliente", "Ingrese su nombre:")
        if nombre:
            citas = lista_citas.buscar_por_cliente(nombre)
            if citas:
                msg = "\n".join([f"{c.id_cita}: {c.fecha} {c.hora} - {', '.join(c.servicios)}" for c in citas])
                messagebox.showinfo("Mis citas", msg)
            else:
                messagebox.showinfo("Mis citas", "No hay citas registradas.")

    # ==========================
    # CANCELAR CITA CLIENTE
    # ==========================
    def cancelar_cita_cliente_gui():
        nombre = simpledialog.askstring("Cliente", "Ingrese su nombre:")
        if nombre:
            citas = lista_citas.buscar_por_cliente(nombre)
            if citas:
                msg = "\n".join([f"{c.id_cita}: {c.fecha} {c.hora} - {', '.join(c.servicios)}" for c in citas])
                id_cita = simpledialog.askstring("Cancelar cita", f"Citas:\n{msg}\nIngrese ID a cancelar:")
                if id_cita:
                    lista_citas.eliminar_cita(id_cita)
                    messagebox.showinfo("Cita cancelada", "Cita eliminada correctamente")
            else:
                messagebox.showinfo("Citas", "No tienes citas registradas.")

    # ==========================
    # FLUJO TRABAJADOR
    # ==========================
    def flujo_trabajador_gui(username):
        frame = tk.Frame(root)
        tk.Label(frame, text=f"Menú Trabajador ({username})", font=("Arial", 18)).pack(pady=10)

        tk.Button(frame, text="Registrar cliente y cita", width=50, command=lambda: agendar_cita_gui("trabajador")).pack(pady=5)
        tk.Button(frame, text="Registrar servicios y generar comprobante", width=50, command=registrar_servicios_gui).pack(pady=5)
        tk.Button(frame, text="Registrar uso de producto", width=50, command=registrar_uso_producto_gui).pack(pady=5)
        tk.Button(frame, text="Agregar producto al inventario", width=50, command=agregar_producto_inventario_gui).pack(pady=5)
        tk.Button(frame, text="Generar comprobante manual", width=50, command=generar_comprobante_manual_gui).pack(pady=5)
        tk.Button(frame, text="Cerrar sesión", width=50, command=main_menu_gui).pack(pady=10)
        cambiar_frame(frame)

    # ==========================
    # FLUJO JEFE
    # ==========================
    def flujo_jefe_gui(username):
        frame = tk.Frame(root)
        tk.Label(frame, text=f"Menú Jefe ({username})", font=("Arial", 18)).pack(pady=10)

        tk.Button(frame, text="Ver inventario", width=50, command=inventario.mostrar_inventario).pack(pady=5)
        tk.Button(frame, text="Reabastecer inventario", width=50, command=agregar_producto_inventario_gui).pack(pady=5)
        tk.Button(frame, text="Ver reporte mensual (TXT)", width=50, command=generar_reporte_jefe_gui).pack(pady=5)
        tk.Button(frame, text="Ver historial de inventario", width=50, command=inventario.mostrar_movimientos).pack(pady=5)
        tk.Button(frame, text="Registrar nuevo usuario", width=50, command=registrar_usuario_gui).pack(pady=5)
        tk.Button(frame, text="Cerrar sesión", width=50, command=main_menu_gui).pack(pady=10)
        cambiar_frame(frame)

    # ==========================
    # FUNCIONES AUXILIARES TRABAJADOR/JEFE
    # ==========================
    def registrar_servicios_gui():
        nombre = simpledialog.askstring("Cliente", "Nombre del cliente registrado:")
        if not nombre:
            return
        cliente = lista_clientes.busqueda_secuencial(nombre)
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado")
            return
        comp = generar_comprobante(cliente)
        for desc, precio in servicios_disponibles:
            if messagebox.askyesno("Servicio", f"¿Registrar {desc} Q{precio}?"):
                comp.agregar_item(desc, precio)
        fname = comp.guardar_pdf()
        if ventas_ram:
            ventas_ram[-1] = comp.to_dict()
        messagebox.showinfo("Comprobante", f"Comprobante generado en {fname}")

    def registrar_uso_producto_gui():
        prod = simpledialog.askstring("Producto", "Nombre del producto usado:")
        if not prod:
            return
        entrada = simpledialog.askstring("Cantidad", "Cantidad usada (unidades/ml):")
        if not entrada:
            return
        try:
            cantidad = float(entrada)
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")
            return
        ok = inventario.registrar_salida(prod, cantidad)
        if ok:
            messagebox.showinfo("Inventario", "Salida registrada correctamente")
        else:
            messagebox.showerror("Inventario", "Producto insuficiente o no encontrado")

    def agregar_producto_inventario_gui():
        prod = simpledialog.askstring("Producto", "Nombre del producto:")
        if not prod:
            return
        try:
            cant = float(simpledialog.askstring("Cantidad", "Cantidad:"))
        except:
            messagebox.showerror("Error", "Cantidad inválida")
            return
        nodo = inventario.busqueda_secuencial(prod)
        if nodo:
            inventario.registrar_entrada(prod, cant)
        else:
            try:
                precio = float(simpledialog.askstring("Precio", "Precio unitario Q:"))
            except:
                messagebox.showerror("Error", "Precio inválido")
                return
            inventario.agregar_producto(prod, cant, precio)
        messagebox.showinfo("Inventario", "Inventario actualizado")

    def generar_comprobante_manual_gui():
        nombre = simpledialog.askstring("Cliente", "Nombre del cliente:")
        if not nombre:
            return
        cliente = lista_clientes.busqueda_secuencial(nombre)
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado")
            return
        comp = generar_comprobante(cliente)
        while True:
            desc = simpledialog.askstring("Servicio", "Descripción del servicio (enter para terminar):")
            if not desc:
                break
            try:
                precio = float(simpledialog.askstring("Precio", "Precio Q:"))
            except:
                messagebox.showerror("Error", "Precio inválido")
                continue
            comp.agregar_item(desc, precio)
        fname = comp.guardar_pdf()
        if ventas_ram:
            ventas_ram[-1] = comp.to_dict()
        messagebox.showinfo("Comprobante", f"PDF guardado en {fname}")

    def generar_reporte_jefe_gui():
        yyyy_mm = simpledialog.askstring("Reporte", "Mes a reportar (YYYY-MM):")
        if not yyyy_mm:
            return
        fname, text = reportes.generar_reporte_mensual_txt(yyyy_mm, inventario_obj=inventario, carpeta="reportes")
        messagebox.showinfo("Reporte", f"Reporte guardado en {fname}")

    def registrar_usuario_gui():
        user = simpledialog.askstring("Nuevo usuario", "Usuario:")
        pwd = simpledialog.askstring("Contraseña", "Contraseña:")
        rol = simpledialog.askstring("Rol", "Rol (trabajador/jefe):").lower()
        ok = usuarios.agregar_usuario(user, pwd, rol)
        if ok:
            messagebox.showinfo("Usuario", "Usuario agregado")
        else:
            messagebox.showerror("Usuario", "Usuario ya existe")

    # ==========================
    # INICIO GUI
    # ==========================
    main_menu_gui()
    root.mainloop()
