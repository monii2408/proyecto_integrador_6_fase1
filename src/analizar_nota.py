"""Demo: analiza un WAV cualquiera y responde qué nota es, su f0 y el error en cents."""

import argparse
import os
import warnings

from scipy.io.wavfile import WavFileWarning

from deteccion import F_MAX, F_MIN, bajar_a_fundamental, buscar_pico, interpolar_pico
from espectro import N, espectro
from evaluacion import error_cents, identificar_nota
from notas import tabla_notas
from preprocesamiento import preprocesar

RAIZ = os.path.join(os.path.dirname(__file__), "..")
CARPETA_FIG = os.path.join(RAIZ, "figuras")
VENTANA_ZOOM = 10  # Hz a cada lado de f0 en el panel de zoom

# Si f0 cae a más de medio semitono de cualquier nota de la tabla, la nota "más
# cercana" no es fiable: la señal está fuera de Do4-Si4 o no es una nota limpia.
UMBRAL_CONFIANZA_CENTS = 50

# Los WAV de FL Studio traen un bloque de metadatos que scipy se salta con un aviso.
# No afecta al audio; se silencia solo aquí para que la demo salga limpia.
warnings.filterwarnings("ignore", category=WavFileWarning)


def analizar_nota(ruta_wav, tabla=None):
    """
    Pipeline completo sobre un solo WAV, sin saber de antemano qué nota es.
    Entra: ruta_wav (str), tabla (dict nombre -> frecuencia, por defecto tabla_notas()).
    Sale: dict con fs, f0_hz, nota, f_tabla_hz, error_cents (contra la nota detectada)
          y, para poder graficar sin repetir el análisis, frecuencias, magnitud y k
          (bin de la fundamental).
    Mismo camino que evaluacion.py: preprocesar -> espectro -> pico -> fundamental -> interpolar -> identificar.
    """
    if tabla is None:
        tabla = tabla_notas()
    fs, senal = preprocesar(ruta_wav)
    frecuencias, magnitud = espectro(senal, fs)
    k = bajar_a_fundamental(frecuencias, magnitud, buscar_pico(frecuencias, magnitud))
    f0 = interpolar_pico(magnitud, k, fs)
    nota = identificar_nota(f0, tabla)
    return {
        "fs": fs,
        "f0_hz": f0,
        "nota": nota,
        "f_tabla_hz": tabla[nota],
        "error_cents": error_cents(f0, tabla[nota]),
        "frecuencias": frecuencias,
        "magnitud": magnitud,
        "k": k,
    }


def graficar(ruta_wav, r, ruta_png):
    """
    Dibuja el espectro de la nota ya analizada: vista completa (hasta 2000 Hz,
    con la banda de búsqueda) y zoom sobre el pico con el f0 interpolado.
    Entra: ruta_wav (str, solo para el título), r (dict, salida de analizar_nota,
           debe incluir frecuencias/magnitud/k), ruta_png (str).
    Sale: nada; crea/sobrescribe ruta_png.
    Mismo criterio que graficar_espectro.py, pero sobre la fundamental ya
    corregida (bajar_a_fundamental) y no solo el pico máximo bruto.
    """
    import matplotlib.pyplot as plt

    frecuencias, magnitud, k = r["frecuencias"], r["magnitud"], r["k"]
    f_cruda = frecuencias[k]

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 4.5))

    vista = frecuencias <= 2000
    ax_a.plot(frecuencias[vista], magnitud[vista], color="tab:blue", linewidth=1)
    ax_a.axvspan(F_MIN, F_MAX, color="tab:green", alpha=0.12,
                 label=f"Rango de búsqueda ({F_MIN}-{F_MAX} Hz)")
    ax_a.set_xlabel("Frecuencia (Hz)")
    ax_a.set_ylabel("Magnitud (u.a.)")
    ax_a.set_title(f"{os.path.basename(ruta_wav)}: espectro con ventana de Hann")
    ax_a.legend()

    zoom = abs(frecuencias - f_cruda) <= VENTANA_ZOOM
    ax_b.plot(frecuencias[zoom], magnitud[zoom], "o-", color="tab:blue", markersize=4,
              label="Bins de la FFT")
    ax_b.axvline(f_cruda, color="tab:orange", linestyle="--", label=f"Bin crudo: {f_cruda:.3f} Hz")
    ax_b.axvline(r["f0_hz"], color="tab:red", linestyle="-",
                 label=f"f0 interpolado: {r['f0_hz']:.3f} Hz")
    ax_b.axvline(r["f_tabla_hz"], color="black", linestyle=":",
                 label=f"Tabla ({r['nota']}): {r['f_tabla_hz']:.3f} Hz")
    ax_b.set_xlabel("Frecuencia (Hz)")
    ax_b.set_ylabel("Magnitud (u.a.)")
    ax_b.set_title(f"Zoom de ±{VENTANA_ZOOM} Hz sobre el pico ({r['error_cents']:+.2f} cents)")
    ax_b.set_ylim(top=1.5 * magnitud[k])
    ax_b.legend(fontsize=8, loc="upper left")

    fig.tight_layout()
    fig.savefig(ruta_png, dpi=150)
    plt.close(fig)


def main():
    """Lee la ruta del WAV (y, opcionalmente, la nota esperada) e imprime el resultado."""
    parser = argparse.ArgumentParser(description="Detecta la nota musical de un archivo WAV.")
    parser.add_argument("wav", help="ruta del archivo WAV (una sola nota, rango Do4-Si4)")
    parser.add_argument("--esperada", help="nota que debería ser (p. ej. Do4), para comprobar el acierto")
    parser.add_argument("--figura", action="store_true",
                         help="además del texto, guarda el espectro de la nota como PNG en figuras/")
    args = parser.parse_args()

    r = analizar_nota(args.wav)
    print(f"Archivo:        {args.wav}")
    print(f"fs = {r['fs']} Hz | N = {N} | df = {r['fs'] / N:.3f} Hz")
    print(f"f0 estimada:    {r['f0_hz']:.3f} Hz")
    print(f"Nota detectada: {r['nota']} (tabla: {r['f_tabla_hz']:.3f} Hz)")
    print(f"Error:          {r['error_cents']:+.2f} cents")
    if abs(r["error_cents"]) > UMBRAL_CONFIANZA_CENTS * 0.99:
        print("Aviso: f0 esta a casi medio semitono de la nota mas cercana; "
              "el resultado no es fiable (senal fuera de Do4-Si4 o no es una nota limpia).")
    if args.esperada:
        veredicto = "CORRECTO" if r["nota"] == args.esperada else "INCORRECTO"
        print(f"Esperada:       {args.esperada} -> {veredicto}")
    if args.figura:
        os.makedirs(CARPETA_FIG, exist_ok=True)
        base = os.path.splitext(os.path.basename(args.wav))[0]
        ruta_png = os.path.join(CARPETA_FIG, f"analisis_{base}.png")
        graficar(args.wav, r, ruta_png)
        print(f"Figura:         {ruta_png}")


if __name__ == "__main__":
    main()
