# Proyecto Integrador 6 · Fase 1 — Analizador de Notas Musicales

**Curso:** Señales y Sistemas (EE2004) · Instituto Kriete de Ingeniería y Ciencias
**Integrantes:** Monica Daniela Alvarenga Mejia · Rodrigo José Marroquín Quijada
**Docente:** Alfonso Abraham Alvarenga Gamero
**Período de la Fase 1:** 9 – 25 de septiembre de 2026

## ¿Qué hace este sistema?

Captura una nota musical (Do4 – Si4) con el micrófono de la laptop, calcula su espectro
con la FFT, estima la frecuencia fundamental f0 con precisión sub-bin (interpolación
parabólica) e identifica la nota comparándola con la tabla del temperamento igual
(La4 = 440 Hz). Reporta el error en *cents*.

```
WAV → normalizar → recortar ataque → ventana de Hann → FFT → pico (80–1000 Hz)
    → interpolación parabólica → f0 → nota + error en cents
```

Todo el análisis ocurre en software (Python). El hardware se limita a la adquisición.

## Decisiones de diseño (cerradas en el Plan de acción v2)

| Parámetro | Valor | Por qué |
|---|---|---|
| Adquisición | Piano virtual en FL Studio: 36 WAV (12 notas × pp, mf, ff) en `audio/originales/` | Permitido por la Declaración de PBL (p. 38, "teclado virtual en PC"). El plan v2 preveía micrófono de la laptop; ver bitácora, entrada 15 |
| Frecuencia de muestreo `fs` | 44 100 Hz (audio de FL Studio) · 48 000 Hz (sintéticos) | El pipeline usa la `fs` de cada archivo; con 44 100 Hz, Nyquist = 22,05 kHz, muy por encima de los armónicos de interés |
| Tamaño de FFT `N` | 32 768 | Δf = fs/N ≈ 1,35 Hz (44 100 Hz) o 1,46 Hz (48 000 Hz); usa 0,74 s de los ~0,9 s útiles. Justificación con Do4: `src/justificar_n.py` y bitácora, entrada 17 |
| Ventana | Hann | Reduce la fuga espectral |
| Rango de búsqueda de f0 | 80 – 1000 Hz | Evita confundir la fundamental con armónicos altos |
| Estimación fina | Interpolación parabólica del pico | Imprescindible para bajar de 5 cents en Do4 |
| Fundamental vs. armónico | Si hay un pico ≥ 25 % del máximo en f/2, f/3 o f/4, ese es la fundamental | En el piano el 2.º o 3.er armónico puede superar a la fundamental (bitácora, entradas 12–13) |
| Inicio de nota | Primera ventana de 10 ms con RMS > 10 % del máximo | Los samples traen silencio antes de la tecla (hasta ~1 s en ff) |
| Duración por nota | ~1 s | Se descartan 75 ms de ataque, contados desde el inicio real de la nota |

Detalle y justificación completa: `informe/Plan_de_Accion_v2.pdf`.

## Criterios de éxito de la Fase 1

1. Reconocimiento correcto ≥ 90 % sobre las 12 notas.
2. Error de f0 < 5 cents en al menos 10 de las 12 notas.
3. Justificar la elección de `N` con Do4 como caso más exigente.
4. Resultados reproducibles por un tercero desde este repositorio.
5. Bitácora con errores y modificaciones relevantes.

## Instalación

**Requiere Python 3.13** (probado con 3.13.14). Con Python 3.14 la instalación falla: `scipy==1.15.3`
no tiene versión precompilada para 3.14 y pip intenta compilarlo (ver bitácora, entrada 18).

```bash
git clone https://github.com/monii2408/proyecto_integrador_6_fase1.git
cd proyecto_integrador_6_fase1
# Windows:
py -3.13 -m venv .venv
.venv\Scripts\activate
# macOS/Linux:
#   python3.13 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
```

Verificación rápida de que el entorno funciona:

```bash
python -c "import numpy, scipy, matplotlib, sounddevice; print('OK')"
```

## Ejecución

Todos los comandos se ejecutan desde la raíz del repositorio, con el `.venv` activo.
En Windows, si al imprimir aparece `UnicodeEncodeError`, ejecutar antes
`$env:PYTHONIOENCODING="utf-8"` (PowerShell).

**Analizar una nota (demo):**

```bash
python src/analizar_nota.py audio/originales/mf/Piano.mf.C4.wav
python src/analizar_nota.py audio/originales/mf/Piano.mf.C4.wav --esperada Do4
```

Devuelve la f0 estimada, la nota detectada y el error en cents.

**Reproducir los resultados del informe:**

| Comando | Qué produce |
|---|---|
| `python src/evaluacion.py` | Pipeline sobre los 12 sintéticos → `datos/resultados.csv` |
| `python src/evaluar_reales.py` | Pipeline sobre los 36 WAV de FL Studio (pp, mf, ff) → `datos/resultados_reales.csv` |
| `python src/prueba_armonicos.py` | Robustez frente a armónicos (tonos en `audio/sinteticos/armonicos/`) |
| `python src/prueba_ruido.py` | Barrido de SNR de 40 a −30 dB → `datos/resultados_ruido.csv` |
| `python src/graficar_comparacion.py` | Espectros de las 12 notas, error por nota y zoom de Do4 → `figuras/` |
| `python src/justificar_n.py` | Error de f0 contra N con Do4 → `datos/justificacion_n.csv`, `figuras/n_vs_error_Do4.png` |
| `python src/graficar_espectro.py` | Espectro de Do4 sintético con pico crudo e interpolado → `figuras/espectro_Do4.png` |

