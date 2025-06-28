import random
import os
import json
from json_utils import cargar_json, guardar_json
from itertools import combinations
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()

RUTA_CARPETA_DATOS = "data"
ARCHIVO_EQUIPOS = os.path.join(RUTA_CARPETA_DATOS, "equipos.json")
ARCHIVO_PARTIDOS_MANUAL = os.path.join(RUTA_CARPETA_DATOS, "partidos_manual.json")

partidos_manual_registrados = [] 

RAINBOW_COLORS = [
    "bold reverse red",
    "bold reverse orange1",
    "bold reverse yellow",
    "bold reverse green",
    "bold reverse blue",
    "bold reverse purple",
    "bold reverse magenta",
    "bold reverse cyan",
    "bold reverse white on black"
]

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def seleccionar_deporte():
    limpiar_pantalla()
    deportes_menu = Text()
    
    deportes_opciones = [
        "1. Fútbol",
        "2. Básquet",
        "3. Vóley",
        "0. Cancelar"
    ]

    for i, opcion_texto in enumerate(deportes_opciones):
        color_idx = i % (len(RAINBOW_COLORS) - 1)
        if opcion_texto == "0. Cancelar":
            color_idx = len(RAINBOW_COLORS) - 1
        deportes_menu.append(f"{opcion_texto}\n", style=RAINBOW_COLORS[color_idx])

    deporte_panel = Panel(
        deportes_menu,
        title="[bold bright_white reverse]Seleccionar Deporte[/bold bright_white reverse]",
        title_align="center",
        expand=True,
        padding=(2, 5),
        width=80
    )
    console.print(deporte_panel)

    opcion = console.input("[bold white on blue]Seleccione un deporte:[/bold white on blue] ").strip()
    deporte_seleccionado = ""

    if opcion == "1":
        deporte_seleccionado = "futbol"
    elif opcion == "2":
        deporte_seleccionado = "basquet"
    elif opcion == "3":
        deporte_seleccionado = "voley"
    elif opcion == "0":
        return None
    else:
        console.print("[bold red reverse]Opción inválida. Por favor, intente de nuevo.[/bold red reverse]")
        return None
    return deporte_seleccionado

def _cargar_equipos():
    try:
        equipos = cargar_json(ARCHIVO_EQUIPOS)
        if not isinstance(equipos, list):
            console.print(f"[bold yellow]Advertencia: El archivo {ARCHIVO_EQUIPOS} no contiene una lista. Se inicializará vacío.[/bold yellow]")
            return []
        return equipos
    except Exception as e:
        console.print(f"[bold red]Ocurrió un error al cargar equipos: {e}[/bold red]")
        return []

def _generar_siguiente_id():
    valid_ids = [p["id"] for p in partidos_manual_registrados if isinstance(p, dict) and "id" in p and isinstance(p["id"], (int, float))]
    return max(valid_ids) + 1 if valid_ids else 1

def _guardar_partidos_manual_en_json():
    guardar_json(ARCHIVO_PARTIDOS_MANUAL, partidos_manual_registrados)

def crear_partido_manual():
    global partidos_manual_registrados
    limpiar_pantalla()
    console.print(Panel("[bold green reverse]=== CREAR PARTIDO MANUAL ===[/bold green reverse]", title_align="center", padding=(1, 2), width=80))

    deporte = seleccionar_deporte()
    if not deporte:
        return

    equipos = _cargar_equipos()
    equipos_disponibles = [e for e in equipos if e.get("deporte", "").lower() == deporte.lower()]

    if len(equipos_disponibles) < 2:
        console.print(f"[bold red reverse]Se necesitan al menos 2 equipos de {deporte.capitalize()} para crear un partido.[/bold red reverse]")
        return

    console.print("\n[bold cyan reverse]Equipos disponibles:[/bold cyan reverse]")
    for i, equipo in enumerate(equipos_disponibles):
        console.print(f"[bold white on black]{i+1}. {equipo['nombre']}[/bold white on black]")

    try:
        idx1 = int(console.input("[bold white on blue]Seleccione el número del equipo LOCAL:[/bold white on blue] ")) - 1
        equipo1 = equipos_disponibles[idx1]

        idx2 = int(console.input("[bold white on blue]Seleccione el número del equipo VISITANTE:[/bold white on blue] ")) - 1
        equipo2 = equipos_disponibles[idx2]

        if equipo1["nombre"] == equipo2["nombre"]:
            console.print("[bold red reverse]Un equipo no puede jugar contra sí mismo.[/bold red reverse]")
            return

        resultado_str = console.input("[bold white on blue]Ingrese el resultado del partido (Ej: '2-1'):[/bold white on blue] ").strip()
        goles_local, goles_visitante = map(int, resultado_str.split('-'))

        fecha = console.input("[bold white on blue]Ingrese la fecha del partido (Ej: '2023-10-26'):[/bold white on blue] ").strip()
        if not fecha:
            fecha = "Fecha Desconocida"

        id_partido = _generar_siguiente_id()
        
        nuevo_partido = {
            "id": id_partido,
            "deporte": deporte,
            "local": equipo1["nombre"], 
            "visitante": equipo2["nombre"], 
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
            "resultado": resultado_str,
            "fecha": fecha,
            "estado": "finalizado",
            "tipo": "manual"
        }

        partidos_manual_registrados.append(nuevo_partido)
        _guardar_partidos_manual_en_json()
        console.print(f"[bold green reverse]Partido entre {equipo1['nombre']} y {equipo2['nombre']} registrado con éxito.[/bold green reverse]")

    except (ValueError, IndexError):
        console.print("[bold red reverse]Entrada inválida. Asegúrese de seleccionar números válidos y un formato de resultado correcto.[/bold red reverse]")
    except Exception as e:
        console.print(f"[bold red reverse]Ocurrió un error inesperado: {e}[/bold red reverse]")


