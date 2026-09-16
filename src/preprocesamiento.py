"""Carga, normalización y recorte del ataque de una grabación (sec. 3.4 del plan)."""

import numpy as np
from scipy.io import wavfile


def cargar_audio(ruta):
    """
    Carga un WAV y lo convierte a float64.
    Entra: ruta (str), ruta del archivo WAV.
    Sale: (fs, senal) — fs (int), senal (np.ndarray float64), un solo canal.
    """
    fs, datos = wavfile.read(ruta)
    if datos.ndim > 1:
        datos = datos[:, 0]  # si es estéreo, se queda con un solo canal
    senal = datos.astype(np.float64)
    return fs, senal


def normalizar(senal):
    """
    Normaliza la señal a amplitud máxima 1, para que el nivel de grabación
    (distancia al micrófono, ganancia) no afecte la magnitud de la FFT.
    Entra: senal (np.ndarray).
    Sale: senal normalizada (np.ndarray float64) en el rango [-1, 1].
    """
    pico = np.max(np.abs(senal))
    return senal / pico if pico > 0 else senal


def recortar_ataque(senal, fs, ms_descarte=75):
    """
    Descarta el ataque inicial (el golpe de tecla es un transitorio no
    periódico que ensuciaría el espectro con energía fuera de la fundamental).
    Entra: senal (np.ndarray), fs (int), ms_descarte (float, 50-100 ms según el plan).
    Sale: senal recortada (np.ndarray).
    """
    n_descarte = int(ms_descarte / 1000 * fs)
    return senal[n_descarte:]


def preprocesar(ruta, ms_descarte=75):
    """
    Pipeline completo: carga -> normaliza -> recorta ataque.
    Entra: ruta (str), ms_descarte (float).
    Sale: (fs, senal) lista para la etapa de espectro.
    """
    fs, senal = cargar_audio(ruta)
    senal = normalizar(senal)
    senal = recortar_ataque(senal, fs, ms_descarte)
    return fs, senal


if __name__ == "__main__":
    import os

    ruta = os.path.join(os.path.dirname(__file__), "..", "audio", "sinteticos", "Do4.wav")
    fs, senal = preprocesar(ruta)
    print(f"fs={fs} Hz, muestras tras recorte={len(senal)}, pico={np.max(np.abs(senal)):.3f}")