Un módulo por etapa del pipeline (ver `src/`):

| Módulo | Etapa | Ecuaciones del plan |
|---|---|---|
| `src/notas.py` | Tabla del temperamento igual | (7), (8) |
| `src/preprocesamiento.py` | Carga, normalización, inicio de nota y recorte del ataque | sec. 3.4 |
| `src/espectro.py` | Ventana de Hann y FFT, eje de frecuencias | (11), (12), (14) |
| `src/deteccion.py` | Pico en 80–1000 Hz, bajada a la fundamental e interpolación parabólica | (15), (16) |
| `src/evaluacion.py` | Error en cents y tasa de reconocimiento | (9) |

## Resultados (ejecutados con este código)

| Conjunto | Reconocimiento | Error < 5 cents |
|---|---|---|
| Sintéticos (12 notas) | 12/12 | 12/12 (máx. 0,43 cents) |
| Piano virtual, mf (conjunto de referencia) | 12/12 | 10/12 |
| Piano virtual, pp | 12/12 | 10/12 |
| Piano virtual, ff | 12/12 | 8/12 |

- Con audio del piano virtual el error medio es de ≈ +4 cents y siempre positivo; en los sintéticos no aparece. La causa no está verificada (hipótesis: afinación de la fuente en FL Studio). Las notas con mayor error son Do#4 y Sol#4. Con la referencia oficial La4 = 440 Hz, el criterio 2 se cumple en mf y pp, y no en ff.
- Robustez al ruido blanco (sobre sintéticos): 100 % hasta SNR = −10 dB; falla entre −10 y −20 dB. No se probó ruido de sala.
- Detalle, límites y errores encontrados: `bitacora/bitacora.md`.

## Estructura del repositorio

```
proyecto_integrador_6_fase1/
├── README.md               este archivo
├── CLAUDE.md               contexto y reglas para trabajar con Claude Code
├── requirements.txt        dependencias con versión fijada
├── audio/
│   ├── originales/         WAV de FL Studio en pp/, mf/, ff/ (NUNCA se sobrescriben) y su léeme
│   ├── sinteticos/         tonos de prueba de frecuencia conocida (y armonicos/)
│   └── procesados/         señales normalizadas y recortadas
├── src/                    código del pipeline, demo (analizar_nota.py) y scripts de evaluación y figuras
├── datos/                  resultados.csv (sintéticos), resultados_reales.csv, resultados_ruido.csv,
│                           justificacion_n.csv: nota real, nota detectada, f0, error en cents
├── figuras/                espectros anotados para el informe
├── informe/                plan de acción e informe técnico
└── bitacora/bitacora.md    entregable transversal obligatorio
```

## Roles

| Integrante | Rol principal | Responsabilidades |
|---|---|---|
| Rodrigo (Integrante 1) | Adquisición y documentación | Grabaciones, verificación en Audacity, respaldo de WAV, bitácora, referencias, redacción del informe |
| Monica (Integrante 2) | Procesamiento y análisis | Código del pipeline, FFT, detección, interpolación, error en cents, tabla de resultados y figuras |
| Ambos | Revisión técnica y decisiones | Revisión cruzada antes de cada hito; elección de fs y N; validación de resultados |

## Reglas de trabajo del equipo

- **Un commit como mínimo por sesión** (mitigación del riesgo "pérdida de código").
- **Cada cambio relevante deja una entrada en `bitacora/bitacora.md`** con el formato definido allí.
- Los archivos de `audio/originales/` no se editan; se trabaja sobre copias en `audio/procesados/`.
- Antes de cada hito, el otro integrante clona y ejecuta el repositorio en su equipo.
- Los tonos sintéticos se validan **antes** que las grabaciones reales: si falla con una senoide de frecuencia conocida, el error está en el código, no en el micrófono.

## Hitos

| Fecha | Sesión | Hito |
|---|---|---|
| 11 sep | 1 | Plan de acción v2 · repositorio · bitácora 01–02 |
| 16 sep | 2 | **Punto de avance:** FFT de extremo a extremo sobre 3–4 notas |
| 18 sep | 3 | **Revisión de avance:** identificación automática + tabla parcial |
| 23 sep | 4 | Evaluación de las 12 notas · borrador del informe |
| 25 sep | 5 | **Entrega final** de la Fase 1 |

## Referencias principales

- J. O. Smith III, *Spectral Audio Signal Processing*, secciones "Quadratic Interpolation of Spectral Peaks" y "Zero Padding Applications". https://ccrma.stanford.edu/~jos/sasp/
- NumPy `numpy.fft.fft` · SciPy `scipy.signal.windows.hann` (documentación oficial).
- ISO 16:1975 — Frecuencia de afinación normalizada (La4 = 440 Hz).

## Uso de herramientas de IA

Se utilizó Claude (Anthropic) para revisar la estructura del plan frente a la rúbrica, detectar omisiones y producir borradores de organización. El contenido técnico, los cálculos y las decisiones de diseño son responsabilidad de los integrantes.
