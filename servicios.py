pila_historial=[]

Precios={
    "Corte de hombre": 30,
    "Corte + Lavado hombre": 40,
    "Barba": 20,
    "Depilacion de cejas hombre": 10,
    "Corte de mujer": 35,
    "Corte + Lavado mujer": 40,
    "Depilacion de cejas mujer": 10

}

Tintes={
    "Completo":(100,200),
    "mechas":(180,170),
    "puntas":(80,90),
    "fantasia":(70,80),
    "tono sobre tono":(76,86)

}


Bases={
    "lacio":(100,250),
    "ondulado":(200,270),
    "rizado":(220,300),
    "afro":(270,320)
}

Servicios_de_hombre=[
    ("corte hombre", Precios["Corte de hombre"]),
    ("Corte + Lavado de hombre", Precios["Corte + Lavado hombre"]),
    ("Barba", Precios["Barba"]),
    ("Depilacion de cejas", Precios["Depilacion de cejas hombre"])

]

Servicios_de_mujer=[
    ("Corte de mujer", Precios["Corte de mujer"]),
    ("Corte + Lavado de mujer", Precios["Corte + Lavado mujer"]),
    ("Depilacion cejas de mujer", Precios["Depilacion de cejas mujer"])
]



def servicios_mostrados_por_genero(genero):
    lista= Servicios_de_hombre if genero == "H" else Servicios_de_mujer
    print("n\== SERVICIOS DISPONIBLES==")
    for i, (nombre, precio) in enumerate(lista,1):
        print(f"{i}. {nombre} == Q{precio}")
    print(f"{len(lista)+1}. Tinte")
    print(f"{len(lista)+2}. Base del pelo capilar")


def Seleccion_de_servicio_establecido(genero, opcion_index):
    lista= Servicios_de_hombre if genero == "H" else Servicios_de_mujer
    idz= opcion_index -1
    if 0 <= idz < len(lista):
        nombre, precio =lista[idz]
        return nombre, float(precio)
    return None, None


def base_menu():
    tipos = list(Bases.keys())
    for i, t in enumerate(tipos, 1):
        print(f"{i}. {t.capitalize()} (corto Q{Bases[t][0]} / largo Q{Bases[t][1]})")
    eleccion= int(input("Eliga el tipo: "))
    tipo=tipos[eleccion-1]
    largo=input("¿Largo (L) o corto (C) el cabello? ").upper()
    precio= Bases[tipo][1] if largo =="L" else Bases[tipo][0] 
    desc = f"Base {tipo} - {'largo' if largo=='L' else 'corto'}"
    return desc,precio

def tinte_menu():
    tipos = list(Tintes.keys())
    for i, t in enumerate(tipos, 1):
        s, l = Tintes[t]  # corto, largo
        print(f"{i}. {t} corto Q{s} / largo Q{l}")
    eleccion = int(input("Elija el tipo: "))
    tipo = tipos[eleccion - 1]
    largo = input("¿Largo (L) o corto (C)?: ").upper()
    precio = Tintes[tipo][1] if largo == "L" else Tintes[tipo][0]
    desc = f"Tinte: {tipo} - {'largo' if largo == 'L' else 'corto'}"
    return desc, precio


def atender_servicios_para_cliente(cliente, comprobante_agregar_func, genero):
    seleccionados=[]
    while True:
        servicios_mostrados_por_genero(genero)
        opcion=input("Nro servicio (0 terminar): ").strip()
        if opcion=="0":
            break
        if not opcion.isdigit(): continue
        opcion=int(opcion)
        lista_len=len(Servicios_de_hombre) if genero=="H" else len(Servicios_de_mujer)
        if 1<=opcion<=lista_len:
            nombres,precio=Seleccion_de_servicio_establecido(genero,opcion)
            seleccionados.append((nombres,precio))
            pila_historial.append((cliente.nombre,nombres,precio))
            comprobante_agregar_func(nombres,precio)
            print(f"Servicio agregado: {nombres} Q{precio}")
        elif opcion==lista_len+1:
            nombres,precio=tinte_menu()
            seleccionados.append((nombres,precio))
            pila_historial.append((cliente.nombre,nombres,precio))
            comprobante_agregar_func(nombres,precio)
        elif opcion==lista_len+2:
            nombres,precio=base_menu()
            seleccionados.append((nombres,precio))
            pila_historial.append((cliente.nombre,nombres,precio))
            comprobante_agregar_func(nombres,precio)
        else:
            print("Opción inválida")
    return seleccionados

# Exportar los diccionarios para que estén disponibles en la interfaz gráfica
__all__ = ['atender_servicios_para_cliente', 'Tintes', 'Bases', 'pila_historial']