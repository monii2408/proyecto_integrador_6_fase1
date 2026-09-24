"""Pico en 80-1000 Hz e interpolación parabólica sub-bin (ecuaciones 15, 16 del plan)."""

import numpy as np

from espectro import N

F_MIN = 80
F_MAX = 1000
RAZON_SUBARMONICO = 0.25  # un pico a f/2, f/3 o f/4 con >= 25 % del máximo es la fundamental


def buscar_pico(frecuencias, magnitud, f_min=F_MIN, f_max=F_MAX):
    """
    Bin de mayor magnitud dentro del rango de búsqueda de f0.
    Entra: frecuencias, magnitud (np.ndarray), f_min, f_max (Hz).
    Sale: k (int), índice del bin del pico en el arreglo completo.
    El rango 80-1000 Hz evita confundir la fundamental con armónicos altos
    o con ruido de baja frecuencia fuera del registro de las notas Do4-Si4.
    """
    indices = np.where((frecuencias >= f_min) & (frecuencias <= f_max))[0]
    return indices[np.argmax(magnitud[indices])]


def bajar_a_fundamental(frecuencias, magnitud, k, f_min=F_MIN, razon=RAZON_SUBARMONICO):
    """
    Corrige el error de octava: en el piano real el 2.º o 3.er armónico puede
    ser más fuerte que la fundamental, y el pico máximo caería en él.
    Mira si hay un pico razonable en la frecuencia del pico dividida por 2, 3 y 4;
    si lo hay (>= `razon` de la magnitud del pico máximo), ese es la fundamental.
    Entra: frecuencias, magnitud (np.ndarray), k (int) bin del pico máximo,
           f_min (Hz), razon (float, fracción mínima de magnitud).
    Sale: k (int), bin de la fundamental (el mismo k si no hay pico por debajo).
    """
    for divisor in (4, 3, 2):  # de menor a mayor frecuencia: gana la más baja que cumpla
        centro = int(round(k / divisor))
        if frecuencias[centro] < f_min:
            continue
        ancho = max(2, int(0.03 * centro))  # tolerancia ~3 % por inarmonicidad del piano
        ventana = np.arange(centro - ancho, centro + ancho + 1)
        candidato = ventana[np.argmax(magnitud[ventana])]
        if magnitud[candidato] >= razon * magnitud[k]:
            return candidato
    return k


def interpolar_pico(magnitud, k, fs, n=N):
    """
    Interpolación parabólica de 3 puntos alrededor del bin k, para estimar
    f0 con precisión sub-bin (el bin crudo solo da resolución Δf=fs/N).
    Entra: magnitud (np.ndarray), k (int) bin del pico, fs (int), n (int).
    Sale: f0 (float), frecuencia estimada en Hz.
    Ecuación (15): δ = 1/2 * (α - γ) / (α - 2β + γ)
    Ecuación (16): f0 = (k + δ) * fs / N
    """
    alfa, beta, gamma = magnitud[k - 1], magnitud[k], magnitud[k + 1]
    delta = 0.5 * (alfa - gamma) / (alfa - 2 * beta + gamma)
    return (k + delta) * fs / n


def detectar_f0(frecuencias, magnitud, fs, n=N, f_min=F_MIN, f_max=F_MAX):
    """
    Pipeline: pico crudo en el rango -> baja a la fundamental si el pico es un
    armónico -> interpola -> f0 final.
    Entra: frecuencias, magnitud (np.ndarray), fs (int), n (int), f_min, f_max (Hz).
    Sale: f0 (float), frecuencia fundamental estimada en Hz.
    """
    k = buscar_pico(frecuencias, magnitud, f_min, f_max)
    k = bajar_a_fundamental(frecuencias, magnitud, k, f_min)
    return interpolar_pico(magnitud, k, fs, n)


if __name__ == "__main__":
    import os

    from notas import tabla_notas
    from preprocesamiento import preprocesar
    from espectro import espectro

    ruta = os.path.join(os.path.dirname(__file__), "..", "audio", "sinteticos", "Do4.wav")
    fs, senal = preprocesar(ruta)
    frecuencias, magnitud = espectro(senal, fs)
    f0 = detectar_f0(frecuencias, magnitud, fs)

    f_real = tabla_notas()["Do4"]
    cents = 1200 * np.log2(f0 / f_real)
    print(f"f0={f0:.4f} Hz (real={f_real:.4f} Hz), error={cents:.3f} cents")
