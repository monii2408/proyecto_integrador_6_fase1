# CLAUDE.md — Contexto para Claude Code

Este repositorio es el **Proyecto Integrador 6, Fase 1** del curso Señales y Sistemas (EE2004).
Es un proyecto **académico, en pareja, con enfoque de aprendizaje (PBL)**. Lee este archivo
completo antes de tocar cualquier cosa.

## Quién trabaja aquí

- **Monica** (Integrante 2): procesamiento y análisis — es quien escribe el código del pipeline.
  Está aprendiendo el tema; el objetivo es que **ella entienda cada línea**, no que el código aparezca solo.
- **Rodrigo** (Integrante 1): adquisición y documentación — grabaciones, bitácora, informe.

## Cómo debes comportarte en este repo

1. **Explica antes de escribir.** Antes de crear o modificar un módulo, describe en 3–6 líneas
   qué hace, qué ecuación del plan implementa y por qué. Espera confirmación.
2. **Una tarea a la vez.** No adelantes módulos que no se pidieron. El cronograma tiene un orden
   de dependencias (ver abajo) y el equipo quiere ir con calma.
3. **Código pequeño y legible.** Funciones cortas con docstring en español que diga qué entra,
   qué sale y qué ecuación implementa. Sin frameworks, sin clases innecesarias.
4. **Comenta la intuición, no lo obvio.** Ej.: por qué se descarta el ataque, por qué Hann,
   por qué la interpolación no es opcional.
5. **Nunca modifiques `audio/originales/`.** Es evidencia de adquisición. Se trabaja sobre copias en `audio/procesados/`.
6. **Recuerda la bitácora.** Al terminar un cambio relevante, propón el texto de la entrada para
   `bitacora/bitacora.md` (formato definido allí) y pregunta si se agrega.
7. **Propón el mensaje de commit** al cerrar cada tarea. Mínimo un commit por sesión.
8. **No inventes resultados.** Si un valor numérico no viene de ejecutar código, dilo.

## Decisiones técnicas ya tomadas (no reabrir sin consultar)

| Parámetro | Valor |
|---|---|
| Lenguaje | Python 3 · NumPy · SciPy · Matplotlib · sounddevice |
| fs | 48 000 Hz (nativa del codec de la laptop) |
| N (FFT) | 32 768 → Δf ≈ 1,465 Hz |
| Ventana | Hann (`scipy.signal.windows.hann`) |
| Rango de búsqueda de f0 | 80 – 1000 Hz |
| Estimación fina | Interpolación parabólica: δ = ½ (α − γ)/(α − 2β + γ), f0 = (k + δ)·fs/N |
| Referencia | La4 = 440 Hz; f_n = 440 · 2^((n−49)/12) |
| Error | cents = 1200 · log2(f_medida / f_tabla) |
| Notas | Do4 – Si4 (teclas 40–51), grabaciones de ~1 s, se descartan los primeros 50–100 ms |
| MATLAB | Solo verificación cruzada, no es la herramienta oficial |

## Orden de dependencias (respetarlo)

```
notas.py  →  preprocesamiento.py  →  espectro.py  →  deteccion.py  →  evaluacion.py
                    ↑
      tonos sintéticos (validar aquí ANTES de usar grabaciones reales)
```

Si algo falla con un tono sintético de frecuencia conocida, el error está en el código.
Si el sintético pasa y la grabación real falla, el problema es de captura o de la señal física.

## Estructura

```
audio/{originales,sinteticos,procesados}/   src/   datos/   figuras/   informe/   bitacora/
```

Un módulo por etapa en `src/`. Los nombres están fijados en el README; no los cambies.

## Criterios de éxito que guían cada decisión

- ≥ 90 % de reconocimiento sobre 12 notas.
- Error < 5 cents en ≥ 10 de 12 notas. **Caso crítico: Do4** (5 cents ≈ 0,76 Hz).
- Reproducible desde cero por un tercero.

## Lo que NO forma parte de la Fase 1

- FFT en el microcontrolador (eso es Fase 2).
- KY-038 / MAX4466 como adquisición principal (solo exploración opcional al final).
- Inversión temporal x[−n] (se menciona en el informe para distinguirla, no se aplica).
