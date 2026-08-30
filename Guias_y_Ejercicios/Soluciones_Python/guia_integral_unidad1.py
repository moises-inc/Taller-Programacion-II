"""Solución Modular Oficial — Guía Integral de Ejercicios Unidad 1.

Universidad San Sebastián · Sede Patagonia
Taller de Programación II · Unidad 1: Manejo y Gestión de Archivos

Implementa las soluciones de los 6 ejercicios:
- Ejercicio 1: Validar existencia de archivo y mostrar contenido
- Ejercicio 2: Solicitar datos con validación y guardar en CSV
- Ejercicio 3: Verificar archivo, crear encabezados si no existe y agregar
- Ejercicio 4: Funciones separadas para leer edades y calcular promedio
- Ejercicio 5: Leer archivo y buscar cliente por coincidencia de nombre
- Ejercicio 6: Menú interactivo coordinado en consola
"""

import csv
from pathlib import Path
from typing import Final


# Configuración del archivo de trabajo
ARCHIVO_CLIENTES_DEFAULT: Final[Path] = Path("clientes.csv")
DELIMITADOR_DEFAULT: Final[str] = ";"
ENCODING_DEFAULT: Final[str] = "utf-8"


# ============================================================================
# EJERCICIO 1: Validar existencia de archivo y mostrar su contenido
# ============================================================================

def validar_y_mostrar_archivo(ruta: Path = ARCHIVO_CLIENTES_DEFAULT) -> None:
    """Verifica si el archivo existe en disco y muestra su contenido en pantalla.

    Si no existe, imprime un mensaje de error controlado sin lanzar excepciones.
    """
    if not ruta.exists():
        print(f"Error: El archivo '{ruta}' no existe en el sistema de archivos.")
        return

    print(f"\n--- CONTENIDO DEL ARCHIVO '{ruta}' ---")
    try:
        with ruta.open("r", newline="", encoding=ENCODING_DEFAULT) as archivo:
            lector = csv.reader(archivo, delimiter=DELIMITADOR_DEFAULT)
            lineas = list(lector)
            if not lineas:
                print("El archivo existe pero está completamente vacío.")
                return

            for numero_linea, fila in enumerate(lineas, start=1):
                print(f"Línea {numero_linea:02d}: {DELIMITADOR_DEFAULT.join(fila)}")
    except Exception as error:
        print(f"Error al intentar leer el archivo: {error}")


# ============================================================================
# EJERCICIO 2: Función que solicite datos al usuario y los guarde en CSV
# ============================================================================

def solicitar_datos_usuario() -> tuple[str, int, str] | None:
    """Solicita nombre, edad y ciudad al usuario con validación estricta de edad."""
    nombre = input("Ingrese nombre del cliente: ").strip()
    ciudad = input("Ingrese ciudad: ").strip()
    edad_raw = input("Ingrese edad: ").strip()

    if not nombre or not ciudad:
        print("Error de validación: El nombre y la ciudad no pueden estar vacíos.")
        return None

    try:
        edad = int(edad_raw)
        if edad <= 0 or edad > 125:
            print("Error de validación: La edad debe ser un entero positivo realista (1-125).")
            return None
    except ValueError:
        print("Error de validación: La edad debe ser un valor numérico entero.")
        return None

    return nombre, edad, ciudad


def guardar_cliente_csv(
    nombre: str,
    edad: int,
    ciudad: str,
    ruta: Path = ARCHIVO_CLIENTES_DEFAULT,
) -> None:
    """Guarda un registro de cliente en el archivo CSV en modo Append ('a')."""
    with ruta.open("a", newline="", encoding=ENCODING_DEFAULT) as archivo:
        escritor = csv.writer(archivo, delimiter=DELIMITADOR_DEFAULT, lineterminator="\n")
        escritor.writerow([nombre, edad, ciudad])
    print(f"Cliente '{nombre}' guardado exitosamente en '{ruta}'.")


# ============================================================================
# EJERCICIO 3: Verificar archivo, crear si no existe con encabezados y agregar
# ============================================================================

def asegurar_archivo_con_encabezados(ruta: Path = ARCHIVO_CLIENTES_DEFAULT) -> None:
    """Crea el archivo CSV con su fila de encabezados si todavía no existe."""
    if not ruta.exists():
        with ruta.open("w", newline="", encoding=ENCODING_DEFAULT) as archivo:
            escritor = csv.writer(archivo, delimiter=DELIMITADOR_DEFAULT, lineterminator="\n")
            escritor.writerow(["Nombre", "Edad", "Ciudad"])
        print(f"Archivo '{ruta}' no existía. Creado con encabezado ['Nombre', 'Edad', 'Ciudad'].")


def agregar_cliente_integral(ruta: Path = ARCHIVO_CLIENTES_DEFAULT) -> None:
    """Asegura la existencia del archivo con encabezados y agrega un nuevo cliente."""
    asegurar_archivo_con_encabezados(ruta)
    datos = solicitar_datos_usuario()
    if datos is not None:
        nombre, edad, ciudad = datos
        guardar_cliente_csv(nombre, edad, ciudad, ruta)


