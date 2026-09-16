# Bitácora de iteraciones — Fase 1

Entregable transversal obligatorio del PBL. Cada cambio relevante del sistema queda registrado
con sus parámetros, resultados, fallos y aprendizajes. **Se registra también lo que salió mal.**

## Formato de cada entrada

| Campo | Contenido |
|---|---|
| Fecha | Día en que se realizó la prueba o el cambio |
| Versión | Versión del sistema o hash del commit |
| Objetivo | Qué se quería comprobar o conseguir |
| Parámetros | fs, N, ventana, duración del tramo, archivo analizado |
| Qué se probó | Descripción breve del experimento o modificación |
| Resultado | Datos observados, con valores concretos |
| Fallo o aprendizaje | Error encontrado o conocimiento obtenido, aunque la prueba no saliera bien |
| Decisión siguiente | Cambio concreto que se implementará a continuación |
| Responsable | Integrante que realizó la tarea |
| Evidencia | Archivo, figura, CSV o hash del commit que respalda lo anterior |

---

## Entrada 01 — 9 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Planificación inicial, previa al repositorio |
| Objetivo | Iniciar la Fase 1 y definir una arquitectura de trabajo |
| Parámetros | Doce notas Do4–Si4; grabaciones de aproximadamente 1 s |
| Qué se probó | Revisión del alcance de la fase; necesidad de grabar en WAV y analizar el espectro mediante FFT |
| Resultado | Se propuso una estructura de carpetas y el uso de la computadora como plataforma principal de adquisición y procesamiento |
| Fallo o aprendizaje | No se había desarrollado aún la justificación técnica de componentes ni el modelo matemático que exige la rúbrica |
| Decisión siguiente | Elaborar el plan v1 y comparar formalmente las alternativas de hardware y software |
| Responsable | Ambos |
| Evidencia | Plan de acción v1, entregado el 11/09/2026 |

## Entrada 02 — 11 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Plan v1 → revisión v2 |
| Objetivo | Evaluar el plan v1 frente a la rúbrica oficial del Avance 1 |
| Parámetros revisados | fs = 44,1 kHz; N = 4096 y 8192; criterios de 5 cents y 90 % de reconocimiento |
| Qué se probó | Autoevaluación documental criterio por criterio y recálculo de la resolución frecuencial declarada |
| Resultado | Se detectó la ausencia de modelo matemático, referencias bibliográficas y responsables por integrante; incoherencia entre el software declarado (MATLAB) y el acordado (Python) |
| Fallo o aprendizaje | Con fs = 44,1 kHz, N = 4096 da Δf ≈ 10,77 Hz y N = 8192 da ≈ 5,38 Hz, no ≤ 2 Hz como afirmaba la v1. El espaciado de bins no equivale a la resolución física, limitada por la duración del registro |
| Decisión siguiente | Emitir la v2; adoptar Python como herramienta oficial; fijar fs = 48 kHz y N = 32 768; incorporar la interpolación parabólica como pieza central del diseño |
| Responsable | Ambos |
| Evidencia | Plan v1, rúbrica de evaluación y Plan de acción v2 (`informe/`) |

## Entrada 03 — (pendiente) creación del repositorio

| Campo | Contenido |
|---|---|
| Fecha | |
| Versión | hash del primer commit |
| Objetivo | Dejar el repositorio clonable y ejecutable en los equipos de ambos integrantes |
| Parámetros | Python 3.x, versiones fijadas en `requirements.txt` |
| Qué se probó | `git clone` + `pip install -r requirements.txt` + verificación de imports en ambos equipos |
| Resultado | |
| Fallo o aprendizaje | |
| Decisión siguiente | Generar tonos sintéticos de frecuencia conocida (audio/sinteticos/) |
| Responsable | |
| Evidencia | |

## Entrada 04 — 16 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/notas.py: tabla de frecuencias del temperamento igual" |
| Objetivo | Implementar la tabla de frecuencias del temperamento igual, primer eslabón del pipeline |
| Parámetros | La4 = 440 Hz, teclas 40–51 (Do4–Si4) |
| Qué se probó | Ejecución de `src/notas.py`, impresión de la tabla de las 12 notas |
| Resultado | Do4 = 261.626 Hz, La4 = 440.000 Hz — coinciden con los valores estándar de referencia |
| Fallo o aprendizaje | Ninguno; ecuación (7) validada directamente contra valores conocidos |
| Decisión siguiente | Implementar `src/preprocesamiento.py` (carga, normalización, recorte del ataque) |
| Responsable | Monica |
| Evidencia | `src/notas.py`, salida de consola de la sesión |

