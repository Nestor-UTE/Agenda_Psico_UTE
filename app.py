from flask import Flask, render_template, request, redirect, url_for
#from flask import Flask, render_template

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


@app.route("/folio", methods=["POST"])
def consultar_folio():
    folio = request.form.get("folio", "").strip()

    # Si el folio llega vacío, regresamos al login
    if not folio:
        return redirect(url_for("inicio"))

    # Datos de ejemplo (después se reemplazan por la consulta a MariaDB)
    cita = {
        "alumno": "Alumno de ejemplo",
        "estado": "Esperando fecha",
        "fecha": "15/10/2026",
        "hora": "10:00",
        "edificio": "D5",
        "nombre_edificio": "POR CONFIRMAR",
        "salon": "00000",
        "referencia": "A un lado derecho de las escaleras",
        "tutor": "Tutor de ejemplo",
        "telefono_tutor": "81 0000 0000",
    }

    return render_template("alumno.html", folio=folio, cita=cita)

if __name__ == "__main__":
    app.run(debug=True)