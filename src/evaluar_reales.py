"""Evaluación del pipeline sobre los samples de piano reales (pp, mf, ff)."""

import csv
import os

from evaluacion import evaluar_nota
from notas import tabla_notas

RAIZ = os.path.join(os.path.dirname(__file__), "..")
CARPETA_SAMPLES = os.path.join(RAIZ, "audio", "originales")
DINAMICAS = ["pp", "mf", "ff"]

# Los samples usan notación inglesa; el proyecto usa la latina (ver el léeme de Rodrigo).
INGLES_A_LATINA = {
    "C4": "Do4", "Db4": "Do#4", "D4": "Re4", "Eb4": "Re#4", "E4": "Mi4", "F4": "Fa4",
    "Gb4": "Fa#4", "G4": "Sol4", "Ab4": "Sol#4", "A4": "La4", "Bb4": "La#4", "B4": "Si4",
}
CAMPOS_CSV = ["dinamica", "nota_real", "nota_detectada", "f0_hz", "error_cents", "acierto"]


def evaluar_dinamica(dinamica, tabla):
    """
    Evalúa las 12 notas de una capa de dinámica (pp, mf o ff).
    Entra: dinamica (str), tabla (dict nombre -> frecuencia).
    Sale: list[dict] con una fila por nota (campos de CAMPOS_CSV).
    Reutiliza evaluar_nota: el mismo pipeline que se validó con sintéticos.
    """
    filas = []
    for ingles, latina in INGLES_A_LATINA.items():
        ruta = os.path.join(CARPETA_SAMPLES, dinamica, f"Piano.{dinamica}.{ingles}.wav")
        fila = evaluar_nota(ruta, latina, tabla)
        fila["dinamica"] = dinamica
        filas.append(fila)
    return filas


def resumen(filas):
    """
    Tasa de reconocimiento y número de notas con error < 5 cents.
    Entra: filas (list[dict]).
    Sale: (tasa en [0, 1], cantidad de notas con |error| < 5 cents).
    """
    tasa = sum(f["acierto"] for f in filas) / len(filas)
    bajo_5 = sum(abs(f["error_cents"]) < 5 for f in filas)
    return tasa, bajo_5


if __name__ == "__main__":
    tabla = tabla_notas()
    todas = []
    for dinamica in DINAMICAS:
        filas = evaluar_dinamica(dinamica, tabla)
        todas += filas
        print(f"--- {dinamica} ---")
        for f in filas:
            print(
                f"{f['nota_real']}: detectada={f['nota_detectada']}, "
                f"f0={f['f0_hz']:.3f} Hz, error={f['error_cents']:.2f} cents, "
                f"acierto={f['acierto']}"
            )
        tasa, bajo_5 = resumen(filas)
        print(f"Reconocimiento: {tasa * 100:.1f}% | error < 5 cents en {bajo_5}/12 notas")

    ruta_csv = os.path.join(RAIZ, "datos", "resultados_reales.csv")
    with open(ruta_csv, "w", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV)
        writer.writeheader()
        writer.writerows(todas)
    print(f"Resultados guardados en {ruta_csv}")