## Entrada 05 — 16 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/generar_sintetico.py: tonos sintéticos para validación" |
| Objetivo | Generar señales de frecuencia conocida para validar el pipeline antes de usar grabaciones reales |
| Parámetros | fs = 48 000 Hz, duración 1 s, amplitud 0.5, 12 notas Do4–Si4 (frecuencias de `notas.py`) |
| Qué se probó | Ejecución de `src/generar_sintetico.py`; lectura de `Do4.wav` para verificar fs, duración y dtype |
| Resultado | 12 archivos WAV generados en `audio/sinteticos/`; `Do4.wav` verificado: fs=48000, 48000 muestras (1 s), int16 |
| Fallo o aprendizaje | Ninguno; generación y escritura funcionaron al primer intento |
| Decisión siguiente | Implementar `src/preprocesamiento.py` y validarlo contra estos tonos sintéticos |
| Responsable | Monica |
| Evidencia | `src/generar_sintetico.py`, `audio/sinteticos/*.wav`, salida de consola |

## Entrada 06 — 16 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/preprocesamiento.py: carga, normalización y recorte del ataque" |
| Objetivo | Implementar la etapa de preprocesamiento (sec. 3.4 del plan) |
| Parámetros | ms_descarte = 75 ms (default), probado sobre `Do4.wav` (sintético, fs=48000) |
| Qué se probó | Ejecución de `src/preprocesamiento.py` sobre el tono sintético de Do4 |
| Resultado | fs=48000 Hz, 44 400 muestras tras recorte (48000 − 3600), pico normalizado = 1.000 |
| Fallo o aprendizaje | Ninguno; la aritmética del recorte y la normalización coinciden con lo esperado |
| Decisión siguiente | Implementar `src/espectro.py` (ventana de Hann + FFT) |
| Responsable | Monica |
| Evidencia | `src/preprocesamiento.py`, salida de consola |

## Entrada 07 — 16 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/espectro.py: ventana de Hann, FFT y eje de frecuencias" |
| Objetivo | Implementar la etapa de espectro (ecuaciones 11, 12, 14 del plan) |
| Parámetros | N=32768, ventana Hann, fs=48000, probado sobre `Do4.wav` preprocesado |
| Qué se probó | Ejecución de `src/espectro.py`; búsqueda del bin de mayor magnitud (sin interpolar) |
| Resultado | Δf=1.465 Hz; pico crudo en bin 179 → 262.207 Hz (real: 261.626 Hz, error ≈0.58 Hz / 3.8 cents, esperado sin interpolación) |
| Fallo o aprendizaje | `UnicodeEncodeError` al imprimir "Δ" en la consola de Windows (cp1252); se resolvió evitando caracteres no-ASCII en los `print()` |
| Decisión siguiente | Implementar `src/deteccion.py`: buscar el pico en 80–1000 Hz e interpolar parabólicamente |
| Responsable | Monica |
| Evidencia | `src/espectro.py`, salida de consola |

## Entrada 08 — 16 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/deteccion.py: pico en 80-1000 Hz e interpolación parabólica" |
| Objetivo | Implementar la estimación fina de f0 (ecuaciones 15, 16 del plan) — paso crítico para el criterio de 5 cents |
| Parámetros | Rango de búsqueda 80–1000 Hz, N=32768, probado sobre las 12 notas sintéticas Do4–Si4 |
| Qué se probó | `detectar_f0` sobre cada uno de los 12 tonos sintéticos, comparando contra `notas.py` |
| Resultado | Error máximo de 0.430 cents (Do#4), mínimo 0.049 cents (Mi4); Do4 (caso crítico) = 0.422 cents. Las 12 notas < 1 cent, muy por debajo del umbral de 5 |
| Fallo o aprendizaje | Ninguno; la interpolación parabólica redujo el error de ~3.8 cents (bin crudo, ver Entrada 07) a menos de 1 cent en todos los casos |
| Decisión siguiente | Implementar `src/evaluacion.py`: identificar la nota por proximidad de frecuencia, calcular tasa de reconocimiento y `datos/resultados.csv` |
| Responsable | Monica |
| Evidencia | `src/deteccion.py`, salida de consola (12 notas) |

## Entrada 09 — 16 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/evaluacion.py: identificación, error en cents y tasa de reconocimiento" |
| Objetivo | Cerrar el pipeline de extremo a extremo (ecuación 9) y generar `datos/resultados.csv` |
| Parámetros | Las 12 notas sintéticas Do4–Si4, tabla de `notas.py` |
| Qué se probó | `evaluar_conjunto` sobre `audio/sinteticos/`, guardado de `datos/resultados.csv` |
| Resultado | 100% de reconocimiento (12/12); error máximo 0.430 cents (Do#4), Do4 = 0.422 cents. Ambos criterios de éxito de la Fase 1 se cumplen sobre sintéticos |
| Fallo o aprendizaje | Ninguno; el pipeline completo (`notas→preprocesamiento→espectro→deteccion→evaluacion`) corre sin errores de extremo a extremo. Pendiente: validar con grabaciones reales, que introducirán ruido y armónicos que los sintéticos no tienen |
| Decisión siguiente | Coordinar con Rodrigo la grabación de las 12 notas reales en `audio/originales/` para repetir esta evaluación sobre señales reales (hito del 18 sep) |
| Responsable | Monica |
| Evidencia | `src/evaluacion.py`, `datos/resultados.csv`, salida de consola |
