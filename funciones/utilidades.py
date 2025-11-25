import pygame


TAM_CELDA = 40
MARGEN = 1

SONIDOS = {
    "musica_menu": "sonidos/musica_menu.mp3",
    # "musica_puntajes":"sonidos/musica_puntajes.mp3",
    # "sonido_derrota": "sonidos/derrota.mp3",
    # "sonido_victoria":"sonidos/victoria.mp3"
}



def cargar_imagenes():
    """Funcion para cargar las imagenes del juego en un diccionario global

    ENTRADA:
    sin entrada
    SALIDA:
    sin salida, funcion de modificacion
    """
    imagenes = {
    "reinicio": pygame.image.load("imagenes/reinicio.png"),
    # "fondo_puntajes": pygame.image.load("imagenes/fondos/fondo_puntajes.jpg"),
    "fondo_menu": pygame.image.load("imagenes/fondo_menu.jpeg"),
    }
    for nombre_img in imagenes:
        if nombre_img != "fondo_menu":
            img_superficie = imagenes[nombre_img]
            imagenes[nombre_img] = pygame.transform.scale(img_superficie,(TAM_CELDA, TAM_CELDA))

    return imagenes




def dibujar_boton_volver(pantalla):
    """
    Funcion del boton para regresar a la pantalla anterior

    ENTRADA:
    pantalla: pantalla de pygame 
    evento: eventos pygame para manejar el click
    SALIDA:
    True: porque el evento colisiono con el boton
    False: el evento no colisiono con la posicion del boton
    """
    fuente = pygame.font.SysFont("arial", 25)
    texto = fuente.render("Volver al menu", True, (255, 255, 255))
    ancho = texto.get_width() + 20
    alto = texto.get_height() + 10
    x = 20
    y = pantalla.get_height() - alto - 10
    rect_volver = pygame.Rect(x, y, ancho, alto)


    pygame.draw.rect(pantalla, (80, 80, 80), rect_volver)
    pantalla.blit(texto, (x + 10, y + 5))

    return rect_volver