"""
Constantes y funciones de cálculo estático
"""

def nivel_carga(carga):
    """Retorna el nivel de carga (0-3) basado en la cantidad numérica"""
    if carga < 93:
        return 0
    elif carga < 180:
        return 1
    elif carga <= 252:
        return 2
    elif carga >= 280:
        return 3
    return 0

def calcular_stats(nivel_transformacion):
    """Calcula stats según el nivel de transformación (lógica original)"""
    return {
        "daño": 8 + 2 * nivel_transformacion,
        "defensa": 3 + 2 * nivel_transformacion,
        "velocidad": 25 * nivel_transformacion
    }
