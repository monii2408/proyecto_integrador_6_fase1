"""Diagrama de bloques del sistema completo (fuente -> preprocesamiento -> FFT ->
detección), para documentar el "montaje" (criterio 1 de la rúbrica: la adquisición
en este proyecto es una cadena de software, no un circuito físico)."""

import os

import matplotlib.pyplot as plt

RAIZ = os.path.join(os.path.dirname(__file__), "..")
CARPETA_FIG = os.path.join(RAIZ, "figuras")

PASOS = [
    "Piano virtual (FL Studio)\n12 notas x 3 intensidades (pp, mf, ff)",
    "Archivo WAV\n44 100 Hz, 16 bits, estéreo\naudio/originales/",
    "Preprocesamiento\nmono, normalizar, detectar inicio (RMS),\nrecortar ataque (75 ms)",
    "Ventana de Hann + FFT\nN = 32 768, Δf ≈ 1,35 Hz",
    "Detección de pico (80-1000 Hz)\ny bajada a la fundamental (f/2, f/3, f/4)",
    "Interpolación parabólica\nprecisión sub-bin",
    "Identificación de nota + error en cents\ndatos/resultados_reales.csv",
]


def graficar_diagrama(ruta_png):
    """
    Dibuja los pasos de PASOS como cajas conectadas por flechas, de arriba a abajo.
    Entra: ruta_png (str).
    Sale: nada; guarda ruta_png.
    """
    n = len(PASOS)
    fig, ax = plt.subplots(figsize=(5, 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ys = [0.94 - i * (0.88 / (n - 1)) for i in range(n)]
    for y, texto in zip(ys, PASOS):
        ax.text(0.5, y, texto, ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#eaf2fb", edgecolor="tab:blue"))
    for y_arriba, y_abajo in zip(ys[:-1], ys[1:]):
        ax.annotate("", xy=(0.5, y_abajo + 0.045), xytext=(0.5, y_arriba - 0.045),
                    arrowprops=dict(arrowstyle="->", color="tab:blue", linewidth=1.3))

    fig.tight_layout()
    fig.savefig(ruta_png, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    ruta_png = os.path.join(CARPETA_FIG, "diagrama_bloques.png")
    graficar_diagrama(ruta_png)
    print(f"Figura guardada en {ruta_png}")
