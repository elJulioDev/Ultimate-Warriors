def nivel_carga(carga):
    if carga < 93:
        return 0
    elif carga < 180:
        return 1
    elif carga <= 252:
        return 2
    else:
        return 3


def calcular_stats(nivel_transformacion):
    return {
        "daño": 8 + 2 * nivel_transformacion,
        "defensa": 3 + 2 * nivel_transformacion,
        "velocidad": 25 * nivel_transformacion
    }