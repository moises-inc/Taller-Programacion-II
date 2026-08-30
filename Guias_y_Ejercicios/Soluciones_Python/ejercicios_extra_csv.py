"""Módulo de Referencia: Solución Unificada de Ejercicios Extra CSV (2.6, 2.7, 2.8).

Universidad San Sebastián · Sede Patagonia
Taller de Programación II · Ejercicios Docentes CSV

Incluye:
- Ejercicio 2.6: Gestor de Productos (datos/productos_extra.csv)
- Ejercicio 2.7: Gestor de Sensores e Inspección de Rangos Físicos (datos/mediciones_sensores.csv)
- Ejercicio 2.8: Gestor de Mantenciones con Estampa de Fecha (datos/bitacora_mantenciones.csv)
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import Final

CARPETA_DATOS: Final[Path] = Path("datos")
ENCODING: Final[str] = "utf-8"


def preparar_directorio() -> None:
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)


# ============================================================================
# EJERCICIO 2.6: GESTOR DE PRODUCTOS
# ============================================================================

ARCHIVO_PRODUCTOS: Final[Path] = CARPETA_DATOS / "productos_extra.csv"

def crear_archivo_productos() -> None:
    preparar_directorio()
    if not ARCHIVO_PRODUCTOS.exists():
        with ARCHIVO_PRODUCTOS.open("w", newline="", encoding=ENCODING) as f:
            escritor = csv.writer(f, delimiter=",")
            escritor.writerow(["Producto", "Precio", "Stock"])
        print(f"✅ Archivo '{ARCHIVO_PRODUCTOS.name}' creado con sus encabezados.")

def registrar_producto(nombre: str, precio: float, stock: int) -> bool:
    crear_archivo_productos()
    if not nombre.strip() or precio < 0 or stock < 0:
        print("❌ Datos inválidos para el producto.")
        return False

    with ARCHIVO_PRODUCTOS.open("a", newline="", encoding=ENCODING) as f:
        escritor = csv.writer(f, delimiter=",")
        escritor.writerow([nombre.strip(), precio, stock])
    print(f"✅ Producto registrado: {nombre.strip()} | ${precio} | Stock: {stock}")
    return True


# ============================================================================
# EJERCICIO 2.7: GESTOR DE SENSORES
# ============================================================================

ARCHIVO_SENSORES: Final[Path] = CARPETA_DATOS / "mediciones_sensores.csv"

def crear_archivo_sensores() -> None:
    preparar_directorio()
    if not ARCHIVO_SENSORES.exists():
        with ARCHIVO_SENSORES.open("w", newline="", encoding=ENCODING) as f:
            escritor = csv.writer(f, delimiter=",")
            escritor.writerow(["Sensor", "Temperatura", "Presion", "Humedad"])
        print(f"✅ Archivo '{ARCHIVO_SENSORES.name}' creado con sus encabezados.")

def validar_medicion_sensor(sensor: str, temp_str: str, pres_str: str, hum_str: str) -> tuple[bool, str, float, float, float]:
    sensor_limpio = sensor.strip()
    if not sensor_limpio:
        return False, "El nombre del sensor no puede estar vacío.", 0.0, 0.0, 0.0

    try:
        temp = float(temp_str.strip())
        pres = float(pres_str.strip())
        hum = float(hum_str.strip())
    except ValueError:
        return False, "Temperatura, Presión y Humedad deben ser valores numéricos.", 0.0, 0.0, 0.0

    if temp < -50.0 or temp > 150.0:
        return False, f"Temperatura fuera de rango físico (-50 a 150 °C): {temp}", 0.0, 0.0, 0.0
    if pres < 0.0:
        return False, f"La presión no puede ser negativa: {pres}", 0.0, 0.0, 0.0
    if hum < 0.0 or hum > 100.0:
        return False, f"Humedad relativa fuera de porcentaje (0 a 100%): {hum}", 0.0, 0.0, 0.0

    return True, "Medición válida.", temp, pres, hum

def registrar_medicion_sensor(sensor: str, temp_str: str, pres_str: str, hum_str: str) -> bool:
    crear_archivo_sensores()
    valido, msg, temp, pres, hum = validar_medicion_sensor(sensor, temp_str, pres_str, hum_str)
    if not valido:
        print(f"❌ Error en Sensor: {msg}")
        return False

    with ARCHIVO_SENSORES.open("a", newline="", encoding=ENCODING) as f:
        escritor = csv.writer(f, delimiter=",")
        escritor.writerow([sensor.strip(), temp, pres, hum])
    print(f"✅ Medición registrada [{sensor.strip()}]: Temp={temp}°C, Presion={pres}hPa, Hum={hum}%")
    return True


# ============================================================================
# EJERCICIO 2.8: GESTOR DE MANTENCIONES CON FECHA AUTOMÁTICA
# ============================================================================

ARCHIVO_MANTENCIONES: Final[Path] = CARPETA_DATOS / "bitacora_mantenciones.csv"

def crear_bitacora_mantenciones() -> None:
    preparar_directorio()
    if not ARCHIVO_MANTENCIONES.exists():
        with ARCHIVO_MANTENCIONES.open("w", newline="", encoding=ENCODING) as f:
            escritor = csv.writer(f, delimiter=",")
            escritor.writerow(["Fecha", "Equipo", "Tecnico", "Descripcion"])
        print(f"✅ Archivo '{ARCHIVO_MANTENCIONES.name}' creado con sus encabezados.")

def agregar_mantencion_auto_fecha(equipo: str, tecnico: str, descripcion: str) -> bool:
    crear_bitacora_mantenciones()
    if not equipo.strip() or not tecnico.strip() or not descripcion.strip():
        print("❌ Todos los campos son obligatorios para la mantención.")
        return False

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    with ARCHIVO_MANTENCIONES.open("a", newline="", encoding=ENCODING) as f:
        escritor = csv.writer(f, delimiter=",")
        escritor.writerow([fecha_hoy, equipo.strip(), tecnico.strip(), descripcion.strip()])

    print(f"✅ Mantención registrada [{fecha_hoy}]: Equipo '{equipo.strip()}' por Técnico '{tecnico.strip()}'")
    return True


# ============================================================================
# DEMOSTRACIÓN DE EJECUCIÓN
# ============================================================================

def ejecutar_suite_extra() -> None:
    print("🚀 EJECUTANDO SUITE DE EJERCICIOS EXTRA CSV (2.6, 2.7, 2.8)...\n")

    # 2.6 Productos
    print("--- Probrando 2.6 Productos ---")
    registrar_producto("Teclado Mecánico", 45000.0, 15)
    registrar_producto("Mouse Óptico", 15000.0, 30)

    # 2.7 Sensores
    print("\n--- Probando 2.7 Sensores ---")
    registrar_medicion_sensor("Sensor-Caldera-01", "85.5", "1013.25", "45.0")
    registrar_medicion_sensor("Sensor-Cámara-Fría", "-22.0", "1015.0", "90.0")
    registrar_medicion_sensor("Sensor-Fallido", "200.0", "100.0", "50.0") # Fallará por rango

    # 2.8 Mantenciones
    print("\n--- Probando 2.8 Mantenciones ---")
    agregar_mantencion_auto_fecha("Torno CNC #4", "Carlos Lopez", "Cambio de aceite hidráulico y calibración")


if __name__ == "__main__":
    ejecutar_suite_extra()
