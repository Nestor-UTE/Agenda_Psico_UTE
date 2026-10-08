from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/panel-psicologa")
def panel_psicologa():
    return render_template("panel_psicologa.html", pagina="inicio")

@app.route("/panel-psicologa/solicitudes")
def solicitudes():
    return render_template("solicitudes.html", pagina="solicitudes")

@app.route("/panel-psicologa/agenda")
def agenda():
    return render_template("agenda.html", pagina="agenda")

@app.route("/panel-psicologa/seguimiento")
def seguimiento():
    return render_template("seguimiento.html", pagina="seguimiento")

@app.route("/panel-psicologa/historial")
def historial():
    return render_template("historial.html", pagina="historial")


@app.route("/panel-psicologa/alumnos")
def lista_alumnos():
    return render_template("lista_alumnos.html", pagina="alumnos")


@app.route("/panel-psicologa/profesores")
def profesores():
    return render_template("lista_profesores.html", pagina="profesores")


@app.route("/panel-profesor")
def panel_profesor():
    return render_template("inicio_profesor.html", pagina="inicio")


@app.route("/panel-profesor/solicitar-cita")
def solicitar_cita():
    return render_template("solicitar_cita.html", pagina="solicitar")


@app.route("/panel-profesor/mis-alumnos")
def mis_alumnos():
    return render_template("mis_alumnos.html", pagina="alumnos")


@app.route("/panel-profesor/seguimiento")
def seguimiento_profesor():
    return render_template("seguimiento_profesor.html", pagina="seguimiento")


if __name__ == "__main__":
    app.run(debug=True)