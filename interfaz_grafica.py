# interfaz_grafica.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from usuario import ListaDeUsuarios
from Clientes import ListaClientes
from citas import ListaCitas
from inventario import Inventario_lista
from comprobante import generar_comprobante
import reportes
import datetime

# ================== INSTANCIAS ==================
usuarios = ListaDeUsuarios()
clientes = ListaClientes()
citas = ListaCitas()
inventario = Inventario_lista()

# ------------------ UTIL ------------------
def validar_fecha_ddmmYYYY(texto):
    try:
        datetime.datetime.strptime(texto, "%d-%m-%Y")
        return True
    except Exception:
        return False

def normalizar_hora(texto):
    return texto.strip().lower()

def obtener_citas_de_cliente(nombre):
    todas = citas.to_list_of_dicts()
    return [c for c in todas if c.get("cliente_nombre", "").lower() == nombre.lower()]

# ================== LOGIN ==================
def login():
    user = entry_user.get().strip()
    pwd = entry_pass.get().strip()
    rol = usuarios.autenticar(user, pwd)

    if rol == "jefe":
        ventana_login.destroy()
        menu_jefe()
    elif rol == "trabajador":
        ventana_login.destroy()
        menu_trabajador()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# ================== MENÚS ==================
def menu_trabajador():
    win = tk.Toplevel()
    win.title("Menú del Trabajador")
    win.geometry("480x420")
    win.config(bg="#faf7fc")

    tk.Label(win, text="Panel del Trabajador", font=("Arial", 16, "bold"), bg="#faf7fc", fg="#4b2b5a").pack(pady=12)

    botones = [
        ("Registrar cliente y cita", registrar_cliente_cita_window),
        ("Registrar servicios prestados (comprobante)", registrar_servicios_y_comprobante),
        ("Registrar uso de producto (salida inventario)", registrar_uso_producto_window),
        ("Agregar producto al inventario", agregar_producto_window),
        ("Generar comprobante manual", generar_comprobante_manual),
        ("Ver inventario (consola)", inventario.mostrar_inventario),
        ("Cerrar sesión", win.destroy)
    ]
    for texto, cmd in botones:
        b = tk.Button(win, text=texto, width=36, height=2, bg="#e6d0f2", fg="#2f1133",
                      font=("Arial", 10, "bold"), relief="flat", command=cmd)
        b.pack(pady=6)

def menu_jefe():
    win = tk.Toplevel()
    win.title("Menú del Jefe")
    win.geometry("480x380")
    win.config(bg="#f7fbfa")

    tk.Label(win, text="Panel del Jefe", font=("Arial", 16, "bold"), bg="#f7fbfa", fg="#244f4b").pack(pady=12)

    botones = [
        ("Ver inventario (consola)", inventario.mostrar_inventario),
        ("Ver historial de movimientos (consola)", mostrar_movimientos_window),
        ("Reabastecer / Agregar producto", agregar_producto_window),
        ("Generar reporte mensual (TXT)", generar_reporte_mensual),
        ("Cerrar sesión", win.destroy)
    ]
    for texto, cmd in botones:
        b = tk.Button(win, text=texto, width=34, height=2, bg="#cfeee6", fg="#07493f",
                      font=("Arial", 10, "bold"), relief="flat", command=cmd)
        b.pack(pady=8)

