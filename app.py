from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import SECRET_KEY
from models.psicologa import Psicologa
from models.tutor import Tutor
from functools import wraps
from models.cita import Cita
from datetime import datetime
from secrets import token_urlsafe
from hmac import compare_digest
from models.alumnos import Alumnos

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


@app.route("/panel-psicologa/cita/realizada", methods=["POST"])
@login_requerido("psicologa")
def marcar_cita_realizada():
    try:
        id_cita = int(request.form.get("id_cita", ""))
    except (ValueError, TypeError):
        flash("La cita seleccionada no es válida", "error")
        return redirect(url_for("agenda"))

    resumen = request.form.get("resumen", "").strip()
    recomendacion = request.form.get("recomendacion", "").strip()

    if not resumen or not recomendacion:
        flash("Completa el resumen y la recomendación", "error")
        return redirect(url_for("agenda"))

    if Cita.marcar_realizada(id_cita, resumen, recomendacion):
        flash("Cita marcada como realizada correctamente", "ok")
    else:
        flash("No se pudo guardar el seguimiento de la cita", "error")

    return redirect(url_for("agenda"))



@app.route("/panel-psicologa/seguimiento")
@login_requerido("psicologa")
def seguimiento():
    seguimientos = Cita.obtener_seguimientos()

    return render_template(
        "seguimiento.html",
        pagina="seguimiento",
        seguimientos=seguimientos
    )


@app.route("/panel-psicologa/seguimiento/mas-sesiones", methods=["POST"])
@login_requerido("psicologa")
def guardar_mas_sesiones():
    try:
        id_cita = int(request.form.get("id_cita", ""))
    except (ValueError, TypeError):
        flash("La cita seleccionada no es válida", "error")
        return redirect(url_for("seguimiento"))

    respuesta = request.form.get("requiere_mas_sesiones", "")

    if Cita.actualizar_mas_sesiones(id_cita, respuesta):
        flash("Decisión guardada correctamente", "ok")
    else:
        flash("No se pudo guardar la decisión", "error")

    return redirect(url_for("seguimiento"))


@app.route("/panel-psicologa/seguimiento/otra-cita", methods=["POST"])
@login_requerido("psicologa")
def guardar_otra_cita():
    try:
        id_cita = int(request.form.get("id_cita", ""))
    except (ValueError, TypeError):
        flash("La cita seleccionada no es válida", "error")
        return redirect(url_for("seguimiento"))

    fecha = request.form.get("fecha", "").strip()
    hora = request.form.get("hora", "").strip()

    if not fecha or not hora:
        flash("Debes seleccionar una fecha y hora", "error")
        return redirect(url_for("seguimiento"))

    try:
        fecha_cita = datetime.strptime(
            f"{fecha} {hora}", "%Y-%m-%d %H:%M"
        )
    except ValueError:
        flash("La fecha u hora no es válida", "error")
        return redirect(url_for("seguimiento"))

    if fecha_cita <= datetime.now():
        flash("La nueva cita debe tener una fecha futura", "error")
        return redirect(url_for("seguimiento"))

    folio, error = Cita.agendar_otra_cita(id_cita, fecha_cita)

    if error:
        flash(error, "error")
    else:
        flash(f"Nueva cita agendada. Folio: {folio}", "ok")

    return redirect(url_for("seguimiento"))


@app.route("/panel-psicologa/historial")
@login_requerido("psicologa")
def historial():
    citas = Cita.obtener_historial()
    return render_template("historial.html", pagina="historial", citas=citas)



@app.route("/panel-psicologa/alumnos")
@login_requerido("psicologa")
def lista_alumnos():
    alumnos = Alumnos.obtener_lista()

    return render_template(
        "lista_alumnos.html",
        pagina="alumnos",
        alumnos=alumnos
    )




@app.route("/panel-psicologa/profesores")
@login_requerido("psicologa")
def profesores():

    # Crear un token de seguridad para la sesión
    if "_csrf_token" not in session:
        session["_csrf_token"] = token_urlsafe(32)

    tutores = Tutor.obtener_resumen()

    return render_template(
        "lista_profesores.html",
        pagina="profesores",
        tutores=tutores
    )