def buscar_partidos_manual():
    limpiar_pantalla()
    console.print(Panel("[bold yellow reverse]=== BUSCAR PARTIDOS ===[/bold yellow reverse]", title_align="center", padding=(1, 2), width=80))

    if not partidos_manual_registrados:
        console.print("[bold red reverse]No hay partidos registrados aún para buscar.[/bold red reverse]")
        return

    criterio = console.input("[bold white on blue]Ingrese el nombre del equipo o la fecha para buscar partidos:[/bold white on blue] ").strip().lower()

    resultados = [
        p for p in partidos_manual_registrados
        if p and isinstance(p, dict) and (
           criterio in p.get("local", "").lower() or 
           criterio in p.get("visitante", "").lower() or
           criterio in p.get("fecha", "").lower()
        )
    ]

    if resultados:
        console.print("\n[bold cyan reverse]Resultados de la búsqueda:[/bold cyan reverse]")
        tabla = Table(title="[bold yellow reverse]Partidos Encontrados[/bold yellow reverse]", show_header=True, header_style="bold bright_white reverse")
        tabla.add_column("ID", width=5)
        tabla.add_column("Deporte", style="bold green")
        tabla.add_column("Local", style="bold blue")
        tabla.add_column("Goles L", style="bold red")
        tabla.add_column("Goles V", style="bold red")
        tabla.add_column("Visitante", style="bold blue")
        tabla.add_column("Fecha", style="bold magenta")
        tabla.add_column("Estado", style="bold yellow")
        tabla.add_column("Tipo", style="bold cyan")

        for p in resultados:
            tabla.add_row(
                str(p.get("id", "N/A")),
                p.get("deporte", "N/A").capitalize(),
                p.get("local", "N/A"),
                str(p.get("goles_local", "N/A")),
                str(p.get("goles_visitante", "N/A")),
                p.get("visitante", "N/A"),
                p.get("fecha", "N/A"),
                p.get("estado", "N/A").capitalize(),
                p.get("tipo", "N/A").capitalize()
            )
        console.print(tabla)
    else:
        console.print("[bold red reverse]No se encontraron partidos con ese criterio.[/bold red reverse]")

def listar_partidos_manual():
    limpiar_pantalla()
    console.print(Panel("[bold cyan reverse]=== LISTADO DE PARTIDOS ===[/bold cyan reverse]", title_align="center", padding=(1, 2), width=80))

    if not partidos_manual_registrados:
        console.print("[bold red reverse]No hay partidos registrados aún.[/bold red reverse]")
        return

    tabla = Table(title="[bold cyan reverse]Todos los Partidos[/bold cyan reverse]", show_header=True, header_style="bold bright_white reverse")
    tabla.add_column("ID", width=5)
    tabla.add_column("Deporte", style="bold green")
    tabla.add_column("Local", style="bold blue")
    tabla.add_column("Goles L", style="bold red")
    tabla.add_column("Goles V", style="bold red")
    tabla.add_column("Visitante", style="bold blue")
    tabla.add_column("Fecha", style="bold magenta")
    tabla.add_column("Estado", style="bold yellow")
    tabla.add_column("Tipo", style="bold cyan")

    for p in partidos_manual_registrados:
        if not isinstance(p, dict):
            continue
        tabla.add_row(
            str(p.get("id", "N/A")),
            p.get("deporte", "N/A").capitalize(),
            p.get("local", "N/A"),
            str(p.get("goles_local", "N/A")),
            str(p.get("goles_visitante", "N/A")),
            p.get("visitante", "N/A"),
            p.get("fecha", "N/A"),
            p.get("estado", "N/A").capitalize(),
            p.get("tipo", "N/A").capitalize()
        )
    console.print(tabla)

