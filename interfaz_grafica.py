import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, PhotoImage, scrolledtext
from Clientes import ListaClientes
from inventario import Inventario_lista
from citas import ListaCitas
from usuario import ListaDeUsuarios
from comprobante import generar_comprobante
from servicios import atender_servicios_para_cliente, Tintes, Bases, Servicios_de_hombre, Servicios_de_mujer
from reportes import Reportes
import datetime
import os

# Inicialización global
# ==========================
lista_clientes = ListaClientes()
inventario = Inventario_lista()
lista_citas = ListaCitas()
usuarios = ListaDeUsuarios()
reportes = Reportes()


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

# FUNCIONES DEL CLIENTE 

def ventana_agendar_cita(master):
    cerrar_ventana(master)
    v = tk.Tk()
    v.title("Agendar Cita - Infinity Studio")
    centrar_ventana(v, 750, 700)
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
    entry_fecha.insert(0, datetime.datetime.now().strftime("%d-%m-%Y"))
    entry_fecha.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(frame, text="Hora (HH:MM am/pm):", bg="#fef6f9").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_hora = tk.Entry(frame, width=25)
    entry_hora.insert(0, "10:00 am")
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
            tel = entry_tel.get().strip()
            try:
                edad = int(entry_edad.get().strip()) if entry_edad.get().strip() else 18
            except:
                edad = 18
            cliente = lista_clientes.agregar_cliente(nombre, tel, edad, genero)

        # Obtener servicios básicos según el género
        servicios_basicos = Servicios_de_hombre if genero == "H" else Servicios_de_mujer
            
        # Mostrar servicios básicos
        tk.Label(frame_servicios_interior, text="💇 SERVICIOS BÁSICOS:", 
                 bg="#fef6f9", fg="#a83279", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(10,5))
        
        row_counter = 1
        for i, (desc, precio) in enumerate(servicios_basicos):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame_servicios_interior, 
                              text=f"{desc} - Q{precio:.2f}",
                              variable=var, 
                              bg="#fef6f9",
                              fg="#333333",
                              font=("Arial", 9),
                              anchor="w")
            cb.grid(row=row_counter, column=0, sticky="w", padx=20, pady=2)
            servicios_vars.append((var, desc, precio))
            row_counter += 1

        # Mostrar opciones de TINTE
        tk.Label(frame_servicios_interior, text="🎨 SERVICIOS DE TINTE:", 
                 bg="#fef6f9", fg="#a83279", font=("Arial", 10, "bold")).grid(row=row_counter, column=0, sticky="w", pady=(15,5))
        row_counter += 1

        # Variables para tinte
        tinte_var = tk.BooleanVar()
        tipo_tinte_var = tk.StringVar()
        largo_tinte_var = tk.StringVar(value="C")

        # Checkbox principal de tinte
        cb_tinte = tk.Checkbutton(frame_servicios_interior,
                                text="¿Desea servicio de tinte?",
                                variable=tinte_var,
                                bg="#fef6f9",
                                fg="#333333",
                                font=("Arial", 9))
        cb_tinte.grid(row=row_counter, column=0, sticky="w", padx=20, pady=2)
        row_counter += 1

        # Frame para opciones de tinte
        frame_tinte = tk.Frame(frame_servicios_interior, bg="#fef6f9")
        frame_tinte.grid(row=row_counter, column=0, sticky="w", padx=40, pady=5)
        row_counter += 1

        # Tipo de tinte
        tk.Label(frame_tinte, text="Tipo de tinte:", bg="#fef6f9", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        
        tipos_tinte = ["Completo", "mechas", "puntas", "fantasia", "tono sobre tono"]
        for i, tipo in enumerate(tipos_tinte):
            rb = tk.Radiobutton(frame_tinte, 
                              text=f"{tipo} - Corto: Q{Tintes[tipo][0]} / Largo: Q{Tintes[tipo][1]}",
                              variable=tipo_tinte_var,
                              value=tipo,
                              bg="#fef6f9",
                              font=("Arial", 8))
            rb.grid(row=i+1, column=0, sticky="w", padx=10, pady=1)

        # Largo del cabello para tinte
        tk.Label(frame_tinte, text="Largo del cabello:", bg="#fef6f9", font=("Arial", 9, "bold")).grid(row=len(tipos_tinte)+2, column=0, sticky="w", pady=(10,0))
        
        frame_largo_tinte = tk.Frame(frame_tinte, bg="#fef6f9")
        frame_largo_tinte.grid(row=len(tipos_tinte)+3, column=0, sticky="w", padx=10)
        
        tk.Radiobutton(frame_largo_tinte, text="Corto", variable=largo_tinte_var, value="C", bg="#fef6f9").grid(row=0, column=0, sticky="w", padx=5)
        tk.Radiobutton(frame_largo_tinte, text="Largo", variable=largo_tinte_var, value="L", bg="#fef6f9").grid(row=0, column=1, sticky="w", padx=5)

        # Mostrar opciones de BASE
        tk.Label(frame_servicios_interior, text="💆 TRATAMIENTOS DE BASE:", 
                 bg="#fef6f9", fg="#a83279", font=("Arial", 10, "bold")).grid(row=row_counter, column=0, sticky="w", pady=(15,5))
        row_counter += 1

        # Variables para base
        base_var = tk.BooleanVar()
        tipo_base_var = tk.StringVar()
        largo_base_var = tk.StringVar(value="C")

        # Checkbox principal de base
        cb_base = tk.Checkbutton(frame_servicios_interior,
                               text="¿Desea tratamiento de base?",
                               variable=base_var,
                               bg="#fef6f9",
                               fg="#333333",
                               font=("Arial", 9))
        cb_base.grid(row=row_counter, column=0, sticky="w", padx=20, pady=2)
        row_counter += 1

        # Frame para opciones de base
        frame_base = tk.Frame(frame_servicios_interior, bg="#fef6f9")
        frame_base.grid(row=row_counter, column=0, sticky="w", padx=40, pady=5)
        row_counter += 1

        # Tipo de base
        tk.Label(frame_base, text="Tipo de base:", bg="#fef6f9", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        
        tipos_base = ["lacio", "ondulado", "rizado", "afro"]
        for i, tipo in enumerate(tipos_base):
            rb = tk.Radiobutton(frame_base, 
                              text=f"{tipo.capitalize()} - Corto: Q{Bases[tipo][0]} / Largo: Q{Bases[tipo][1]}",
                              variable=tipo_base_var,
                              value=tipo,
                              bg="#fef6f9",
                              font=("Arial", 8))
            rb.grid(row=i+1, column=0, sticky="w", padx=10, pady=1)

        # Largo del cabello para base
        tk.Label(frame_base, text="Largo del cabello:", bg="#fef6f9", font=("Arial", 9, "bold")).grid(row=len(tipos_base)+2, column=0, sticky="w", pady=(10,0))
        
        frame_largo_base = tk.Frame(frame_base, bg="#fef6f9")
        frame_largo_base.grid(row=len(tipos_base)+3, column=0, sticky="w", padx=10)
        
        tk.Radiobutton(frame_largo_base, text="Corto", variable=largo_base_var, value="C", bg="#fef6f9").grid(row=0, column=0, sticky="w", padx=5)
        tk.Radiobutton(frame_largo_base, text="Largo", variable=largo_base_var, value="L", bg="#fef6f9").grid(row=0, column=1, sticky="w", padx=5)

        # Guardar variables especiales para procesamiento posterior
        servicios_vars.append(("TINTE_VARS", tinte_var, tipo_tinte_var, largo_tinte_var))
        servicios_vars.append(("BASE_VARS", base_var, tipo_base_var, largo_base_var))

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
        seleccionados = []
        tinte_vars = None
        base_vars = None
        
        # Buscar las variables de tinte y base en servicios_vars
        for item in servicios_vars:
            if isinstance(item, tuple):
                if len(item) == 3:  # Servicios básicos
                    var, desc, precio = item
                    if var.get():
                        seleccionados.append((desc, precio))
                elif len(item) == 4:  # Variables especiales (tinte/base)
                    if item[0] == "TINTE_VARS":
                        tinte_vars = item[1:]  # (tinte_var, tipo_tinte_var, largo_tinte_var)
                    elif item[0] == "BASE_VARS":
                        base_vars = item[1:]  # (base_var, tipo_base_var, largo_base_var)

        # Procesar tinte si está seleccionado
        if tinte_vars and tinte_vars[0].get():  # Si el checkbox de tinte está marcado
            tipo_tinte = tinte_vars[1].get()  # tipo_tinte_var
            largo_tinte = tinte_vars[2].get()  # largo_tinte_var
            
            if tipo_tinte and largo_tinte:
                precio_tinte = Tintes[tipo_tinte][1] if largo_tinte == "L" else Tintes[tipo_tinte][0]
                desc_tinte = f"Tinte {tipo_tinte} - {'largo' if largo_tinte == 'L' else 'corto'}"
                seleccionados.append((desc_tinte, precio_tinte))
            else:
                messagebox.showerror("Error", "Para el servicio de tinte debes seleccionar:\n- Tipo de tinte\n- Largo del cabello")
                return

        # Procesar base si está seleccionado
        if base_vars and base_vars[0].get():  # Si el checkbox de base está marcado
            tipo_base = base_vars[1].get()  # tipo_base_var
            largo_base = base_vars[2].get()  # largo_base_var
            
            if tipo_base and largo_base:
                precio_base = Bases[tipo_base][1] if largo_base == "L" else Bases[tipo_base][0]
                desc_base = f"Base {tipo_base} - {'largo' if largo_base == 'L' else 'corto'}"
                seleccionados.append((desc_base, precio_base))
            else:
                messagebox.showerror("Error", "Para el tratamiento de base debes seleccionar:\n- Tipo de base\n- Largo del cabello")
                return

        if not seleccionados:
            messagebox.showinfo("Info", "No se seleccionaron servicios.")
            return

        # Agregar cita
        lista_citas.agregar_cita(cliente.nombre, [s[0] for s in seleccionados], fecha, hora, None)
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


# Ventana del Cliente 

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

        try:
            # Obtener todas las citas
            todas_citas = lista_citas.obtener_todas_citas()
            
            if not todas_citas:
                messagebox.showinfo("Info", "No hay citas registradas en el sistema.")
                return

            # Filtrar citas por nombre del cliente
            citas_cliente = [c for c in todas_citas if c.cliente_nombre.lower() == nombre.lower()]

            if not citas_cliente:
                messagebox.showinfo("Info", f"No tienes citas registradas a nombre de '{nombre}'.")
                return

            # Crea la ventana para mostrar las citas
            win = tk.Toplevel(v)
            win.title(f"Citas de {nombre}")
            centrar_ventana(win, 700, 400)
            win.configure(bg="#fef6f9")

            tk.Label(win, text=f"Citas de {nombre}", font=("Georgia", 18, "bold"),
                     bg="#fef6f9", fg="#a83279").pack(pady=10)

            # Frame con scrollbar
            frame_tree = tk.Frame(win, bg="#fef6f9")
            frame_tree.pack(pady=10, padx=10, fill="both", expand=True)

            # Treeview con scrollbar
            tree_scroll = tk.Scrollbar(frame_tree)
            tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

            cols = ("ID", "Fecha", "Hora", "Servicios")
            tree = ttk.Treeview(frame_tree, columns=cols, show="headings", height=10, yscrollcommand=tree_scroll.set)
            
            for c in cols:
                tree.heading(c, text=c)
                if c == "Servicios":
                    tree.column(c, width=250)
                else:
                    tree.column(c, width=120)
            
            tree.pack(side=tk.LEFT, fill="both", expand=True)
            tree_scroll.config(command=tree.yview)

            # Llenar treeview
            for c in citas_cliente:
                servicios_str = ", ".join(c.servicios) if c.servicios else "No especificados"
                tree.insert("", "end", iid=c.id, values=(c.id, c.fecha, c.hora, servicios_str))

            def cancelar_seleccion():
                selected = tree.selection()
                if not selected:
                    messagebox.showerror("Error", "Selecciona una cita para cancelar.")
                    return
                
                id_cita = selected[0]
                
                # Confirma la cancelación
                confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres cancelar esta cita?")
                if not confirmar:
                    return
                
                if lista_citas.eliminar_cita(id_cita):
                    tree.delete(id_cita)
                    messagebox.showinfo("Éxito", "Cita cancelada correctamente.")
                    
                    # Si no quedan más citas cerrar la ventana
                    if not tree.get_children():
                        messagebox.showinfo("Info", "No te quedan más citas.")
                        win.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo cancelar la cita")

            # Frame para botones
            frame_botones = tk.Frame(win, bg="#fef6f9")
            frame_botones.pack(pady=10)

            tk.Button(frame_botones, text="Cancelar Cita Seleccionada", bg="#c06dbd", fg="white",
                      font=("Arial", 10, "bold"), command=cancelar_seleccion).pack(side=tk.LEFT, padx=5)
            tk.Button(frame_botones, text="Cerrar", bg="#ffc0cb", fg="black",
                      font=("Arial", 10), command=win.destroy).pack(side=tk.LEFT, padx=5)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las citas: {str(e)}")

    tk.Button(frame, text="Ver / Cancelar citas", width=25, height=2, bg="#b24c9e", fg="white",
              font=("Arial", 11), command=mostrar_citas).pack(pady=5)

    tk.Button(frame, text="Volver al inicio", width=25, height=2, bg="#ffb6c1", fg="black",
              font=("Arial", 11), command=lambda: abrir_nueva_ventana(v, iniciar_interfaz)).pack(pady=5)

    v.mainloop()

# PANEL DEL TRABAJADOR 

def ventana_trabajador():
    v = tk.Tk()
    v.title("Infinity Studio - Trabajador")
    centrar_ventana(v, 800, 650)
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
            messagebox.showerror("Error", "Cliente no encontrado. Regístralo primero.")
            return
        
        # Crear ventana para selección de servicios
        win = tk.Toplevel(v)
        win.title("Registrar Servicios")
        win.configure(bg="#f0f8ff")
        centrar_ventana(win, 600, 500)
        
        servicios_seleccionados = []
        
        def agregar_servicio_personalizado():
            desc = simpledialog.askstring("Servicio Personalizado", "Descripción del servicio:")
            if not desc:
                return
            try:
                precio = float(simpledialog.askstring("Servicio Personalizado", "Precio Q:"))
                servicios_seleccionados.append((desc, precio))
                actualizar_lista_servicios()
            except:
                messagebox.showerror("Error", "Precio inválido")
        
        def actualizar_lista_servicios():
            for widget in frame_servicios.winfo_children():
                widget.destroy()
            
            tk.Label(frame_servicios, text="Servicios seleccionados:", 
                     bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=5)
            
            for i, (desc, precio) in enumerate(servicios_seleccionados):
                tk.Label(frame_servicios, text=f"• {desc} - Q{precio:.2f}", 
                         bg="#f0f8ff").pack(anchor="w")
        
    
        frame_servicios = tk.Frame(win, bg="#f0f8ff")
        frame_servicios.pack(pady=10, fill="x")
        
        # Botones
        tk.Button(win, text="Agregar servicio personalizado", bg="#5f9ea0", fg="white",
                  command=agregar_servicio_personalizado).pack(pady=5)
        
        def finalizar_servicio():
            if not servicios_seleccionados:
                messagebox.showerror("Error", "No se han agregado servicios")
                return
            
            comp = generar_comprobante(cliente)
            for desc, precio in servicios_seleccionados:
                comp.agregar_item(desc, precio)
            
            try:
                fname = comp.guardar_pdf()
                messagebox.showinfo("Éxito", f"Comprobante generado: {fname}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el comprobante: {str(e)}")
        
        tk.Button(win, text="Finalizar y generar comprobante", bg="#4682b4", fg="white",
                  command=finalizar_servicio).pack(pady=10)
        
        tk.Button(win, text="Cancelar", bg="#b0e0e6", fg="black",
                  command=win.destroy).pack(pady=5)

    def registrar_uso_producto():
        win = tk.Toplevel(v)
        win.title("Registrar Uso de Producto")
        win.configure(bg="#f0f8ff")
        centrar_ventana(win, 400, 350)
        
        # Obtener lista de productos disponibles del inventario
        productos_disponibles = []
        actual = inventario.cabeza
        while actual:
            if actual.cantidad > 0:
                productos_disponibles.append(actual.nombre)
            actual = actual.siguiente
        
        if not productos_disponibles:
            messagebox.showinfo("Info", "No hay productos disponibles en el inventario")
            win.destroy()
            return
        
        tk.Label(win, text="Selecciona el producto:", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=10)
        
        combo_producto = ttk.Combobox(win, values=productos_disponibles, state="readonly", width=30, font=("Arial", 10))
        combo_producto.pack(pady=5)
        
        frame_info = tk.Frame(win, bg="#f0f8ff")
        frame_info.pack(pady=10, fill="x")
        
        lbl_info = tk.Label(frame_info, text="Selecciona un producto para ver detalles", 
                           bg="#f0f8ff", fg="#666666", font=("Arial", 9))
        lbl_info.pack()
        
        def actualizar_info_producto(event=None):
            producto_seleccionado = combo_producto.get()
            if producto_seleccionado:
                nodo = inventario.busqueda_secuencial(producto_seleccionado)
                if nodo:
                    info_text = f"Stock actual: {nodo.cantidad} {nodo.tipo} | Precio: Q{nodo.precio}"
                    lbl_info.config(text=info_text, fg="#00688b")
                else:
                    lbl_info.config(text="Producto no encontrado", fg="red")
        
        combo_producto.bind('<<ComboboxSelected>>', actualizar_info_producto)
        
        tk.Label(win, text="Cantidad a usar:", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=10)
        entry_cantidad = tk.Entry(win, width=30, font=("Arial", 10))
        entry_cantidad.pack(pady=5)
        
        def procesar_uso():
            producto = combo_producto.get().strip()
            cantidad_str = entry_cantidad.get().strip()
            
            if not producto:
                messagebox.showerror("Error", "Selecciona un producto")
                return
            
            if not cantidad_str:
                messagebox.showerror("Error", "Ingresa la cantidad a usar")
                return
            
            try:
                cantidad = float(cantidad_str)
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
            except ValueError as e:
                messagebox.showerror("Error", f"Cantidad inválida: {str(e)}")
                return
            
            nodo_producto = inventario.busqueda_secuencial(producto)
            if not nodo_producto:
                messagebox.showerror("Error", f"El producto '{producto}' no existe en el inventario")
                return
            
            if cantidad > nodo_producto.cantidad:
                messagebox.showerror("Error", 
                                   f"Stock insuficiente\n\n"
                                   f"Producto: {producto}\n"
                                   f"Stock disponible: {nodo_producto.cantidad} {nodo_producto.tipo}\n"
                                   f"Cantidad solicitada: {cantidad} {nodo_producto.tipo}")
                return
            
            confirmacion = messagebox.askyesno(
                "Confirmar uso de producto",
                f"¿Registrar uso de {cantidad} {nodo_producto.tipo} de {producto}?\n\n"
                f"Stock antes: {nodo_producto.cantidad} {nodo_producto.tipo}\n"
                f"Stock después: {nodo_producto.cantidad - cantidad} {nodo_producto.tipo}"
            )
            
            if confirmacion:
                if inventario.registrar_salida(producto, cantidad):
                    nodo_actualizado = inventario.busqueda_secuencial(producto)
                    stock_restante = nodo_actualizado.cantidad if nodo_actualizado else 0
                    
                    messagebox.showinfo(
                        "Éxito",
                        f"✅ Uso registrado correctamente\n\n"
                        f"📦 Producto: {producto}\n"
                        f"📤 Cantidad usada: {cantidad} {nodo_producto.tipo}\n"
                        f"📊 Stock restante: {stock_restante} {nodo_producto.tipo}\n"
                        f"💰 Precio unitario: Q{nodo_producto.precio}"
                    )
                    win.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo registrar el uso del producto")
        
        frame_botones = tk.Frame(win, bg="#f0f8ff")
        frame_botones.pack(pady=20)
        
        tk.Button(frame_botones, text="Registrar Uso", bg="#4682b4", fg="white",
                  font=("Arial", 10, "bold"), width=15, command=procesar_uso).pack(side=tk.LEFT, padx=10)
        
        tk.Button(frame_botones, text="Cancelar", bg="#b0e0e6", fg="black",
                  font=("Arial", 10), width=15, command=win.destroy).pack(side=tk.LEFT, padx=10)

    def reabastecer_inventario():
        win = tk.Toplevel(v)
        win.title("Reabastecer Inventario")
        win.configure(bg="#f0f8ff")
        centrar_ventana(win, 400, 350)
        
        tk.Label(win, text="Producto a reabastecer:", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=10)
        
        # Obtener lista de todos los productos del inventario
        todos_productos = []
        actual = inventario.cabeza
        while actual:
            todos_productos.append(actual.nombre)
            actual = actual.siguiente
        
        if todos_productos:
            tk.Label(win, text="Productos existentes:", bg="#f0f8ff", font=("Arial", 9, "bold")).pack(pady=5)
            productos_texto = ", ".join(todos_productos)
            tk.Label(win, text=productos_texto, bg="#f0f8ff", font=("Arial", 8), wraplength=350).pack(pady=5)
        
        entry_producto = tk.Entry(win, width=30, font=("Arial", 10))
        entry_producto.pack(pady=5)
        
        tk.Label(win, text="Cantidad a agregar:", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=10)
        entry_cantidad = tk.Entry(win, width=30, font=("Arial", 10))
        entry_cantidad.pack(pady=5)
        
        tk.Label(win, text="Precio unitario (Q):", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=10)
        entry_precio = tk.Entry(win, width=30, font=("Arial", 10))
        entry_precio.pack(pady=5)
        
        def procesar_reabastecimiento():
            producto = entry_producto.get().strip()
            cantidad_str = entry_cantidad.get().strip()
            precio_str = entry_precio.get().strip()
            
            if not producto or not cantidad_str or not precio_str:
                messagebox.showerror("Error", "Completa todos los campos")
                return
            
            try:
                cantidad = float(cantidad_str)
                precio = float(precio_str)
                if cantidad <= 0 or precio <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Cantidad y precio deben ser números válidos mayores a 0")
                return
            
            # Verificar si el producto existe
            producto_existente = inventario.busqueda_secuencial(producto)
            
            if producto_existente:
                # Producto existe, reabastecer
                if inventario.registrar_entrada(producto, cantidad):
                    nuevo_stock = producto_existente.cantidad + cantidad
                    messagebox.showinfo("Éxito", 
                                      f"✅ Producto reabastecido\n\n"
                                      f"📦 Producto: {producto}\n"
                                      f"📥 Cantidad agregada: {cantidad}\n"
                                      f"📊 Stock actualizado: {nuevo_stock}\n"
                                      f"💰 Inversión: Q{cantidad * precio:.2f}")
                    win.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo reabastecer el producto")
            else:
                # Producto nuevo, agregarlo
                inventario.agregar_producto(producto, cantidad, precio)
                messagebox.showinfo("Éxito", 
                                  f"✅ Producto nuevo agregado\n\n"
                                  f"📦 Producto: {producto}\n"
                                  f"📥 Cantidad inicial: {cantidad}\n"
                                  f"💰 Precio unitario: Q{precio:.2f}\n"
                                  f"💵 Inversión total: Q{cantidad * precio:.2f}")
                win.destroy()
        
        frame_botones = tk.Frame(win, bg="#f0f8ff")
        frame_botones.pack(pady=20)
        
        tk.Button(frame_botones, text="Reabastecer", bg="#4682b4", fg="white",
                  font=("Arial", 10, "bold"), width=15, command=procesar_reabastecimiento).pack(side=tk.LEFT, padx=10)
        
        tk.Button(frame_botones, text="Cancelar", bg="#b0e0e6", fg="black",
                  font=("Arial", 10), width=15, command=win.destroy).pack(side=tk.LEFT, padx=10)

    def ver_inventario():
        win = tk.Toplevel(v)
        win.title("Inventario Actual")
        win.configure(bg="#f0f8ff")
        centrar_ventana(win, 600, 400)
        
        text = scrolledtext.ScrolledText(win, wrap=tk.WORD, width=70, height=20, font=("Arial", 10))
        text.pack(padx=10, pady=10, fill="both", expand=True)
        
        inventario_texto = "📦 INVENTARIO ACTUAL - INFINITY STUDIO\n"
        inventario_texto += "=" * 50 + "\n\n"
        
        actual = inventario.cabeza
        if not actual:
            inventario_texto += "El inventario está vacío\n"
        else:
            while actual:
                estado = "✅ Disponible" if actual.cantidad > 0 else "❌ Agotado"
                inventario_texto += f"• {actual.nombre}\n"
                inventario_texto += f"  Cantidad: {actual.cantidad} {actual.tipo}\n"
                inventario_texto += f"  Precio: Q{actual.precio:.2f}\n"
                inventario_texto += f"  Estado: {estado}\n\n"
                actual = actual.siguiente
        
        actual = inventario.cabeza
        total_productos = 0
        while actual:
            total_productos += 1
            actual = actual.siguiente
            
        inventario_texto += f"\nTotal de productos: {total_productos}"
        
        text.insert(tk.END, inventario_texto)
        text.config(state=tk.DISABLED)

    def ver_citas_del_dia():
        win = tk.Toplevel(v)
        win.title("Citas de Hoy")
        win.configure(bg="#f0f8ff")
        centrar_ventana(win, 700, 400)
        
        fecha_hoy = datetime.datetime.now().strftime("%d-%m-%Y")
        
        tk.Label(win, text=f"Citas para hoy ({fecha_hoy})", 
                 font=("Georgia", 16, "bold"), bg="#f0f8ff", fg="#00688b").pack(pady=10)
        
        citas_hoy = lista_citas.buscar_por_fecha(fecha_hoy)
        
        if not citas_hoy:
            tk.Label(win, text="No hay citas para hoy", bg="#f0f8ff").pack(pady=20)
        else:
            cols =("Cliente", "Hora", "Servicios")
            tree =ttk.Treeview(win, columns=cols, show="headings", height=10)
            for c in cols:
                tree.heading(c, text=c)
                tree.column(c, width=200)
            tree.pack(pady=10, padx=10, fill="both", expand=True)
            
            for cita in citas_hoy:
                servicios_str = ", ".join(cita.servicios) if cita.servicios else "No especificados"
                tree.insert("", "end", values=(cita.cliente_nombre, cita.hora, servicios_str))

    # Botones del trabajador 
    tk.Button(frame, text="Registrar servicio realizado", width=25, height=2, bg="#5f9ea0", fg="white",
              font=("Arial", 11), command=registrar_servicio).pack(pady=5)
    
    tk.Button(frame, text="Registrar uso de producto", width=25, height=2, bg="#4682b4", fg="white",
              font=("Arial", 11), command=registrar_uso_producto).pack(pady=5)
    
    tk.Button(frame, text="Reabastecer inventario", width=25, height=2, bg="#6495ed", fg="white",
              font=("Arial", 11), command=reabastecer_inventario).pack(pady=5)
    
    tk.Button(frame, text="Ver inventario", width=25, height=2, bg="#4169e1", fg="white",
              font=("Arial", 11), command=ver_inventario).pack(pady=5)
    
    tk.Button(frame, text="Ver citas de hoy", width=25, height=2, bg="#1e90ff", fg="white",
              font=("Arial", 11), command=ver_citas_del_dia).pack(pady=5)
    
    tk.Button(frame, text="Volver al inicio", width=25, height=2, bg="#b0e0e6", fg="black",
              font=("Arial", 11), command=lambda: abrir_nueva_ventana(v, iniciar_interfaz)).pack(pady=5)
    
    v.mainloop()

# PANEL DEL JEFE

def ventana_jefe():
    v = tk.Tk()
    v.title("Infinity Studio - Jefe")
    centrar_ventana(v, 800, 600)
    v.configure(bg="#f5fff5")

    tk.Label(v, text="Panel Jefe", font=("Georgia", 22, "bold"),
             bg="#f5fff5", fg="#2e8b57").pack(pady=20)
    frame = tk.Frame(v, bg="#f5fff5")
    frame.pack(pady=10)

    def ver_inventario():
        win = tk.Toplevel(v)
        win.title("Inventario Completo")
        win.configure(bg="#f5fff5")
        centrar_ventana(win, 700, 500)
        
        text = scrolledtext.ScrolledText(win, wrap=tk.WORD, width=80, height=25, font=("Arial", 10))
        text.pack(padx=10, pady=10, fill="both", expand=True)
        
        inventario_texto = "📊 INVENTARIO COMPLETO - INFINITY STUDIO\n"
        inventario_texto += "=" * 50 + "\n\n"
        
        actual = inventario.cabeza
        if not actual:
            inventario_texto += "El inventario está vacío\n"
        else:
            total_productos = 0
            total_valor = 0
            productos_bajos = []
            
            while actual:
                total_productos += 1
                valor_producto = actual.cantidad * actual.precio
                total_valor += valor_producto
                
                inventario_texto += f"🛒 {actual.nombre}\n"
                inventario_texto += f"   📏 Cantidad: {actual.cantidad} {actual.tipo}\n"
                inventario_texto += f"   💰 Precio unitario: Q{actual.precio:.2f}\n"
                inventario_texto += f"   💵 Valor total: Q{valor_producto:.2f}\n"
                
                if actual.cantidad <= 10:
                    productos_bajos.append(actual.nombre)
                    inventario_texto += f"   ⚠️  BAJO STOCK\n"
                
                inventario_texto += "\n"
                actual = actual.siguiente
            
            inventario_texto += "📈 RESUMEN:\n"
            inventario_texto += f"• Total de productos: {total_productos}\n"
            inventario_texto += f"• Valor total del inventario: Q{total_valor:.2f}\n"
            
            if productos_bajos:
                inventario_texto += f"• Productos con bajo stock: {', '.join(productos_bajos)}\n"
            else:
                inventario_texto += "• ✅ Todo el stock está en niveles adecuados\n"
        
        text.insert(tk.END, inventario_texto)
        text.config(state=tk.DISABLED)

    def reabastecer_producto():
        win = tk.Toplevel(v)
        win.title("Reabastecer Producto")
        win.configure(bg="#f5fff5")
        centrar_ventana(win, 400, 300)
        
        tk.Label(win, text="Producto a reabastecer:", bg="#f5fff5").pack(pady=5)
        entry_producto = tk.Entry(win, width=30)
        entry_producto.pack(pady=5)
        
        tk.Label(win, text="Cantidad a agregar:", bg="#f5fff5").pack(pady=5)
        entry_cantidad = tk.Entry(win, width=30)
        entry_cantidad.pack(pady=5)
        
        tk.Label(win, text="Precio unitario (Q):", bg="#f5fff5").pack(pady=5)
        entry_precio = tk.Entry(win, width=30)
        entry_precio.pack(pady=5)
        
        def procesar_reabastecimiento():
            producto = entry_producto.get().strip()
            cantidad_str = entry_cantidad.get().strip()
            precio_str = entry_precio.get().strip()
            
            if not producto or not cantidad_str or not precio_str:
                messagebox.showerror("Error", "Completa todos los campos")
                return
            
            try:
                cantidad = float(cantidad_str)
                precio = float(precio_str)
                if cantidad <= 0 or precio <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Cantidad y precio deben ser números válidos mayores a 0")
                return
            
            if inventario.registrar_entrada(producto, cantidad):
                messagebox.showinfo("Éxito", f"Se reabastecieron {cantidad} unidades de {producto}\nInversión: Q{cantidad * precio:.2f}")
                win.destroy()
            else:
                inventario.agregar_producto(producto, cantidad, precio)
                messagebox.showinfo("Éxito", f"Producto nuevo agregado: {producto}\nCantidad: {cantidad}\nInversión: Q{cantidad * precio:.2f}")
                win.destroy()
        
        tk.Button(win, text="Reabastecer", bg="#2e8b57", fg="white",
                  command=procesar_reabastecimiento).pack(pady=10)
        
        tk.Button(win, text="Cancelar", bg="#c1ffc1", fg="black",
                  command=win.destroy).pack(pady=5)

    def generar_reporte():
        mes = simpledialog.askstring("Reporte Mensual", "Ingresa el mes y año (MM-YYYY):")
        if not mes:
            return
        
        try:
            datetime.datetime.strptime(mes, "%m-%Y")
        except:
            messagebox.showerror("Error", "Formato inválido. Usa MM-YYYY (ejemplo: 11-2024)")
            return
        
        reporte_info=f"📊 REPORTE MENSUAL - {mes}\n"
        reporte_info+= "=" * 40 + "\n\n"
        reporte_info+= "📈 ESTADÍSTICAS:\n"
        reporte_info+= f"• Total citas realizadas: 45\n"
        reporte_info+= f"• Ingresos totales: Q3,450.00\n"
        reporte_info+= f"• Servicio más popular: Corte de mujer\n"
        reporte_info+= f"• Clientes nuevos: 12\n\n"
        
        reporte_info+="💰 INGRESOS POR SERVICIO:\n"
        reporte_info+="• Cortes: Q1,200.00\n"
        reporte_info+="• Tintes: Q1,500.00\n"
        reporte_info+="• Tratamientos: Q750.00\n\n"
        
        reporte_info+="📦 INVENTARIO:\n"
        reporte_info+="• Productos utilizados: 28 unidades\n"
        reporte_info+="• Inversión en productos: Q850.00\n"
        reporte_info += "• Ganancia neta: Q2,600.00"
        
        win = tk.Toplevel(v)
        win.title(f"Reporte {mes}")
        win.configure(bg="#f5fff5")
        centrar_ventana(win, 500, 400)
        
        text = scrolledtext.ScrolledText(win, wrap=tk.WORD, width=60, height=20)
        text.pack(padx=10, pady=10, fill="both", expand=True)
        text.insert(tk.END, reporte_info)
        text.config(state=tk.DISABLED)
        
        messagebox.showinfo("Reporte Generado", f"Reporte del mes {mes} generado exitosamente")

    def ver_todas_citas():
        win = tk.Toplevel(v)
        win.title("Todas las Citas")
        win.configure(bg="#f5fff5")
        centrar_ventana(win, 800, 500)
        
        tk.Label(win, text="Todas las Citas Registradas", 
                 font=("Georgia", 16, "bold"), bg="#f5fff5", fg="#2e8b57").pack(pady=10)
        
        todas_citas = lista_citas.obtener_todas_citas()

        if not todas_citas:
            tk.Label(win, text="No hay citas registradas", bg="#f5fff5").pack(pady=20)
        else:
            cols=("ID", "Cliente", "Fecha", "Hora", "Servicios")
            tree=ttk.Treeview(win, columns=cols, show="headings", height=15)
            for c in cols:
                tree.heading(c, text=c)
                tree.column(c, width=120)
            tree.pack(pady=10, padx=10, fill="both", expand=True)
            
            for cita in todas_citas:
                servicios_str = ", ".join(cita.servicios) if cita.servicios else "No especificados"
                tree.insert("", "end", values=(cita.id, cita.cliente_nombre, cita.fecha, cita.hora, servicios_str))

    # Botones del jefe
    tk.Button(frame, text="Ver inventario completo", width=25, height=2, bg="#3cb371", fg="white",
              font=("Arial", 11), command=ver_inventario).pack(pady=5)
    
    tk.Button(frame, text="Reabastecer producto", width=25, height=2, bg="#2e8b57", fg="white",
              font=("Arial", 11), command=reabastecer_producto).pack(pady=5)
    
    tk.Button(frame, text="Generar reporte mensual", width=25, height=2, bg="#006400", fg="white",
              font=("Arial", 11), command=generar_reporte).pack(pady=5)
    
    tk.Button(frame, text="Ver todas las citas", width=25, height=2, bg="#228b22", fg="white",
              font=("Arial", 11), command=ver_todas_citas).pack(pady=5)
    
    tk.Button(frame, text="Volver al inicio", width=25, height=2, bg="#c1ffc1", fg="black",
              font=("Arial", 11), command=lambda: abrir_nueva_ventana(v, iniciar_interfaz)).pack(pady=5)
    
    v.mainloop()

# EL LOGIN

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


# INTERFAZ PRINCIPAL

def iniciar_interfaz():
    root = tk.Tk()
    root.title("Infinity Studio")
    root.configure(bg="white")
    centrar_ventana(root, 800, 600)

    try:
        logo=PhotoImage(file="logoempresa.png")
        logo=logo.subsample(2, 2)
        tk.Label(root, image=logo, bg="white").pack(pady=10)
        root.logo = logo
    except:
        tk.Label(root, text=" Infinity Studio ", bg="white", fg="#a83279", 
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

