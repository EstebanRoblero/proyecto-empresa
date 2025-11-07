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
reportes_obj = reportes.Reportes()

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

# ================== FUNCIONES PLACEHOLDER ==================
def mostrar_movimientos_window():
    # Función para mostrar movimientos del inventario en consola
    inventario.mostrar_inventario()  # puedes reemplazarlo con lógica real de historial
    print("Aquí se mostraría el historial de movimientos (consola).")

def registrar_cliente_cita_window():
    # Placeholder para ventana de registro de cliente y cita
    messagebox.showinfo("Función", "Registrar cliente y cita aún no implementado.")

def registrar_servicios_y_comprobante():
    messagebox.showinfo("Función", "Registrar servicios y generar comprobante aún no implementado.")

def registrar_uso_producto_window():
    messagebox.showinfo("Función", "Registrar uso de producto aún no implementado.")

def agregar_producto_window():
    messagebox.showinfo("Función", "Agregar producto al inventario aún no implementado.")

def generar_comprobante_manual():
    messagebox.showinfo("Función", "Generar comprobante manual aún no implementado.")

def generar_reporte_mensual():
    reportes_obj.mostrar_reporte_del_mes()
    messagebox.showinfo("Reporte mensual", "Reporte mensual generado en consola.")

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
    tk.Label(win, text="Género (H/M/N):").pack(pady=4)
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
    # Por simplicidad, solo mensaje
    messagebox.showinfo("Agendar cita", f"Función de agendar cita para {nombre} aún no implementada.")

def cliente_ver_citas_window(nombre):
    messagebox.showinfo("Ver citas", f"Función de ver citas de {nombre} aún no implementada.")

def cliente_cancelar_cita_window(nombre):
    messagebox.showinfo("Cancelar cita", f"Función de cancelar cita de {nombre} aún no implementada.")

def cliente_mostrar_servicios():
    messagebox.showinfo("Servicios", "Función de mostrar servicios aún no implementada.")

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