def modificar_partido_manual():
    global partidos_manual_registrados
    limpiar_pantalla()
    console.print(Panel("[bold purple reverse]=== MODIFICAR PARTIDO ===[/bold purple reverse]", title_align="center", padding=(1, 2), width=80))

    if not partidos_manual_registrados:
        console.print("[bold red reverse]No hay partidos para modificar.[/bold red reverse]")
        return

    listar_partidos_manual()

    try:
        id_modificar = int(console.input("[bold white on blue]Ingrese el ID del partido a modificar:[/bold white on blue] "))
    except ValueError:
        console.print("[bold red reverse]Entrada inválida. El ID debe ser un número.[/bold red reverse]")
        return

    partido_encontrado = next((p for p in partidos_manual_registrados if p.get("id") == id_modificar and isinstance(p, dict)), None)

    if partido_encontrado:
        console.print(f"[bold bright_white reverse]Modificando partido (ID: {id_modificar}, {partido_encontrado.get('local', 'N/A')} vs {partido_encontrado.get('visitante', 'N/A')}).[/bold bright_white reverse]")

        try:
            nuevo_resultado = console.input(f"[bold white on blue]Nuevo resultado ({partido_encontrado.get('resultado', 'N/A')}):[/bold white on blue] ").strip()
            if nuevo_resultado:
                goles_local, goles_visitante = map(int, nuevo_resultado.split('-'))
                partido_encontrado["resultado"] = nuevo_resultado
                partido_encontrado["goles_local"] = goles_local
                partido_encontrado["goles_visitante"] = goles_visitante

            nueva_fecha = console.input(f"[bold white on blue]Nueva fecha ({partido_encontrado.get('fecha', 'N/A')}):[/bold white on blue] ").strip()
            if nueva_fecha:
                partido_encontrado["fecha"] = nueva_fecha

            _guardar_partidos_manual_en_json()
            console.print("[bold green reverse]Partido modificado con éxito.[/bold green reverse]")
        except ValueError:
            console.print("[bold red reverse]Formato de resultado inválido. Por favor, use 'goles-goles'.[/bold red reverse]")
    else:
        console.print("[bold red reverse]Partido no encontrado con ese ID.[/bold red reverse]")

def eliminar_partido_manual():
    global partidos_manual_registrados
    limpiar_pantalla()
    console.print(Panel("[bold red reverse]=== ELIMINAR PARTIDO ===[/bold red reverse]", title_align="center", padding=(1, 2), width=80))

    if not partidos_manual_registrados:
        console.print("[bold red reverse]No hay partidos para eliminar.[/bold red reverse]")
        return

    listar_partidos_manual()

    try:
        id_eliminar = int(console.input("[bold white on blue]Ingrese el ID del partido a eliminar:[/bold white on blue] "))
    except ValueError:
        console.print("[bold red reverse]Entrada inválida. El ID debe ser un número.[/bold red reverse]")
        return

    partido_encontrado = next((p for p in partidos_manual_registrados if p.get("id") == id_eliminar and isinstance(p, dict)), None)

    if partido_encontrado:
        confirmacion = console.input(f"[bold white on red]¿Estás seguro de eliminar el partido (ID: {id_eliminar}, {partido_encontrado.get('local', 'N/A')} vs {partido_encontrado.get('visitante', 'N/A')})? (s/n):[/bold white on red] ").strip().lower()
        if confirmacion == 's':
            partidos_manual_registrados = [p for p in partidos_manual_registrados if p.get("id") != id_eliminar]
            _guardar_partidos_manual_en_json()
            console.print("[bold green reverse]Partido eliminado con éxito.[/bold green reverse]")
        else:
            console.print("[bold yellow reverse]Eliminación cancelada.[/bold yellow reverse]")
    else:
        console.print("[bold red reverse]Partido no encontrado con ese ID.[/bold red reverse]")

