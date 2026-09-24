"""Piso de ruido real, desviación estándar del error y repetibilidad (criterio 4 de la rúbrica)."""

import csv
import os

import numpy as np

from analizar_nota import analizar_nota
from deteccion import F_MAX, F_MIN, N
from espectro import espectro
from evaluar_reales import CARPETA_SAMPLES, INGLES_A_LATINA
from notas import tabla_notas
from preprocesamiento import cargar_audio, detectar_inicio, normalizar

RAIZ = os.path.join(os.path.dirname(__file__), "..")
DINAMICAS = ["pp", "mf", "ff"]
CAMPOS_CSV = ["dinamica", "nota", "silencio_s", "piso_dbfs", "pico_ruido_mag",
              "pico_senal_mag", "razon_senal_ruido_db"]


def segmento_silencio(ruta_wav):
    """
    Tramo de la grabación anterior al inicio real de la nota (ver detectar_inicio).
    Entra: ruta_wav (str).
    Sale: (fs, segmento) — segmento (np.ndarray) puede tener longitud 0 si la nota
    empieza en la primera muestra (no hay silencio que medir).
    Es el mismo criterio de recortar_ataque, pero se queda con lo que esa función
    descarta, no con lo que conserva.
    """
    fs, senal = cargar_audio(ruta_wav)
    senal = normalizar(senal)
    inicio = detectar_inicio(senal, fs)
    return fs, senal[:inicio]


def piso_ruido_dbfs(segmento):
    """
    Nivel RMS del segmento en dBFS (0 dB = amplitud máxima 1, tras normalizar).
    Entra: segmento (np.ndarray).
    Sale: float (dB) o None si el segmento está vacío o es silencio digital puro.
    """
    if len(segmento) == 0:
        return None
    rms = np.sqrt(np.mean(segmento.astype(np.float64) ** 2))
    return 20 * np.log10(rms) if rms > 0 else None


def analizar_ruido_archivo(dinamica, ingles, latina):
    """
    Piso de ruido de un archivo: nivel en dBFS y magnitud de su pico espectral
    en la banda de búsqueda, comparada con el pico de la señal en el mismo archivo.
    Entra: dinamica (str), ingles (str, nombre en notación inglesa), latina (str).
    Sale: dict con los campos de CAMPOS_CSV, o None si el archivo no tiene silencio
    previo que medir (la nota empieza en la muestra 0).
    """
    ruta = os.path.join(CARPETA_SAMPLES, dinamica, f"Piano.{dinamica}.{ingles}.wav")
    fs, silencio = segmento_silencio(ruta)
    if len(silencio) < N:
        return None  # no alcanza para una FFT del mismo tamaño que el pipeline

    dbfs = piso_ruido_dbfs(silencio)
    frecuencias, magnitud_ruido = espectro(silencio, fs)
    banda = (frecuencias >= F_MIN) & (frecuencias <= F_MAX)
    pico_ruido = magnitud_ruido[banda].max()

    r = analizar_nota(ruta, tabla_notas())
    pico_senal = r["magnitud"][r["k"]]
    razon_db = 20 * np.log10(pico_senal / pico_ruido) if pico_ruido > 0 else None

    return {
        "dinamica": dinamica, "nota": latina,
        "silencio_s": len(silencio) / fs,
        "piso_dbfs": dbfs, "pico_ruido_mag": pico_ruido,
        "pico_senal_mag": pico_senal, "razon_senal_ruido_db": razon_db,
    }


def desviacion_por_dinamica(ruta_csv):
    """
    Media y desviación estándar del error en cents, agrupadas por intensidad.
    Entra: ruta_csv (str, resultados_reales.csv).
    Sale: dict dinamica -> (media, desviacion), con las 12 notas de cada una.
    """
    filas = list(csv.DictReader(open(ruta_csv)))
    out = {}
    for d in DINAMICAS:
        errores = [float(f["error_cents"]) for f in filas if f["dinamica"] == d]
        out[d] = (float(np.mean(errores)), float(np.std(errores)))
    return out


def repetibilidad(ruta_wav, tabla, repeticiones=5):
    """
    Corre analizar_nota varias veces sobre el mismo archivo y mide la variación de f0.
    Entra: ruta_wav (str), tabla (dict), repeticiones (int).
    Sale: (lista de f0 (Hz), desviación estándar (Hz)).
    El pipeline no tiene aleatoriedad: no hay captura en vivo ni ruido añadido, así
    que se espera desviación 0 (el resultado depende solo de los bits del archivo).
    """
    f0s = [analizar_nota(ruta_wav, tabla)["f0_hz"] for _ in range(repeticiones)]
    return f0s, float(np.std(f0s))


if __name__ == "__main__":
    filas = []
    for d in DINAMICAS:
        for ingles, latina in INGLES_A_LATINA.items():
            fila = analizar_ruido_archivo(d, ingles, latina)
            if fila is not None:
                filas.append(fila)

    print("--- Piso de ruido (segmento antes del inicio detectado de la nota) ---")
    for d in DINAMICAS:
        del_d = [f for f in filas if f["dinamica"] == d]
        if not del_d:
            print(f"{d}: sin silencio medible (la nota empieza en la muestra 0)")
            continue
        dbfs = [f["piso_dbfs"] for f in del_d if f["piso_dbfs"] is not None]
        razon = [f["razon_senal_ruido_db"] for f in del_d if f["razon_senal_ruido_db"] is not None]
        print(f"{d}: {len(del_d)} notas con silencio previo | "
              f"piso medio = {np.mean(dbfs):.1f} dBFS | "
              f"razón señal/ruido media = {np.mean(razon):.1f} dB")

    ruta_csv = os.path.join(RAIZ, "datos", "piso_ruido.csv")
    with open(ruta_csv, "w", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV)
        writer.writeheader()
        writer.writerows(filas)
    print(f"Detalle guardado en {ruta_csv}")

    print("\n--- Desviación estándar del error por intensidad (12 notas c/u) ---")
    for d, (media, desv) in desviacion_por_dinamica(os.path.join(RAIZ, "datos", "resultados_reales.csv")).items():
        print(f"{d}: media = {media:+.2f} cents | desviación estándar = {desv:.2f} cents")

    print("\n--- Repetibilidad (5 ejecuciones sobre el mismo archivo, Do4 mf) ---")
    ruta_do4 = os.path.join(CARPETA_SAMPLES, "mf", "Piano.mf.C4.wav")
    f0s, desv = repetibilidad(ruta_do4, tabla_notas())
    print(f"f0 en las 5 corridas: {[f'{v:.6f}' for v in f0s]}")
    print(f"Desviación estándar: {desv:.2e} Hz")
