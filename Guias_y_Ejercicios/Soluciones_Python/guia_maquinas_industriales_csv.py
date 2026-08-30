"""Módulo de Referencia: Registro de Condiciones de Máquinas Industriales en CSV.

Universidad San Sebastián · Sede Patagonia
Taller de Programación II · Guía Ejercicio Integral CSV Máquinas Industriales

Mantiene el archivo datos/registro_maquinas.csv con delimitador ';' y codificación UTF-8.
Aplica validaciones estrictas y cálculo automático del estado operacional.
"""

import csv
from pathlib import Path
from typing import Final, TypedDict

CARPETA_DATOS: Final[Path] = Path("datos")
ARCHIVO_MAQUINAS: Final[Path] = CARPETA_DATOS / "registro_maquinas.csv"
DELIMITADOR: Final[str] = ";"
ENCODING: Final[str] = "utf-8"


class RegistroMaquina(TypedDict):
    fecha: str
    maquina: str
    temperatura: int
    horas_trabajo: int
    estado: str


def preparar_entorno() -> None:
    """Asegura la existencia de la carpeta 'datos'."""
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)


def inicializar_archivo_maquinas() -> None:
    """Crea el CSV con encabezados si no existe previamente."""
    preparar_entorno()
    if not ARCHIVO_MAQUINAS.exists():
        with ARCHIVO_MAQUINAS.open("w", newline="", encoding=ENCODING) as f:
            escritor = csv.writer(f, delimiter=DELIMITADOR, lineterminator="\n")
            escritor.writerow(["Fecha", "Maquina", "Temperatura", "Horas_Trabajo", "Estado"])
        print(f"✅ Archivo '{ARCHIVO_MAQUINAS.name}' inicializado con sus 5 encabezados.")


def evaluar_estado(temperatura: int, horas: int) -> str:
    """Determina automáticamente el estado según la matriz de reglas industriales.
    
    - Normal: Temp <= 70 °C y Horas <= 8.
    - Advertencia: Temp 71-90 °C o Horas 9-12.
    - Critico: Temp > 90 °C o Horas > 12.
    """
    if temperatura > 90 or horas > 12:
        return "Critico"
    elif (71 <= temperatura <= 90) or (9 <= horas <= 12):
        return "Advertencia"
    else:
        return "Normal"


def validar_revision(fecha: str, maquina: str, temp_str: str, horas_str: str) -> tuple[bool, str, int, int]:
    """Valida los campos según los criterios mínimos de la guía docente."""
    f_limpia = fecha.strip()
    m_limpia = maquina.strip()

    if not f_limpia:
        return False, "La fecha no puede quedar vacía.", 0, 0
    if not m_limpia:
        return False, "Debe ingresar el nombre o código de la máquina.", 0, 0

    try:
        temp = int(temp_str.strip())
        if temp < 0:
            return False, "La temperatura debe ser un entero mayor o igual a 0 °C.", 0, 0
    except ValueError:
        return False, "La temperatura debe ser un número entero válido.", 0, 0

    try:
        horas = int(horas_str.strip())
        if horas < 0 or horas > 24:
            return False, "Las horas de trabajo deben ser un número entero entre 0 y 24.", 0, 0
    except ValueError:
        return False, "Las horas de trabajo deben ser un número entero válido.", 0, 0

    return True, "Validación exitosa.", temp, horas


def registrar_revision(fecha: str, maquina: str, temp_str: str, horas_str: str) -> bool:
    """Valida, calcula el estado y anexa una revisión en modo Append ('a')."""
    inicializar_archivo_maquinas()

    valido, mensaje, temp, horas = validar_revision(fecha, maquina, temp_str, horas_str)
    if not valido:
        print(f"❌ Error de Validación: {mensaje} (Registro cancelado)")
        return False

    estado = evaluar_estado(temp, horas)

    with ARCHIVO_MAQUINAS.open("a", newline="", encoding=ENCODING) as f:
        escritor = csv.writer(f, delimiter=DELIMITADOR, lineterminator="\n")
        escritor.writerow([fecha.strip(), maquina.strip(), temp, horas, estado])

    print(f"✅ Revisión registrada: {maquina.strip()} | Temp: {temp}°C | Horas: {horas}h | Estado: {estado}")
    return True


