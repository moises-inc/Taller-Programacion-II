"""Módulo de Práctica Intensiva I/O: Archivos TXT y CSV.

Universidad San Sebastián · Sede Patagonia
Taller de Programación II · Sprint de Entrenamiento Solemnes 2026

Diseñado para práctica interactiva de laboratorio y prueba escrita.
Cubre:
1. Creación defensiva de rutas con pathlib.Path
2. Modos de apertura 'a', 'r', 'w'
3. Limpieza con strip() y split(';')
4. Lectura/Escritura con módulo csv (newline='')
5. Consumo de encabezados con next()
6. Validación de datos con try-except ValueError
7. Operaciones CRUD completas y reescritura atómica
"""

import csv
from pathlib import Path
from typing import Final, TypedDict

# Rutas de trabajo en el Espacio del Estudiante
CARPETA_DATOS: Final[Path] = Path("datos")
ARCHIVO_TXT: Final[Path] = CARPETA_DATOS / "bitacora_practica.txt"
ARCHIVO_CSV: Final[Path] = CARPETA_DATOS / "inventario_laboratorio.csv"
DELIMITADOR_CSV: Final[str] = ";"
ENCODING: Final[str] = "utf-8"


class ItemInventario(TypedDict):
    id: int
    equipo: str
    laboratorio: str
    cantidad: int
    estado: str


# ============================================================================
# DESAFÍO 1: Creación Defensiva de Directorio y Archivos
# ============================================================================

def preparar_entorno_trabajo() -> None:
    """Crea la carpeta 'datos' si no existe y verifica las rutas de trabajo."""
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    print(f"✅ Entorno preparado. Carpeta de datos: '{CARPETA_DATOS.resolve()}'")


# ============================================================================
# DESAFÍO 2: Persistencia TXT (Modo 'a', f-strings y \n)
# ============================================================================

def registrar_evento_txt(evento: str) -> None:
    """Anexa un evento de bitácora al archivo TXT en modo Append ('a')."""
    preparar_entorno_trabajo()
    texto_limpio = evento.strip()
    if not texto_limpio:
        print("⚠️ Advertencia: No se puede registrar un evento vacío.")
        return

    with ARCHIVO_TXT.open("a", encoding=ENCODING) as archivo:
        archivo.write(f"{texto_limpio}\n")

    print(f"✅ Evento escrito en '{ARCHIVO_TXT.name}': {texto_limpio}")


def leer_bitacora_txt() -> list[str]:
    """Lee secuencialmente el archivo TXT procesando cada línea con .strip()."""
    if not ARCHIVO_TXT.exists():
        print(f"⚠️ El archivo '{ARCHIVO_TXT.name}' aún no existe.")
        return []

    eventos: list[str] = []
    with ARCHIVO_TXT.open("r", encoding=ENCODING) as archivo:
        for linea in archivo:
            limpia = linea.strip()
            if limpia:
                eventos.append(limpia)

    return eventos


# ============================================================================
# DESAFÍO 3: CSV con Módulo Estándar (newline='', csv.writer, csv.reader)
# ============================================================================

def inicializar_inventario_csv() -> None:
    """Crea inventario_laboratorio.csv con su encabezado solo si no existe."""
    preparar_entorno_trabajo()
    if not ARCHIVO_CSV.exists():
        with ARCHIVO_CSV.open("w", newline="", encoding=ENCODING) as archivo:
            escritor = csv.writer(archivo, delimiter=DELIMITADOR_CSV, lineterminator="\n")
            escritor.writerow(["ID", "Equipo", "Laboratorio", "Cantidad", "Estado"])
        print(f"✅ Archivo '{ARCHIVO_CSV.name}' creado con encabezado ['ID', 'Equipo', 'Laboratorio', 'Cantidad', 'Estado'].")


def agregar_equipo_csv(equipo: str, laboratorio: str, cantidad: int, estado: str = "Operativo") -> None:
    """Valida los campos y anexa un equipo al inventario calculando el siguiente ID."""
    inicializar_inventario_csv()
    items = leer_inventario_csv()
    siguiente_id = max([item["id"] for item in items], default=0) + 1

    with ARCHIVO_CSV.open("a", newline="", encoding=ENCODING) as archivo:
        escritor = csv.writer(archivo, delimiter=DELIMITADOR_CSV, lineterminator="\n")
        escritor.writerow([siguiente_id, equipo.strip(), laboratorio.strip(), cantidad, estado.strip()])

    print(f"✅ Equipo registrado [ID {siguiente_id:02d}]: {equipo} ({laboratorio})")


