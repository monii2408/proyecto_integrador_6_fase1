"""Justificación del tamaño de FFT N con Do4, el caso más exigente (criterio 3 del plan)."""

import csv
import os

import matplotlib.pyplot as plt
import numpy as np

from deteccion import bajar_a_fundamental, buscar_pico, interpolar_pico
from espectro import espectro
from evaluacion import error_cents
from notas import tabla_notas
from preprocesamiento import preprocesar

RAIZ = os.path.join(os.path.dirname(__file__), "..")
RUTA_SINT = os.path.join(RAIZ, "audio", "sinteticos", "armonicos", "Do4.wav")
RUTA_REAL = os.path.join(RAIZ, "audio", "originales", "mf", "Piano.mf.C4.wav")
TAMANOS_N = [4096, 8192, 16384, 32768, 65536]
UMBRAL_CENTS = 5
CAMPOS_CSV = [
    "n", "delta_f_hz", "delta_f_cents", "ancho_hann_hz", "duracion_s",
    "muestras_disponibles_sint", "muestras_disponibles_real",
    "err_crudo_sint", "err_interp_sint", "err_crudo_real", "err_interp_real",
]


def errores_para_n(senal, fs, n, f_tabla):
    """
    Error de f0 en cents con el bin crudo y con interpolación parabólica, para un N dado.
    Entra: senal (np.ndarray, ya preprocesada), fs (int), n (int), f_tabla (float, Hz).
    Sale: (error del bin crudo, error interpolado), ambos en cents.
    Si la señal tiene menos de n muestras, espectro() rellena con ceros: interpola el
    espectro pero no añade resolución física (sec. 3.6 del plan).
    """
    frecuencias, magnitud = espectro(senal, fs, n)
    k = bajar_a_fundamental(frecuencias, magnitud, buscar_pico(frecuencias, magnitud))
    return error_cents(frecuencias[k], f_tabla), error_cents(interpolar_pico(magnitud, k, fs, n), f_tabla)


def calcular_tabla(f_tabla):
    """
    Una fila por cada N de TAMANOS_N, con la parte teórica y los errores medidos.
    Entra: f_tabla (float, Hz de Do4).
    Sale: list[dict] con los campos de CAMPOS_CSV.
    Teoría: Δf = fs/N (ec. 14); el lóbulo principal de Hann mide 4 bins (4·Δf).
    """
    fs_s, sint = preprocesar(RUTA_SINT)
    fs_r, real = preprocesar(RUTA_REAL)
    filas = []
    for n in TAMANOS_N:
        df = fs_r / n  # espaciado con la fs de las grabaciones reales (44 100 Hz)
        crudo_s, interp_s = errores_para_n(sint, fs_s, n, f_tabla)
        crudo_r, interp_r = errores_para_n(real, fs_r, n, f_tabla)
        filas.append({
            "n": n,
            "delta_f_hz": df,
            "delta_f_cents": error_cents(f_tabla + df, f_tabla),
            "ancho_hann_hz": 4 * df,
            "duracion_s": n / fs_r,
            "muestras_disponibles_sint": len(sint),
            "muestras_disponibles_real": len(real),
            "err_crudo_sint": crudo_s, "err_interp_sint": interp_s,
            "err_crudo_real": crudo_r, "err_interp_real": interp_r,
        })
    return filas


def graficar(filas, ruta_png):
    """
    Error de f0 en Do4 contra N, con y sin interpolación, y el umbral de 5 cents.
    Entra: filas (list[dict], ver calcular_tabla), ruta_png (str).
    Sale: nada; guarda el PNG.
    """
    n = [f["n"] for f in filas]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(n, [abs(f["err_crudo_real"]) for f in filas], "o--", color="tab:blue",
            label="Piano virtual: bin crudo")
    ax.plot(n, [abs(f["err_interp_real"]) for f in filas], "o-", color="tab:blue",
            label="Piano virtual: interpolado")
    ax.plot(n, [abs(f["err_crudo_sint"]) for f in filas], "s--", color="tab:orange",
            label="Sintético: bin crudo")
    ax.plot(n, [abs(f["err_interp_sint"]) for f in filas], "s-", color="tab:orange",
            label="Sintético: interpolado")
    ax.axhline(UMBRAL_CENTS, color="tab:red", linestyle=":", label=f"Criterio: {UMBRAL_CENTS} cents")
    ax.set_xscale("log", base=2)
    ax.set_xticks(n)
    ax.set_xticklabels([str(v) for v in n])
    ax.set_xlabel("Tamaño de FFT, N")
    ax.set_ylabel("|Error de f0| en Do4 (cents)")
    ax.set_title("Do4: error de f0 según N (fs = 44 100 Hz en las grabaciones)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta_png, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    f_tabla = tabla_notas()["Do4"]
    print(f"Do4 = {f_tabla:.3f} Hz | 5 cents = {f_tabla * (2 ** (5 / 1200) - 1):.3f} Hz | "
          f"semitono = {f_tabla * (2 ** (1 / 12) - 1):.2f} Hz")
    filas = calcular_tabla(f_tabla)
    for f in filas:
        print(
            f"N={f['n']:>5}: df={f['delta_f_hz']:6.3f} Hz ({f['delta_f_cents']:5.2f} cents) | "
            f"Hann={f['ancho_hann_hz']:5.2f} Hz | {f['duracion_s']:.3f} s | "
            f"sint crudo/interp={f['err_crudo_sint']:+6.2f}/{f['err_interp_sint']:+5.2f} | "
            f"real crudo/interp={f['err_crudo_real']:+6.2f}/{f['err_interp_real']:+5.2f}"
        )
    print(f"Muestras disponibles tras preprocesar: sintético={filas[0]['muestras_disponibles_sint']}, "
          f"real={filas[0]['muestras_disponibles_real']}")

    ruta_csv = os.path.join(RAIZ, "datos", "justificacion_n.csv")
    with open(ruta_csv, "w", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV)
        writer.writeheader()
        writer.writerows(filas)
    graficar(filas, os.path.join(RAIZ, "figuras", "n_vs_error_Do4.png"))
    print(f"Guardado: {ruta_csv} y figuras/n_vs_error_Do4.png")
