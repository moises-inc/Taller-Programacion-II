"""SIMULACRO DE CONTROL 1 DE LABORATORIO (TALLER DE PROGRAMACIÓN II).

Universidad San Sebastián · Sede Patagonia
Fecha Simulada: Jueves 3 de Septiembre de 2026 (17:00 hrs · Sala A306)
Tiempo Estimado: 60 minutos | Ponderación: 10% de la Nota Final

==============================================================================
ENUNCIADO DEL EVALUACIÓN PRÁCTICA:
==============================================================================
Desarrolle un sistema en Python para la gestión de préstamos de equipos en los
laboratorios de la universidad, aplicando persistencia en archivos CSV y JSON,
validación de datos con Try-Except y funciones modulares desacopladas.

REQUERIMIENTOS TÉCNICOS:
1. Usar pathlib.Path para definir la carpeta 'datos' y el archivo 'prestamos.csv'.
2. El archivo CSV debe usar punto y coma ';' como delimitador y codificación UTF-8.
3. Formato del CSV: ID_Prestamo;Alumno;RUT;Equipo;Cantidad;Estado
4. Implementar las siguientes funciones:
   a) asegurar_archivo_prestamos(): Crea datos/prestamos.csv con encabezados si no existe.
   b) registrar_prestamo(): Solicita Alumno, RUT, Equipo y Cantidad. Valida que la cantidad
      sea un entero > 0 y que Alumno y RUT no estén vacíos. Anexa la fila con ID incremental
      y estado 'Prestado'.
   c) devolver_equipo(): Pide el ID del préstamo, cambia su estado a 'Devuelto' y reescribe
      el archivo CSV completo en modo 'w'.
   d) exportar_resumen_json(): Lee los préstamos del CSV y genera el archivo 'datos/resumen_prestamos.json'
      con la cuenta de préstamos activos y el detalle formateado con indent=4.
   e) menu_principal(): Bucle continuo while True para interactuar con el sistema.
==============================================================================
"""

import csv
import json
from pathlib import Path
from typing import Final, TypedDict

# Definición de rutas y constantes
CARPETA_DATOS: Final[Path] = Path("datos")
ARCHIVO_CSV_PRESTAMOS: Final[Path] = CARPETA_DATOS / "prestamos.csv"
ARCHIVO_JSON_RESUMEN: Final[Path] = CARPETA_DATOS / "resumen_prestamos.json"
DELIMITADOR: Final[str] = ";"
ENCODING: Final[str] = "utf-8"


class Prestamo(TypedDict):
    id_prestamo: int
    alumno: str
    rut: str
    equipo: str
    cantidad: int
    estado: str


# ============================================================================
# 1. INICIALIZACIÓN DEFENSIVA Y PERSISTENCIA CSV
# ============================================================================

def asegurar_archivo_prestamos() -> None:
    """Crea la carpeta 'datos' y el archivo CSV con su encabezado si no existe."""
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    if not ARCHIVO_CSV_PRESTAMOS.exists():
        with ARCHIVO_CSV_PRESTAMOS.open("w", newline="", encoding=ENCODING) as f:
            escritor = csv.writer(f, delimiter=DELIMITADOR, lineterminator="\n")
            escritor.writerow(["ID_Prestamo", "Alumno", "RUT", "Equipo", "Cantidad", "Estado"])
        print(f"✅ Archivo '{ARCHIVO_CSV_PRESTAMOS.name}' inicializado con sus encabezados.")


def leer_prestamos() -> list[Prestamo]:
    """Lee el CSV, omite el encabezado y deserializa los registros como diccionarios."""
    if not ARCHIVO_CSV_PRESTAMOS.exists():
        return []

    prestamos: list[Prestamo] = []
    with ARCHIVO_CSV_PRESTAMOS.open("r", newline="", encoding=ENCODING) as f:
        lector = csv.reader(f, delimiter=DELIMITADOR)
        try:
            _encabezado = next(lector)
        except StopIteration:
            return []

        for numero_linea, fila in enumerate(lector, start=2):
            if len(fila) < 6:
                continue
            try:
                p: Prestamo = {
                    "id_prestamo": int(fila[0].strip()),
                    "alumno": fila[1].strip(),
                    "rut": fila[2].strip(),
                    "equipo": fila[3].strip(),
                    "cantidad": int(fila[4].strip()),
                    "estado": fila[5].strip(),
                }
                prestamos.append(p)
            except ValueError:
                print(f"⚠️ Advertencia: Fila {numero_linea} descartada por formato incorrecto.")

    return prestamos


# ============================================================================
# 2. OPERACIONES DE NEGOCIO (REGISTRAR, DEVOLVER, EXPORTAR)
# ============================================================================

def registrar_prestamo() -> None:
    """Solicita datos por teclado con validación defensiva y los guarda en el CSV."""
    asegurar_archivo_prestamos()
    print("\n--- REGISTRO DE NUEVO PRÉSTAMO DE EQUIPO ---")

    alumno = input("Nombre completo del alumno: ").strip()
    rut = input("RUT del alumno (ej: 20123456-7): ").strip()
    equipo = input("Nombre o código del equipo: ").strip()
    cantidad_raw = input("Cantidad a prestar: ").strip()

    # Validaciones defensivas de entrada
    if not alumno or not rut or not equipo:
        print("❌ Error de Validación: Los campos Alumno, RUT y Equipo no pueden estar vacíos.")
        return

    try:
        cantidad = int(cantidad_raw)
        if cantidad <= 0:
            print("❌ Error de Validación: La cantidad prestada debe ser un entero estrictamente mayor a 0.")
            return
    except ValueError:
        print("❌ Error de Validación: La cantidad debe ser un valor numérico entero.")
        return

    # Generación de ID incremental
    prestamos_existentes = leer_prestamos()
    siguiente_id = max([p["id_prestamo"] for p in prestamos_existentes], default=0) + 1

    # Escritura en modo Append
    with ARCHIVO_CSV_PRESTAMOS.open("a", newline="", encoding=ENCODING) as f:
        escritor = csv.writer(f, delimiter=DELIMITADOR, lineterminator="\n")
        escritor.writerow([siguiente_id, alumno, rut, equipo, cantidad, "Prestado"])

    print(f"🎉 Préstamo registrado con éxito [ID: {siguiente_id:03d}] para {alumno}.")