@app.route("/panel-psicologa/registrar-tutor", methods=["GET", "POST"])
@login_requerido("psicologa")
def registrar_tutor():


    # Crear un token CSRF si todavía no existe
    if "_csrf_token" not in session:
        session["_csrf_token"] = token_urlsafe(32)

    # Verificar el token antes de registrar
    if request.method == "POST":
        token_recibido = request.form.get("_csrf_token", "")
        token_esperado = session.get("_csrf_token")

        if not token_esperado or not compare_digest(
            token_recibido, token_esperado
        ):
            flash("Solicitud no autorizada. Intenta nuevamente", "error")
            return redirect(url_for("registrar_tutor"))


    # Mostrar el formulario
    if request.method == "GET":
        return render_template(
            "registrar_tutor.html",
            pagina="profesores",
            datos={}
        )

    # Obtener los datos del formulario
    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip().lower()
    telefono = request.form.get("telefono", "").strip()
    contrasena = request.form.get("contrasena", "")
    cuatrimestre = request.form.get("cuatrimestre", "").strip()
    grupo = request.form.get("grupo", "").strip().upper()
    carrera = request.form.get("carrera", "").strip()

    error = None

    # Validar los datos recibidos
    if not nombre or len(nombre) > 45:
        error = "El nombre es obligatorio (máximo 45 caracteres)"

    elif not correo or len(correo) > 45 or "@" not in correo:
        error = "Ingresa un correo electrónico válido"

    elif telefono and (
        not telefono.isascii()
        or not telefono.isdigit()
        or not 10 <= len(telefono) <= 15
    ):
        error = "El teléfono debe tener entre 10 y 15 números"

    elif not cuatrimestre.isascii() or not cuatrimestre.isdigit():
        error = "El cuatrimestre debe ser un número"

    elif not 1 <= int(cuatrimestre) <= 11:
        error = "El cuatrimestre debe estar entre 1 y 11"

    elif not grupo or len(grupo) > 10:
        error = "El grupo es obligatorio (máximo 10 caracteres)"

    elif not carrera or len(carrera) > 100:
        error = "La carrera es obligatoria (máximo 100 caracteres)"

    elif not 8 <= len(contrasena) <= 128:
        error = "La contraseña debe tener entre 8 y 128 caracteres"

    elif Tutor.buscar_por_correo(correo) is not None:
        error = "Ya existe un tutor registrado con ese correo"

    # Si los datos son correctos, crear el tutor
    if error is None:

        tutor = Tutor.nuevo(
            nombre=nombre,
            telefono=telefono or None,
            correo=correo,
            contrasena_plana=contrasena,
            cuatrimestre=int(cuatrimestre),
            grupo=grupo,
            carrera=carrera
        )

        if tutor.guardar():
            flash("Tutor registrado correctamente", "ok")
            return redirect(url_for("registrar_tutor"))

        error = "No se pudo registrar el tutor. Revisa la conexión con MariaDB"

    # Mostrar el error sin borrar los datos del formulario
    flash(error, "error")

    return render_template(
        "registrar_tutor.html",
        pagina="profesores",
        datos=request.form
    )

