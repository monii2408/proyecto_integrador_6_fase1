"""Figura en el dominio del tiempo: forma de onda de Do4 en pp/mf/ff, con el
inicio detectado y el ataque descartado (criterio 2 de la rúbrica: gráficas de
tiempo que distinguen las condiciones estudiadas)."""

import os

import matplotlib.pyplot as plt
import numpy as np

from evaluar_reales import CARPETA_SAMPLES
from preprocesamiento import cargar_audio, detectar_inicio, normalizar

RAIZ = os.path.join(os.path.dirname(__file__), "..")
CARPETA_FIG = os.path.join(RAIZ, "figuras")
DINAMICAS = ["pp", "mf", "ff"]
MS_ATAQUE = 75  # mismo valor que recortar_ataque() en preprocesamiento.py


def graficar_forma_onda(nota_ingles="C4", nota_latina="Do4", duracion_s=1.5, ruta_png=None):
    """
    Forma de onda normalizada de una nota en las tres intensidades (pp, mf, ff),
    con el inicio detectado por detectar_inicio() y la ventana de ataque
    descartada por recortar_ataque().
    Entra: nota_ingles (str, nombre de archivo), nota_latina (str, para el título),
           duracion_s (float, cuánto mostrar desde el inicio del archivo),
           ruta_png (str).
    Sale: nada; guarda ruta_png.
    Es la única figura del informe en el dominio del tiempo: hasta ahora todas
    eran espectros. Muestra, por ejemplo, que ff empieza casi 1 s después que pp.
    """
    fig, ejes = plt.subplots(3, 1, figsize=(9, 7), sharex=True, sharey=True)
    for ax, dinamica in zip(ejes, DINAMICAS):
        ruta = os.path.join(CARPETA_SAMPLES, dinamica, f"Piano.{dinamica}.{nota_ingles}.wav")
        fs, senal = cargar_audio(ruta)
        senal = normalizar(senal)
        inicio = detectar_inicio(senal, fs)

        n_max = int(duracion_s * fs)
        t = np.arange(min(n_max, len(senal))) / fs
        ax.plot(t, senal[: len(t)], linewidth=0.4, color="tab:blue")

        t_inicio = inicio / fs
        t_fin_ataque = t_inicio + MS_ATAQUE / 1000
        ax.axvline(t_inicio, color="tab:orange", linestyle="--",
                    label=f"Inicio detectado: {t_inicio * 1000:.0f} ms")
        ax.axvspan(t_inicio, t_fin_ataque, color="tab:red", alpha=0.15,
                   label=f"Ataque descartado ({MS_ATAQUE} ms)")
        ax.set_ylabel(f"{dinamica}\nAmplitud")
        ax.set_ylim(-1.05, 1.05)
        ax.legend(fontsize=8, loc="upper right")

    ejes[-1].set_xlabel("Tiempo (s)")
    ejes[-1].set_xlim(0, duracion_s)
    fig.suptitle(f"{nota_latina}: forma de onda normalizada en pp, mf y ff "
                 f"(primeros {duracion_s} s)")
    fig.tight_layout()
    fig.savefig(ruta_png, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    ruta_png = os.path.join(CARPETA_FIG, "forma_onda_Do4_pp_mf_ff.png")
    graficar_forma_onda(ruta_png=ruta_png)
    print(f"Figura guardada en {ruta_png}")
