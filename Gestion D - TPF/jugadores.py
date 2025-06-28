# Importación de módulos
import json
import os
from json_utils import cargar_json, guardar_json
from tabulate import tabulate
from equipos import limpiar_pantalla
from rich.console import Console
from rich import print

console = Console()

# Rutas de archivos
RUTA_JUGADORES = "data/jugadores.json"
RUTA_EQUIPOS = "data/equipos.json"

# Tupla de opciones para deportes
disciplinas = ('', 'Futbol', 'Volley', 'Basquet')

#######################################################################################################################

def agregar_jugador():
    jugadores = cargar_json(RUTA_JUGADORES)
    print("============ Agregar Jugador ===========")
    nombre = input("Ingrese el nombre del jugador: ").strip().lower()
    deporte = int(input("Seleccione un numero \n1- Futbol\n2- Volley\n3- Basquet"))

    while deporte not in range(1, 4):
        print("Opcion incorrecta, porfavor intente otra vez")
        deporte = int(input("Seleccione un numero \n1- Futbol\n2- Volley\n3- Basquet"))

    nuevo_jugador = {
        "nombre": nombre,
        "deporte": disciplinas[deporte],
        "club": 'Libre'
    }

    for i in jugadores:
        if i["nombre"] == nombre and i["deporte"] == disciplinas[deporte]:
            print("El jugador ya existe.")
            input("Presione Enter para continuar...")
            return

    jugadores.append(nuevo_jugador)
    guardar_json(RUTA_JUGADORES, jugadores)
    
#######################################################################################################################

def ver_jugadores():
    jugadores = cargar_json(RUTA_JUGADORES)
    if jugadores:
        print("Lista de jugadores\n")
        tabla = [[j['nombre'], j['deporte'], j['club']] for j in jugadores]
        encabezado = ["Nombre", "Deporte", "Club"]
        print(tabulate(tabla, headers=encabezado, tablefmt="fancy_grid"))
    else:
        print("No hay jugadores registrados en el sistema.\n")
    input("Presione enter para continuar.")
    
 #######################################################################################################################   

def buscar_jugador():
    jugadores = cargar_json(RUTA_JUGADORES)
    if jugadores:
        nombre = console.input("[bold green]Ingrese el nombre del jugador que desea buscar: [/bold green]").strip().lower()
        for jugador in jugadores:
            if nombre == jugador['nombre']:
                print(tabulate([jugador], headers="keys", tablefmt="fancy_grid"))
                input("Presione enter para continuar.")
                return
        print("Jugador no encontrado.")
    else:
        print("No hay jugadores registrados en el sistema.\n")
    input("Presione enter para continuar.")
    
#######################################################################################################################

def listar_jugadores(jugadores: list):
    print("Lista de jugadores\n")
    tabla = [{
        'Opcion': i,
        'Nombre': jugador['nombre'],
        'Deporte': jugador['deporte'],
        'Club': jugador['club']
    } for i, jugador in enumerate(jugadores)]
    print(tabulate(tabla, headers="keys", tablefmt="fancy_grid"))
    
    
#######################################################################################################################


def editar_jugador():
    jugadores = cargar_json(RUTA_JUGADORES)
    if not jugadores:
        print("No hay jugadores registrados en el sistema.\n")
        input("Presione enter para continuar.")
        return

    listar_jugadores(jugadores)
    codigo = int(console.input("[bold red]Seleccione el número de opción correspondiente al jugador a editar: [/bold red]"))

    while codigo not in range(len(jugadores)):
        print("Opción incorrecta, por favor intente otra vez.")
        codigo = int(input("Seleccione el número de opción correspondiente al jugador a editar: "))

    jugador = jugadores[codigo]
    print("Jugador seleccionado:\n")
    print(tabulate([[jugador['nombre'], jugador['deporte']]], headers=["Nombre", "Deporte"], tablefmt='fancy_grid'))

    opc = int(console.input("[bold magenta on white]1- Editar nombre\n2- Editar deporte\n3- Editar ambos\nSeleccione una opción: [/bold magenta on white]"))
    while opc not in (1, 2, 3):
        print("Opción incorrecta, por favor intente otra vez.")
        opc = int(input("1- Editar nombre\n2- Editar deporte\n3- Editar ambos\nSeleccione una opción: "))

    if opc == 1:
        jugador['nombre'] = input("Ingrese el nuevo nombre: ").strip().lower()
    elif opc == 2:
        nuevo_dep = int(input("1- Futbol\n2- Volley\n3- Basquet\nSeleccione un deporte: "))
        while nuevo_dep not in (1, 2, 3):
            nuevo_dep = int(input("Opción incorrecta. Seleccione un deporte válido: "))
        jugador['deporte'] = disciplinas[nuevo_dep]
    else:
        jugador['nombre'] = input("Ingrese el nuevo nombre: ").strip().lower()
        nuevo_dep = int(input("1- Futbol\n2- Volley\n3- Basquet\nSeleccione un deporte: "))
        while nuevo_dep not in (1, 2, 3):
            nuevo_dep = int(input("Opción incorrecta. Seleccione un deporte válido: "))
        jugador['deporte'] = disciplinas[nuevo_dep]

    guardar_json(RUTA_JUGADORES, jugadores)
    print("\nJugador editado con éxito:")
    print(tabulate([[jugador['nombre'], jugador['deporte']]], headers=["Nombre", "Deporte"], tablefmt='fancy_grid'))
    input("Presione enter para continuar.")

#######################################################################################################################

