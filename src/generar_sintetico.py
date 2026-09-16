"""Genera tonos sintéticos (senoides puras) para validar el pipeline antes de usar grabaciones reales."""

import os

import numpy as np
from scipy.io import wavfile

from notas import tabla_notas

FS = 48000  # Hz, misma frecuencia de muestreo que la adquisición real
DURACION_S = 1.0
AMPLITUD = 0.5


def generar_tono(frecuencia_hz, duracion_s=DURACION_S, fs=FS, amplitud=AMPLITUD):
    """
    Senoide pura de frecuencia conocida, para validar el pipeline sin depender del micrófono.
    Entra: frecuencia_hz (float), duracion_s (float), fs (int), amplitud (float, 0-1).
    Sale: señal (np.ndarray float64), x[n] = amplitud * sin(2*pi*frecuencia_hz*n/fs).
    No corresponde a una ecuación numerada del plan; es la señal de prueba controlada
    que permite aislar errores de código de errores de captura (ver CLAUDE.md).
    """
    n = np.arange(int(duracion_s * fs))
    return amplitud * np.sin(2 * np.pi * frecuencia_hz * n / fs)


def guardar_wav(ruta, senal, fs=FS):
    """
    Escribe la señal como WAV de 16 bits.
    Entra: ruta (str), senal (np.ndarray, rango [-1, 1]), fs (int).
    Sale: nada; crea el archivo en disco.
    """
    senal_int16 = np.int16(np.clip(senal, -1.0, 1.0) * 32767)
    wavfile.write(ruta, fs, senal_int16)


if __name__ == "__main__":
    carpeta_salida = os.path.join(os.path.dirname(__file__), "..", "audio", "sinteticos")
    os.makedirs(carpeta_salida, exist_ok=True)

    for nombre, hz in tabla_notas().items():
        senal = generar_tono(hz)
        ruta = os.path.join(carpeta_salida, f"{nombre}.wav")
        guardar_wav(ruta, senal)
        print(f"{nombre}: {hz:.3f} Hz -> {ruta}")