def _simular_fecha_deporte_interna(deporte_seleccionado, fecha_simular, equipos_disponibles):
    partidos_simulados = []
    
    equipos_filtrados = [e for e in equipos_disponibles if e.get("deporte", "").lower() == deporte_seleccionado.lower()]

    if len(equipos_filtrados) < 2:
        console.print(f"[bold red reverse]Se necesitan al menos 2 equipos de {deporte_seleccionado.capitalize()} para simular una fecha.[/bold red reverse]")
        return []

    siguiente_id_disponible = _generar_siguiente_id()
    
    console_for_capture = Console(record=True, color_system=None) 

    with console_for_capture.capture() as capture: 
        console_for_capture.print(Panel(f"=== Simulando Fecha: {fecha_simular} de {deporte_seleccionado.capitalize()} ===", title_align="center", padding=(1, 2), width=80)) 
        
        for equipo1, equipo2 in combinations(equipos_filtrados, 2):
            goles_local, goles_visitante = 0, 0
            if deporte_seleccionado == "futbol":
                goles_local = random.randint(0, 5)
                goles_visitante = random.randint(0, 5)
            elif deporte_seleccionado == "basquet":
                goles_local = random.randint(50, 120)
                goles_visitante = random.randint(50, 120)
            elif deporte_seleccionado == "voley":
                sets_ganados_1 = 0
                sets_ganados_2 = 0
                while sets_ganados_1 < 3 and sets_ganados_2 < 3 and (sets_ganados_1 + sets_ganados_2 < 5): 
                    if random.random() > 0.5:
                        sets_ganados_1 += 1
                    else:
                        sets_ganados_2 += 1
                goles_local = sets_ganados_1
                goles_visitante = sets_ganados_2
            else:
                continue

            resultado = f"{goles_local}-{goles_visitante}"
            
            id_simulado = siguiente_id_disponible
            siguiente_id_disponible += 1
            
            partidos_simulados.append({
                "id": id_simulado,
                "deporte": deporte_seleccionado,
                "local": equipo1["nombre"], 
                "visitante": equipo2["nombre"],
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "resultado": resultado,
                "fecha": fecha_simular,
                "estado": "finalizado",
                "tipo": "fecha_simulada"
            })

        if partidos_simulados:
            tabla_terminal = Table(title=f"[bold magenta reverse]Resultados de la Fecha {fecha_simular}[/bold magenta reverse]", show_header=True, header_style="bold bright_white reverse")
            tabla_terminal.add_column("Equipo Local", style="bold blue")
            tabla_terminal.add_column("Equipo Visitante", style="bold green")
            tabla_terminal.add_column("Resultado", style="bold red")
            tabla_terminal.add_column("ID", style="bold yellow")

            for p in partidos_simulados:
                tabla_terminal.add_row(p["local"], p["visitante"], p["resultado"], str(p["id"]))
            
            console.print(tabla_terminal) 
            console.print(f"[bold cyan reverse]Cantidad de partidos generados: {len(partidos_simulados)}[/bold cyan reverse]") 

            console_for_capture.print(Panel(f"=== Resultados de la Fecha {fecha_simular} ===", title_align="center", padding=(1, 2), width=80)) 
            tabla_no_color = Table(title=f"Resultados de la Fecha {fecha_simular}", show_header=True) 
            tabla_no_color.add_column("Equipo Local") 
            tabla_no_color.add_column("Equipo Visitante") 
            tabla_no_color.add_column("Resultado") 
            tabla_no_color.add_column("ID") 

            for p in partidos_simulados:
                tabla_no_color.add_row(p["local"], p["visitante"], p["resultado"], str(p["id"]))
            
            console_for_capture.print(tabla_no_color) 
            console_for_capture.print(f"Cantidad de partidos generados: {len(partidos_simulados)}") 

        else:
            console.print(f"[bold red reverse]No se generaron partidos para {deporte_seleccionado.capitalize()} en la fecha {fecha_simular}.[/bold red reverse]") 
            console_for_capture.print(f"No se generaron partidos para {deporte_seleccionado.capitalize()} en la fecha {fecha_simular}.") 
    
    texto_exportado = capture.get() 

    if not os.path.exists("data/reporte_txt"):
        os.makedirs("data/reporte_txt")
    
    nombre_archivo_txt = f"data/reporte_txt/simulacion_{deporte_seleccionado}_{fecha_simular.replace(' ', '_')}_{random.randint(1000, 9999)}.txt"
    with open(nombre_archivo_txt, "w", encoding="utf-8") as f:
        f.write(texto_exportado)
    console.print(f"[bold green reverse]Reporte guardado en: {nombre_archivo_txt}[/bold green reverse]")

    return partidos_simulados