def mostrar_tabla(lista, opciones, key, valor):
    tabla = []
    for i, item in enumerate(lista):
        if valor.lower() == item.get(key, '').lower():
            opciones.append(i)
            tabla.append({
                "Opcion": i,
                "Nombre": item.get("nombre"),
                "Deporte": item.get("deporte")
            })
    if tabla:
        print(tabulate(tabla, headers="keys", tablefmt="fancy_grid"))
    else:
        print(f"No hay {valor}.")
        
#######################################################################################################################

def vincular_jugador():
    jugadores = cargar_json(RUTA_JUGADORES)
    equipos = cargar_json(RUTA_EQUIPOS)

    lista_opcj = []
    lista_opce = []

    if not jugadores:
        print("No hay jugadores registrados en el sistema.")
        input("Presione enter para continuar")
        return

    print("Lista de jugadores libres:\n")
    mostrar_tabla(jugadores, lista_opcj, 'club', "Libre")

    if not lista_opcj:
        print("No hay jugadores libres.")
        input("Presione enter para continuar")
        return

    opcj = int(console.input("[underline blue]Seleccione el número de opción correspondiente a un jugador: [/underline blue]"))
    while opcj not in lista_opcj:
        print("Opción incorrecta, por favor intente otra vez.")
        opcj = int(input("Seleccione el número de opción correspondiente a un jugador: "))

    mostrar_tabla(equipos, lista_opce, 'deporte', jugadores[opcj]['deporte'])
    opce = int(console.input("[underline blue]Seleccione el número de opción correspondiente a un equipo: [/underline blue]"))
    while opce not in lista_opce:
        print("Opción incorrecta, por favor intente otra vez.")
        opce = int(console.input("[underline blue]Seleccione el número de opción correspondiente a un equipo: [/underline blue]"))

    jugadores[opcj]['club'] = equipos[opce]['nombre']
    guardar_json(RUTA_JUGADORES, jugadores)
    print("Jugador vinculado con éxito.")
    print(f"Nombre: {jugadores[opcj]['nombre']} Deporte: {jugadores[opcj]['deporte']} Club: {jugadores[opcj]['club']}")
    input("Presione enter para continuar")


#######################################################################################################################


def eliminar_jugador():
    jugadores = cargar_json(RUTA_JUGADORES)
    lista_opc = []

    if not jugadores:
        print("No hay jugadores en el sistema.")
        input("Presione enter para continuar")
        return

    opc = int(input("Ingrese una opción:\n1- Eliminar jugador de un club\n2- Eliminar jugador del sistema\n"))

    if opc == 1:
        tabla = []
        for i, j in enumerate(jugadores):
            if j['club'] != 'Libre':
                lista_opc.append(i)
                tabla.append({
                    'Opcion': i,
                    'Nombre': j['nombre'],
                    'Deporte': j['deporte'],
                    'Club': j['club']
                })
        if tabla:
            print(tabulate(tabla, headers="keys", tablefmt="fancy_grid"))
            opcj = int(input("Ingrese el número de opción correspondiente a un jugador: "))
            while opcj not in lista_opc:
                print("Opción incorrecta, por favor intente otra vez.")
                opcj = int(input("Ingrese el número de opción correspondiente a un jugador: "))
            jugadores[opcj]['club'] = 'Libre'
            guardar_json(RUTA_JUGADORES, jugadores)
            limpiar_pantalla()
            print("Jugador liberado correctamente.")
            print(tabulate([[jugadores[opcj]['nombre'], jugadores[opcj]['deporte'], jugadores[opcj]['club']]], headers=["Nombre", "Deporte", "Club"], tablefmt="fancy_grid"))
        else:
            print("No hay jugadores contratados.")
    elif opc == 2:
        listar_jugadores(jugadores)
        codigo = int(input("Seleccione el número de opción correspondiente al jugador a eliminar: "))
        while codigo not in range(len(jugadores)):
            print("Opción incorrecta, por favor intente otra vez.")
            codigo = int(input("Seleccione el número de opción correspondiente al jugador a eliminar: "))
        limpiar_pantalla()
        print("Jugador eliminado correctamente.")
        print(tabulate([[jugadores[codigo]['nombre'], jugadores[codigo]['deporte'], jugadores[codigo]['club']]], headers=["Nombre", "Deporte", "Club"], tablefmt="fancy_grid"))
        jugadores.pop(codigo)
        guardar_json(RUTA_JUGADORES, jugadores)
    else:
        print("Opción incorrecta")
    input("Presione enter para continuar")
    
#######################################################################################################################
#######################################################################################################################

def menu_jugadores():
    print("============ Gestión de Equipos ============")
    while True:
        console.print("1. Agregar jugador", style="#1E90FF")
        console.print("2. Ver Jugadores", style="#1EFF1E")
        console.print("3. Buscar jugadores", style="#C01E82")
        console.print("4. Editar jugador", style="#BDBA27")
        console.print("5. Eliminar jugador", style="#341AAA")
        console.print("6. Vincular Jugador", style="#349980")
        console.print("7. Volver al Menú Principal", style="#F00C0C")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_jugador()
        elif opcion == "2":
            ver_jugadores()
        elif opcion == "3":
            buscar_jugador()
        elif opcion == "4":
            editar_jugador()
        elif opcion == "5":
            eliminar_jugador()
        elif opcion == "6":
            vincular_jugador()
        elif opcion == "7":
            break
        else:
            input("Opción no válida. Presione Enter para continuar...")