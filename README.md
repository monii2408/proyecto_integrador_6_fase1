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
| Adquisición | Micrófono + tarjeta de sonido de la laptop | 16 bits, filtro antialiasing incluido, sin compra |
| Frecuencia de muestreo `fs` | 48 000 Hz | Nativa del codec; Nyquist = 24 kHz, muy por encima de los armónicos de interés |
| Tamaño de FFT `N` | 32 768 | Δf = fs/N ≈ 1,46 Hz; usa 0,74 s de los ~0,9 s útiles |
| Ventana | Hann | Reduce la fuga espectral |
| Rango de búsqueda de f0 | 80 – 1000 Hz | Evita confundir la fundamental con armónicos altos |
| Estimación fina | Interpolación parabólica del pico | Imprescindible para bajar de 5 cents en Do4 |
| Duración por nota | ~1 s | Se descartan los primeros 50–100 ms (ataque) |

Detalle y justificación completa: `informe/Plan_de_Accion_v2.pdf`.

## Criterios de éxito de la Fase 1

1. Reconocimiento correcto ≥ 90 % sobre las 12 notas.
2. Error de f0 < 5 cents en al menos 10 de las 12 notas.
3. Justificar la elección de `N` con Do4 como caso más exigente.
4. Resultados reproducibles por un tercero desde este repositorio.
5. Bitácora con errores y modificaciones relevantes.

## Instalación

```bash
git clone <URL-del-repositorio>
cd proyecto_integrador_6_fase1
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Verificación rápida de que el entorno funciona:

```bash
python -c "import numpy, scipy, matplotlib, sounddevice; print('OK')"
```

## Ejecución

> Esta sección se completa a medida que existan los scripts. Estado actual: **esqueleto del repositorio, sin código aún.**

Orden previsto del pipeline (un módulo por etapa, ver `src/`):

| Módulo | Etapa | Ecuaciones del plan |
|---|---|---|
| `src/notas.py` | Tabla del temperamento igual | (7), (8) |
| `src/preprocesamiento.py` | Carga, normalización, recorte del ataque | sec. 3.4 |
| `src/espectro.py` | Ventana de Hann y FFT, eje de frecuencias | (11), (12), (14) |
| `src/deteccion.py` | Pico en 80–1000 Hz e interpolación parabólica | (15), (16) |
| `src/evaluacion.py` | Error en cents y tasa de reconocimiento | (9) |

## Estructura del repositorio

```
proyecto_integrador_6_fase1/
├── README.md               este archivo
├── CLAUDE.md               contexto y reglas para trabajar con Claude Code
├── requirements.txt        dependencias con versión fijada
├── audio/
│   ├── originales/         grabaciones sin modificar (NUNCA se sobrescriben)
│   ├── sinteticos/         tonos de prueba de frecuencia conocida
│   └── procesados/         señales normalizadas y recortadas
├── src/                    código del pipeline
├── datos/resultados.csv    nota real, nota detectada, f0, error en cents
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