# ================== CLIENTE ==================
def iniciar_cliente():
    """Primero solicita los datos del cliente y lo registra si no existe"""
    win = tk.Toplevel()
    win.title("Ingreso Cliente")
    win.geometry("400x380")
    win.config(bg="#fff")

    tk.Label(win, text="Ingreso Cliente", font=("Arial", 16, "bold"), bg="#fff", fg="#8b3b66").pack(pady=10)
    tk.Label(win, text="Nombre completo:").pack(pady=4)
    en_nombre = tk.Entry(win); en_nombre.pack()
    tk.Label(win, text="Teléfono:").pack(pady=4)
    en_tel = tk.Entry(win); en_tel.pack()
    tk.Label(win, text="Edad:").pack(pady=4)
    en_edad = tk.Entry(win); en_edad.pack()
    tk.Label(win, text="Género (H/M):").pack(pady=4)
    en_gen = tk.Entry(win); en_gen.pack()

    def continuar():
        nombre = en_nombre.get().strip()
        tel = en_tel.get().strip()
        try:
            edad = int(en_edad.get().strip())
            if edad < 0:
                messagebox.showerror("Error", "Edad inválida.")
                return
        except:
            messagebox.showerror("Error", "Edad inválida.")
            return
        genero = en_gen.get().strip().upper()
        if genero not in ("H", "M", "N"):
            messagebox.showerror("Error", "Género inválido. Usa H, M o N.")
            return

        cliente_existente = clientes.busqueda_secuencial(nombre)
        if not cliente_existente:
            clientes.agregar_cliente(nombre, tel, edad, genero)
            messagebox.showinfo("Registro", f"No estabas en el sistema, pero ya estás registrado {nombre}.")

        win.destroy()
        menu_cliente(nombre)

    tk.Button(win, text="Continuar", bg="#c491d8", fg="white", command=continuar).pack(pady=10)

def menu_cliente(nombre):
    win = tk.Toplevel()
    win.title(f"Menú Cliente - {nombre}")
    win.geometry("520x420")
    win.config(bg="#fff7fb")

    tk.Label(win, text=f"Bienvenido {nombre}", font=("Arial", 18, "bold"), bg="#fff7fb", fg="#8b3b66").pack(pady=12)

    tk.Button(win, text="Agendar cita", width=36, height=2, bg="#f7dbe6", fg="#5a1230",
              font=("Arial", 11, "bold"), command=lambda: cliente_agendar_cita_window(nombre)).pack(pady=8)

    tk.Button(win, text="Ver mis citas", width=36, height=2, bg="#f7dbe6", fg="#5a1230",
              font=("Arial", 11, "bold"), command=lambda: cliente_ver_citas_window(nombre)).pack(pady=8)

    tk.Button(win, text="Cancelar una cita", width=36, height=2, bg="#f7dbe6", fg="#5a1230",
              font=("Arial", 11, "bold"), command=lambda: cliente_cancelar_cita_window(nombre)).pack(pady=8)

    tk.Button(win, text="Ver servicios y precios", width=36, height=2, bg="#f7dbe6", fg="#5a1230",
              font=("Arial", 11, "bold"), command=cliente_mostrar_servicios).pack(pady=8)

    tk.Button(win, text="Cerrar", width=20, height=1, bg="#d4b2c9", fg="white", command=win.destroy).pack(pady=14)

