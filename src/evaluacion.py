"""Identificación de nota, error en cents y tasa de reconocimiento (ecuación 9 del plan)."""

import csv
import os

import numpy as np

from deteccion import detectar_f0
from espectro import espectro
from notas import tabla_notas
from preprocesamiento import preprocesar

CAMPOS_CSV = ["nota_real", "nota_detectada", "f0_hz", "error_cents", "acierto"]


def error_cents(f_medida, f_tabla):
    """
    Error de f0 respecto a la frecuencia tabulada, en cents.
    Entra: f_medida, f_tabla (float, Hz).
    Sale: error en cents (float).
    Ecuación (9): cents = 1200 * log2(f_medida / f_tabla)
    """
    return 1200 * np.log2(f_medida / f_tabla)


def identificar_nota(f0, tabla):
    """
    Nota de la tabla cuya frecuencia está más cerca de f0, medida en cents
    (distancia logarítmica/perceptual, no Hz lineales).
    Entra: f0 (float), tabla (dict nombre -> frecuencia).
    Sale: nombre de la nota más cercana (str).
    """
    return min(tabla, key=lambda nombre: abs(error_cents(f0, tabla[nombre])))


def evaluar_nota(ruta_wav, nota_real, tabla):
    """
    Pipeline completo sobre un archivo: preprocesa, calcula el espectro,
    detecta f0, identifica la nota y calcula el error en cents contra nota_real.
    Entra: ruta_wav (str), nota_real (str) nombre esperado, tabla (dict).
    Sale: dict con nota_real, nota_detectada, f0_hz, error_cents, acierto.
    """
    fs, senal = preprocesar(ruta_wav)
    frecuencias, magnitud = espectro(senal, fs)
    f0 = detectar_f0(frecuencias, magnitud, fs)
    nota_detectada = identificar_nota(f0, tabla)
    return {
        "nota_real": nota_real,
        "nota_detectada": nota_detectada,
        "f0_hz": f0,
        "error_cents": error_cents(f0, tabla[nota_real]),
        "acierto": nota_detectada == nota_real,
    }


def evaluar_conjunto(carpeta, tabla=None):
    """
    Evalúa todas las notas de una carpeta (un WAV por nota, nombrado <Nota>.wav)
    y calcula la tasa de reconocimiento sobre el conjunto.
    Entra: carpeta (str), tabla (dict, por defecto tabla_notas()).
    Sale: (resultados, tasa) — resultados: list[dict], tasa: float en [0, 1].
    """
    if tabla is None:
        tabla = tabla_notas()
    resultados = [
        evaluar_nota(os.path.join(carpeta, f"{nombre}.wav"), nombre, tabla)
        for nombre in tabla
    ]
    tasa = sum(r["acierto"] for r in resultados) / len(resultados)
    return resultados, tasa


def guardar_csv(resultados, ruta_csv):
    """
    Guarda los resultados como CSV (nota_real, nota_detectada, f0_hz, error_cents, acierto).
    Entra: resultados (list[dict]), ruta_csv (str).
    Sale: nada; crea/sobrescribe el archivo.
    """
    with open(ruta_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        writer.writeheader()
        writer.writerows(resultados)


if __name__ == "__main__":
    carpeta_sinteticos = os.path.join(os.path.dirname(__file__), "..", "audio", "sinteticos")
    resultados, tasa = evaluar_conjunto(carpeta_sinteticos)

    for r in resultados:
        print(
            f"{r['nota_real']}: detectada={r['nota_detectada']}, "
            f"f0={r['f0_hz']:.3f} Hz, error={r['error_cents']:.3f} cents, "
            f"acierto={r['acierto']}"
        )
    print(f"Tasa de reconocimiento: {tasa * 100:.1f}%")

    ruta_csv = os.path.join(os.path.dirname(__file__), "..", "datos", "resultados.csv")
    guardar_csv(resultados, ruta_csv)
    print(f"Resultados guardados en {ruta_csv}")
