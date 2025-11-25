import pygame
from .configuraciones import *


BOTONES = []

boton_musica = pygame.Rect(20, 20, 100, 40)




def mostrar_textos(pantalla)->None:
    """
    muestra el titulo "BUSCAMINAS" en el menu
    ENTRADA:
    pantalla:pygame, donde se dibuja el texto
    SALIDA:
    none
    """
    fuente = pygame.font.SysFont("arial", pantalla.get_height() // 8)
    texto = fuente.render("Sudoku", True, (255, 102, 102))

    padding = 20
    ancho = texto.get_width() + padding
    alto = texto.get_height() + padding
    x = (pantalla.get_width() - ancho) // 2
    y = 30

    rect_fondo = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, (100, 100, 100), rect_fondo)  # Fondo gris como los botones

    pantalla.blit(texto, (x + padding // 2, y + padding // 2))





def dibujar_botones_menu(pantalla)->None:
    """
    dibuja los botones del menu principal en la pantalla

    ENTRADA:
    pantalla:pygame, donde se dibujan los botones
    SALIDA:
    none
    """
    BOTONES.clear()
    textos = ["Jugar", f"Nivel: ({get_dificultad_actual()})", "Ver Puntajes", f"Resoluciones ({configuracion_juego['resolucion_actual']})", "Salir"]


    pygame.draw.rect(pantalla, (200, 200, 200), boton_musica)
    fuente = pygame.font.SysFont("arial", 24)
    texto = fuente.render("Musica", True, (0, 0, 0))
    pantalla.blit(texto, (boton_musica.x + 20, boton_musica.y + 8))

    for i in range(len(textos)):
        w = pantalla.get_width() // 4
        h = pantalla.get_height() // 12
        x = (pantalla.get_width() - w) // 2
        y = pantalla.get_height() // 3 + i * (h + 20)


        fuente = pygame.font.SysFont("arial", h // 2)
        if "Resoluciones" in  textos[i]:
             fuente = pygame.font.SysFont("arial", h // 3)

        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(pantalla, (100, 100, 100), rect)
        texto = fuente.render(textos[i], True, (255, 255, 255)) 
        pantalla.blit(texto, (x + (w - texto.get_width()) // 2, y + (h - texto.get_height()) // 2))

        BOTONES.append(rect) 

def manejar_click_menu(pos:tuple[int,int], estado_juego:dict)->None:
    """
    detecta si el click fue sobre algun boton
    ENTRADA:
    pos:tupla con la posicion (X,y) del click del mouse
    estado_juego: dict con el estado actual del juego
    SALIDA:
    none
    """
    if boton_musica.collidepoint(pos):
        if estado_juego["musica_pausada"]:
            pygame.mixer.music.unpause()
            estado_juego["musica_pausada"] = False
        else:
            pygame.mixer.music.pause()
            estado_juego["musica_pausada"] = True
    else:
        pygame.mixer.music.pause()
        estado_juego["musica_pausada"] = True

    for i in range(len(BOTONES)):
        if BOTONES[i].collidepoint(pos):
            ejecutar_botones_menu(i, estado_juego)

def ejecutar_botones_menu(indice:int, estado_juego:dict)-> None:
    """
    ejecuta la accion segun el rectangulo clickeado

    ENTRADA:
    indice:int, indica la accion a ejecutar
    estado_juego: dict con el estado actual del juego
    SALIDA:
    none 
    """
    if indice == 0:
        estado_juego["perdio"] = False
        set_pantalla_actual("juego")
    elif indice == 1:
        cambiar_dificultad()
    elif indice == 2:
        set_pantalla_actual("puntaje")
    elif indice == 3:
        cambiar_resolucion()
    elif indice == 4:
        salir(estado_juego)







def salir(estado_juego:dict)->None:
    """
    cierra el pygame y termina el programa
    ENTRADA:
    ninguna
    SALIDA:
    ninguna(finaliza la ejecucion)
    """
    estado_juego["Running"] = False
    print("Saliendo del juego...")
    