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

## Entrada 10 — 16 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/prueba_armonicos.py: robustez frente a armónicos" |
| Objetivo | Verificar que `deteccion.py` encuentra la fundamental y no un armónico, antes de usar grabaciones reales |
| Parámetros | Fundamental + 4 armónicos, amplitudes [1.0, 0.6, 0.4, 0.25, 0.15], 12 notas Do4–Si4 |
| Qué se probó | Pipeline completo sobre tonos sintéticos con armónicos, guardados en `audio/sinteticos/armonicos/` |
| Resultado | Error idéntico al de las senoides puras (máximo 0.430 cents); ningún caso confundió la fundamental con un armónico, incluido Si4 (2do armónico ≈988 Hz, dentro del rango de búsqueda) |
| Fallo o aprendizaje | Ninguno; la combinación de rango 80–1000 Hz + criterio de magnitud máxima resultó robusta frente a armónicos con la relación de amplitudes probada. Queda pendiente probar con ruido de fondo |
| Decisión siguiente | Pedirle a Rodrigo 2–3 grabaciones reales para validar contra el hito del 18 sep; en paralelo, considerar prueba de robustez con ruido |
| Responsable | Monica |
| Evidencia | `src/prueba_armonicos.py`, `audio/sinteticos/armonicos/*.wav`, salida de consola |

## Entrada 11 — 18 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/graficar_espectro.py: figura del espectro con pico crudo e interpolado" |
| Objetivo | Producir el gráfico espectral que faltaba del entregable de la Sesión 2 y hacer visible el efecto de la interpolación parabólica |
| Parámetros | fs = 48 000 Hz, N = 32 768, ventana de Hann, `audio/sinteticos/armonicos/Do4.wav`, zoom de ±10 Hz |
| Qué se probó | Ejecución de `src/graficar_espectro.py`: panel A con el espectro hasta 2 kHz y el rango de búsqueda; panel B con los bins alrededor del pico, el bin crudo, el f0 interpolado y la frecuencia de tabla |
| Resultado | Bin crudo 262,207 Hz (+3,84 cents); f0 interpolado 261,689 Hz (+0,42 cents); tabla 261,626 Hz. Figura en `figuras/espectro_Do4.png` |
| Fallo o aprendizaje | En la primera versión la leyenda del panel B tapaba el flanco del pico; se subió el límite superior del eje. La figura solo dibuja lo que ya devuelven `espectro`, `buscar_pico` e `interpolar_pico` |
| Decisión siguiente | Repetir la figura con las grabaciones reales de Rodrigo y comparar contra la sintética |
| Responsable | Monica |
| Evidencia | `src/graficar_espectro.py`, `figuras/espectro_Do4.png` |


