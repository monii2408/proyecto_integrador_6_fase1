"""Demo: analiza un WAV cualquiera y responde qué nota es, su f0 y el error en cents."""

import argparse
import warnings

from scipy.io.wavfile import WavFileWarning

from deteccion import detectar_f0
from espectro import N, espectro
from evaluacion import error_cents, identificar_nota
from notas import tabla_notas
from preprocesamiento import preprocesar

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
    Sale: dict con fs, f0_hz, nota, f_tabla_hz y error_cents (contra la nota detectada).
    Mismo camino que evaluacion.py: preprocesar -> espectro -> detectar_f0 -> identificar.
    """
    if tabla is None:
        tabla = tabla_notas()
    fs, senal = preprocesar(ruta_wav)
    frecuencias, magnitud = espectro(senal, fs)
    f0 = detectar_f0(frecuencias, magnitud, fs)
    nota = identificar_nota(f0, tabla)
    return {
        "fs": fs,
        "f0_hz": f0,
        "nota": nota,
        "f_tabla_hz": tabla[nota],
        "error_cents": error_cents(f0, tabla[nota]),
    }


def main():
    """Lee la ruta del WAV (y, opcionalmente, la nota esperada) e imprime el resultado."""
    parser = argparse.ArgumentParser(description="Detecta la nota musical de un archivo WAV.")
    parser.add_argument("wav", help="ruta del archivo WAV (una sola nota, rango Do4-Si4)")
    parser.add_argument("--esperada", help="nota que debería ser (p. ej. Do4), para comprobar el acierto")
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


if __name__ == "__main__":
    main()
