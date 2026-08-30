"""Módulo de práctica básica de manejo de archivos TXT en Python.

Universidad San Sebastián · Sede Patagonia
Taller de Programación II · Unidad 1

Implementa las operaciones de las guías docentes:
- Preparación de rutas relativas con pathlib.Path
- Creación segura en modo 'a' (Append)
- Escritura y persistencia de líneas con salto explícito
- Lectura secuencial y limpieza con strip()
- Conteo y numeración de registros con enumerate()
- Modularización en funciones y menú interactivo de consola
"""

from pathlib import Path
from typing import Final


# Constantes de ruta para garantizar que el proyecto cree datos/registro.txt
CARPETA_DATOS: Final[Path] = Path("datos")
ARCHIVO_REGISTRO: Final[Path] = CARPETA_DATOS / "registro.txt"


def preparar_archivo() -> None:
    """Crea la carpeta 'datos' si no existe y asegura el archivo 'registro.txt'."""
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    with ARCHIVO_REGISTRO.open("a", encoding="utf-8"):
        pass


def agregar_linea(texto: str) -> None:
    """Escribe una línea en el archivo usando modo 'a' y agregando el salto de línea."""
    preparar_archivo()
    linea_limpia = texto.strip()
    if not linea_limpia:
        return
    with ARCHIVO_REGISTRO.open("a", encoding="utf-8") as archivo:
        archivo.write(f"{linea_limpia}\n")


def agregar_saludo(nombre: str) -> None:
    """Registra un saludo formateado para un usuario."""
    nombre_limpio = nombre.strip()
    if nombre_limpio:
        agregar_linea(f"Hola, {nombre_limpio}")


def agregar_producto(producto: str) -> None:
    """Registra el nombre de un producto en una línea nueva."""
    producto_limpio = producto.strip()
    if producto_limpio:
        agregar_linea(producto_limpio)


def agregar_lote_productos(productos: list[str]) -> None:
    """Registra una lista de productos en una misma operación."""
    preparar_archivo()
    with ARCHIVO_REGISTRO.open("a", encoding="utf-8") as archivo:
        for p in productos:
            p_limpio = p.strip()
            if p_limpio:
                archivo.write(f"{p_limpio}\n")


def solicitar_y_agregar_dato() -> None:
    """Solicita un dato textual por teclado y lo anexa al archivo."""
    while True:
        dato = input("Ingrese un dato o producto para registrar: ").strip()
        if dato:
            agregar_linea(dato)
            print(f"Registro guardado exitosamente: '{dato}'")
            break
        print("Error: el dato no puede estar vacío.")


def leer_datos() -> list[str]:
    """Lee el archivo secuencialmente y retorna la lista de líneas limpias."""
    if not ARCHIVO_REGISTRO.exists():
        return []
    with ARCHIVO_REGISTRO.open("r", encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def contar_registros() -> int:
    """Retorna la cantidad total de registros guardados en el archivo TXT."""
    return len(leer_datos())


def mostrar_datos() -> None:
    """Muestra todas las líneas almacenadas sin saltos dobles."""
    registros = leer_datos()
    print("\n--- CONTENIDO DE 'datos/registro.txt' ---")
    if not registros:
        print("El archivo está vacío o aún no contiene registros.")
        return
    for linea in registros:
        print(linea)


def mostrar_registros_numerados() -> None:
    """Muestra los registros anteponiendo una numeración correlativa desde 1."""
    registros = leer_datos()
    print("\n--- REGISTROS NUMERADOS ---")
    if not registros:
        print("No existen registros para mostrar.")
        return
    for numero, linea in enumerate(registros, start=1):
        print(f"[{numero:02d}] {linea}")
    print(f"Total acumulado: {len(registros)} registros.")


def menu_principal() -> None:
    """Menú interactivo básico que coordina la captura y visualización."""
    preparar_archivo()
    while True:
        print("\n" + "=" * 45)
        print("SISTEMA DE GESTIÓN BÁSICA DE ARCHIVOS TXT")
        print("=" * 45)
        print("  1. Agregar dato")
        print("  2. Mostrar datos guardados")
        print("  3. Mostrar datos numerados y total")
        print("  4. Salir")
        print("=" * 45)

        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            solicitar_y_agregar_dato()
        elif opcion == "2":
            mostrar_datos()
        elif opcion == "3":
            mostrar_registros_numerados()
        elif opcion == "4":
            print("\nFinalizando programa. La información permanece en 'datos/registro.txt'.")
            break
        else:
            print("Opción inválida. Ingrese un número del 1 al 4.")


if __name__ == "__main__":
    try:
        menu_principal()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSesión interrumpida por el usuario. Salida segura.")
