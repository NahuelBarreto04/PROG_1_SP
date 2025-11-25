import pygame
#Archivos de configuracion_juegoes
#DICCIONARIO DE CONFIGURACION
configuracion_juego = {
    "resolucion_actual": "800x600",
    "dificultad_actual": "facil",
    "pantalla_actual": "menu",
    "PANTALLA:": None
}

#Pantalla pygame

def get_pantalla_pygame():
    """Obtiene la Pantalla pygame
    ENTRADA:
    Sin entrada
    Salida:
    pantalla pygame
    """
    return configuracion_juego["PANTALLA"]


#Resolución
def get_resolucion_actual() -> tuple:
    """
    Obtiene la resolucion actual de la pantalla
    Entrada:
    Sin entrada
    Salida:
    tupla con ancho (int) y alto (int) de la pantalla
    """
    partes = configuracion_juego["resolucion_actual"].split("x")
    ancho = int(partes[0])
    alto = int(partes[1])
    return ancho, alto

def set_resolucion_actual(valor:str) -> None: 
    """
    establece la resolución actual en forma de string
    ENTRADA:
    valor: string de la resolución actual
    Salida:
    Sin salida
    """
    configuracion_juego["resolucion_actual"] = valor
    print(f"Nueva resolución: {configuracion_juego["resolucion_actual"]}")

    if configuracion_juego["PANTALLA"]:
        ancho,alto = get_resolucion_actual()
        configuracion_juego["PANTALLA"] = pygame.display.set_mode((ancho, alto), pygame.SCALED)

def cambiar_resolucion() -> None:
    """Alterna entre las resoluciones para el boton del menu.
    Entrada:
    Sin entrada
    Salida:
    Sin salida, se usa para configurar el diccionario
    """
    if configuracion_juego["resolucion_actual"] == "800x600":
        set_resolucion_actual("1024x768")
    elif configuracion_juego["resolucion_actual"] == "1024x768":
        set_resolucion_actual("620x480")
    else:
        set_resolucion_actual("800x600")



#DIFICULTAD
def get_dificultad_actual():
    """Devuelve la dificultad actual.
    Entrada:
    Sin entrada
    SALIDA:
    string: devuelve la dificultad actual en forma de string (facil, normal, dificil)
    """
    return configuracion_juego["dificultad_actual"]


def cambiar_dificultad():
    """Alterna entre las dificultades: fácil, media, difícil."""
    if configuracion_juego["dificultad_actual"] == "facil":
        configuracion_juego["dificultad_actual"] = "medio"
    elif configuracion_juego["dificultad_actual"] == "medio":
        configuracion_juego["dificultad_actual"] = "dificil"
    else:
        configuracion_juego["dificultad_actual"] = "facil"



#Pantalla actual
def get_pantalla_actual():
    """
    obtiene la pantalla actual (menu, juego, puntaje)
    ENTRADA:
    Sin entrada
    Salida:
    string: pantalla actual del juego
    """
    return configuracion_juego["pantalla_actual"]

def set_pantalla_actual(pantalla_actual: str) -> None:
    """
    setea la pantalla actual en el diccionario
    ENTRADA:
    pantalla_actual: str (menu,juego,puntajes)
    SALIDA:
    Sin salida
    """
    configuracion_juego["pantalla_actual"] = pantalla_actual





