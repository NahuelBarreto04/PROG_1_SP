from .menu import mostrar_textos, dibujar_botones_menu,manejar_click_menu
from .configuraciones import *
from .juego import iniciar_juego_sudoku, dibujar_tablero_sudoku, manejar_eventos_sudoku, dibujar_boton_reinicio, controlar_boton_reinicio, dibujar_puntaje
from .utilidades import dibujar_boton_volver
from .puntajes import cargar_puntajes




def controlar_pantallas(pantalla_actual, evento, estado_juego):
    """
    Controla la pantalla a mostrar según la pantalla actual.
    Llama a la función correspondiente para cada pantalla.

    ENTRADA:
    pantalla_actual: str, nombre de la pantalla actual ("menu", "juego", etc.)
    evento: pygame.event.Event, evento actual del bucle principal
    estado_juego: dict, estado actual del juego

    SALIDA:
    no devuelve nada, solo llama a la función adecuada para mostrar la pantalla
    """
    if pantalla_actual == "menu":
        ejecutar_pantalla_menu(evento, estado_juego)
    elif pantalla_actual == "juego":
        ejecutar_pantalla_juego(evento, estado_juego)
    elif pantalla_actual == "puntaje":
        ejecutar_pantalla_puntajes(get_pantalla_pygame(), evento)





def ejecutar_pantalla_menu(evento, estado_juego):
    """
    Muestra el menu principal.
    Carga la imagen de fondo, dibuja los textos y los botones,
    y actualiza la pantalla con todo eso.
    Usa funciones de otros archivos para cada parte.

    ENTRADA:
    no recibe parametros
    SALIDA:
    no devuelve nada , solo actualiza lo que se ve en pantalla
    """
    pantalla = get_pantalla_pygame()
    imagen_fondo = pygame.transform.scale(estado_juego["IMAGENES"]["fondo_menu"], (pantalla.get_width(), pantalla.get_height()))
    pantalla.blit(imagen_fondo, (0, 0))
    mostrar_textos(pantalla)
    dibujar_botones_menu(pantalla)
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        manejar_click_menu(evento.pos, estado_juego)
    pygame.display.flip()




def ejecutar_pantalla_juego(evento, estado_juego):
    """
    Muestra la pantalla de juego.
    Dibuja el tablero, las celdas y el puntaje,
    y actualiza la pantalla con todo eso.

    ENTRADA:
    evento: evento actual del bucle principal
    estado_juego: diccionario con el estado actual del juego
    SALIDA:
    no devuelve nada , solo actualiza lo que se ve en pantalla
    """

    pantalla = get_pantalla_pygame()
    pantalla.fill((0, 0, 0))
    if not estado_juego["juego_iniciado"]:
        iniciar_juego_sudoku(pantalla, estado_juego)

    dibujar_tablero_sudoku(pantalla, estado_juego)
    manejar_eventos_sudoku(evento, estado_juego)
    rect_boton_reinicio = dibujar_boton_reinicio(get_pantalla_pygame(), estado_juego["IMAGENES"])
    controlar_boton_reinicio(evento, rect_boton_reinicio, estado_juego)
    dibujar_puntaje(pantalla, estado_juego)

    rect_volver = dibujar_boton_volver(get_pantalla_pygame())
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if rect_volver.collidepoint(evento.pos):
            estado_juego["juego_iniciado"] = False
            set_pantalla_actual("menu")

    pygame.display.flip()


def ejecutar_pantalla_puntajes(pantalla, evento):
    """
    Muestra la pantalla de puntajes.
    Dibuja los puntajes guardados y un botón para volver al menú,
    y actualiza la pantalla con todo eso.

    ENTRADA:
    pantalla: superficie donde se dibuja la pantalla
    evento: evento actual del bucle principal

    SALIDA:
    no devuelve nada , solo actualiza lo que se ve en pantalla
    """
    fuente = pygame.font.SysFont("Arial", 40)
    fuente_texto = pygame.font.SysFont("Arial", 30)

    puntajes = cargar_puntajes()
    pantalla.fill((30, 30, 30))

    titulo = fuente.render("Mejores 5 Puntajes", True, (255,255,255))
    pantalla.blit(titulo, (pantalla.get_width()//2 - titulo.get_width()//2, 50))
    
    y = 150
    if len(puntajes) == 0:
        texto = fuente_texto.render("No hay puntajes aún", True, (200,200,200))
        pantalla.blit(texto, (pantalla.get_width()//2 - texto.get_width()//2, y))
    else:
        for nombre, valor in puntajes:
            linea = fuente_texto.render(f"{nombre} — {valor}", True, (255,255,255))
            pantalla.blit(linea, (pantalla.get_width()//2 - linea.get_width()//2, y))
            y += 40




    rect_volver = dibujar_boton_volver(pantalla)
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if rect_volver.collidepoint(evento.pos):
            set_pantalla_actual("menu")

    pygame.display.flip()