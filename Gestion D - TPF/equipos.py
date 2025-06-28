import json  # Módulo para trabajar con archivos JSON
import os    # Módulo para trabajar con el sistema operativo, útil para limpiar pantalla
from json_utils import cargar_json, guardar_json



 # Creamos una instancia de Console para usar Rich
from rich.console import Console
from rich import print


console = Console()


# aca cargamos el json de equipos en una variable

RUTA_EQUIPOS = "data/equipos.json"
 

# Función para limpiar la consola 
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
def agregar_equipo():
    
    equipo = cargar_json(RUTA_EQUIPOS)
    
    print("============ Agregar Equipo ============")
    nombre = input("Ingrese el nombre del equipo: ").strip()
    deporte = input("Ingrese el deporte: ").strip()

    nuevo_equipo = {
        "nombre": nombre,
        "deporte": deporte,
        
    }

    equipo.append(nuevo_equipo)
    guardar_json(RUTA_EQUIPOS, equipo)
    print("Equipo agregado exitosamente.")
    input("Presione Enter para continuar...")
    
    
    
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000



def ver_equipos():
    equipo = cargar_json(RUTA_EQUIPOS)

    
    print ("=============ver equipos ===========")
    if not equipo:
    
        print("No hay equipos registrados.")                                                    
        input("Presione Enter para continuar...")
        return
    else:
        print("Lista de Equipos:")
        for i in equipo:
            print(f"Nombre: {i.get("nombre")}, ========  Deporte: {i.get('deporte')}")
    
    
    
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
    
def Buscar_equipo():
    equipos = cargar_json(RUTA_EQUIPOS)
    limpiar_pantalla()
    print("============ Buscar Equipo ============")
    buscar_nombre = input("Ingrese el nombre del equipo a buscar: ").strip().lower()

    for equipo in equipos:
        if equipo['nombre'].strip().lower() == buscar_nombre:
            print(f"Equipo encontrado: {equipo['nombre']}, Deporte: {equipo['deporte']}")
            return equipo

    print("Equipo no encontrado.")
    input("Presione Enter para continuar...")
    return None



# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000


def modificar_equipo():


    equipos = cargar_json(RUTA_EQUIPOS)
    print("============ Modificar Equipo ============")

    ver_equipos()
     
    equipo_editar = input("Ingrese el nombre del equipo a modificar: ").strip()
    
    
    for i in equipos:
            
            if i["nombre"].lower() == equipo_editar.lower() :
                print(f"Equipo encontrado: {i['nombre']}, Deporte: {i['deporte']}")
                
                nuevo_nombre = input("Ingrese el nuevo nombre del equipo: ").strip()
                nueva_disiplina = input("Ingrese la nueva disiplina: ").strip()
              
                if nuevo_nombre:
                    i["nombre"] = nuevo_nombre
                if nueva_disiplina:
                    i["deporte"] = nueva_disiplina
                    guardar_json(RUTA_EQUIPOS, equipos)
                    


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000

def eliminar_equipo():
    limpiar_pantalla()
    ver_equipos()
    
    equipos = cargar_json(RUTA_EQUIPOS)
    
    print("============ Eliminar Equipo ============")
    
    borrar_nombre = input("Ingrese el nombre del equipo a eliminar: ").strip().lower()
    for i in equipos [:]:
        if i["nombre"].lower().strip() == borrar_nombre:
            equipos.remove(i)
            guardar_json(RUTA_EQUIPOS, equipos)
            
            print(f"Equipo '{borrar_nombre}' eliminado exitosamente.")
            input("Presione Enter para continuar...")
            
            return
    print(f"Equipo '{borrar_nombre}' no encontrado.")
    input("Presione Enter para continuar...")
    
    
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
            


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000

def menu_equipos():
    
    print("============ Gestion de Equipos ============")
    while True:
        console.print("1. Agregar Equipo", style="#1E90FF")
        console.print("2. Ver Equipos" , style="#1EFF1E")
        console.print("3. Buscar Equipo", style="#C01E82")
        console.print("4. Modificar Equipo" , style="#BDBA27")
        console.print("5. Eliminar Equipo", style="#341AAA")
        console.print("6. Volver al Menu Principal", style="#F00C0C")

        opcion = input("Seleccione una opcion: ")

        if opcion == "x":
            print("Saliendo del menu de equipos...")
            break
            
        elif  opcion == "1":
            agregar_equipo()
        elif opcion == "2":
            ver_equipos()
        elif opcion == "3":
            Buscar_equipo()
        elif opcion == "4":
            modificar_equipo()
        elif opcion == "5":
            eliminar_equipo()
        elif opcion == "6":
            break
        else:
            input("Opcion no valida. Presione Enter para continuar...") 