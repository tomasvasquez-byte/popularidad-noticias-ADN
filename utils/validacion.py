"""Validación de las entradas del formulario."""
from .campos import CANALES, DIAS, TODOS_LOS_CAMPOS


def _a_numero(texto, tipo):
    texto = (texto or "").strip().replace(",", ".")
    if texto == "":
        raise ValueError("Este campo es obligatorio.")
    try:
        valor = float(texto)
    except ValueError:
        raise ValueError("Debe ser un número.")
    if valor != valor or valor in (float("inf"), float("-inf")):
        raise ValueError("Debe ser un número finito.")
    if tipo == "int":
        if valor != int(valor):
            raise ValueError("Debe ser un número entero.")
        return int(valor)
    return valor


def validar(formulario):
    """Devuelve (valores, errores).

    `valores` tiene los números ya convertidos más las claves `canal` y `dia`.
    `errores` es un dict {campo: mensaje}; si está vacío, la entrada es válida.
    """
    valores, errores = {}, {}

    for campo in TODOS_LOS_CAMPOS:
        nombre = campo["nombre"]
        try:
            valor = _a_numero(formulario.get(nombre), campo["tipo"])
            if not campo["min"] <= valor <= campo["max"]:
                raise ValueError(f"Debe estar entre {campo['min']} y {campo['max']}.")
            valores[nombre] = valor
        except ValueError as e:
            errores[nombre] = str(e)

    canal = formulario.get("canal", "")
    if canal not in {c[0] for c in CANALES}:
        errores["canal"] = "Elija una opción de la lista."
    valores["canal"] = canal

    dia = formulario.get("dia", "")
    if dia not in {d[0] for d in DIAS}:
        errores["dia"] = "Elija una opción de la lista."
    valores["dia"] = dia

    # Regla de coherencia entre campos
    if ("num_hrefs" in valores and "num_self_hrefs" in valores
            and valores["num_self_hrefs"] > valores["num_hrefs"]):
        errores["num_self_hrefs"] = "No puede superar a los enlaces totales."

    return valores, errores
