"""Ventana de Hann, FFT y eje de frecuencias (ecuaciones 11, 12, 14 del plan)."""

import numpy as np
from scipy.signal.windows import hann

N = 32768  # tamaño de FFT -> Δf = fs/N ≈ 1.465 Hz


def ventanear(senal, n=N):
    """
    Aplica la ventana de Hann sobre los primeros n puntos de la señal
    (recorta si es más larga, rellena con ceros si es más corta).
    Entra: senal (np.ndarray), n (int).
    Sale: senal_ventaneada (np.ndarray), longitud n.
    Ecuación (11): x_w[n] = x[n] * w[n], w[n] = ventana de Hann.
    La ventana evita el corte abrupto en los bordes del tramo, que generaría
    fuga espectral (leakage) y ensuciaría la estimación del pico.
    """
    if len(senal) >= n:
        tramo = senal[:n]
    else:
        tramo = np.pad(senal, (0, n - len(senal)))
    return tramo * hann(n)


def calcular_fft(senal_ventaneada, n=N):
    """
    Magnitud del espectro unilateral vía FFT.
    Entra: senal_ventaneada (np.ndarray, longitud n).
    Sale: magnitud (np.ndarray), bins 0 a n/2 (de 0 Hz a fs/2).
    Ecuación (12): X[k] = FFT(x_w[n]).
    """
    espectro_complejo = np.fft.fft(senal_ventaneada, n)
    return np.abs(espectro_complejo[: n // 2 + 1])


def eje_frecuencias(n=N, fs=48000):
    """
    Eje de frecuencias correspondiente a cada bin k del espectro unilateral.
    Entra: n (int), fs (int).
    Sale: frecuencias (np.ndarray), f[k] = k * fs / n.
    Ecuación (14): f[k] = k * fs / N.
    """
    return np.arange(n // 2 + 1) * fs / n


def espectro(senal, fs, n=N):
    """
    Pipeline: ventanea -> FFT -> eje de frecuencias.
    Entra: senal (np.ndarray), fs (int), n (int).
    Sale: (frecuencias, magnitud), listos para deteccion.py.
    """
    senal_ventaneada = ventanear(senal, n)
    magnitud = calcular_fft(senal_ventaneada, n)
    frecuencias = eje_frecuencias(n, fs)
    return frecuencias, magnitud


if __name__ == "__main__":
    import os

    from preprocesamiento import preprocesar

    ruta = os.path.join(os.path.dirname(__file__), "..", "audio", "sinteticos", "Do4.wav")
    fs, senal = preprocesar(ruta)
    frecuencias, magnitud = espectro(senal, fs)
    k_pico = int(np.argmax(magnitud))
    print(f"df={fs / N:.3f} Hz, pico en bin {k_pico} -> {frecuencias[k_pico]:.3f} Hz")
