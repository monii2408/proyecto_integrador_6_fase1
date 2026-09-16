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