def simular_fecha():
    global partidos_manual_registrados 

    partidos_manual_registrados = cargar_json(ARCHIVO_PARTIDOS_MANUAL)
    if not isinstance(partidos_manual_registrados, list):
        partidos_manual_registrados = []


    while True:
        limpiar_pantalla()
        menu_principal_opciones = [
            "1. Simular Partidos por Fecha",
            "2. CRUD de Partidos Manuales",
            "0. Volver al Menú Principal"
        ]

        menu_content = Text()
        for i, opcion_texto in enumerate(menu_principal_opciones):
            color_idx = i % (len(RAINBOW_COLORS) - 1)
            if opcion_texto == "0. Volver al Menú Principal":
                color_idx = len(RAINBOW_COLORS) - 1
            menu_content.append(f"{opcion_texto}\n", style=RAINBOW_COLORS[color_idx])

        menu_panel = Panel(
            menu_content,
            title="[bold bright_white reverse]=== GESTIÓN DE PARTIDOS Y SIMULACIONES ===[/bold bright_white reverse]",
            title_align="center",
            expand=True,
            padding=(2, 5),
            width=80
        )
        console.print(menu_panel)

        opcion_principal = console.input("[bold white on blue]Seleccione una opción:[/bold white on blue] ").strip()

        if opcion_principal == "1":
            deporte_sim = seleccionar_deporte()
            if deporte_sim:
                equipos_disponibles = _cargar_equipos()
                fecha_simular = console.input("[bold white on blue]Ingrese la fecha a simular (ej. 'Fecha 1'):[/bold white on blue] ").strip()
                if fecha_simular:
                    nuevos_partidos_simulados = _simular_fecha_deporte_interna(deporte_sim, fecha_simular, equipos_disponibles)
                    if nuevos_partidos_simulados:
                        partidos_manual_registrados.extend(nuevos_partidos_simulados) 
                        _guardar_partidos_manual_en_json()
                else:
                    console.print("[bold red reverse]La fecha no puede estar vacía.[/bold red reverse]")
            console.input("[bold grey58 reverse]Presioná Enter para seguir...[/bold grey58 reverse]")

        elif opcion_principal == "2":
            partidos_manual_registrados = cargar_json(ARCHIVO_PARTIDOS_MANUAL)
            if not isinstance(partidos_manual_registrados, list):
                partidos_manual_registrados = []
            while True:
                limpiar_pantalla()
                crud_menu_opciones = [
                    "1. Crear Partido Manual",
                    "2. Buscar Partidos Manuales",
                    "3. Listar Todos los Partidos",
                    "4. Modificar Partido Manual",
                    "5. Eliminar Partido Manual",
                    "0. Volver al Menú Anterior"
                ]

                crud_menu_content = Text()
                for i, opcion_texto in enumerate(crud_menu_opciones):
                    color_idx = i % (len(RAINBOW_COLORS) - 1)
                    if opcion_texto == "0. Volver al Menú Anterior":
                        color_idx = len(RAINBOW_COLORS) - 1
                    crud_menu_content.append(f"{opcion_texto}\n", style=RAINBOW_COLORS[color_idx])

                crud_menu_panel = Panel(
                    crud_menu_content,
                    title="[bold bright_white reverse]=== GESTIÓN DE PARTIDOS MANUALES ===[/bold bright_white reverse]",
                    title_align="center",
                    expand=True,
                    padding=(2, 5),
                    width=80
                )
                console.print(crud_menu_panel)

                opcion_crud = console.input("[bold white on blue]Seleccione una opción:[/bold white on blue] ").strip()

                if opcion_crud == "1":
                    crear_partido_manual()
                elif opcion_crud == "2":
                    buscar_partidos_manual()
                elif opcion_crud == "3":
                    listar_partidos_manual()
                elif opcion_crud == "4":
                    modificar_partido_manual()
                elif opcion_crud == "5":
                    eliminar_partido_manual()
                elif opcion_crud == "0":
                    break
                else:
                    console.print("[bold red reverse]¡Ojo! Esa opción no va. Probá de nuevo, pibe.[/bold red reverse]")
                console.input("[bold grey58 reverse]Presioná Enter para seguir...[/bold grey58 reverse]")
        elif opcion_principal == "0":
            break
        else:
            console.print("[bold red reverse]¡Ojo! Esa opción no va. Probá de nuevo, pibe.[/bold red reverse]")
            console.input("[bold grey58 reverse]Presioná Enter para seguir...[/bold grey58 reverse]")


if __name__ == "__main__":
    simular_fecha()