def leer_registros() -> list[RegistroMaquina]:
    """Lee el CSV omitiendo la cabecera y deserializa los datos."""
    if not ARCHIVO_MAQUINAS.exists():
        return []

    registros: list[RegistroMaquina] = []
    with ARCHIVO_MAQUINAS.open("r", newline="", encoding=ENCODING) as f:
        lector = csv.reader(f, delimiter=DELIMITADOR)
        try:
            _encabezado = next(lector)
        except StopIteration:
            return []

        for numero_linea, fila in enumerate(lector, start=2):
            if len(fila) < 5:
                continue
            try:
                reg: RegistroMaquina = {
                    "fecha": fila[0].strip(),
                    "maquina": fila[1].strip(),
                    "temperatura": int(fila[2].strip()),
                    "horas_trabajo": int(fila[3].strip()),
                    "estado": fila[4].strip(),
                }
                registros.append(reg)
            except ValueError:
                print(f"⚠️ Advertencia: Fila {numero_linea} descartada por formato erróneo.")

    return registros


def mostrar_registros() -> None:
    """Imprime el listado ordenado distinguiendo los encabezados."""
    registros = leer_registros()
    print("\n" + "=" * 70)
    print("HISTORIAL DE REVISIONES DE MÁQUINAS INDUSTRIALES")
    print("=" * 70)

    if not registros:
        print("No existen revisiones registradas en el sistema.")
        return

    print(f"{'Fecha':<12}{'Máquina':<18}{'Temp (°C)':<12}{'Horas':<10}{'Estado':<12}")
    print("-" * 70)
    for r in registros:
        print(f"{r['fecha']:<12}{r['maquina']:<18}{r['temperatura']:<12}{r['horas_trabajo']:<10}{r['estado']:<12}")
    print("=" * 70)


def generar_resumen() -> None:
    """Calcula las estadísticas del parque industrial."""
    registros = leer_registros()
    print("\n" + "=" * 50)
    print("RESUMEN OPERACIONAL DE MÁQUINAS")
    print("=" * 50)

    if not registros:
        print("No hay datos para generar el resumen.")
        return

    total = len(registros)
    promedio_temp = sum(r["temperatura"] for r in registros) / total
    normales = sum(1 for r in registros if r["estado"].lower() == "normal")
    advertencias = sum(1 for r in registros if r["estado"].lower() == "advertencia")
    criticos = sum(1 for r in registros if r["estado"].lower() == "critico")

    print(f"• Cantidad total de revisiones: {total}")
    print(f"• Promedio de temperatura:     {promedio_temp:.1f} °C")
    print(f"• Registros en estado Normal:  {normales}")
    print(f"• Registros en Advertencia:    {advertencias}")
    print(f"• Registros en estado Crítico:  {criticos}")
    print("=" * 50)


def menu_maquinas() -> None:
    """Menú interactivo de consola."""
    inicializar_archivo_maquinas()
    while True:
        print("\n" + "=" * 45)
        print("SISTEMA DE MANTENIMIENTO INDUSTRIAL (CSV)")
        print("=" * 45)
        print("  1. Registrar nueva revisión de máquina")
        print("  2. Mostrar historial de revisiones")
        print("  3. Ver resumen estadístico operacional")
        print("  4. Salir")
        print("=" * 45)

        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            print("\n--- INGRESO DE REVISIÓN ---")
            f = input("Fecha (YYYY-MM-DD): ")
            m = input("Máquina (Código/Nombre): ")
            t = input("Temperatura (°C): ")
            h = input("Horas de Trabajo: ")
            registrar_revision(f, m, t, h)
        elif opcion == "2":
            mostrar_registros()
        elif opcion == "3":
            generar_resumen()
        elif opcion == "4":
            print("\nFinalizando programa de mantenimiento industrial.")
            break
        else:
            print("❌ Opción no válida. Ingrese un número entre 1 y 4.")


if __name__ == "__main__":
    menu_maquinas()
