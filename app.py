import math

from flask import Flask, render_template, request

from utils.campos import CANAL_DEFECTO, CANALES, DIA_DEFECTO, DIAS, GRUPOS
from utils.config import MAE_LOG_TEST, MEDIANA_SHARES
from utils.modelo import predecir
from utils.validacion import validar

app = Flask(__name__)

# La regla visual va de 500 a 20.000 compartidos, en escala logarítmica
REGLA_MIN, REGLA_MAX = 500, 20000


def formato_miles(numero):
    """12345.6 -> '12.346' (separador de miles chileno)."""
    return f"{round(numero):,}".replace(",", ".")


def posicion_en_regla(valor):
    """Convierte un valor a un porcentaje (0-100) dentro de la regla logarítmica."""
    lo, hi = math.log10(REGLA_MIN), math.log10(REGLA_MAX)
    valor = min(max(valor, REGLA_MIN), REGLA_MAX)
    return (math.log10(valor) - lo) / (hi - lo) * 100


def formato_decimal(valor):
    """4.66 -> '4,66'; los enteros se muestran sin decimales."""
    if isinstance(valor, float):
        return f"{valor:g}".replace(".", ",")
    return str(valor)


app.jinja_env.filters["miles"] = formato_miles
app.jinja_env.filters["dec"] = formato_decimal
app.jinja_env.filters["regla"] = posicion_en_regla


def contexto_formulario(datos, errores):
    return dict(grupos=GRUPOS, canales=CANALES, dias=DIAS, datos=datos, errores=errores)


def datos_iniciales():
    datos = {c["nombre"]: c["defecto"] for g in GRUPOS for c in g["campos"]}
    datos["canal"], datos["dia"] = CANAL_DEFECTO, DIA_DEFECTO
    return datos


@app.route("/")
def index():
    return render_template("index.html", **contexto_formulario(datos_iniciales(), {}))


@app.route("/predecir", methods=["POST"])
def predecir_noticia():
    valores, errores = validar(request.form)
    if errores:
        # Se vuelve al formulario con lo escrito y los mensajes de error
        return render_template("index.html", **contexto_formulario(request.form, errores)), 400

    resultado = predecir(valores)
    return render_template("resultado.html", r=resultado, valores=valores,
                           mediana=MEDIANA_SHARES, mae=MAE_LOG_TEST,
                           grupos=GRUPOS, canales=CANALES, dias=DIAS)


@app.errorhandler(404)
def no_encontrado(_):
    return render_template("index.html", **contexto_formulario(datos_iniciales(), {})), 404


if __name__ == "__main__":
    app.run(debug=True)