# ================== CLIENTE FUNCIONES ==================
def cliente_agendar_cita_window(nombre):
    win = tk.Toplevel()
    win.title("Agendar Cita")
    win.geometry("520x520")
    win.config(bg="#fffaf8")

    tk.Label(win, text="Agendar cita", font=("Arial", 14, "bold"), bg="#fffaf8").pack(pady=8)
    tk.Label(win, text="Fecha (DD-MM-YYYY):").pack(); en_fecha = tk.Entry(win); en_fecha.pack()
    tk.Label(win, text="Hora (HH:MM AM/PM):").pack(); en_hora = tk.Entry(win); en_hora.pack()

    lista_servicios = [
        ("Corte", 20),
        ("Tinte", None),
        ("Peinado", 15),
        ("Bases", 10)
    ]
    tk.Label(win, text="Selecciona servicios:").pack(pady=6)
    vars_checks = []
    for n, p in lista_servicios:
        var = tk.IntVar()
        chk = tk.Checkbutton(win, text=f"{n} {'Q'+str(p) if p else ''}", variable=var, bg="#fffaf8")
        chk.pack(anchor="w")
        vars_checks.append(var)

    frame_tinte = tk.Frame(win, bg="#fffaf8")
    tk.Label(frame_tinte, text="Tipo de cabello (C/L):").pack(anchor="w")
    var_largo = tk.StringVar(value="C")
    tk.Radiobutton(frame_tinte, text="Corto", variable=var_largo, value="C", bg="#fffaf8").pack(anchor="w")
    tk.Radiobutton(frame_tinte, text="Largo", variable=var_largo, value="L", bg="#fffaf8").pack(anchor="w")

    tk.Label(frame_tinte, text="Tipo de tinte:").pack(anchor="w")
    var_tipo_tinte = tk.IntVar(value=1)
    tk.Radiobutton(frame_tinte, text="Tinte completo", variable=var_tipo_tinte, value=1, bg="#fffaf8").pack(anchor="w")
    tk.Radiobutton(frame_tinte, text="Mechas", variable=var_tipo_tinte, value=2, bg="#fffaf8").pack(anchor="w")
    tk.Radiobutton(frame_tinte, text="Raíces", variable=var_tipo_tinte, value=3, bg="#fffaf8").pack(anchor="w")

    vars_checks[1].trace_add("write", lambda *a: frame_tinte.pack(pady=6, anchor="w") if vars_checks[1].get() else frame_tinte.forget())

    def agendar():
        fecha = en_fecha.get().strip()
        if not validar_fecha_ddmmYYYY(fecha):
            messagebox.showerror("Error", "Fecha inválida. Usa DD-MM-YYYY.")
            return
        hora = normalizar_hora(en_hora.get().strip())
        if not hora.endswith(("am", "pm")):
            messagebox.showerror("Error", "Incluye AM/PM en la hora.")
            return

        citas_mismo_dia = citas.buscar_por_fecha(fecha)
        for c in citas_mismo_dia:
            if c.hora.lower() == hora.lower():
                messagebox.showwarning("Duplicado", "Ya existe una cita en esa hora.")
                return

        servicios_sel = []
        if vars_checks[0].get():
            servicios_sel.append(("Corte", 20))
        if vars_checks[1].get():
            largo = var_largo.get()
            tipo = var_tipo_tinte.get()
            if tipo == 1:
                precio = 50 if largo == "C" else 80
                servicios_sel.append((f"Tinte completo ({'corto' if largo=='C' else 'largo'})", precio))
            elif tipo == 2:
                precio = 30 if largo == "C" else 50
                servicios_sel.append((f"Mechas ({'corto' if largo=='C' else 'largo'})", precio))
            else:
                precio = 25 if largo == "C" else 40
                servicios_sel.append((f"Raíces ({'corto' if largo=='C' else 'largo'})", precio))
        if vars_checks[2].get():
            servicios_sel.append(("Peinado", 15))
        if vars_checks[3].get():
            servicios_sel.append(("Bases", 10))

        if not servicios_sel:
            messagebox.showwarning("Sin servicios", "Selecciona al menos uno.")
            return

        lista_nombres = [s[0] for s in servicios_sel]
        citas.agregar_cita(nombre, lista_nombres, fecha, hora)
        total = sum(p for _, p in servicios_sel)
        messagebox.showinfo("Éxito", f"Cita agendada para {nombre} el {fecha} a las {hora}\nTotal estimado: Q{total:.2f}")
        win.destroy()

    tk.Button(win, text="Agendar", bg="#c491d8", fg="white", command=agendar).pack(pady=10)

def cliente_ver_citas_window(nombre):
    win = tk.Toplevel()
    win.title("Ver mis citas")
    win.geometry("520x360")
    win.config(bg="#fff")

    lb = tk.Listbox(win, width=80, height=10)
    lb.pack(pady=10)

    lst = obtener_citas_de_cliente(nombre)
    if not lst:
        lb.insert(tk.END, "No se encontraron citas.")
    else:
        for c in lst:
            servicios = ", ".join(c.get("servicios", [])) if c.get("servicios") else "Sin servicios"
            lb.insert(tk.END, f"ID: {c.get('id')} | {c.get('fecha')} {c.get('hora')} | {servicios}")

