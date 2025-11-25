



def guardar_puntaje(nombre, puntaje, archivo="data/puntajes.txt"):
    """
    Funcion para guardar los puntajes en un archivo.
    ENTRADA:
    nombre: str, nombre del jugador
    puntaje: int, puntaje del jugador
    archivo: str, ruta del archivo de puntajes
    SALIDA:
    Sin salida.
    
    """
    with open(archivo, "a") as puntajes_file:
        puntajes_file.write(f"{nombre},{puntaje}\n")

def cargar_puntajes(archivo="data/puntajes.txt"):
    """
    Funcion para recuperar los puntajes guardados desde un archivo.
    ENTRADA:
    archivo: str, ruta del archivo de puntajes
    SALIDA:
    list: lista de tuplas con los puntajes (nombre, puntaje)
    """
    puntajes = []

    with open(archivo, "r") as puntajes_file:
            for linea in puntajes_file:
                nombre, valor = linea.strip().split(",")
                puntajes.append((nombre, int(valor)))

    puntajes.sort(key=lambda puntaje: puntaje[1], reverse=True)
    return puntajes[:5]

