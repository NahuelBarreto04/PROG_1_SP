import random
import pygame
import copy
from .configuraciones import *
from .puntajes import guardar_puntaje

pygame.mixer.init()

sonidos = {
    "valido": pygame.mixer.Sound("sonidos/valido.mp3"),
    "no_valido": pygame.mixer.Sound("sonidos/no_valido.mp3"),
}


COLORES = {
    "fondo": (30, 30, 30),
    "linea": (255, 255, 255),
    "linea_gruesa": (255, 255, 255),
    "celda_normal": (60, 60, 60),
    "celda_fija": (90, 90, 90),
    "celda_seleccionada": (70, 120, 200),
    "celda_error": (180, 50, 50),
    "texto_fijo": (255, 255, 255),
    "texto_usuario": (0, 220, 255),
    "error": (255, 0, 0),
}

CELDA_SUDOKU = {"valor": 0, "rect": None, "fija": False, "no_valido":False}


def generar_tablero_sudoku(filas: int, columnas: int) -> list:
    """Genera una matriz vacía 9x9 con la estructura de celdas"""
    tablero = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            celda = CELDA_SUDOKU.copy()
            fila.append(celda)
        tablero.append(fila)
    return tablero


def generar_sudoku_completo() -> list:
    """Genera un tablero de Sudoku completo válido.
    Entrada:
    sin entrada
    Salida:
    lista: con el tablero completo de sudoku
    """
    tablero = []
    for fila in range(9):
        fila_lista = []
        for col in range(9):
            fila_lista.append({"valor": 0})
        tablero.append(fila_lista)

    def llenar():
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col]["valor"] == 0:
                    numeros = list(range(1, 10))
                    random.shuffle(numeros)

                    for n in numeros:
                        if validar_numero(tablero, fila, col, n):
                            tablero[fila][col]["valor"] = n
                            if llenar():
                                return True
                            tablero[fila][col]["valor"] = 0

                    return False
        return True

    llenar()
    return tablero


def aplicar_dificultad_por_region(tablero_completo:list, dificultad: str) -> list:
    """Elimina valores por región dejando x visibles por dificultad por región.
    
    ENTRADA:
    tablero_completo: lista, tablero completo de sudoku
    dificultad: str, dificultad actual del juego
    SALIDA:
    lista: tablero de sudoku con valores eliminados según dificultad
    """
    if dificultad == "facil":
        visibles = 5
    elif dificultad == "medio":
        visibles = 4
    else:
        visibles = 3

    tablero = copy.deepcopy(tablero_completo)

    for fila_region in range(0, 9, 3):        
        for col_region in range(0, 9, 3):     

            indices = []
            for i in range(3):
                for j in range(3):
                    fila = fila_region + i
                    col = col_region + j
                    indices.append((fila, col))

            random.shuffle(indices)
            # dejar visibles los primeros y poner valor 0 al resto
            for f, c in indices[visibles:]:
                tablero[f][c]["valor"] = 0

    return tablero

def mostrar_tablero(tablero: list) -> None:
    """Funcion para mostrar el tablero en consola
    Entrada:
    tablero: lista, tablero de sudoku
    Salida:
    sin salida, solo imprime en consola 
    """
    for fila in tablero:
        for celda in fila:
            print(celda["valor"], end=" ")
        print()

