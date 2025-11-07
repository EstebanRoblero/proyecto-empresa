import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, PhotoImage
from Clientes import ListaClientes
from inventario import Inventario_lista
from citas import ListaCitas
from usuario import ListaDeUsuarios
from comprobante import generar_comprobante
from servicios import atender_servicios_para_cliente
from reportes import Reportes

# ==========================
# Inicialización global
# ==========================
lista_clientes = ListaClientes()
inventario = Inventario_lista()
lista_citas = ListaCitas()
usuarios = ListaDeUsuarios()  # contiene admin/1234
reportes = Reportes()

# ==========================
# FUNCIONES AUXILIARES
# ==========================
def cerrar_ventana(ventana):
    ventana.destroy()

def abrir_nueva_ventana(ventana_actual, nueva_funcion):
    cerrar_ventana(ventana_actual)
    nueva_funcion()

def centrar_ventana(ventana, ancho=600, alto=400):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# ==========================
# FUNCIONES CLIENTE
# ==========================
def ventana_agendar_cita(master):
    cerrar_ventana(master)
    v = tk.Tk()
    v.title("Agendar Cita - Infinity Studio")
    centrar_ventana(v, 700, 600)
    v.configure(bg="#fef6f9")

    tk.Label(v, text="Agendar Cita", font=("Georgia", 20, "bold"),
             bg="#fef6f9", fg="#a83279").pack(pady=10)

    frame = tk.Frame(v, bg="#fef6f9")
    frame.pack(pady=10)

    # Campos
    tk.Label(frame, text="Nombre:", bg="#fef6f9").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_nombre = tk.Entry(frame, width=25)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Teléfono:", bg="#fef6f9").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_tel = tk.Entry(frame, width=25)
    entry_tel.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Edad:", bg="#fef6f9").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_edad = tk.Entry(frame, width=25)
    entry_edad.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame, text="Género (H/M):", bg="#fef6f9").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    combo_genero = ttk.Combobox(frame, values=["H", "M"], state="readonly", width=22)
    combo_genero.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame, text="Fecha (DD-MM-YYYY):", bg="#fef6f9").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_fecha = tk.Entry(frame, width=25)
    entry_fecha.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(frame, text="Hora (HH:MM am/pm):", bg="#fef6f9").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_hora = tk.Entry(frame, width=25)
    entry_hora.grid(row=5, column=1, padx=5, pady=5)

    # Frame para mostrar los servicios
    frame_servicios = tk.LabelFrame(v, text="Servicios disponibles",
                                    bg="#fef6f9", fg="#a83279", font=("Arial", 10, "bold"))
    frame_servicios.pack(pady=10, padx=20, fill="both", expand=True)

    # Scrollbar para servicios
    scroll_servicios = tk.Scrollbar(frame_servicios)
    scroll_servicios.pack(side=tk.RIGHT, fill=tk.Y)

    canvas_servicios = tk.Canvas(frame_servicios, bg="#fef6f9", yscrollcommand=scroll_servicios.set)
    canvas_servicios.pack(side=tk.LEFT, fill="both", expand=True)

    scroll_servicios.config(command=canvas_servicios.yview)

    frame_servicios_interior = tk.Frame(canvas_servicios, bg="#fef6f9")
    canvas_servicios.create_window((0, 0), window=frame_servicios_interior, anchor="nw")

    servicios_vars = []

    def cargar_servicios():
        # Limpiar servicios anteriores
        for widget in frame_servicios_interior.winfo_children():
            widget.destroy()
        servicios_vars.clear()

        nombre = entry_nombre.get().strip()
        genero = combo_genero.get().strip().upper()
        
        if not nombre:
            messagebox.showerror("Error", "Ingresa tu nombre primero")
            return
            
        if genero not in ["H", "M"]:
            messagebox.showerror("Error", "Selecciona el género (H/M)")
            return

        # Buscar o crear cliente
        cliente = lista_clientes.busqueda_secuencial(nombre)
        if not cliente:
            # Si no existe, usar datos del formulario
            tel = entry_tel.get().strip()
            try:
                edad = int(entry_edad.get().strip()) if entry_edad.get().strip() else 18
            except:
                edad = 18
            cliente = lista_clientes.agregar_cliente(nombre, tel, edad, genero)

        # Función dummy para atender_servicios_para_cliente
        def dummy_agregar(desc, precio):
            pass

        # Obtener servicios disponibles según el género
        servicios_disponibles = atender_servicios_para_cliente(cliente, dummy_agregar, genero=genero)

        # Mostrar servicios como checkbuttons
        for i, (desc, precio) in enumerate(servicios_disponibles):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame_servicios_interior, 
                              text=f"{desc} - Q{precio:.2f}",
                              variable=var, 
                              bg="#fef6f9",
                              fg="#a83279",
                              font=("Arial", 9),
                              anchor="w")
            cb.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            servicios_vars.append((var, desc, precio))

        # Actualizar el canvas
        frame_servicios_interior.update_idletasks()
        canvas_servicios.config(scrollregion=canvas_servicios.bbox("all"))

    # Botón para cargar servicios
    tk.Button(v, text="Cargar Servicios", bg="#a83279", fg="white", width=20,
              font=("Arial", 10, "bold"), command=cargar_servicios).pack(pady=5)

    def guardar_cita():
        nombre = entry_nombre.get().strip()
        tel = entry_tel.get().strip()
        edad_str = entry_edad.get().strip()
        genero = combo_genero.get().strip().upper()
        fecha = entry_fecha.get().strip()
        hora = entry_hora.get().strip().lower()

        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return
        if not tel:
            messagebox.showerror("Error", "El teléfono es obligatorio.")
            return
        if not edad_str:
            messagebox.showerror("Error", "La edad es obligatoria.")
            return
        if genero not in ["H", "M"]:
            messagebox.showerror("Error", "Selecciona un género válido (H/M).")
            return
        if not fecha:
            messagebox.showerror("Error", "La fecha es obligatoria.")
            return
        if not hora:
            messagebox.showerror("Error", "La hora es obligatoria.")
            return

        try:
            edad = int(edad_str)
            if edad <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Edad inválida.")
            return

        # Verificar formato de hora
        if not any(x in hora for x in ['am', 'pm']):
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM am/pm")
            return

        # Buscar o crear cliente
        cliente = lista_clientes.busqueda_secuencial(nombre)
        if not cliente:
            cliente = lista_clientes.agregar_cliente(nombre, tel, edad, genero)

        # Verificar disponibilidad de hora
        for c in lista_citas.buscar_por_fecha(fecha):
            if c.hora.lower() == hora:
                messagebox.showerror("Error", "Ya existe una cita en esa hora.")
                return

        # Obtener servicios seleccionados
        seleccionados = [(d, p) for var, d, p in servicios_vars if var.get()]
        if not seleccionados:
            messagebox.showinfo("Info", "No se seleccionaron servicios.")
            return

        # Agregar cita
        lista_citas.agregar_cita(cliente.nombre, [s[0] for s in seleccionados], fecha, hora)
        total = sum(s[1] for s in seleccionados)
        detalle = "\n".join([f"• {s[0]} - Q{s[1]:.2f}" for s in seleccionados])
        
        messagebox.showinfo("Cita registrada",
                           f"✅ Cita agendada exitosamente!\n\n"
                           f"👤 Cliente: {cliente.nombre}\n"
                           f"📅 Fecha: {fecha}\n"
                           f"⏰ Hora: {hora}\n\n"
                           f"💇 Servicios:\n{detalle}\n\n"
                           f"💰 Total: Q{total:.2f}")
        
        abrir_nueva_ventana(v, ventana_cliente)

    # Botones finales
    tk.Button(v, text="Guardar Cita", bg="#a83279", fg="white", width=20,
              font=("Arial", 10, "bold"), command=guardar_cita).pack(pady=10)
    
    tk.Button(v, text="Volver", bg="#ffc0cb", fg="black", width=20,
              font=("Arial", 10), command=lambda: abrir_nueva_ventana(v, ventana_cliente)).pack(pady=5)

    v.mainloop()

