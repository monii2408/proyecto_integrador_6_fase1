"""Diagrama de bloques del sistema completo (fuente -> preprocesamiento -> FFT ->
detección), para documentar el "montaje" (criterio 1 de la rúbrica: la adquisición
en este proyecto es una cadena de software, no un circuito físico)."""

import os

import matplotlib.pyplot as plt

RAIZ = os.path.join(os.path.dirname(__file__), "..")
CARPETA_FIG = os.path.join(RAIZ, "figuras")

PASOS = [
    "Piano virtual\n(FL Studio)",
    "WAV\n44,1 kHz",
    "Preproceso\n(inicio + ataque)",
    "Hann + FFT\nN = 32 768",
    "Pico +\nfundamental",
    "Interpolación\nparabólica",
    "Nota + error\n(cents)",
]


def graficar_diagrama(ruta_png):
    """
    Dibuja los pasos de PASOS como cajas conectadas por flechas, en una sola
    fila (de izquierda a derecha), para minimizar la altura de la figura.
    Entra: ruta_png (str).
    Sale: nada; guarda ruta_png.
    """
    n = len(PASOS)
    fig, ax = plt.subplots(figsize=(12, 1.9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    xs = [0.07 + i * (0.86 / (n - 1)) for i in range(n)]
    for x, texto in zip(xs, PASOS):
        ax.text(x, 0.5, texto, ha="center", va="center", fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#eaf2fb", edgecolor="tab:blue"))
    for x_izq, x_der in zip(xs[:-1], xs[1:]):
        ax.annotate("", xy=(x_der - 0.058, 0.5), xytext=(x_izq + 0.058, 0.5),
                    arrowprops=dict(arrowstyle="->", color="tab:blue", linewidth=1.3))

    fig.savefig(ruta_png, dpi=150, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


if __name__ == "__main__":
    ruta_png = os.path.join(CARPETA_FIG, "diagrama_bloques.png")
    graficar_diagrama(ruta_png)
    print(f"Figura guardada en {ruta_png}")
