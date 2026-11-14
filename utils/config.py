"""Constantes de la aplicación. Los valores de referencia salen del notebook."""

# Percentiles 0, 5, 10, ..., 100 de `shares` en el dataset (sin la fila con error).
PERCENTILES_SHARES = [4, 589, 716, 811, 888, 962, 1000, 1100, 1200, 1400, 1500,
                      1600, 1800, 2100, 2400, 2900, 3500, 4700, 6400, 11700, 843300]

MEDIANA_SHARES = 1500

# MAE en escala log1p(shares) sobre el conjunto de prueba (sección 6 del notebook).
# Se usa para dar un rango orientativo alrededor de la predicción.
MAE_LOG_TEST = 0.733
