"""Carga del modelo y generación de predicciones."""
import os

import joblib
import numpy as np
import pandas as pd

from .campos import CANALES, DIAS
from .config import MAE_LOG_TEST, MEDIANA_SHARES, PERCENTILES_SHARES

RUTA_MODELO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "models", "modelo_popularidad.pkl")

# Se carga una sola vez, al iniciar la aplicación.
PAQUETE = joblib.load(RUTA_MODELO)


def construir_fila(valores):
    """Arma la fila de entrada con el mismo orden de columnas del entrenamiento.

    Lo que el formulario no pide se completa con la mediana de train, igual que
    en `predecir_shares` del notebook (sección 8).
    """
    fila = dict(PAQUETE["medianas"])

    for columna in PAQUETE["columnas"]:
        if columna in valores:
            fila[columna] = valores[columna]

    # Selectores -> columnas binarias (el grupo completo se reinicia primero)
    for _, _, columna in CANALES + DIAS:
        if columna:
            fila[columna] = 0
    for clave, _, columna in CANALES:
        if clave == valores["canal"] and columna:
            fila[columna] = 1
    for clave, _, columna in DIAS:
        if clave == valores["dia"] and columna:
            fila[columna] = 1

    return pd.DataFrame([fila], columns=PAQUETE["columnas"])


def percentil_de(shares):
    """Posición aproximada (0-100) de un valor dentro de la distribución real."""
    return float(np.interp(shares, PERCENTILES_SHARES, np.arange(0, 101, 5)))


def predecir(valores):
    entrada = construir_fila(valores)
    pred_log = float(PAQUETE["modelo"].predict(entrada)[0])
    shares = float(np.expm1(pred_log))
    return {
        "shares": shares,
        "minimo": float(np.expm1(max(pred_log - MAE_LOG_TEST, 0))),
        "maximo": float(np.expm1(pred_log + MAE_LOG_TEST)),
        "percentil": percentil_de(shares),
        "contra_mediana": shares / MEDIANA_SHARES,
        "modelo": PAQUETE["nombre"],
    }
