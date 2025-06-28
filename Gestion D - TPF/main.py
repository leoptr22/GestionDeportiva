import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Importamos las funciones de los módulos principales.
from partidos_torneo import simular_torneo
from equipos import menu_equipos
from jugadores import menu_jugadores
from partidos_fecha import simular_fecha             
from partidos_torneo import ver_torneo_simulado

# Rich
console = Console()

def limpiar_pantalla():
    """Limpia la pantalla de la consola, ¡para que no se amontone todo!"""
    os.system("cls" if os.name == "nt" else "clear")

def menu_principal():
    """Este es el menú principal de la aplicación, donde arranca toda la gestión deportiva."""
    while True:
        limpiar_pantalla()

       
        menu_items = [
            Text("1. Gestión de Equipos", style="bold reverse green"),
            Text("2. Gestión de Jugadores", style="bold reverse blue"),
            Text("3. Gestión de Partidos", style="bold reverse magenta"),
            Text("4. Simular torneo completo", style="bold reverse yellow"),
            Text("5. Ver Torneo Simulado", style="bold reverse cyan"),
            Text("6. Salir del sistema", style="bold reverse white on black"),
        ]

        menu_content = Text("============¡Bienvenidos a Gestión Deportiva!===========\n\n", style="bold yellow")
        for item in menu_items:
            menu_content.append(item)
            menu_content.append("\n")

        menu_panel = Panel(
            menu_content,
            title="[bold bright_white]Menú Principal[/bold bright_white]",
            title_align="center",
            border_style="bold hot_pink",
            expand=False,
            padding=(1, 2)
        )
        console.print(menu_panel)

        opcion = console.input("[bold light_sky_blue1]Elegí una opción: [/bold light_sky_blue1]").strip()

        if opcion == "1":
            menu_equipos()
        elif opcion == "2":
            menu_jugadores()
        elif opcion == "3":
            simular_fecha()
            console.input("[grey58]Presioná Enter para volver al menú...[/grey58]")

        elif opcion == "4":
            simular_torneo()
            console.input("[bold grey58]Presioná Enter para seguir, maquinola...[/bold grey58]")
        elif opcion == "5":
            ver_torneo_simulado()
            console.input("[bold grey58]Presioná Enter para seguir, maquinola...[/bold grey58]")
        elif opcion == "6":
            console.print("[bold green]¡Listo! Nos vemos la próxima. ¡Gracias por usar el sistema![/bold green]")
            break
        else:
            console.print("[bold red]¡Ojo! Esa opción no va. Probá de nuevo, pibe.[/bold red]")
            console.input("[bold grey58]Presioná Enter para seguir, maquinola...[/bold grey58]")

if __name__ == "__main__":
    menu_principal()