# ==========================
# Ventana Cliente
# ==========================
def ventana_cliente():
    v = tk.Tk()
    v.title("Infinity Studio - Cliente")
    centrar_ventana(v)
    v.configure(bg="#fef6f9")

    tk.Label(v, text="Panel Cliente", font=("Georgia", 22, "bold"),
             bg="#fef6f9", fg="#a83279").pack(pady=20)

    frame = tk.Frame(v, bg="#fef6f9")
    frame.pack(pady=10)

    tk.Button(frame, text="Agendar cita", width=25, height=2, bg="#a83279", fg="white",
              font=("Arial", 11, "bold"), command=lambda: ventana_agendar_cita(v)).pack(pady=5)

    def mostrar_citas():
        nombre = simpledialog.askstring("Mis Citas", "Ingresa tu nombre:")
        if not nombre:
            return

        citas = lista_citas.buscar_por_cliente(nombre)
        if not citas:
            messagebox.showinfo("Info", "No tienes citas registradas.")
            return

        win = tk.Toplevel(v)
        win.title(f"Citas de {nombre}")
        centrar_ventana(win, 700, 400)
        win.configure(bg="#fef6f9")

        tk.Label(win, text=f"Citas de {nombre}", font=("Georgia", 18, "bold"),
                 bg="#fef6f9", fg="#a83279").pack(pady=10)

        cols = ("ID", "Fecha", "Hora", "Servicios")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=150)
        tree.pack(pady=10, padx=10, fill="both", expand=True)

        for c in citas:
            tree.insert("", "end", iid=c.id, values=(c.id, c.fecha, c.hora, ", ".join(c.servicios)))

        def cancelar_seleccion():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Selecciona una cita para cancelar.")
                return
            id_cita = selected[0]
            lista_citas.eliminar_cita(id_cita)
            tree.delete(id_cita)
            messagebox.showinfo("Éxito", "Cita cancelada correctamente.")

        tk.Button(win, text="Cancelar Cita Seleccionada", bg="#c06dbd", fg="white",
                  command=cancelar_seleccion).pack(pady=5)
        tk.Button(win, text="Cerrar", bg="#ffc0cb", fg="black",
                  command=win.destroy).pack(pady=5)

    tk.Button(frame, text="Ver / Cancelar citas", width=25, height=2, bg="#b24c9e", fg="white",
              font=("Arial", 11), command=mostrar_citas).pack(pady=5)

    tk.Button(frame, text="Volver al inicio", width=25, height=2, bg="#ffb6c1", fg="black",
              font=("Arial", 11), command=lambda: abrir_nueva_ventana(v, iniciar_interfaz)).pack(pady=5)

    v.mainloop()

