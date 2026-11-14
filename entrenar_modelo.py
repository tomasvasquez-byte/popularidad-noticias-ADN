"""Regenera models/modelo_popularidad.pkl con las versiones instaladas en SU entorno.

Reproduce los pasos del notebook (secciones 3, 4, 5 y 8) para el modelo final:
  - elimina la fila con error de registro,
  - excluye url, timedelta, kw_*, self_reference_* y las columnas redundantes,
  - separa train/test 80/20 con random_state=42,
  - entrena Random Forest sobre log1p(shares) con los hiperparámetros elegidos.

Uso (con el entorno virtual activado):
    pip install -r requirements-entrenamiento.txt
    python entrenar_modelo.py                      # busca el .xlsx en esta carpeta
    python entrenar_modelo.py ruta/al/dataset.xlsx

Si en el notebook cambia el modelo final o sus hiperparámetros, hay que cambiarlos aquí también.
"""
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# --- Configuración del modelo final (sección 5.5 y 6.1 del notebook) ---
NOMBRE = "Random Forest"
HIPERPARAMETROS = dict(n_estimators=200, max_depth=10, min_samples_leaf=10,
                       random_state=42, n_jobs=-1)

DESTINO = Path(__file__).resolve().parent / "models" / "modelo_popularidad.pkl"


def buscar_dataset():
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    for ruta in [Path("Dataset_OnlineNewsPopularity.xlsx"), Path("data/Dataset_OnlineNewsPopularity.xlsx")]:
        if ruta.exists():
            return ruta
    sys.exit("No se encontró Dataset_OnlineNewsPopularity.xlsx. Indique la ruta como argumento.")


def main():
    df = pd.read_excel(buscar_dataset(), sheet_name="Dataset_OnlineNews")

    # Fila con proporciones > 1 (error de registro)
    tasas = ["n_unique_tokens", "n_non_stop_words", "n_non_stop_unique_tokens"]
    df = df.drop(index=df[(df[tasas] > 1).any(axis=1)].index)

    columnas_excluir = (["url", "timedelta", "shares"]
                        + [c for c in df.columns if c.startswith("kw_")]
                        + [c for c in df.columns if c.startswith("self_reference_")]
                        + ["weekday_is_sunday", "is_weekend", "LDA_04", "n_non_stop_words"])
    X, y = df.drop(columns=columnas_excluir), df["shares"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    modelo = RandomForestRegressor(**HIPERPARAMETROS)
    modelo.fit(X_train, np.log1p(y_train))

    mae_log = mean_absolute_error(np.log1p(y_test), modelo.predict(X_test))
    print(f"Filas: {len(df)} | Train: {len(X_train)} | Test: {len(X_test)} | Predictores: {X.shape[1]}")
    print(f"MAE log en test: {mae_log:.3f}  (debe coincidir con MAE_LOG_TEST en utils/config.py)")

    paquete = {
        "nombre": NOMBRE,
        "modelo": modelo,
        "columnas": list(X_train.columns),
        "medianas": X_train.median().to_dict(),
        "version_sklearn": sklearn.__version__,
    }
    DESTINO.parent.mkdir(exist_ok=True)
    joblib.dump(paquete, DESTINO)
    print("Modelo guardado en:", DESTINO, "| scikit-learn", sklearn.__version__)


if __name__ == "__main__":
    main()
