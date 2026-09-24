"""Figuras del informe: espectros de las 12 notas (piano virtual mf vs. sintético) y error en cents."""

import os

import matplotlib.pyplot as plt
import numpy as np

from deteccion import F_MAX, F_MIN, bajar_a_fundamental, buscar_pico, interpolar_pico
from espectro import espectro
from evaluacion import error_cents
from evaluar_reales import INGLES_A_LATINA
from notas import tabla_notas
from preprocesamiento import preprocesar

RAIZ = os.path.join(os.path.dirname(__file__), "..")
CARPETA_REAL = os.path.join(RAIZ, "audio", "originales", "mf")
CARPETA_SINT = os.path.join(RAIZ, "audio", "sinteticos", "armonicos")
CARPETA_FIG = os.path.join(RAIZ, "figuras")
F_TOPE_VISTA = 2000  # Hz, hasta dónde se dibuja cada espectro
VENTANA_ZOOM = 10    # Hz a cada lado de la frecuencia teórica en la figura de zoom
UMBRAL_CENTS = 5     # criterio 2 del plan


def analizar(ruta_wav, f_tabla):
    """
    Corre el pipeline sobre un WAV y devuelve lo necesario para dibujarlo.
    Entra: ruta_wav (str), f_tabla (float, Hz de la nota esperada).
    Sale: dict con frecuencias, magnitud normalizada al pico de la banda 80-1000 Hz,
          f0 (Hz interpolada) y error (cents contra f_tabla).
    Es el mismo camino que evaluacion.py: pico -> bajar a la fundamental -> interpolar.
    """
    fs, senal = preprocesar(ruta_wav)
    frecuencias, magnitud = espectro(senal, fs)
    k = bajar_a_fundamental(frecuencias, magnitud, buscar_pico(frecuencias, magnitud))
    f0 = interpolar_pico(magnitud, k, fs)
    banda = (frecuencias >= F_MIN) & (frecuencias <= F_MAX)
    return {
        "frecuencias": frecuencias,
        "magnitud": magnitud / magnitud[banda].max(),
        "f0": f0,
        "error": error_cents(f0, f_tabla),
    }


def analizar_todas(tabla):
    """
    Analiza las 12 notas en las dos fuentes.
    Entra: tabla (dict nombre -> frecuencia).
    Sale: dict nombre -> {"real": resultado, "sintetico": resultado} (ver analizar).
    """
    ingles = {latina: ing for ing, latina in INGLES_A_LATINA.items()}
    return {
        nota: {
            "real": analizar(os.path.join(CARPETA_REAL, f"Piano.mf.{ingles[nota]}.wav"), f),
            "sintetico": analizar(os.path.join(CARPETA_SINT, f"{nota}.wav"), f),
        }
        for nota, f in tabla.items()
    }


def figura_espectros(datos, tabla, ruta_png):
    """
    Cuadrícula 4x3 con el espectro de cada nota: real (azul) y sintético (naranja).
    Entra: datos (ver analizar_todas), tabla (dict), ruta_png (str).
    Sale: nada; guarda el PNG.
    Escala logarítmica: permite ver los armónicos débiles y el piso de ruido.
    La línea punteada es la frecuencia de la tabla y las marcas son los f0 estimados.
    """
    fig, ejes = plt.subplots(4, 3, figsize=(13, 13), sharex=True, sharey=True)
    for ax, (nota, f_tabla) in zip(ejes.flat, tabla.items()):
        for fuente, color, etiqueta in (("real", "tab:blue", "Piano virtual (mf)"),
                                        ("sintetico", "tab:orange", "Sintético")):
            r = datos[nota][fuente]
            vista = r["frecuencias"] <= F_TOPE_VISTA
            ax.plot(r["frecuencias"][vista], r["magnitud"][vista], color=color,
                    linewidth=0.8, alpha=0.9, label=etiqueta)
        ax.axvspan(F_MIN, F_MAX, color="tab:green", alpha=0.08)
        ax.axvline(f_tabla, color="black", linestyle=":", linewidth=1)
        ax.set_yscale("log")
        ax.set_ylim(1e-4, 5)
        ax.set_title(f"{nota} ({f_tabla:.1f} Hz): real {datos[nota]['real']['error']:+.1f} c, "
                     f"sint. {datos[nota]['sintetico']['error']:+.1f} c", fontsize=10)
    for ax in ejes[-1]:
        ax.set_xlabel("Frecuencia (Hz)")
    for ax in ejes[:, 0]:
        ax.set_ylabel("Magnitud normalizada")
    ejes[0, 0].legend(fontsize=8, loc="lower right")
    fig.suptitle("Espectros de las 12 notas (Hann, N = 32 768). Banda verde: rango de búsqueda "
                 "80-1000 Hz; línea punteada: frecuencia de la tabla", fontsize=11)
    fig.tight_layout()
    fig.savefig(ruta_png, dpi=130)
    plt.close(fig)


