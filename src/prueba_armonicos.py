"""Valida deteccion.py con tonos sintéticos que incluyen armónicos, simulando
el timbre de un instrumento real antes de depender de grabaciones reales."""

import os

import numpy as np

from deteccion import detectar_f0
from espectro import espectro
from evaluacion import error_cents
from generar_sintetico import DURACION_S, FS, guardar_wav
from notas import tabla_notas
from preprocesamiento import preprocesar

# Amplitudes relativas de la fundamental y los primeros 4 armónicos (decrecientes,
# como en un tono de piano real). No corresponde a una ecuación numerada del plan;
# es un modelo de señal más realista para poner a prueba la detección del pico.
AMPLITUDES_ARMONICOS = [1.0, 0.6, 0.4, 0.25, 0.15]


def generar_tono_con_armonicos(frecuencia_hz, amplitudes=AMPLITUDES_ARMONICOS,
                                duracion_s=DURACION_S, fs=FS):
    """
    Senoide con armónicos superpuestos: x[n] = sum_h amplitudes[h] * sin(2*pi*h*f*n/fs).
    Entra: frecuencia_hz (float) fundamental, amplitudes (list[float]), duracion_s, fs.
    Sale: señal (np.ndarray float64), normalizada a pico 1 (evita saturar el WAV).
    """
    n = np.arange(int(duracion_s * fs))
    senal = np.zeros_like(n, dtype=np.float64)
    for h, amplitud in enumerate(amplitudes, start=1):
        senal += amplitud * np.sin(2 * np.pi * h * frecuencia_hz * n / fs)
    return senal / np.max(np.abs(senal))


if __name__ == "__main__":
    carpeta = os.path.join(os.path.dirname(__file__), "..", "audio", "sinteticos", "armonicos")
    os.makedirs(carpeta, exist_ok=True)

    tabla = tabla_notas()
    for nombre, f_real in tabla.items():
        senal = generar_tono_con_armonicos(f_real)
        ruta = os.path.join(carpeta, f"{nombre}.wav")
        guardar_wav(ruta, senal * 0.5)

        fs, senal_proc = preprocesar(ruta)
        frecuencias, magnitud = espectro(senal_proc, fs)
        f0 = detectar_f0(frecuencias, magnitud, fs)
        cents = error_cents(f0, f_real)
        print(f"{nombre}: f0={f0:.3f} Hz (real={f_real:.3f} Hz), error={cents:.3f} cents")