# ============================================================================
# EJERCICIO 4: Funciones separadas para leer edades y calcular promedio
# ============================================================================

def leer_edades_desde_archivo(ruta: Path = ARCHIVO_CLIENTES_DEFAULT) -> list[int]:
    """Lee exclusivamente la columna de edades desde el archivo CSV.

    Aplica principio de Responsabilidad Única: solo lee y deserializa enteros.
    """
    if not ruta.exists():
        return []

    edades: list[int] = []
    with ruta.open("r", newline="", encoding=ENCODING_DEFAULT) as archivo:
        lector = csv.reader(archivo, delimiter=DELIMITADOR_DEFAULT)
        try:
            _encabezado = next(lector)  # Omitir fila de encabezados
        except StopIteration:
            return []

        for fila in lector:
            if len(fila) >= 2 and fila[1].strip():
                try:
                    edad = int(fila[1].strip())
                    edades.append(edad)
                except ValueError:
                    continue  # Ignorar registros corruptos

    return edades


def calcular_promedio(valores: list[int]) -> float:
    """Calcula el promedio aritmético a partir de una lista numérica.

    Aplica principio de Responsabilidad Única: función matemática pura.
    """
    if not valores:
        return 0.0
    return sum(valores) / len(valores)


def mostrar_promedio_edades(ruta: Path = ARCHIVO_CLIENTES_DEFAULT) -> None:
    """Coordina la lectura de edades y presentación del promedio."""
    edades = leer_edades_desde_archivo(ruta)
    if not edades:
        print(f"\nNo se encontraron registros de edad válidos en '{ruta}'.")
        return

    promedio = calcular_promedio(edades)
    print(f"\nTotal de clientes analizados: {len(edades)}")
    print(f"Promedio de edad calculado: {promedio:.2f} años.")


# ============================================================================
# EJERCICIO 5: Leer archivo y buscar un nombre específico
# ============================================================================

def buscar_cliente_por_nombre(
    nombre_buscado: str,
    ruta: Path = ARCHIVO_CLIENTES_DEFAULT,
) -> list[list[str]]:
    """Busca registros que coincidan con el nombre (búsqueda insensible a mayúsculas)."""
    termino = nombre_buscado.strip().lower()
    if not termino or not ruta.exists():
        return []

    coincidencias: list[list[str]] = []
    with ruta.open("r", newline="", encoding=ENCODING_DEFAULT) as archivo:
        lector = csv.reader(archivo, delimiter=DELIMITADOR_DEFAULT)
        try:
            _encabezado = next(lector)
        except StopIteration:
            return []

        for fila in lector:
            if fila and termino in fila[0].lower():
                coincidencias.append(fila)

    return coincidencias


def ejecutar_busqueda_interactiva(ruta: Path = ARCHIVO_CLIENTES_DEFAULT) -> None:
    """Solicita un nombre por teclado y muestra las coincidencias encontradas."""
    termino = input("\nIngrese el nombre del cliente a buscar: ").strip()
    if not termino:
        print("Error: Debe ingresar un texto para realizar la búsqueda.")
        return

    resultados = buscar_cliente_por_nombre(termino, ruta)
    print("\n--- RESULTADOS DE BÚSQUEDA ---")
    if not resultados:
        print(f"No se encontró ningún cliente que coincida con '{termino}'.")
        return

    for fila in resultados:
        nombre, edad, ciudad = fila[0], fila[1], fila[2]
        print(f"• Nombre: {nombre:<20} | Edad: {edad:<3} años | Ciudad: {ciudad}")


# ============================================================================
# EJERCICIO 6: Menú de opciones interactivo con funciones
# ============================================================================

def menu_principal(ruta: Path = ARCHIVO_CLIENTES_DEFAULT) -> None:
    """Menú interactivo de consola en ciclo continuo que integra los ejercicios 1 a 5."""
    asegurar_archivo_con_encabezados(ruta)

    while True:
        print("\n" + "=" * 45)
        print("SISTEMA DE CLIENTES — GUÍA INTEGRAL UNIDAD 1")
        print("=" * 45)
        print("  1. Ver contenido del archivo")
        print("  2. Agregar nuevo cliente")
        print("  3. Mostrar promedio de edad")
        print("  4. Buscar cliente por nombre")
        print("  5. Salir")
        print("=" * 45)

        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            validar_y_mostrar_archivo(ruta)
        elif opcion == "2":
            agregar_cliente_integral(ruta)
        elif opcion == "3":
            mostrar_promedio_edades(ruta)
        elif opcion == "4":
            ejecutar_busqueda_interactiva(ruta)
        elif opcion == "5":
            print(f"\nFinalizando programa. Datos preservados en '{ruta}'.")
            break
        else:
            print("Opción inválida. Ingrese un número entre 1 y 5.")


if __name__ == "__main__":
    try:
        menu_principal()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSesión finalizada por el usuario.")