# ==========================
# PANEL TRABAJADOR
# ==========================
def ventana_trabajador():
    v = tk.Tk()
    v.title("Infinity Studio - Trabajador")
    centrar_ventana(v)
    v.configure(bg="#f0f8ff")

    tk.Label(v, text="Panel Trabajador", font=("Georgia", 22, "bold"),
             bg="#f0f8ff", fg="#00688b").pack(pady=20)
    frame = tk.Frame(v, bg="#f0f8ff")
    frame.pack(pady=10)

    def registrar_servicio():
        nombre = simpledialog.askstring("Registrar Servicio", "Nombre del cliente:")
        if not nombre:
            return
        cliente = lista_clientes.busqueda_secuencial(nombre)
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado")
            return
        
        comp = generar_comprobante(cliente)
        servicios = atender_servicios_para_cliente(cliente, comp.agregar_item, genero=cliente.genero)
        if servicios:
            fname = comp.guardar_pdf()
            messagebox.showinfo("Éxito", f"Comprobante generado: {fname}")

    tk.Button(frame, text="Registrar servicio realizado", width=25, height=2, bg="#5f9ea0", fg="white",
              command=registrar_servicio).pack(pady=5)
    
    def registrar_uso_producto():
        prod = simpledialog.askstring("Uso de Producto", "Producto usado:")
        if not prod:
            return
        cantidad = simpledialog.askfloat("Uso de Producto", "Cantidad usada:")
        if not cantidad:
            return
        if inventario.registrar_salida(prod, cantidad):
            messagebox.showinfo("Éxito", "Salida registrada")
        else:
            messagebox.showerror("Error", "No se pudo registrar la salida")

    tk.Button(frame, text="Registrar uso de producto", width=25, height=2, bg="#4682b4", fg="white",
              command=registrar_uso_producto).pack(pady=5)
    
    def ver_inventario():
        win = tk.Toplevel(v)
        win.title("Inventario")
        centrar_ventana(win, 500, 300)
        text = tk.Text(win, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # Aquí deberías tener un método para obtener el inventario como string
        text.insert(tk.END, "Inventario actual:\n\n")

    tk.Button(frame, text="Ver inventario", width=25, height=2, bg="#6495ed", fg="white",
              command=ver_inventario).pack(pady=5)
    
    tk.Button(frame, text="Volver al inicio", width=25, height=2, bg="#b0e0e6", fg="black",
              command=lambda: abrir_nueva_ventana(v, iniciar_interfaz)).pack(pady=5)
    v.mainloop()

# ==========================
# PANEL JEFE
# ==========================
def ventana_jefe():
    v = tk.Tk()
    v.title("Infinity Studio - Jefe")
    centrar_ventana(v)
    v.configure(bg="#f5fff5")

    tk.Label(v, text="Panel Jefe", font=("Georgia", 22, "bold"),
             bg="#f5fff5", fg="#2e8b57").pack(pady=20)
    frame = tk.Frame(v, bg="#f5fff5")
    frame.pack(pady=10)

    def ver_inventario():
        inventario.mostrar_inventario()

    tk.Button(frame, text="Ver inventario", width=25, height=2, bg="#3cb371", fg="white",
              command=ver_inventario).pack(pady=5)
    
    def reabastecer_producto():
        prod = simpledialog.askstring("Reabastecer", "Producto:")
        if not prod:
            return
        cantidad = simpledialog.askfloat("Reabastecer", "Cantidad:")
        if not cantidad:
            return
        inventario.registrar_entrada(prod, cantidad)
        messagebox.showinfo("Éxito", "Producto reabastecido")

    tk.Button(frame, text="Reabastecer producto", width=25, height=2, bg="#2e8b57", fg="white",
              command=reabastecer_producto).pack(pady=5)
    
    def generar_reporte():
        mes = simpledialog.askstring("Reporte", "Mes (YYYY-MM):")
        if mes:
            messagebox.showinfo("Reporte", f"Reporte del mes {mes} generado")

    tk.Button(frame, text="Generar reporte mensual", width=25, height=2, bg="#006400", fg="white",
              command=generar_reporte).pack(pady=5)
    
    tk.Button(frame, text="Volver al inicio", width=25, height=2, bg="#c1ffc1", fg="black",
              command=lambda: abrir_nueva_ventana(v, iniciar_interfaz)).pack(pady=5)
    v.mainloop()

# ==========================
# LOGIN
# ==========================
def ventana_login():
    v = tk.Tk()
    v.title("Inicio de Sesión - Infinity Studio")
    centrar_ventana(v)
    v.configure(bg="#fff5f7")

    tk.Label(v, text="Iniciar Sesión", font=("Georgia", 22, "bold"),
             bg="#fff5f7", fg="#a83279").pack(pady=30)
    tk.Label(v, text="Usuario:", bg="#fff5f7").pack()
    user_entry = tk.Entry(v, width=25)
    user_entry.pack()
    tk.Label(v, text="Contraseña:", bg="#fff5f7").pack()
    pass_entry = tk.Entry(v, show="*", width=25)
    pass_entry.pack()

    def autenticar():
        user = user_entry.get().strip()
        pwd = pass_entry.get().strip()
        rol = usuarios.autenticar(user, pwd)
        if rol == "jefe":
            abrir_nueva_ventana(v, ventana_jefe)
        elif rol == "trabajador":
            abrir_nueva_ventana(v, ventana_trabajador)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(v, text="Ingresar", bg="#a83279", fg="white", width=20,
              command=autenticar).pack(pady=10)
    tk.Button(v, text="Volver", bg="#ffc0cb", width=20,
              command=lambda: abrir_nueva_ventana(v, iniciar_interfaz)).pack()
    v.mainloop()

# ==========================
# INTERFAZ PRINCIPAL
# ==========================
def iniciar_interfaz():
    root = tk.Tk()
    root.title("Infinity Studio")
    root.configure(bg="white")
    centrar_ventana(root, 800, 600)

    try:
        logo = PhotoImage(file="logoempresa.png")
        logo = logo.subsample(2, 2)
        tk.Label(root, image=logo, bg="white").pack(pady=10)
        root.logo = logo
    except:
        tk.Label(root, text="[Logo Infinity Studio]", bg="white", fg="#a83279", 
                 font=("Georgia", 16, "bold")).pack(pady=10)

    tk.Label(root, text="INFINITY STUDIO M", font=("Georgia", 28, "bold"),
             fg="#a83279", bg="white").pack(pady=10)
    tk.Label(root, text="Salón Nails y Barber Shop", font=("Georgia", 16, "italic"),
             fg="#0099cc", bg="white").pack()

    frame = tk.Frame(root, bg="white")
    frame.pack(pady=40)
    
    tk.Button(frame, text="Cliente", width=20, height=2, bg="#ba55d3", fg="white",
              font=("Arial", 12, "bold"), command=lambda: abrir_nueva_ventana(root, ventana_cliente)).pack(pady=10)
    tk.Button(frame, text="Trabajador", width=20, height=2, bg="#9370db", fg="white",
              font=("Arial", 12, "bold"), command=lambda: abrir_nueva_ventana(root, ventana_login)).pack(pady=10)
    tk.Button(frame, text="Jefe", width=20, height=2, bg="#8a2be2", fg="white",
              font=("Arial", 12, "bold"), command=lambda: abrir_nueva_ventana(root, ventana_login)).pack(pady=10)
    tk.Button(frame, text="Salir", width=20, height=2, bg="#dda0dd", fg="black",
              font=("Arial", 12), command=root.destroy).pack(pady=10)
    
    root.mainloop()