def leer_inventario_csv() -> list[ItemInventario]:
    """Lee el CSV omitiendo el encabezado con next() y convierte tipos a int."""
    if not ARCHIVO_CSV.exists():
        return []

    inventario: list[ItemInventario] = []
    with ARCHIVO_CSV.open("r", newline="", encoding=ENCODING) as archivo:
        lector = csv.reader(archivo, delimiter=DELIMITADOR_CSV)
        try:
            _encabezado = next(lector)  # Consumir primera fila
        except StopIteration:
            return []

        for numero_fila, fila in enumerate(lector, start=2):
            if len(fila) < 5:
                continue
            try:
                item: ItemInventario = {
                    "id": int(fila[0].strip()),
                    "equipo": fila[1].strip(),
                    "laboratorio": fila[2].strip(),
                    "cantidad": int(fila[3].strip()),
                    "estado": fila[4].strip(),
                }
                inventario.append(item)
            except ValueError:
                print(f"⚠️ Fila {numero_fila} descartada por valores inválidos: {fila}")

    return inventario


# ============================================================================
# DESAFÍO 4: Búsquedas case-insensitive y Operaciones CRUD
# ============================================================================

def buscar_equipos(criterio: str) -> list[ItemInventario]:
    """Filtra los equipos que coincidan en nombre o laboratorio (insensible a mayúsculas)."""
    termino = criterio.strip().lower()
    if not termino:
        return []

    items = leer_inventario_csv()
    return [
        item for item in items
        if termino in item["equipo"].lower() or termino in item["laboratorio"].lower() or termino in item["estado"].lower()
    ]


def actualizar_estado_equipo(id_equipo: int, nuevo_estado: str) -> bool:
    """Actualiza el estado de un equipo y reescribe atómicamente el CSV en modo 'w'."""
    items = leer_inventario_csv()
    encontrado = False

    for item in items:
        if item["id"] == id_equipo:
            item["estado"] = nuevo_estado.strip()
            encontrado = True
            break

    if not encontrado:
        print(f"❌ Error: No se encontró ningún equipo con ID {id_equipo}.")
        return False

    # Reescribir el archivo completo en modo 'w'
    with ARCHIVO_CSV.open("w", newline="", encoding=ENCODING) as archivo:
        escritor = csv.writer(archivo, delimiter=DELIMITADOR_CSV, lineterminator="\n")
        escritor.writerow(["ID", "Equipo", "Laboratorio", "Cantidad", "Estado"])
        for item in items:
            escritor.writerow([item["id"], item["equipo"], item["laboratorio"], item["cantidad"], item["estado"]])

    print(f"✅ Estado del ID {id_equipo} actualizado a '{nuevo_estado}' exitosamente.")
    return True


def mostrar_reporte_inventario() -> None:
    """Muestra una tabla de inventario en consola alineada adecuadamente."""
    items = leer_inventario_csv()
    print("\n" + "=" * 65)
    print("REPORTE DE INVENTARIO DE LABORATORIOS")
    print("=" * 65)

    if not items:
        print("El inventario se encuentra vacío.")
        return

    print(f"{'ID':<5}{'Equipo':<25}{'Laboratorio':<18}{'Cant.':<8}{'Estado':<10}")
    print("-" * 65)
    for item in items:
        print(f"{item['id']:<5}{item['equipo']:<25}{item['laboratorio']:<18}{item['cantidad']:<8}{item['estado']:<10}")
    print("=" * 65)
    print(f"Total de items en inventario: {len(items)}")


# ============================================================================
# PRUEBAS AUTOMÁTICAS E INTERFAZ DE PRÁCTICA
# ============================================================================

def ejecutar_suite_practica() -> None:
    """Ejecuta una demostración de control para validar el correcto funcionamiento."""
    print("🚀 INICIANDO SUITE DE PRÁCTICA INTENSIVA I/O...\n")

    # 1. Probar TXT
    registrar_evento_txt("Inicio de sesión de laboratorio - Alumno: Moisés")
    registrar_evento_txt("Calibración de osciloscopios completada")
    bitacora = leer_bitacora_txt()
    print(f"📋 Eventos en bitacora TXT ({len(bitacora)}): {bitacora}\n")

    # 2. Probar CSV
    inicializar_inventario_csv()
    agregar_equipo_csv("Osciloscopio Digital", "Lab A306", 5, "Operativo")
    agregar_equipo_csv("Generador de Funciones", "Lab A306", 3, "En Mantencion")
    agregar_equipo_csv("Multimetro Fluke 87V", "Lab A308", 10, "Operativo")

    # 3. Mostrar reporte y buscar
    mostrar_reporte_inventario()

    coincidencias = buscar_equipos("a306")
    print(f"\n🔍 Coincidencias para 'a306': {len(coincidencias)} equipos hallados.")

    # 4. Actualizar estado
    actualizar_estado_equipo(2, "Operativo")
    mostrar_reporte_inventario()


if __name__ == "__main__":
    ejecutar_suite_practica()
