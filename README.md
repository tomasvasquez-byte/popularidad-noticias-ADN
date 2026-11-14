# Compartidos esperados: predicción de popularidad de noticias

Proyecto semestral de Análisis de Negocios (UTFSM, 2026-02). Aplicación web en Flask que estima
cuántas veces será compartida una noticia de Mashable a partir de lo que se conoce al publicarla.

## Integrantes
Grupo N.º **[COMPLETAR]**

| Nombre completo | Rol principal |
|---|---|
| [COMPLETAR] | [COMPLETAR] |
| [COMPLETAR] | [COMPLETAR] |
| [COMPLETAR] | [COMPLETAR] |
| [COMPLETAR] | [COMPLETAR] |

## Problema, dataset y modelo
- **Problema:** regresión. Variable objetivo `shares` (veces que se compartió la noticia).
- **Dataset:** `Dataset_OnlineNewsPopularity.xlsx`, 3.500 noticias de Mashable (2013 y 2014). Se elimina una fila con error de registro y quedan 3.499.
- **Momento de predicción:** al publicar. Por eso se excluyen `url`, `timedelta`, `kw_*` y `self_reference_*` (notebook, secciones 2.5 y 3).
- **Modelo seleccionado:** Random Forest Regressor, entrenado sobre `log1p(shares)` (la app aplica `np.expm1` para devolver compartidos).
- **Hiperparámetros del modelo final:** `n_estimators=200`, `max_depth=10`, `min_samples_leaf=10`, `random_state=42`.
- **Partición:** 80 % train (2.799) y 20 % test (700), `random_state=42`.
- **Desempeño en test:** MAE log 0,733 y R² log 0,074 (K-Fold K=5 sobre train: MAE log 0,680 ± 0,030).

## Estructura del proyecto
```
app.py                          Aplicación Flask (rutas)
entrenar_modelo.py              Regenera models/modelo_popularidad.pkl con las versiones del entorno
requirements.txt                Dependencias de la app (incluye gunicorn para Render)
requirements-entrenamiento.txt  Dependencias extra para entrenar (openpyxl)
.python-version                 Versión de Python que usa Render
models/                         modelo_popularidad.pkl (modelo + columnas + medianas)
utils/                          campos.py, validacion.py, modelo.py, config.py
templates/                      base.html, index.html, resultado.html
static/                         css/estilo.css, js/app.js
```

## Ejecución local
```bash
python -m venv venv
# Windows (PowerShell):  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass ; .\venv\Scripts\Activate.ps1
# Mac/Linux:             source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Abrir http://127.0.0.1:5000

### Si el modelo no carga (versiones de scikit-learn)
El `.pkl` solo se carga con la versión de scikit-learn con que se guardó. Para regenerarlo con las versiones de su entorno:
```bash
pip install -r requirements-entrenamiento.txt
python entrenar_modelo.py ruta/a/Dataset_OnlineNewsPopularity.xlsx
```
Luego fije en `requirements.txt` las versiones instaladas (`pip freeze`).

## Modalidad de ejecución seleccionada
**[COMPLETAR: borre la opción que no use]**

**Opción A, ejecución local.** La aplicación se ejecuta desde el computador de un integrante con los pasos de arriba.

**Opción B, despliegue en la nube (GitHub + Render).**
- Repositorio: **[COMPLETAR: https://github.com/USUARIO/REPOSITORIO]**
- URL pública: **[COMPLETAR: https://NOMBRE.onrender.com]**
- Render: Web Service, rama `main`, Build Command `pip install -r requirements.txt`, Start Command `gunicorn app:app`.
- Nota: en el plan gratuito el servicio se duerme tras 15 minutos sin uso y la primera visita puede tardar cerca de un minuto.