def devolver_equipo() -> None:
    """Cambia el estado de un préstamo a 'Devuelto' y sincroniza el CSV completo en modo 'w'."""
    prestamos = leer_prestamos()
    if not prestamos:
        print("\n⚠️ No hay préstamos registrados para realizar devoluciones.")
        return

    print("\n--- DEVOLUCIÓN DE EQUIPO ---")
    id_raw = input("Ingrese el ID del préstamo a devolver: ").strip()
    try:
        id_buscado = int(id_raw)
    except ValueError:
        print("❌ Error: El ID debe ser un número entero.")
        return

    encontrado = False
    for p in prestamos:
        if p["id_prestamo"] == id_buscado:
            if p["estado"].lower() == "devuelto":
                print(f"ℹ️ El préstamo ID {id_buscado:03d} ya figuraba como 'Devuelto'.")
                return
            p["estado"] = "Devuelto"
            encontrado = True
            break

    if not encontrado:
        print(f"❌ No se encontró ningún préstamo con el ID {id_buscado:03d}.")
        return

    # Reescribir el CSV completo en modo 'w'
    with ARCHIVO_CSV_PRESTAMOS.open("w", newline="", encoding=ENCODING) as f:
        escritor = csv.writer(f, delimiter=DELIMITADOR, lineterminator="\n")
        escritor.writerow(["ID_Prestamo", "Alumno", "RUT", "Equipo", "Cantidad", "Estado"])
        for p in prestamos:
            escritor.writerow([p["id_prestamo"], p["alumno"], p["rut"], p["equipo"], p["cantidad"], p["estado"]])

    print(f"✅ Devuelto: El préstamo ID {id_buscado:03d} ha sido actualizado a 'Devuelto'.")


def exportar_resumen_json() -> None:
    """Genera el resumen de préstamos y lo exporta a 'datos/resumen_prestamos.json'."""
    prestamos = leer_prestamos()
    if not prestamos:
        print("\n⚠️ No existen préstamos para exportar a JSON.")
        return

    prestamos_activos = [p for p in prestamos if p["estado"].lower() == "prestado"]
    total_equipos_prestados = sum(p["cantidad"] for p in prestamos_activos)

    resumen = {
        "titulo_reporte": "Resumen de Préstamos de Laboratorio USS",
        "total_registros_historicos": len(prestamos),
        "total_prestamos_activos": len(prestamos_activos),
        "total_equipos_en_uso": total_equipos_prestados,
        "detalle_activos": prestamos_activos,
    }

    with ARCHIVO_JSON_RESUMEN.open("w", encoding=ENCODING) as f:
        json.dump(resumen, f, indent=4, ensure_ascii=False)

    print(f"📊 Resumen JSON exportado exitosamente en '{ARCHIVO_JSON_RESUMEN.name}'.")
    print(f"   • Préstamos Activos: {len(prestamos_activos)} | Equipos en Uso: {total_equipos_prestados}")


def mostrar_reporte_prestamos() -> None:
    """Muestra una vista ordenada de todos los préstamos en pantalla."""
    prestamos = leer_prestamos()
    print("\n" + "=" * 75)
    print("REPORTE GENERAL DE PRÉSTAMOS DE LABORATORIO")
    print("=" * 75)

    if not prestamos:
        print("No existen préstamos registrados.")
        return

    print(f"{'ID':<6}{'Alumno':<22}{'RUT':<14}{'Equipo':<18}{'Cant.':<7}{'Estado':<10}")
    print("-" * 75)
    for p in prestamos:
        print(f"{p['id_prestamo']:<6:03d}{p['alumno']:<22}{p['rut']:<14}{p['equipo']:<18}{p['cantidad']:<7}{p['estado']:<10}")
    print("=" * 75)


# ============================================================================
# 3. INTERFAZ Y CONTROLADOR PRINCIPAL
# ============================================================================

def menu_principal() -> None:
    """Menú interactivo de consola para el control de laboratorio."""
    asegurar_archivo_prestamos()

    while True:
        print("\n" + "=" * 50)
        print("SISTEMA DE PRESTAMOS DE LABORATORIO — USS")
        print("=" * 50)
        print("  1. Ver todos los préstamos")
        print("  2. Registrar nuevo préstamo de equipo")
        print("  3. Devolver equipo prestado (Modificar ID)")
        print("  4. Exportar resumen estadístico a JSON")
        print("  5. Salir")
        print("=" * 50)

        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            mostrar_reporte_prestamos()
        elif opcion == "2":
            registrar_prestamo()
        elif opcion == "3":
            devolver_equipo()
        elif opcion == "4":
            exportar_resumen_json()
        elif opcion == "5":
            print("\nFinalizando sistema de préstamos. Éxito en el Control 1 de Laboratorio.")
            break
        else:
            print("❌ Opción inválida. Ingrese un número entre 1 y 5.")


if __name__ == "__main__":
    try:
        menu_principal()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSesión cancelada por el usuario. Salida segura.")
