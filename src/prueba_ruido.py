"""Robustez frente a ruido: tonos con armónicos + ruido blanco a distintos SNR."""

import csv
import os

import numpy as np

from deteccion import detectar_f0
from espectro import espectro
from evaluacion import error_cents, identificar_nota
from notas import tabla_notas
from preprocesamiento import cargar_audio, normalizar, recortar_ataque

RAIZ = os.path.join(os.path.dirname(__file__), "..")
CARPETA = os.path.join(RAIZ, "audio", "sinteticos", "armonicos")
SNRS_DB = [40, 30, 20, 10, 5, 0, -10, -20, -30]
REPETICIONES = 20
SEMILLA = 2026  # semilla fija: el resultado se reproduce igual en otro equipo
CAMPOS_CSV = ["snr_db", "tasa_reconocimiento", "error_max_cents", "error_medio_cents"]


def agregar_ruido(senal, snr_db, rng):
    """
    Suma ruido blanco gaussiano para lograr una relación señal/ruido dada.
    Entra: senal (np.ndarray), snr_db (float), rng (np.random.Generator).
    Sale: señal con ruido (np.ndarray).
    SNR = 10*log10(P_senal / P_ruido)  ->  P_ruido = P_senal / 10^(SNR/10)
    """
    potencia_ruido = np.mean(senal**2) / 10 ** (snr_db / 10)
    return senal + rng.normal(0, np.sqrt(potencia_ruido), len(senal))


def evaluar_con_ruido(senal, fs, nota_real, tabla):
    """
    Mismo pipeline que evaluacion.py, pero partiendo de una señal ya en memoria.
    Entra: senal (np.ndarray), fs (int), nota_real (str), tabla (dict).
    Sale: (acierto (bool), error en cents (float)).
    """
    senal = recortar_ataque(normalizar(senal), fs)
    frecuencias, magnitud = espectro(senal, fs)
    f0 = detectar_f0(frecuencias, magnitud, fs)
    return identificar_nota(f0, tabla) == nota_real, error_cents(f0, tabla[nota_real])


if __name__ == "__main__":
    tabla = tabla_notas()
    rng = np.random.default_rng(SEMILLA)
    limpias = {n: cargar_audio(os.path.join(CARPETA, f"{n}.wav")) for n in tabla}

    filas = []
    for snr in SNRS_DB:
        aciertos, errores = [], []
        for nota, (fs, senal) in limpias.items():
            for _ in range(REPETICIONES):
                ok, err = evaluar_con_ruido(agregar_ruido(senal, snr, rng), fs, nota, tabla)
                aciertos.append(ok)
                errores.append(abs(err))
        fila = {
            "snr_db": snr,
            "tasa_reconocimiento": float(np.mean(aciertos)),
            "error_max_cents": float(np.max(errores)),
            "error_medio_cents": float(np.mean(errores)),
        }
        filas.append(fila)
        print(
            f"SNR {snr:>2} dB: reconocimiento={fila['tasa_reconocimiento'] * 100:5.1f}% | "
            f"error medio={fila['error_medio_cents']:.2f} cents | max={fila['error_max_cents']:.2f} cents"
        )

    ruta_csv = os.path.join(RAIZ, "datos", "resultados_ruido.csv")
    with open(ruta_csv, "w", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV)
        writer.writeheader()
        writer.writerows(filas)
    print(f"Resultados guardados en {ruta_csv}")
