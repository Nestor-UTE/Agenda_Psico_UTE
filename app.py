from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import SECRET_KEY
from models.psicologa import Psicologa
from models.tutor import Tutor
from functools import wraps
from models.cita import Cita
from datetime import datetime

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

def validar_solicitud(form):
    """Revisa los datos del formulario de solicitar cita.
    Regresa (alumno, motivo, error). Si hay error, los dos primeros son None."""
    matricula = form.get("matricula", "").strip()
    nombre = form.get("nombre", "").strip()
    a_paterno = form.get("a_paterno", "").strip()
    a_materno = form.get("a_materno", "").strip()
    grupo = form.get("grupo", "").strip().upper()
    carrera = form.get("carrera", "").strip()
    motivo = form.get("motivo", "").strip()

    if not (matricula.isascii() and matricula.isdigit() and 6 <= len(matricula) <= 9):
        return None, None, "La matrícula debe tener entre 6 y 9 números"
    if not nombre or len(nombre) > 45:
        return None, None, "El nombre es obligatorio (máximo 45 caracteres)"
    if not a_paterno or len(a_paterno) > 45:
        return None, None, "El apellido paterno es obligatorio (máximo 45 caracteres)"
    if len(a_materno) > 45:
        return None, None, "El apellido materno es muy largo (máximo 45 caracteres)"
    try:
        grado = int(form.get("grado", ""))
    except ValueError:
        return None, None, "El grado debe ser un número"
    if not 1 <= grado <= 11:
        return None, None, "El grado debe estar entre 1 y 11"
    if not (grupo.isalpha() and len(grupo) <= 2):
        return None, None, "El grupo debe ser una o dos letras, por ejemplo A"
    if not carrera or len(carrera) > 45:
        return None, None, "La carrera es obligatoria (máximo 45 caracteres)"
    if not motivo or len(motivo) > 255:
        return None, None, "El motivo es obligatorio (máximo 255 caracteres)"

    alumno = {
        "matricula": int(matricula), "nombre": nombre, "a_paterno": a_paterno,
        "a_materno": a_materno, "grado": grado, "grupo": grupo, "carrera": carrera,
    }
    return alumno, motivo, None


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
    
@app.route("/panel-psicologa/solicitudes/agendar", methods=["POST"])
@login_requerido("psicologa")
def agendar_cita():
    fecha = request.form.get("fecha", "")
    hora = request.form.get("hora", "")

    # Validamos que lleguen datos correctos (el formulario del navegador se puede saltar)
    try:
        id_cita = int(request.form.get("id_cita", ""))
        fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    except ValueError:
        flash("La cita, la fecha o la hora no son válidas", "error")
        return redirect(url_for("solicitudes"))

    if fecha_hora < datetime.now():
        flash("No se puede agendar una cita en una fecha pasada", "error")
        return redirect(url_for("solicitudes"))

    if Cita.agendar(id_cita, fecha_hora):
        flash("Cita agendada correctamente", "ok")
    else:
        flash("No se pudo agendar: la cita ya no estaba pendiente", "error")
    return redirect(url_for("solicitudes"))

@app.route("/panel-psicologa/solicitudes/rechazar", methods=["POST"])
@login_requerido("psicologa")
def rechazar_cita():
    try:
        id_cita = int(request.form.get("id_cita", ""))
    except ValueError:
        flash("La cita no es válida", "error")
        return redirect(url_for("solicitudes"))

    if Cita.rechazar(id_cita):
        flash("Solicitud rechazada", "ok")
    else:
        flash("No se pudo rechazar: la solicitud ya no estaba pendiente", "error")
    return redirect(url_for("solicitudes"))

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


@app.route("/panel-profesor/solicitar-cita", methods=["GET", "POST"])
@login_requerido("tutor")
def solicitar_cita():
    if request.method == "GET":
        return render_template("solicitar_cita.html", pagina="solicitar", datos={})

    alumno, motivo, error = validar_solicitud(request.form)
    if error is None:
        folio, error = Cita.solicitar(session["id"], motivo, alumno)

    if error:
        # Se vuelve a mostrar el formulario con lo que escribió, para que no lo capture de nuevo
        flash(error, "error")
        return render_template("solicitar_cita.html", pagina="solicitar", datos=request.form)

    flash(f"Solicitud enviada. Folio de la cita: {folio}", "ok")
    return redirect(url_for("solicitar_cita"))


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
    folio = request.form.get("folio", "").strip().lower()
    if not folio or len(folio) > 45:
        return redirect(url_for("inicio"))

    cita = Cita.obtener_por_folio(folio)
    if cita is None:
        flash("Folio no encontrado")
        return redirect(url_for("inicio"))

    # Preparamos lo que ve el alumno
    estatus = cita["estatus"]
    cita["estado"] = "Esperando fecha" if estatus == "Solicitada" else estatus

    fecha = cita["fecha"]
    if estatus in ("Solicitada", "Rechazada") or fecha is None:
        cita["fecha"] = None
        cita["hora"] = None
    else:
        cita["fecha"] = fecha.strftime("%d/%m/%Y")
        cita["hora"] = fecha.strftime("%H:%M")

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