def cliente_cancelar_cita_window(nombre):
    win = tk.Toplevel()
    win.title("Cancelar cita")
    win.geometry("520x360")
    win.config(bg="#fff")

    lb = tk.Listbox(win, width=80, height=10)
    lb.pack(pady=8)

    lst = obtener_citas_de_cliente(nombre)
    if not lst:
        lb.insert(tk.END, "No se encontraron citas.")
    else:
        for c in lst:
            servicios = ", ".join(c.get("servicios", [])) if c.get("servicios") else "Sin servicios"
            lb.insert(tk.END, f"ID: {c.get('id')} | {c.get('fecha')} {c.get('hora')} | {servicios}")

    def cancelar_seleccion():
        sel = lb.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona una cita.")
            return
        texto = lb.get(sel[0])
        try:
            id_part = texto.split("ID:")[1].split("|")[0].strip()
        except:
            messagebox.showerror("Error", "No se pudo obtener el ID.")
            return
        ok = citas.eliminar_cita(id_part)
        if ok:
            messagebox.showinfo("Éxito", "Cita cancelada.")
            win.destroy()
        else:
            messagebox.showerror("Error", "No se pudo cancelar.")

    tk.Button(win, text="Cancelar cita seleccionada", command=cancelar_seleccion, bg="#e08fbf", fg="white").pack(pady=10)

def cliente_mostrar_servicios():
    win = tk.Toplevel()
    win.title("Servicios y precios")
    win.geometry("400x260")
    win.config(bg="#fff8f9")
    servicios = [
        ("Corte", 20),
        ("Tinte completo (corto/largo)", "50/80"),
        ("Mechas (corto/largo)", "30/50"),
        ("Raíces (corto/largo)", "25/40"),
        ("Peinado", 15),
        ("Bases", 10)
    ]
    tk.Label(win, text="Servicios y precios", font=("Arial", 14, "bold"), bg="#fff8f9").pack(pady=8)
    for s in servicios:
        tk.Label(win, text=f"{s[0]}  -  Q{s[1]}", bg="#fff8f9").pack(anchor="w", padx=18)

# ================== INTERFAZ PRINCIPAL ==================
def iniciar_interfaz():
    global entry_user, entry_pass, ventana_login

    ventana_login = tk.Tk()
    ventana_login.title("Peluquería - Sistema")
    ventana_login.geometry("700x420")
    ventana_login.config(bg="#fbf6ff")

    tk.Label(ventana_login, text="Sistema de Gestión - Salón de Belleza", bg="#fbf6ff",
             fg="#5b3472", font=("Arial", 20, "bold")).pack(pady=18)

    marco = tk.Frame(ventana_login, bg="#efe0f6", bd=2, relief="groove")
    marco.pack(padx=20, pady=6, fill="x")

    center = tk.Frame(marco, bg="#efe0f6")
    center.pack(pady=12)

    tk.Label(center, text="Usuario:", bg="#efe0f6").pack(pady=6)
    entry_user = tk.Entry(center); entry_user.pack(pady=2)
    tk.Label(center, text="Contraseña:", bg="#efe0f6").pack(pady=6)
    entry_pass = tk.Entry(center, show="*"); entry_pass.pack(pady=2)

    frame_bot = tk.Frame(ventana_login, bg="#fbf6ff")
    frame_bot.pack(pady=24)

    tk.Button(frame_bot, text="Jefe", width=14, height=2, bg="#c8b0e3", fg="#3a1d4b",
              font=("Arial", 12, "bold"), command=login).grid(row=0, column=0, padx=20)
    tk.Button(frame_bot, text="Cliente", width=14, height=2, bg="#f7dbe6", fg="#5a1230",
              font=("Arial", 12, "bold"), command=iniciar_cliente).grid(row=0, column=1, padx=20)
    tk.Button(frame_bot, text="Trabajador", width=14, height=2, bg="#d4bdf2", fg="#3a1d4b",
              font=("Arial", 12, "bold"), command=login).grid(row=0, column=2, padx=20)

    tk.Label(ventana_login, text="(Clientes no necesitan iniciar sesión: pulse Cliente)", bg="#fbf6ff").pack(pady=6)
    ventana_login.mainloop()
