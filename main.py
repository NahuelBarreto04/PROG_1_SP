import pygame
from funciones import configuraciones
from funciones.pantallas import controlar_pantallas
from funciones.utilidades import cargar_imagenes
from funciones.configuraciones import configuracion_juego
pygame.init()
pygame.font.init()
pygame.display.set_caption("Sudoku")
COLOR_FONDO = (54, 54, 54)
ANCHO_INICIAL, ALTO_INICIAL = configuraciones.get_resolucion_actual()
PANTALLA = pygame.display.set_mode((ANCHO_INICIAL, ALTO_INICIAL), pygame.SCALED)
# configuraciones.set_pantalla_pygame(PANTALLA)
configuracion_juego["PANTALLA"] = PANTALLA
reloj = pygame.time.Clock()
IMAGENES = cargar_imagenes()
COLOR_FONDO = (54, 54, 54)
pygame.mixer.music.load("sonidos/musica_menu.mp3")
pygame.mixer.music.play(-1)

estado_juego = {
    "Running": True,
    "nombre_jugador": "",
    "pedir_nombre": False,
    "juego_iniciado": False,
    "gano": False,
    "puntaje": 0,
    "inicio_timer": None,
    "tablero": None,
    "solucion": None,
    "celda_seleccionada": (None, None),  # (fila, columna),
    "IMAGENES":IMAGENES,
    "musica_pausada": False,
}



while estado_juego["Running"]:
    """
    bucle principal de el juego
    
    -muestra las pantallas("menu","juego","puntajes")
    -reproduce la musica correspondiente
    -pide el nombre del jugador en caso de victoria
    -verifica si el jugador gana o pierde
    
    ENTRADA:
    Sin entrada
    SALIDA:
    Sin salida
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            estado_juego["Running"] = False
            # pygame.mixer.music.stop()
        
        controlar_pantallas(configuraciones.get_pantalla_actual(), evento, estado_juego)


        # pygame.display.update()
        reloj.tick(60)

pygame.quit()