"""Definición de los campos del formulario.

Solo se piden variables que el equipo editorial conoce al publicar. Las demás
columnas del modelo (LDA_*, tasas de palabras positivas/negativas, polaridades
de palabras, etc.) se completan con la mediana de train (ver utils/modelo.py).
"""

GRUPOS = [
    {
        "titulo": "Texto",
        "campos": [
            {"nombre": "n_tokens_title", "etiqueta": "Palabras en el título", "tipo": "int",
             "min": 1, "max": 30, "defecto": 10, "ayuda": "Entre 1 y 30."},
            {"nombre": "n_tokens_content", "etiqueta": "Palabras en el cuerpo", "tipo": "int",
             "min": 0, "max": 8000, "defecto": 411, "ayuda": "Entre 0 y 8.000."},
            {"nombre": "average_token_length", "etiqueta": "Largo promedio de palabra", "tipo": "float",
             "min": 0, "max": 10, "defecto": 4.66, "step": "0.01", "ayuda": "En letras, entre 0 y 10."},
            {"nombre": "num_keywords", "etiqueta": "Palabras clave", "tipo": "int",
             "min": 1, "max": 10, "defecto": 7, "ayuda": "Entre 1 y 10."},
        ],
    },
    {
        "titulo": "Enlaces y multimedia",
        "campos": [
            {"nombre": "num_hrefs", "etiqueta": "Enlaces totales", "tipo": "int",
             "min": 0, "max": 150, "defecto": 8, "ayuda": "Incluye los enlaces a Mashable."},
            {"nombre": "num_self_hrefs", "etiqueta": "Enlaces a otras noticias de Mashable", "tipo": "int",
             "min": 0, "max": 150, "defecto": 3, "ayuda": "No puede superar a los enlaces totales."},
            {"nombre": "num_imgs", "etiqueta": "Imágenes", "tipo": "int",
             "min": 0, "max": 100, "defecto": 1, "ayuda": "Entre 0 y 100."},
            {"nombre": "num_videos", "etiqueta": "Videos", "tipo": "int",
             "min": 0, "max": 100, "defecto": 0, "ayuda": "Entre 0 y 100."},
        ],
    },
    {
        "titulo": "Tono del contenido",
        "campos": [
            {"nombre": "global_subjectivity", "etiqueta": "Subjetividad del texto", "tipo": "float",
             "min": 0, "max": 1, "defecto": 0.46, "step": "0.01", "ayuda": "0 es objetivo, 1 es muy subjetivo."},
            {"nombre": "global_sentiment_polarity", "etiqueta": "Polaridad del texto", "tipo": "float",
             "min": -1, "max": 1, "defecto": 0.12, "step": "0.01", "ayuda": "-1 negativo, 1 positivo."},
            {"nombre": "title_subjectivity", "etiqueta": "Subjetividad del título", "tipo": "float",
             "min": 0, "max": 1, "defecto": 0.14, "step": "0.01", "ayuda": "Entre 0 y 1."},
            {"nombre": "title_sentiment_polarity", "etiqueta": "Polaridad del título", "tipo": "float",
             "min": -1, "max": 1, "defecto": 0.0, "step": "0.01", "ayuda": "Entre -1 y 1."},
        ],
    },
]

# Selectores: cada opción activa una columna binaria del modelo.
# `None` significa "ninguna": todas las columnas del grupo quedan en 0.
CANALES = [
    ("none", "Otro canal", None),
    ("lifestyle", "Estilo de vida", "data_channel_is_lifestyle"),
    ("entertainment", "Entretenimiento", "data_channel_is_entertainment"),
    ("bus", "Negocios", "data_channel_is_bus"),
    ("socmed", "Redes sociales", "data_channel_is_socmed"),
    ("tech", "Tecnología", "data_channel_is_tech"),
    ("world", "Mundo", "data_channel_is_world"),
]

# Domingo es la categoría de referencia (en el notebook se eliminó `weekday_is_sunday`).
DIAS = [
    ("monday", "Lunes", "weekday_is_monday"),
    ("tuesday", "Martes", "weekday_is_tuesday"),
    ("wednesday", "Miércoles", "weekday_is_wednesday"),
    ("thursday", "Jueves", "weekday_is_thursday"),
    ("friday", "Viernes", "weekday_is_friday"),
    ("saturday", "Sábado", "weekday_is_saturday"),
    ("sunday", "Domingo", None),
]

CANAL_DEFECTO = "none"
DIA_DEFECTO = "tuesday"

TODOS_LOS_CAMPOS = [c for g in GRUPOS for c in g["campos"]]