def figura_errores(datos, ruta_png):
    """
    Error en cents por nota, real vs. sintético, con la banda de ±5 cents del criterio.
    Entra: datos (ver analizar_todas), ruta_png (str).
    Sale: nada; guarda el PNG.
    """
    notas = list(datos)
    x = np.arange(len(notas))
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.axhspan(-UMBRAL_CENTS, UMBRAL_CENTS, color="tab:green", alpha=0.12,
               label=f"±{UMBRAL_CENTS} cents (criterio)")
    ax.bar(x - 0.2, [datos[n]["sintetico"]["error"] for n in notas], 0.4,
           color="tab:orange", label="Sintético")
    ax.bar(x + 0.2, [datos[n]["real"]["error"] for n in notas], 0.4,
           color="tab:blue", label="Piano virtual (mf)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(notas)
    ax.set_ylabel("Error de f0 (cents)")
    ax.set_title("Error de f0 respecto a la tabla (La4 = 440 Hz), 12 notas")
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta_png, dpi=150)
    plt.close(fig)


def figura_zoom(datos, nota, f_tabla, ruta_png):
    """
    Zoom de ±VENTANA_ZOOM Hz sobre el pico de una nota, real vs. sintético.
    Entra: datos (ver analizar_todas), nota (str), f_tabla (float), ruta_png (str).
    Sale: nada; guarda el PNG.
    Cada punto es un bin (Δf = fs/N). La línea vertical es el f0 tras interpolar.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for fuente, color, etiqueta in (("real", "tab:blue", "Piano virtual (mf)"),
                                    ("sintetico", "tab:orange", "Sintético")):
        r = datos[nota][fuente]
        zoom = abs(r["frecuencias"] - f_tabla) <= VENTANA_ZOOM
        ax.plot(r["frecuencias"][zoom], r["magnitud"][zoom], "o-", markersize=3,
                color=color, label=f"{etiqueta}: f0 = {r['f0']:.3f} Hz ({r['error']:+.2f} cents)")
        ax.axvline(r["f0"], color=color, linestyle="-", linewidth=1)
    ax.axvline(f_tabla, color="black", linestyle=":", label=f"Tabla: {f_tabla:.3f} Hz")
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Magnitud normalizada")
    ax.set_title(f"{nota}: zoom de ±{VENTANA_ZOOM} Hz sobre la fundamental")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_ylim(top=1.5)  # espacio arriba para que la leyenda no tape el pico
    fig.tight_layout()
    fig.savefig(ruta_png, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    tabla = tabla_notas()
    datos = analizar_todas(tabla)
    figura_espectros(datos, tabla, os.path.join(CARPETA_FIG, "espectros_12_notas.png"))
    figura_errores(datos, os.path.join(CARPETA_FIG, "error_cents_12_notas.png"))
    figura_zoom(datos, "Do4", tabla["Do4"], os.path.join(CARPETA_FIG, "zoom_Do4_real_vs_sintetico.png"))
    for nota in tabla:
        print(f"{nota}: real {datos[nota]['real']['error']:+.2f} cents | "
              f"sintético {datos[nota]['sintetico']['error']:+.2f} cents")
    print(f"Figuras guardadas en {CARPETA_FIG}")