@app.route("/panel-psicologa/editar-tutor/<int:id_tutor>", methods=["GET", "POST"])
@login_requerido("psicologa")
def editar_tutor(id_tutor):

    # Crear un token CSRF si todavía no existe
    if "_csrf_token" not in session:
        session["_csrf_token"] = token_urlsafe(32)

    # Verificar el token antes de actualizar
    if request.method == "POST":
        token_recibido = request.form.get("_csrf_token", "")
        token_esperado = session.get("_csrf_token")

        if not token_esperado or not compare_digest(
            token_recibido, token_esperado
        ):
            flash("Solicitud no autorizada. Intenta nuevamente", "error")
            return redirect(
                url_for("editar_tutor", id_tutor=id_tutor)
            )

    tutor = Tutor.buscar_por_id(id_tutor)

    if tutor is None:
        flash("Tutor no encontrado", "error")
        return redirect(url_for("profesores"))

    if request.method == "GET":
        datos = {
            "nombre": tutor.nombre,
            "correo": tutor.correo,
            "telefono": tutor.telefono,
            "cuatrimestre": tutor.cuatrimestre,
            "grupo": tutor.grupo,
            "carrera": tutor.carrera
        }

        return render_template(
            "editar_tutor.html",
            pagina="profesores",
            id_tutor=id_tutor,
            datos=datos
        )

    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip().lower()
    telefono = request.form.get("telefono", "").strip()
    cuatrimestre = request.form.get("cuatrimestre", "").strip()
    grupo = request.form.get("grupo", "").strip().upper()
    carrera = request.form.get("carrera", "").strip()

    error = None

    if not nombre or len(nombre) > 45:
        error = "El nombre es obligatorio (máximo 45 caracteres)"

    elif not correo or len(correo) > 45 or "@" not in correo:
        error = "Ingresa un correo electrónico válido"

    elif telefono and (
        not telefono.isascii()
        or not telefono.isdigit()
        or not 10 <= len(telefono) <= 15
    ):
        error = "El teléfono debe tener entre 10 y 15 números"

    elif not cuatrimestre.isascii() or not cuatrimestre.isdigit():
        error = "El cuatrimestre debe ser un número"

    elif not 1 <= int(cuatrimestre) <= 11:
        error = "El cuatrimestre debe estar entre 1 y 11"

    elif not grupo or len(grupo) > 10:
        error = "El grupo es obligatorio (máximo 10 caracteres)"

    elif not carrera or len(carrera) > 100:
        error = "La carrera es obligatoria (máximo 100 caracteres)"

    else:
        existente = Tutor.buscar_por_correo(correo)
        if existente is not None and existente.id_tutor != id_tutor:
            error = "Ya existe otro tutor registrado con ese correo"

    if error is None:
        tutor.nombre = nombre
        tutor.correo = correo
        tutor.telefono = telefono or None
        tutor.cuatrimestre = int(cuatrimestre)
        tutor.grupo = grupo
        tutor.carrera = carrera

        if tutor.actualizar():
            flash("Tutor actualizado correctamente", "ok")
            return redirect(url_for("profesores"))

        error = "No se pudo actualizar el tutor. Revisa la conexión con MariaDB"

    flash(error, "error")

    return render_template(
        "editar_tutor.html",
        pagina="profesores",
        id_tutor=id_tutor,
        datos=request.form
    )


@app.route("/panel-psicologa/eliminar-tutor/<int:id_tutor>", methods=["POST"])
@login_requerido("psicologa")
def eliminar_tutor(id_tutor):
    """Elimina un tutor si no tiene alumnos ni citas relacionadas."""

    # Verificar el token de seguridad
    token_recibido = request.form.get("_csrf_token", "")
    token_esperado = session.get("_csrf_token")

    if not token_esperado or not compare_digest(
        token_recibido, token_esperado
    ):
        flash("Solicitud no autorizada. Intenta nuevamente", "error")
        return redirect(url_for("profesores"))


    # Verificar que el tutor exista
    tutor = Tutor.buscar_por_id(id_tutor)

    if tutor is None:
        flash("El tutor no existe o ya fue eliminado", "error")
        return redirect(url_for("profesores"))

    # Intentar eliminar el tutor
    eliminado, mensaje = Tutor.eliminar_por_id(id_tutor)

    if eliminado:
        flash(mensaje, "ok")
    else:
        flash(mensaje, "error")

    # Regresar a la lista de profesores
    return redirect(url_for("profesores"))




@app.route("/panel-profesor")
@login_requerido("tutor")
def panel_profesor():
    return render_template("inicio_profesor.html", pagina="inicio")


@app.route("/panel-profesor/solicitar-cita", methods=["GET", "POST"])
@login_requerido("tutor")
def solicitar_cita():
    
    if request.method == "GET":
        matricula = request.args.get("matricula", "").strip()
        datos = {}

        if matricula:
            alumno = Alumnos.obtener_por_matricula_y_tutor(
                matricula,
                session["id"]
            )

            if alumno is None:
                flash("No se encontró el alumno asignado a tu cuenta", "error")
                return redirect(url_for("mis_alumnos"))

            datos = alumno

        return render_template(
            "solicitar_cita.html",
            pagina="solicitar",
            datos=datos
        )
    alumno, motivo, error = validar_solicitud(request.form)
    if error is None:
        folio, error = Cita.solicitar(session["id"], motivo, alumno)


    if error:
        # Se vuelve a mostrar el formulario con lo que escribió, para que no lo capture de nuevo
        flash(error, "error")
        return render_template("solicitar_cita.html", pagina="solicitar", datos=request.form)
    
    return render_template(
        "solicitar_cita.html",
        pagina="solicitar",
        datos={},
        folio_generado=folio
    )




@app.route("/panel-profesor/mis-alumnos")
@login_requerido("tutor")
def mis_alumnos():
    id_tutor = session["id"]

    alumnos = Alumnos.obtener_estado_por_tutor(id_tutor)

    return render_template(
        "mis_alumnos.html",
        pagina="alumnos",
        alumnos=alumnos
    )



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