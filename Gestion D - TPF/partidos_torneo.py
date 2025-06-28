import json                            # Para manipular archivos JSON
import os                              # Para limpiar la consola
import random                          # Para simular resultados aleatorios
from json_utils import cargar_json, guardar_json  # Funciones reutilizables para archivos JSON

from itertools import combinations     # Para combinar equipos en partidos
from tabulate import tabulate  # Para mostrar tablas
from rich.console import Console

console = Console(record=True)  # para generar y grabar el reporte de la consola
from rich import print



def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


RUTA_EQUIPOS = "data/equipos.json"

def simular_torneo():
    equipos = cargar_json(RUTA_EQUIPOS)

    opcion = int(input("Elige una opción (1: Fútbol, 2: Básquet, 3: Voley, 5: Reportes): "))

    if opcion == 1:
        tabla_resultados_futbol = []
        console.print("Simulando torneo de fútbol...")

        for equipo1, equipo2 in combinations(equipos, 2):
            if equipo1["deporte"].lower() == "futbol" and equipo2["deporte"].lower() == "futbol":
                resultado = f"{random.randint(0,5)} - {random.randint(0,5)}"
                tabla_resultados_futbol.append([
                    equipo1["nombre"],
                    resultado,
                    equipo2["nombre"],
                ])

        console.print(tabulate(tabla_resultados_futbol, headers=["Equipo 1", "Resultado", "Equipo 2"], tablefmt="fancy_grid"))

        torneo = "data/partidos_torneo_futbol.json"
        guardar_json(torneo, tabla_resultados_futbol)
        campeon(torneo)

    ###############################################################################################################################################
    elif opcion == 2:
        tabla_resultados_basquet = []
        console.print("Simulando torneo de básquet...")

        for equipo1, equipo2 in combinations(equipos, 2):
            if equipo1["deporte"].lower() == "basquet" and equipo2["deporte"].lower() == "basquet":
                resultado = f"{random.randint(70,115)} - {random.randint(70,115)}"
                tabla_resultados_basquet.append([
                    equipo1["nombre"],
                    resultado,
                    equipo2["nombre"]
                ])

        console.print(tabulate(tabla_resultados_basquet, headers=["Equipo 1", "Resultado", "Equipo 2"], tablefmt="fancy_grid"))

        torneo = "data/partidos_torneo_basquet.json"
        guardar_json(torneo, tabla_resultados_basquet)
        campeon(torneo)

    ################################################################################################################################################
    elif opcion == 3:
        tabla_resultados_voley = []
        console.print("Simulando torneo de vóley...")

        for equipo1, equipo2 in combinations(equipos, 2):
            if equipo1["deporte"].lower() == "voley" and equipo2["deporte"].lower() == "voley":
                resultado = f"{random.randint(0,3)} - {random.randint(0,3)}"
                tabla_resultados_voley.append([
                    equipo1["nombre"],
                    resultado,
                    equipo2["nombre"]
                ])

        console.print(tabulate(tabla_resultados_voley, headers=["Equipo 1", "Resultado", "Equipo 2"], tablefmt="fancy_grid"))

        torneo = "data/partidos_torneo_voley.json"
        guardar_json(torneo, tabla_resultados_voley)
        campeon(torneo)

    #################################################################################################################################################
    elif opcion == 5:
        ver = int(input("¿Qué reporte de partidos querés ver? (1: Fútbol, 2: Básquet, 3: Vóley): "))


        if ver == 1:
            if os.path.exists("data/partidos_torneo_futbol.json"):
                partidos_futbol = cargar_json("data/partidos_torneo_futbol.json")
                console.print(tabulate(partidos_futbol, headers=["Equipo 1", "Resultado", "Equipo 2"], tablefmt="fancy_grid"))
            else:
                console.print("[bold red]No hay partidos de fútbol simulados.[/bold red]")

        elif ver == 2:
            if os.path.exists("data/partidos_torneo_basquet.json"):
                partidos_basquet = cargar_json("data/partidos_torneo_basquet.json")
                console.print(tabulate(partidos_basquet, headers=["Equipo 1", "Resultado", "Equipo 2"], tablefmt="fancy_grid"))
            else:
                console.print("[bold red]No hay partidos de básquet simulados.[/bold red]")

        elif ver == 3:
            if os.path.exists("data/partidos_torneo_voley.json"):
                partidos_voley = cargar_json("data/partidos_torneo_voley.json")
                console.print(tabulate(partidos_voley, headers=["Equipo 1", "Resultado", "Equipo 2"], tablefmt="fancy_grid"))
            else:
                console.print("[bold red]No hay partidos de vóley simulados.[/bold red]")

        else:
            console.print("[bold red]Opción no válida.[/bold red]")

        
            
#################################################################################################################################################
def campeon(ruta_partidos):
    partidos = cargar_json(ruta_partidos)
    if not partidos:
        console.print("No hay partidos registrados.")
        return

    goles_totales = {}

    for partido in partidos:
        equipo1 = partido[0]
        resultado = partido[1].replace(" ", "")  # Eliminar espacios
        equipo2 = partido[2]

        goles_equipo1 = int(resultado.split('-')[0])
        goles_equipo2 = int(resultado.split('-')[1])

        goles_totales[equipo1] = goles_totales.get(equipo1, 0) + goles_equipo1
        goles_totales[equipo2] = goles_totales.get(equipo2, 0) + goles_equipo2

    campeon_equipo = max(goles_totales, key=goles_totales.get)
    mayor_goles = goles_totales[campeon_equipo]

    console.print(f"El campeón del torneo es: {campeon_equipo} con {mayor_goles} tantos anotados.")


######################################################################################################################
def ver_torneo_simulado():
    console = Console(record=True) # lo pongo al principio.... y aca para reiniciar el buffer, sino imprime 2 veces la misma tabla
    console.print("Verificando el torneo simulado...")
    
    if os.path.exists("data/partidos_torneo_futbol.json"):
        partidos_futbol = cargar_json("data/partidos_torneo_futbol.json")
        console.print("Partidos de Fútbol:")
        console.print(tabulate(partidos_futbol, headers=["Equipo 1", "Resultado", "Equipo 2"], tablefmt="fancy_grid"))
    else:
        console.print("No hay partidos de fútbol simulados.")

    if os.path.exists("data/partidos_torneo_basquet.json"):
        partidos_basquet = cargar_json("data/partidos_torneo_basquet.json")
        console.print("\nPartidos de Básquet:")
        console.print(tabulate(partidos_basquet, headers=["Equipo 1", "Resultado", "Equipo 2"], tablefmt="fancy_grid"))
    else:
        console.print("No hay partidos de básquet simulados.")

    if os.path.exists("data/partidos_torneo_voley.json"):
        partidos_voley = cargar_json("data/partidos_torneo_voley.json")
        console.print("\nPartidos de Vóley:")
        console.print(tabulate(partidos_voley, headers=["Equipo 1", "Resultado", "Equipo 2"], tablefmt="fancy_grid"))
    else:
        console.print("No hay partidos de vóley simulados.")

    # Exporta lo que se imprimió en consola a un archivo
    texto_exportado = console.export_text()
    with open("data/reporte_txt/reportes_torneos.txt", "w", encoding="utf-8") as f:
        f.write(texto_exportado)

    console.print("✅  [underline blue]Se generó un reporte .txt con toda la info completa.[/underline blue]")
    console.print("[italic green]¡Gracias por usar el sistema de gestión deportiva![/italic green]")
    console.print("[italic green]¡Hasta la próxima![/italic green]")
