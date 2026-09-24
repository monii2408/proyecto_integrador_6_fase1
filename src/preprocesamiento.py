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


def detectar_inicio(senal, fs, umbral=0.1, ms_ventana=10):
    """
    Índice de la muestra donde empieza la nota: la primera ventana corta cuya
    energía (RMS) supera `umbral` veces la de la ventana más fuerte.
    Los samples reales traen silencio o ruido antes de la tecla (en ff, hasta
    ~1 s); si se analizara ese tramo, la FFT vería ruido y no la nota.
    Entra: senal (np.ndarray), fs (int), umbral (float, fracción del RMS máximo),
           ms_ventana (float, ancho de la ventana de energía).
    Sale: índice de la muestra de inicio (int); 0 si la señal ya empieza sonando.
    """
    ancho = max(1, int(ms_ventana / 1000 * fs))
    n_ventanas = len(senal) // ancho
    if n_ventanas == 0:
        return 0
    bloques = senal[: n_ventanas * ancho].reshape(n_ventanas, ancho)
    rms = np.sqrt(np.mean(bloques**2, axis=1))
    if rms.max() == 0:
        return 0
    primera = int(np.argmax(rms > umbral * rms.max()))
    return primera * ancho


def recortar_ataque(senal, fs, ms_descarte=75):
    """
    Descarta el silencio previo y el ataque inicial (el golpe de tecla es un
    transitorio no periódico que ensuciaría el espectro con energía fuera de
    la fundamental). El descarte de ms_descarte se cuenta desde el inicio
    real de la nota, no desde el inicio del archivo.
    Entra: senal (np.ndarray), fs (int), ms_descarte (float, 50-100 ms según el plan).
    Sale: senal recortada (np.ndarray).
    """
    n_descarte = detectar_inicio(senal, fs) + int(ms_descarte / 1000 * fs)
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