def iniciar_juego_sudoku(pantalla, estado_juego: dict) -> None:
    """Inicia un nuevo juego de Sudoku.
    Genera un nuevo tablero y configura el estado del juego.
    ENTRADA:
    pantalla: pantalla pygame
    estado_juego: dict, estado actual del juego
    SALIDA:
    none, solo modifica el estado del juego
    """

    estado_juego["gano"] = False
    estado_juego["juego_iniciado"] = True
    estado_juego["puntaje"] = 0

    filas, columnas = 9, 9
    dificultad = get_dificultad_actual()

    sudoku_completo = generar_sudoku_completo()
    mostrar_tablero(sudoku_completo)

    puzzle = aplicar_dificultad_por_region(sudoku_completo, dificultad)

    tablero = generar_tablero_sudoku(filas, columnas)

    for f in range(9):
        for c in range(9):
            val = puzzle[f][c]["valor"]
            tablero[f][c]["valor"] = val
            tablero[f][c]["fija"] = (val != 0)
            tablero[f][c]["no_valido"] = False

    ancho_disp = pantalla.get_width() - 100
    alto_disp = pantalla.get_height() - 200
    tam_celda = min(ancho_disp // 9, alto_disp // 9)
    ancho_tablero = columnas * tam_celda
    alto_tablero = filas * tam_celda
    offset_x = (pantalla.get_width() - ancho_tablero) // 2
    offset_y = (pantalla.get_height() - alto_tablero) // 2

    for f in range(filas):
        for c in range(columnas):
            x = offset_x + c * tam_celda
            y = offset_y + f * tam_celda
            tablero[f][c]["rect"] = pygame.Rect(x, y, tam_celda, tam_celda)

    estado_juego["tablero"] = tablero
    estado_juego["tam_celda"] = tam_celda
    estado_juego["offset"] = (offset_x, offset_y)




def validar_numero(tablero: list, fila: int, columna: int, numero:int) -> bool:
    """
    Funcion para validar si un numero se puede colocar en una celda del sudoku

    ENTRADA:
    tablero: lista, tablero de sudoku
    fila: int, fila de la celda
    columna: int, columna de la celda
    numero: int, numero a validar
    SALIDA:
    bool, True si es valido, False si no lo es
    """
    valido = True
    
    for c in range(9):
        if c != columna and tablero[fila][c]["valor"] == numero:
            valido = False

    for f in range(9):
        if f != fila and tablero[f][columna]["valor"] == numero:
            valido = False

    # Región 3x3
    region_fila = (fila // 3) * 3
    region_col = (columna // 3) * 3

    for f in range(region_fila, region_fila + 3):
        for c in range(region_col, region_col + 3):
            if not (f == fila and c == columna) and tablero[f][c]["valor"] == numero:
                valido = False

    return valido 


def dibujar_tablero_sudoku(pantalla, estado_juego:dict) -> None:
    """
    Funcion para dibujar el tablero de sudoku en pantalla

    Entrada:
    pantalla: pantalla pygame
    estado_juego: dict, estado actual del juego
    Salida:
    none, solo dibuja en pantalla
    """
    tablero = estado_juego["tablero"]
    tam = estado_juego["tam_celda"]
    offset_x, offset_y = estado_juego["offset"]
    fuente = pygame.font.SysFont("arial", tam // 2)

    fila_sel, col_sel = estado_juego.get("celda_seleccionada", (None, None))

    for fila in range(9):
        for col in range(9):
            celda = tablero[fila][col]
            rect = celda["rect"]

            if (fila, col) == (fila_sel, col_sel):
                color_fondo = COLORES["celda_seleccionada"]
            elif celda["fija"]:
                color_fondo = COLORES["celda_fija"]
            elif celda["no_valido"] == True:
                color_fondo = COLORES["celda_error"]
            else:
                color_fondo = COLORES["celda_normal"]

            pygame.draw.rect(pantalla, color_fondo, rect)

            valor = celda["valor"]
            if valor != 0:
                if celda["fija"]:
                    color_texto = COLORES["texto_fijo"]
                elif celda["no_valido"] == True:
                    color_texto = COLORES["error"]
                else:
                    color_texto = COLORES["texto_usuario"]
                texto = fuente.render(str(valor), True, color_texto)
                pantalla.blit(
                    texto,
                    (rect.x + (tam - texto.get_width()) // 2,
                     rect.y + (tam - texto.get_height()) // 2)
                )

            # Bordes finos entre celdas
            pygame.draw.rect(pantalla, COLORES["linea"], rect, 1)

    for i in range(10):
        y = offset_y + i * tam
        x = offset_x + i * tam

        #Linea gruesa cada 3 celdas
        if i in (0, 3, 6, 9):
            grosor = 3
        else:
            grosor = 1

        #Horizontal
        pygame.draw.line(
            pantalla, COLORES["linea_gruesa"],
            (offset_x, y), (offset_x + 9*tam, y), grosor
        )

        #Vertical
        pygame.draw.line(
            pantalla, COLORES["linea_gruesa"],
            (x, offset_y), (x, offset_y + 9*tam), grosor
        )




def obtener_fila_columna(pos, tablero:list) -> tuple[int,int]:
    """Funcion para obtener fila y columna del click
    
    ENTRADA: 
    pos: posicion del evento
    tablero: lista tablero del juego
    SALIDA:
    tuple, con fila y columna seleccionada
    """
    x, y = pos
    for f in range(len(tablero)):
        for c in range(len(tablero[0])):
            if tablero[f][c]["rect"].collidepoint(x, y):
                return f, c
    return -1, -1






def manejar_eventos_sudoku(evento, estado_juego):
    """Funcion para manejar eventos en juego
    
    ENTRADA:
    evento: evento pygame
    estado_juego: dict, estado actual del juego
    SALIDA:
    none, solo modifica el estado del juego
    """

    
    tablero = estado_juego["tablero"]

    if evento.type == pygame.MOUSEBUTTONDOWN:
        fila, col = obtener_fila_columna(evento.pos, tablero)
        if fila != -1:
            estado_juego["celda_seleccionada"] = (fila, col)

    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_r:
            resetear_juego(estado_juego)

        fila_sel, col_sel = estado_juego.get("celda_seleccionada")
        if fila_sel is not None:
            celda = tablero[fila_sel][col_sel]

            if not celda["fija"]:
                if evento.key == pygame.K_0 or evento.key == pygame.K_DELETE or evento.key == pygame.K_BACKSPACE:
                    celda["valor"] = 0
                    celda["no_valido"] = False
                    revalidar_celdas_no_validas(estado_juego)

                else:
                    numero = 0
                    if not evento.unicode.isdigit():
                        pass
                    else:
                        numero = int(evento.unicode)

                        
                    if 1 <= numero <= 9:
                        validar_puntaje(fila_sel, col_sel, numero, estado_juego, celda)
                        revalidar_celdas_no_validas(estado_juego)
                        
                        if not validar_numero(tablero, fila_sel, col_sel, numero):
                            sonidos["no_valido"].play()

                        if verificar_region_completa(tablero, fila_sel, col_sel):
                            sonidos["valido"].play()
                        
                        if verificar_tablero_completo(tablero):
                            estado_juego["gano"] = True
                            sonidos["valido"].play()
                            print("¡Has completado el Sudoku!")
                            estado_juego["pedir_nombre"] = True
                        
                        if estado_juego["pedir_nombre"]:
                            nombre = pedir_nombre(get_pantalla_pygame())
                            estado_juego["nombre_jugador"] = nombre
                            estado_juego["pedir_nombre"] = False
                            guardar_puntaje(nombre, estado_juego["puntaje"])
                            estado_juego["nombre_jugador"] = ""
                            set_pantalla_actual("menu")



def revalidar_celdas_no_validas(estado_juego:dict) -> None:
    """
    Revalida todas las celdas marcadas como no válidas en el tablero.
    ENTRADA:
    estado_juego: dict, estado actual del juego
    SALIDA:
    none, solo modifica el estado del juego
    """
    
    tablero = estado_juego["tablero"]

    for f in range(9):
        for c in range(9):
            celda = tablero[f][c]

            if celda["valor"] == 0:
                celda["no_valido"] = False
                continue

            numero = celda["valor"]
            if validar_numero(tablero, f, c, numero):
                celda["no_valido"] = False
            else:
                celda["no_valido"] = True





def dibujar_boton_reinicio(pantalla, fuente: pygame.font.Font) -> pygame.Rect:
    """
    Muestra el texto 'Reinicio' con un pequeño fondo detrás.
    Retorna el rect del fondo para detectar clics.
    ENTRADA:
    pantalla: pygame, donde se dibuja el texto
    fuente: pygame.font.Font, fuente para el texto
    SALIDA:
    pygame.Rect: rectángulo del botón de reinicio

    """
    fuente = pygame.font.SysFont("arial", pantalla.get_height() // 22)
    texto = fuente.render("Reiniciar", True, (255, 255, 255))
    rect_texto = texto.get_rect()

    x = pantalla.get_width() // 2 - rect_texto.width // 2
    y = 40

    rect_texto.x = x
    rect_texto.y = y

    # Fondo un poco más grande que el texto
    padding = 10
    rect_fondo = pygame.Rect(
        rect_texto.x - padding,
        rect_texto.y - padding,
        rect_texto.width + padding * 2,
        rect_texto.height + padding * 2
    )

    pygame.draw.rect(pantalla, (50, 50, 50), rect_fondo)

    pantalla.blit(texto, rect_texto)

    return rect_fondo

def controlar_boton_reinicio(evento, rect_reinicio, estado_juego:dict)-> None:
    """
    detecta si el jugador toca el boton de reinicio
    ENTRADa:
    evento: pygame, el evento actual
    rect_reinicio:pygame , rectangulo que define el area del boton de reiniciar
    estado_juego:dict, estado actual del juego
    SALIDA:
    sin salida, solo modifica el estado del juego
    """
    if evento is not None and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if rect_reinicio.collidepoint(evento.pos):
            resetear_juego(estado_juego)




def resetear_juego(estado_juego:dict)-> None:
    """
    reinicia el juego y su estado del juego para iniciar un nuevo juego

    ENTRADA:
    estado_juego: diccionario 
    SALIDA:
    none, solo modifica el estado del juego
    """
    estado_juego["juego_iniciado"] = False
    estado_juego["gano"] = False




def dibujar_puntaje(pantalla, estado_juego):
    """
    Dibuja el puntaje actual en la pantalla.
    ENTRADA:
    pantalla: pantalla pygame
    estado_juego: dict, estado actual del juego
    SALIDA:
    Sin salida, solo dibuja en pantalla"""

    font = pygame.font.SysFont("arial", 25)
    texto = font.render(f"Puntaje: {estado_juego['puntaje']:04d}", True, (255,255,255))

    pantalla.blit(texto, (80, 40))


def validar_puntaje(fila:int, columna:int, numero:int, estado_juego:dict, celda:dict) -> None:
    """
    Valida el numero ingresado y actualiza el puntaje del jugador.
    ENTRADA:
    fila: int, fila de la celda
    columna: int, columna de la celda
    numero: int, numero ingresado
    estado_juego: dict, estado actual del juego
    celda: dict, celda actual
    SALIDA:
    Sin salida, solo modifica el estado del juego
    """

    tablero = estado_juego["tablero"]

    if tablero[fila][columna]["fija"]:
        return

    if validar_numero(tablero, fila, columna, numero):
        celda["valor"] = numero
        celda["no_valido"] = False


        if verificar_region_completa(tablero, fila, columna):
            estado_juego["puntaje"] += 9

        if verificar_tablero_completo(tablero):
            estado_juego["puntaje"] += 81

    else:
        celda["valor"] = numero
        estado_juego["puntaje"] -= 1
        celda["no_valido"] = True



def verificar_tablero_completo(tablero:list) -> bool:
    """
    Verifica si el tablero está completo (sin celdas vacías).
    ENTRADA:
    tablero: lista, tablero de sudoku
    SALIDA:
    bool: True si el tablero está completo, False si no lo está
    """
    
    completo = True
    for f in range(9):
        for c in range(9):
            if tablero[f][c]["valor"] == 0 or not validar_numero(tablero, f, c, tablero[f][c]["valor"]):
                completo = False
                break
    return completo

def verificar_region_completa(tablero: list, fila:int, columna:int) -> bool:
    """
    Verifica si la región 3x3 que contiene la celda (fila, columna) está completa.
    ENTRADA:
    tablero: lista, tablero de sudoku
    fila: int, fila de la celda
    columna: int, columna de la celda
    SALIDA:
    bool: True si la región está completa, False si no lo está
    """

    region_f = (fila // 3) * 3
    region_c = (columna // 3) * 3
    completa = True
    for f in range(region_f, region_f + 3):
        for c in range(region_c, region_c + 3):
            if tablero[f][c]["valor"] == 0 or not validar_numero(tablero, f, c, tablero[f][c]["valor"]):
                completa = False
                break
    return completa


def pedir_nombre(pantalla) -> str:
    """
    Pide al jugador que ingrese su nombre.
    ENTRADA:
    pantalla: pantalla pygame
    SALIDA:
    str: nombre ingresado por el jugador
    """
    nombre = ""
    font = pygame.font.SysFont("arial", 40)

    escribiendo = True
    while escribiendo:
        pantalla.fill((30, 30, 30))

        texto = font.render("Ingresa tu nombre:", True, (255,255,255))
        pantalla.blit(texto, (50, 50))

        entrada = font.render(nombre, True, (0,255,255))
        pantalla.blit(entrada, (50, 120))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nombre != "":
                        escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 12:
                        nombre += evento.unicode

    return nombre
