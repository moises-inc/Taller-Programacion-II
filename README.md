# 🐍 Taller de Programación II — Universidad San Sebastián

> **Curso de Programación en Python orientado a la gestión profesional de archivos: TXT, CSV y JSON.**  
> Repositorio público de material docente, apuntes maestros, cuadernos Jupyter y ejercicios resueltos del ramo **Taller de Programación II** — *Universidad San Sebastián · Sede Patagonia*.

[![Python 3.13](https://img.shields.io/badge/Python-3.13-4B8BBE?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter Notebooks](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-D4AF37?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Universidad San Sebastián](https://img.shields.io/badge/USS-Sede%20Patagonia-00205B)](https://www.uss.cl/)
[![moises-inc](https://img.shields.io/badge/moises--inc-Taller--Programacion--II-00205B)](https://github.com/moises-inc/Taller-Programacion-II)

---

## 📚 Descripción

El ramo **Taller de Programación II** profundiza en la **persistencia de datos** mediante el manejo sistemático de archivos en Python:
el paso de un programa *en memoria* a un *sistema de información* que sobrevive entre ejecuciones. Este repositorio contiene
la copia pública, sanitizada y estructurada de los materiales del curso: apuntes maestros con la teoría consolidada, guías
docentes originales, soluciones completas en Python y cuadernos Jupyter con celdas pre-renderizadas para seguimiento paso a paso.

### Estructura del curso (Unidades)

| Unidad | Contenido |
| :--- | :--- |
| **Unidad 0 — Repaso** | Recuperación de fundamentos de Programación I: variables, condicionales, ciclos, listas, funciones y diccionarios. |
| **Unidad 1 — Manejo de Archivos TXT / CSV / JSON** | Streams y *buffers*, context manager (`with open`), modos de apertura, `seek`/`tell`, CRUD atómico, `pathlib`, corte de control, apareo de archivos y serialización `csv`/`json`. |

---

## 📑 Tabla de Contenidos

- [📚 Descripción](#-descripción)
- [🗂️ Organización del Repositorio](#-organización-del-repositorio)
- [👨‍🏫 Apuntes Teóricos (Maestros)](#-apuntes-teóricos-maestros)
- [📄 Guías Docentes](#-guías-docentes)
- [🖥️ Soluciones en Python (.py)](#-soluciones-en-python-py)
- [📓 Índice de Cuadernos Jupyter](#-índice-de-cuadernos-jupyter)
- [📂 Datos de Ejemplo](#-datos-de-ejemplo)
- [🚀 Instalación y Ejecución](#-instalación-y-ejecución)
- [📜 Licencia](#-licencia)

---

## 🗂️ Organización del Repositorio

```
Taller-Programacion-II/
├── Apuntes/                       # Notas maestras teóricas (Markdown sanitizado)
├── Guias_y_Ejercicios/            # Guías docentes PDF/DOCX + soluciones Python
│   ├── Guias_Docente/             #    (archivos PDF/DOCX originales)
│   ├── Soluciones_Python/         #    (scripts .py resueltos)
│   └── datos/                     #    datos de ejemplo
└── Entrenamiento_Laboratorio/     # Cuadernos Jupyter + datos de práctica
```

---

## 👨‍🏫 Apuntes Teóricos (Maestros)

Apuntes consolidados a partir de las presentaciones de cátedra, el texto guía y referencias web, con leyenda de trazabilidad de fuentes:

| Apunte | Descripción |
| :--- | :--- |
| [Repaso_Programacion_I.md](Apuntes/Repaso_Programacion_I.md) | Repaso de Programación I y conexión al trabajo con archivos. |
| [Manejo_Archivos_Python.md](Apuntes/Manejo_Archivos_Python.md) | Nota maestra: gestión exhaustiva de archivos TXT, modos de apertura, CRUD atómico, corte de control y JSON. |
| [Archivos_CSV_Python.md](Apuntes/Archivos_CSV_Python.md) | Guía maestra de persistencia con CSV: RFC 4180, `DictReader`/`DictWriter`, limpieza y estructuración de datos. |

---

## 📄 Guías Docentes

Guías originales del curso en `Guias_y_Ejercicios/`:

- `Guia_Basica_paso_a_paso_Manejo_Archivos_TXT_Python` (PDF + DOCX)
- `Guia_Practica_Ejercicios_Archivos_TXT_Python` (PDF + DOCX)
- `Guia Integral Ejercicios_Unidad1` (PDF)
- `Guia_Ejercicio_Integral_CSV_Maquinas_Industriales` (PDF + DOCX)
- `Ejercicios Extra CSV` — ejercicios 2.6, 2.7 y 2.8 (PDF)
- `Guia_Ejercicios_Manejo_Archivos_Produccion_Python` (PDF + DOCX)
- `Actividad_Registro_Ventas_Archivos_Python` (PDF)

---

## 🖥️ Soluciones en Python (.py)

Módulos resueltos en `Guias_y_Ejercicios/Soluciones_Python/`:

- `guia_maquinas_industriales_csv.py` — Registro de condiciones de máquinas industriales en CSV.
- `ejercicios_extra_csv.py` — Ejercicios extra CSV (productos, sensores, mantenciones).
- `guia_integral_unidad1.py` — Guía integral de la Unidad 1 (funciones, validaciones y diccionarios).
- `programa_produccion.py` — CRUD persistente de órdenes de producción (TXT delimitado por `;`).
- `practica_archivos_basica.py` — Primeros pasos con archivos TXT.
- `practica_intensiva_io_txt_csv.py` — Práctica intensiva de E/S en TXT y CSV.
- `practica_serializacion_json.py` — Serialización y deserialización JSON.
- `simulacro_control1_laboratorio.py` — Simulacro de Control 1 (préstamos con respaldo JSON).

> Los scripts crean automáticamente la carpeta `datos/` y los archivos de trabajo necesarios.

---

## 📓 Índice de Cuadernos Jupyter

Cuadernos con celdas pre-renderizadas para seguimiento paso a paso, en `Entrenamiento_Laboratorio/`:

| Cuaderno | Tema |
| :--- | :--- |
| [Solucion_Guia_Basica_Paso_a_Paso_Archivos_TXT.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_Basica_Paso_a_Paso_Archivos_TXT.ipynb) | Primeros pasos con archivos TXT. |
| [Solucion_Guia_Practica_Ejercicios_Archivos_TXT.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_Practica_Ejercicios_Archivos_TXT.ipynb) | Práctica de ejercicios con archivos TXT. |
| [Solucion_Guia_Integral_Ejercicios_Unidad1.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_Integral_Ejercicios_Unidad1.ipynb) | Funciones compuestas, validaciones robustas y gestión de clientes. |
| [Solucion_Guia_CSV_Maquinas_Industriales.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_CSV_Maquinas_Industriales.ipynb) | Registro de condiciones de máquinas industriales (CSV). |
| [Solucion_Ejercicios_Extra_CSV.ipynb](Entrenamiento_Laboratorio/Solucion_Ejercicios_Extra_CSV.ipynb) | Ejercicios extra CSV: productos, sensores y mantenciones. |
| [Solucion_Guia_Manejo_Archivos_Produccion.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_Manejo_Archivos_Produccion.ipynb) | Sistema de control de productos y órdenes de producción. |
| [Solucion_Actividad_Registro_Ventas_Archivos.ipynb](Entrenamiento_Laboratorio/Solucion_Actividad_Registro_Ventas_Archivos.ipynb) | Registro de ventas con archivos: captura, guardado y resumen. |
| [Solucion_Simulacro_Control1_Laboratorio.ipynb](Entrenamiento_Laboratorio/Solucion_Simulacro_Control1_Laboratorio.ipynb) | Pauta oficial del simulacro: préstamos con respaldo JSON. |
| [Cuaderno_Entrenamiento_Solemnes_TallerII.ipynb](Entrenamiento_Laboratorio/Cuaderno_Entrenamiento_Solemnes_TallerII.ipynb) | Entrenamiento intensivo para las solemnidades del curso. |

---

## 📂 Datos de Ejemplo

En `datos/` de cada carpeta de soluciones se incluyen archivos de ejemplo (`produccion.txt`, `registro.txt`, `ventas.txt`, `registro_ventas.txt`).
Los programas y cuadernos también **crean** sus propios archivos si no existen, por lo que el repositorio es 100 % reproducible al clonarlo.

---

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/moises-inc/Taller-Programacion-II.git
cd Taller-Programacion-II
```

### 2. Ejecutar un módulo Python

```bash
cd Guias_y_Ejercicios/Soluciones_Python
python3 programa_produccion.py     # CRUD de órdenes de producción
python3 guia_maquinas_industriales_csv.py
```

### 3. Ejecutar un cuaderno Jupyter

```bash
cd Entrenamiento_Laboratorio
jupyter notebook Solucion_Guia_Basica_Paso_a_Paso_Archivos_TXT.ipynb
```

> **Requisitos:** Python 3.10+ (se recomienda Python 3.13). Los cuadernos solo requieren la biblioteca estándar; `jupyter` para ejecutarlos.

---

## 📜 Licencia

Este material se publica bajo la **Licencia MIT** — © 2026 Moisés Vera / moises-inc. Ver [LICENSE](LICENSE).
