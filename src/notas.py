"""Tabla de frecuencias del temperamento igual para las notas Do4 a Si4."""

NOTAS = ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]

LA4_HZ = 440.0
TECLA_LA4 = 49  # numeración de tecla de piano estándar (La0 = tecla 1)


def frecuencia_tecla(n):
    """
    Frecuencia de la tecla de piano n según el temperamento igual.
    Entra: n (int), número de tecla (La4 = 49).
    Sale: frecuencia en Hz (float).
    Ecuación (7): f_n = 440 * 2**((n - 49) / 12)
    """
    return LA4_HZ * 2 ** ((n - TECLA_LA4) / 12)


def tabla_notas(tecla_inicio=40, tecla_fin=51):
    """
    Tabla nota -> frecuencia para el rango de teclas dado (por defecto Do4 a Si4).
    Entra: tecla_inicio, tecla_fin (int).
    Sale: dict {nombre_nota: frecuencia_hz}.
    Ecuación (8): recorre las teclas del rango y aplica frecuencia_tecla a cada una.
    """
    tabla = {}
    for n in range(tecla_inicio, tecla_fin + 1):
        nombre = NOTAS[(n - 40) % 12] + "4"
        tabla[nombre] = frecuencia_tecla(n)
    return tabla


if __name__ == "__main__":
    for nombre, hz in tabla_notas().items():
        print(f"{nombre}: {hz:.3f} Hz")
