"""Figura del espectro de una nota: vista completa y zoom sobre el pico (ecuaciones 14, 15, 16 del plan)."""

import os

import matplotlib.pyplot as plt

from deteccion import F_MAX, F_MIN, buscar_pico, interpolar_pico
from espectro import espectro
from evaluacion import error_cents
from notas import tabla_notas
from preprocesamiento import preprocesar

F_TOPE_VISTA = 2000  # Hz, hasta dónde se dibuja el panel A
VENTANA_ZOOM = 10    # Hz a cada lado de la frecuencia teórica en el panel B


def graficar_espectro(ruta_wav, nota, ruta_png):
    """
    Dibuja el espectro de una nota con el pico crudo, el f0 interpolado y la
    frecuencia teórica marcados, y guarda la figura como PNG.
    Entra: ruta_wav (str), nota (str, nombre en la tabla, p. ej. "Do4"), ruta_png (str).
    Sale: nada; crea/sobrescribe ruta_png.
    No calcula nada nuevo: solo dibuja lo que devuelven espectro(), buscar_pico()
    e interpolar_pico().
    """
    fs, senal = preprocesar(ruta_wav)
    frecuencias, magnitud = espectro(senal, fs)
    k = buscar_pico(frecuencias, magnitud)
    f_cruda = frecuencias[k]
    f0 = interpolar_pico(magnitud, k, fs)
    f_tabla = tabla_notas()[nota]

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Panel A: la nota completa. Se ve la fundamental y sus armónicos, y la banda
    # de búsqueda 80-1000 Hz que evita confundir la fundamental con un armónico.
    vista = frecuencias <= F_TOPE_VISTA
    ax_a.plot(frecuencias[vista], magnitud[vista], color="tab:blue", linewidth=1)
    ax_a.axvspan(F_MIN, F_MAX, color="tab:green", alpha=0.12,
                 label=f"Rango de búsqueda ({F_MIN}-{F_MAX} Hz)")
    ax_a.set_xlabel("Frecuencia (Hz)")
    ax_a.set_ylabel("Magnitud (u.a.)")
    ax_a.set_title(f"{nota}: espectro con ventana de Hann")
    ax_a.legend()

    # Panel B: zoom sobre el pico. Cada punto es un bin de la FFT (separados
    # Δf = fs/N); el bin más alto solo acierta hasta media resolución, y la
    # parábola por los 3 puntos centrales estima dónde está el máximo real.
    zoom = abs(frecuencias - f_tabla) <= VENTANA_ZOOM
    ax_b.plot(frecuencias[zoom], magnitud[zoom], "o-", color="tab:blue", markersize=4,
              label="Bins de la FFT")
    ax_b.axvline(f_cruda, color="tab:orange", linestyle="--",
                 label=f"Bin crudo: {f_cruda:.3f} Hz ({error_cents(f_cruda, f_tabla):+.2f} cents)")
    ax_b.axvline(f0, color="tab:red", linestyle="-",
                 label=f"f0 interpolado: {f0:.3f} Hz ({error_cents(f0, f_tabla):+.2f} cents)")
    ax_b.axvline(f_tabla, color="black", linestyle=":",
                 label=f"Tabla: {f_tabla:.3f} Hz")
    ax_b.set_xlabel("Frecuencia (Hz)")
    ax_b.set_ylabel("Magnitud (u.a.)")
    ax_b.set_title(f"{nota}: zoom de ±{VENTANA_ZOOM} Hz sobre el pico")
    ax_b.set_ylim(top=1.5 * magnitud[k])  # deja espacio arriba para que la leyenda no tape el pico
    ax_b.legend(fontsize=8, loc="upper left")

    fig.tight_layout()
    fig.savefig(ruta_png, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..")
    ruta_wav = os.path.join(base, "audio", "sinteticos", "armonicos", "Do4.wav")
    ruta_png = os.path.join(base, "figuras", "espectro_Do4.png")
    graficar_espectro(ruta_wav, "Do4", ruta_png)
    print(f"Figura guardada en {ruta_png}")
