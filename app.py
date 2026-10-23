from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import SECRET_KEY
from models.psicologa import Psicologa
from models.tutor import Tutor
from functools import wraps
from models.cita import Cita

app = Flask(__name__)
app.secret_key = SECRET_KEY

def login_requerido(rol):
    """Solo deja pasar si la sesión tiene el rol indicado ('psicologa' o 'tutor')."""
    def decorador(funcion):
        @wraps(funcion)
        def envoltura(*args, **kwargs):
            if session.get("rol") != rol:
                flash("Inicia sesión para continuar")
                return redirect(url_for("inicio"))
            return funcion(*args, **kwargs)
        return envoltura
    return decorador


@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/panel-psicologa")
@login_requerido("psicologa")
def panel_psicologa():
    return render_template("panel_psicologa.html", pagina="inicio")

@app.route("/panel-psicologa/solicitudes")
@login_requerido("psicologa")
def solicitudes():
    citas = Cita.obtener_solicitudes()
    return render_template("solicitudes.html", pagina="solicitudes", citas=citas)

@app.route("/panel-psicologa/agenda")
@login_requerido("psicologa")
def agenda():
    citas = Cita.obtener_agenda()
    return render_template("agenda.html", pagina="agenda", citas=citas)

@app.route("/panel-psicologa/seguimiento")
@login_requerido("psicologa")
def seguimiento():
    return render_template("seguimiento.html", pagina="seguimiento")

@app.route("/panel-psicologa/historial")
@login_requerido("psicologa")
def historial():
    citas = Cita.obtener_historial()
    return render_template("historial.html", pagina="historial", citas=citas)


@app.route("/panel-psicologa/alumnos")
@login_requerido("psicologa")
def lista_alumnos():
    return render_template("lista_alumnos.html", pagina="alumnos")


@app.route("/panel-psicologa/profesores")
@login_requerido("psicologa")
def profesores():
    tutores = Tutor.obtener_resumen()
    return render_template("lista_profesores.html", pagina="profesores", tutores=tutores)


@app.route("/panel-profesor")
@login_requerido("tutor")
def panel_profesor():
    return render_template("inicio_profesor.html", pagina="inicio")


@app.route("/panel-profesor/solicitar-cita")
@login_requerido("tutor")
def solicitar_cita():
    return render_template("solicitar_cita.html", pagina="solicitar")


@app.route("/panel-profesor/mis-alumnos")
@login_requerido("tutor")
def mis_alumnos():
    return render_template("mis_alumnos.html", pagina="alumnos")


@app.route("/panel-profesor/seguimiento")
@login_requerido("tutor")
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

@app.route("/login", methods=["POST"])
def login():
    rol = request.form.get("rol", "tutor")
    usuario = request.form.get("usuario", "").strip()
    contrasena = request.form.get("password", "")

    # Según el selector, buscamos en una tabla u otra
    if rol == "psicologa":
        persona = Psicologa.buscar_por_usuario(usuario)
    else:
        persona = Tutor.buscar_por_correo(usuario)

    # Mismo mensaje si falla el usuario o la contraseña (no damos pistas)
    if persona is None or not persona.verificar_contrasena(contrasena):
        flash("Usuario o contraseña incorrectos")
        return redirect(url_for("inicio"))

    # Login correcto: limpiamos cualquier sesión vieja y guardamos los datos
    session.clear()
    session["rol"] = rol
    session["nombre"] = persona.nombre

    if rol == "psicologa":
        session["id"] = persona.id_psicologa
        return redirect(url_for("panel_psicologa"))

    session["id"] = persona.id_tutor
    return redirect(url_for("panel_profesor"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)