## Entrada 12 — 23 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/evaluar_reales.py y detectar_inicio: evaluación sobre samples de piano" |
| Objetivo | Evaluar el pipeline sobre audio real (los 36 samples de piano de Rodrigo: 12 notas × pp, mf, ff) y comprobar los criterios de éxito fuera de los sintéticos |
| Parámetros | Samples a 44 100 Hz, estéreo, 18–70 s de duración; N = 32 768, Hann, rango 80–1000 Hz, descarte de ataque 75 ms. Notación inglesa traducida a latina (C4 → Do4, Db4 → Do#4, ...) |
| Qué se probó | `src/evaluar_reales.py` con el pipeline sin cambios; luego diagnóstico gráfico del espectro de tres casos fallidos (Do4 pp, Re4 mf, Do#4 ff) |
| Resultado | Sin cambios al pipeline: reconocimiento pp 11/12, mf 9/12, ff 6/12; error < 5 cents en 5, 6 y 3 de 12 notas. Los criterios de la Fase 1 NO se cumplían con audio real |
| Fallo o aprendizaje | Dos causas independientes. (1) Los ff empiezan a sonar hacia ~1 s (pp a 0,1 s, mf a 0,3 s); el descarte fijo de 75 ms analizaba silencio y la FFT veía ruido de 80–150 Hz. (2) En Do4 pp y Re4 mf la 2.ª armónica es más fuerte que la fundamental (magnitudes 2026 vs 874 y 1423 vs 974), y "pico máximo en 80–1000 Hz" elegía el armónico. Los sintéticos no lo mostraban porque siempre tenían la fundamental dominante |
| Decisión siguiente | Detectar el inicio real de la nota en `preprocesamiento.py` y bajar a la fundamental en `deteccion.py` |
| Responsable | Monica |
| Evidencia | `src/evaluar_reales.py`, `datos/resultados_reales.csv`, gráfico de diagnóstico de los tres espectros, salida de consola |

## Entrada 13 — 23 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Corrige detección en audio real: inicio de nota y bajada a la fundamental" |
| Objetivo | Corregir las dos causas de fallo halladas en la Entrada 12 sin reabrir las decisiones de diseño (fs, N, Hann, rango) |
| Parámetros | `detectar_inicio`: ventanas de 10 ms, umbral = 10 % del RMS máximo, más 75 ms de ataque contados desde ese inicio. `bajar_a_fundamental`: revisa f/2, f/3 y f/4 con tolerancia ±3 % y razón mínima 0,25 de la magnitud del pico máximo |
| Qué se probó | Cada corrección por separado y las dos juntas sobre los 36 samples; regresión sobre los 12 sintéticos y la prueba de armónicos |
| Resultado | Solo con el detector de inicio: los fallos de ff bajan de 6 a 3 y todos los que quedan son de octava. Con ambas correcciones: reconocimiento 12/12 en pp, mf y ff; error < 5 cents en 10/12 (pp), 10/12 (mf) y 8/12 (ff). Sintéticos: 100 %, `resultados.csv` sin cambios; prueba de armónicos sin cambios |
| Fallo o aprendizaje | Con el detector de inicio solo, dos notas pp que acertaban (Re#4, Mi4) pasaron a fallar: antes acertaban por casualidad porque se analizaba mal el tramo. Queda un sesgo sistemático de +2 a +8 cents (media ≈ +4) en casi todas las notas y dinámicas, que no aparece en los sintéticos. Hipótesis sin comprobar: los samples están afinados cerca de 441 Hz (+3,9 cents respecto a 440). Do#4 y Sol#4 se desvían más que el resto. Con la referencia oficial La4 = 440 Hz, el criterio de < 5 cents no se cumple en ff |
| Decisión siguiente | Prueba de robustez con ruido; preguntar a Rodrigo el origen y afinación de los samples; reportar en el informe el error contra 440 Hz y, aparte, el error relativo a la afinación propia del sample |
| Responsable | Monica |
| Evidencia | `src/preprocesamiento.py` (`detectar_inicio`), `src/deteccion.py` (`bajar_a_fundamental`), `datos/resultados_reales.csv`, salida de consola |


## Entrada 14 — 23 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/prueba_ruido.py: robustez frente a ruido blanco" |
| Objetivo | Cerrar la prueba de robustez frente a ruido que las Entradas 10 y 11 dejaron pendiente y localizar el punto donde el pipeline falla |
| Parámetros | 12 tonos sintéticos con armónicos (`audio/sinteticos/armonicos/`), ruido blanco gaussiano, SNR = 40, 30, 20, 10, 5, 0, −10, −20 y −30 dB, 20 repeticiones por nota y por nivel, semilla fija 2026 |
| Qué se probó | `src/prueba_ruido.py`: suma ruido a cada señal y ejecuta el pipeline completo (normalizar, recortar ataque, Hann, FFT, pico, bajada a la fundamental, interpolación) |
| Resultado | De 40 a −10 dB: reconocimiento 100 %, error medio 0,25 a 0,28 cents, error máximo 0,43 a 0,87 cents. A −20 dB: 68,3 % y error medio 644 cents. A −30 dB: 8,3 %. El sistema se rompe entre −10 y −20 dB. Salida en `datos/resultados_ruido.csv` |
| Fallo o aprendizaje | La robustez se explica por la FFT de N = 32 768: la energía del tono se concentra en pocos bins y el ruido blanco se reparte entre 16 384. Sirve como argumento adicional para la elección de N. Límites: el ruido blanco no equivale al ruido de una habitación (más grave, dentro de la banda 80–1000 Hz) y las señales son sintéticas; no se probó ruido coloreado ni piano con ruido. El ruido tampoco explica el sesgo de ~+4 cents visto en los samples (Entrada 13) |
| Decisión siguiente | Figura del espectro con una nota real; justificación de N con Do4 (criterio 3); actualizar README e informe |
| Responsable | Monica |
| Evidencia | `src/prueba_ruido.py`, `datos/resultados_ruido.csv`, salida de consola |

## Entrada 15 — 23 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Mueve los samples de FL Studio a audio/originales/ y actualiza evaluar_reales.py" |
| Objetivo | Documentar el origen del audio y su desviación respecto al plan v2, y colocarlo en la carpeta de evidencia de adquisición |
| Parámetros | 36 WAV (12 notas × 3 dinámicas: pp suave, mf normal, ff fuerte) generados con un piano virtual en FL Studio; 44 100 Hz, estéreo, 16 bits; notación inglesa en el nombre de archivo |
| Qué se probó | `git mv` de `samples marro piano/{pp,mf,ff}` a `audio/originales/` y del léeme a `audio/originales/LEEME_notacion_y_dinamicas.txt`; se corrió `src/evaluar_reales.py` de nuevo |
| Resultado | Resultados idénticos a antes del movimiento (`datos/resultados_reales.csv` sin cambios byte a byte): reconocimiento 12/12 en las tres dinámicas; error < 5 cents en 10/12 (pp), 10/12 (mf) y 8/12 (ff) |
| Fallo o aprendizaje | El plan v2 (sec. 2.5) fija como fuente un teclado o piano físico captado con el micrófono de la laptop. Se usa en su lugar un piano virtual, opción que la Declaración de PBL permite en "Actividades sugeridas" (p. 38: "teclado virtual en PC"). Los archivos se habían subido a una carpeta aparte y no a `audio/originales/`. El conjunto de referencia para los criterios de éxito son los 12 mf; pp y ff son variantes de dinámica. La fuente virtual no incluye ruido de micrófono ni de sala, y el ruido se evaluó aparte (Entrada 14). El sesgo de ~+4 cents puede deberse a la afinación de la fuente en FL Studio; sin verificar |
| Decisión siguiente | Revisar en FL Studio la afinación del plugin de piano; reportar en el informe el error contra La4 = 440 Hz y, aparte, el relativo a la afinación propia del sample; actualizar el README |
| Responsable | Monica (Rodrigo confirma el origen de los archivos) |
| Evidencia | `audio/originales/`, `src/evaluar_reales.py`, `datos/resultados_reales.csv` |


## Entrada 16 — 23 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/graficar_comparacion.py: espectros de las 12 notas y error en cents" |
| Objetivo | Producir los espectros anotados y la comparación piano virtual vs. sintético que pide el informe (Declaración de PBL p. 38: espectros representativos anotados y notas con mayor error) |
| Parámetros | 12 notas mf de `audio/originales/mf/` (44 100 Hz) contra los 12 sintéticos con armónicos (48 000 Hz); N = 32 768, Hann, rango 80–1000 Hz; espectros normalizados al pico de la banda de búsqueda |
| Qué se probó | `src/graficar_comparacion.py`: cuadrícula 4×3 de espectros, barras de error por nota con banda de ±5 cents y zoom de ±10 Hz sobre Do4. Usa el mismo camino que `evaluacion.py` (pico, bajada a la fundamental, interpolación) |
| Resultado | Sintético: error entre −0,43 y +0,42 cents en las 12 notas. Piano virtual mf: entre +0,37 y +7,58 cents, todos positivos; 10/12 bajo 5 cents. Mayor error: Do#4 (+7,58) y Sol#4 (+6,24). Figuras: `figuras/espectros_12_notas.png`, `figuras/error_cents_12_notas.png`, `figuras/zoom_Do4_real_vs_sintetico.png` |
| Fallo o aprendizaje | En Re4, Re#4 y Mi4 del piano virtual el pico más alto de la banda es un armónico y no la fundamental, lo que muestra gráficamente por qué hace falta `bajar_a_fundamental`. Los armónicos altos del piano virtual quedan algo por encima de los sintéticos (posible inarmonicidad; sin medir). El sesgo positivo constante sigue sin explicación verificada: hipótesis, afinación de la fuente en FL Studio |
| Decisión siguiente | Justificar N con Do4 (criterio 3); revisar la afinación del plugin en FL Studio; incorporar las figuras al informe |
| Responsable | Monica |
| Evidencia | `src/graficar_comparacion.py`, las tres figuras en `figuras/`, salida de consola |

## Entrada 17 — 23 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/justificar_n.py: justificación de N con Do4" |
| Objetivo | Cumplir el criterio 3: justificar el tamaño de ventana por la resolución necesaria para distinguir semitonos adyacentes, con Do4 como caso más exigente |
| Parámetros | N = 4096, 8192, 16 384, 32 768 y 65 536; Do4 = 261,626 Hz (5 cents = 0,757 Hz; semitono = 15,56 Hz); Δf calculado con fs = 44 100 Hz; Do4 sintético (48 000 Hz) y Do4 mf del piano virtual |
| Qué se probó | `src/justificar_n.py`: espaciado de bins, ancho del lóbulo de Hann (4 bins), duración consumida y error de f0 con bin crudo y con interpolación, en las dos fuentes |
| Resultado | Con interpolación, Do4 queda bajo 5 cents con los cinco N (sintético −4,07 a −0,13; real −3,13 a +3,40). Sin interpolar, el error crudo supera 5 cents salvo con N = 65 536; con N = 32 768 el real da +5,35 cents crudo y +2,89 interpolado. Ancho de Hann: 43,1 / 21,5 / 10,8 / 5,4 / 2,7 Hz. Salida en `datos/justificacion_n.csv` y `figuras/n_vs_error_Do4.png` |
| Fallo o aprendizaje | Argumento de la elección: (1) el lóbulo de Hann debe ser menor que el semitono de 15,56 Hz, lo que exige N ≥ 16 384; (2) N = 65 536 consumiría 1,49 s, más que los ~0,9 s útiles de una toma de 1 s, y solo se alcanzaría rellenando con ceros; (3) N = 32 768 (0,743 s, Δf = 1,35 Hz) es la mayor potencia de 2 que cabe y da más margen que 16 384. Es la opción A de la Tabla 7 del plan. Límites: el archivo real dura 40 s, así que su fila de N = 65 536 usa 1,49 s de señal y no es comparable con una toma corta; la fs difiere entre fuentes (48 000 vs. 44 100 Hz); el error real no baja de forma monótona con N y no se separó afinación de la fuente, decaimiento y ruido; la lectura de que N = 4096 apenas cumple sale de un solo caso |
| Decisión siguiente | Redactar la justificación de N en el informe con estos números; repetir el análisis con más notas si hay tiempo; unificar la fs en README y plan (44 100 Hz) |
| Responsable | Monica |
| Evidencia | `src/justificar_n.py`, `datos/justificacion_n.csv`, `figuras/n_vs_error_Do4.png` |


## Entrada 18 — 23 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega src/analizar_nota.py: demo de análisis de un WAV" |
| Objetivo | Tener un comando que reciba un WAV cualquiera y devuelva nota detectada, f0 y error en cents sin saber de antemano qué nota es (criterio de cierre de la Sesión 3 del plan) y que sirva de escena central del video de demostración |
| Parámetros | Mismo pipeline de `evaluacion.py` (N = 32 768, Hann, rango 80–1000 Hz, descarte de ataque 75 ms desde el inicio real, bajada a la fundamental); argumento opcional `--esperada` para comprobar el acierto |
| Qué se probó | `python src/analizar_nota.py <wav> [--esperada Nota]` sobre Do4 mf, Re4 mf (donde el armónico supera a la fundamental), La4 sintético con nota esperada equivocada a propósito, y la invocación sin argumentos. Ejecutado también en el equipo de Monica con el `.venv` de Python 3.13 y las versiones de `requirements.txt` |
| Resultado | Do4 mf: 262,062 Hz, Do4, +2,89 cents, CORRECTO. Re4 mf: 293,728 Hz, Re4, +0,37 cents, CORRECTO. La4 sintético con esperada Sol4: detecta La4 (439,930 Hz, −0,28 cents) y marca INCORRECTO. Sin argumentos: muestra el uso. Los valores coinciden con `datos/resultados_reales.csv` y `datos/resultados.csv` |
| Fallo o aprendizaje | (1) `pip install -r requirements.txt` falló con Python 3.14 porque SciPy 1.15.3 no tiene versión precompilada para 3.14 y pip intentó compilarlo desde el código fuente (pide compilador de Fortran). Se resolvió creando el `.venv` con Python 3.13. Con esas versiones fijadas los resultados de reales y sintéticos son idénticos a los calculados con NumPy 2.4.3 / SciPy 1.17.1 (verificado). (2) Los WAV de FL Studio traen un bloque de metadatos que SciPy se salta con un aviso (`WavFileWarning`); no afecta al audio y se silencia solo en `analizar_nota.py`. No se probó el aviso de resultado no fiable (f0 a casi medio semitono de la tabla) |
| Decisión siguiente | Actualizar el README (versión de Python soportada, comandos de ejecución); decidir si se silencia el aviso también en `preprocesamiento.py`; completar `informe.tex` |
| Responsable | Monica |
| Evidencia | `src/analizar_nota.py`, salida de consola en el equipo de Monica |


## Entrada 19 — 24 de septiembre de 2026

| Campo | Contenido |
|---|---|
| Versión | Commit: "Agrega --figura a analizar_nota.py: espectro de la nota analizada" |
| Objetivo | Que la demo de `analizar_nota.py` produzca también una figura del pipeline oficial (espectro + zoom con f0 interpolado), como material visual para el video de demostración, ya que se descartó usar `afinador-local.html` (no aplica Hann, interpolación ni bajada a la fundamental; se declara "lectura visual, no el resultado oficial") |
| Parámetros | Flag `--figura`; guarda en `figuras/analisis_<nombre_wav>.png`; panel A hasta 2000 Hz con la banda 80–1000 Hz, panel B con zoom de ±10 Hz sobre la fundamental corregida (bin crudo, f0 interpolado y frecuencia de tabla) |
| Qué se probó | Regresión sin `--figura` sobre Do4 mf (idéntico a antes: +2,89 cents); con `--figura` sobre Re4 mf, caso donde el pico más alto del espectro es el 2.º armónico (~587 Hz) y no la fundamental (~294 Hz) |
| Resultado | La figura de Re4 muestra en el panel A el armónico dominante y en el zoom del panel B la fundamental correcta (293,728 Hz, +0,37 cents), confirmando visualmente que `--figura` usa la fundamental ya corregida por `bajar_a_fundamental` y no el pico máximo bruto |
| Fallo o aprendizaje | Ninguno; se reutilizó el mismo criterio de `graficar_espectro.py` pero generalizado a un WAV y una nota detectada cualesquiera, sin recalcular el pico dos veces (analizar_nota ahora expone frecuencias, magnitud y k en su resultado) |
| Decisión siguiente | Guion del video con `analizar_nota.py --figura`; retomar la revisión del informe cuando el equipo la traiga con cambios |
| Responsable | Monica |
| Evidencia | `src/analizar_nota.py`, `figuras/analisis_Piano.mf.D4.png`, salida de consola |
