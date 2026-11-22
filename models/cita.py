import pymysql
import secrets
from database.conexion import obtener_conexion


class Cita:
    def __init__(
        self,
        num_folio,
        fecha,
        estatus,
        motivo,
        matricula_alumno,
        id_tutor,
        id_psicologa,
        id_cita=None,
    ):
        self.id_cita = id_cita
        self.num_folio = num_folio
        self.fecha = fecha
        self.estatus = estatus
        self.motivo = motivo
        self.matricula_alumno = matricula_alumno
        self.id_tutor = id_tutor
        self.id_psicologa = id_psicologa

    def guardar(self):
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO cita (num_folio, fecha, estatus, motivo, matricula_alumno, id_tutor, id_psicologa) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(
                    sql,
                    (
                        self.num_folio,
                        self.fecha,
                        self.estatus,
                        self.motivo,
                        self.matricula_alumno,
                        self.id_tutor,
                        self.id_psicologa,
                    ),
                )
                self.id_cita = cursor.lastrowid
            conexion.commit()
            return True
        except pymysql.MySQLError as error:
            print(f"Error al guardar la cita: {error}")
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @staticmethod
    def obtener_todos():
        """Regresa o muestra la lista de las citas ."""
        conexion = obtener_conexion()
        if conexion is None:
            return []
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM cita")
                filas = cursor.fetchall()
            return [
                Cita(
                    f["num_folio"],
                    f["fecha"],
                    f["estatus"],
                    f["motivo"],
                    f["matricula_alumno"],
                    f["id_tutor"],
                    f["id_psicologa"],
                    f["id_cita"],
                )
                for f in filas
            ]
        except pymysql.MySQLError as error:
            print(f"Error al mostrar las citas: {error}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def obtener_agenda():
        """Citas ya agendadas, la más próxima primero.
        Regresa una lista de diccionarios listos para la pantalla."""
        conexion = obtener_conexion()
        if conexion is None:
            return []
        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT c.id_cita, c.num_folio, c.fecha, c.estatus, c.motivo,
                           a.matricula,
                           CONCAT(a.nombre, ' ', a.a_paterno, ' ', a.a_materno) AS alumno,
                           CONCAT(a.grado, a.grupo) AS grupo,
                           t.nombre AS tutor
                    FROM cita c
                    LEFT JOIN alumnos a ON a.matricula = c.matricula_alumno
                    LEFT JOIN tutor t ON t.id_tutor = c.id_tutor
                    WHERE c.estatus = 'Agendada'
                    ORDER BY c.fecha ASC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except pymysql.MySQLError as error:
            print(f"Error al consultar la agenda: {error}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def obtener_historial():
        """Citas ya cerradas (realizadas, reprogramadas o rechazadas), la más reciente primero."""
        conexion = obtener_conexion()
        if conexion is None:
            return []
        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT c.id_cita, c.num_folio, c.fecha, c.estatus,
                           a.matricula,
                           CONCAT(a.nombre, ' ', a.a_paterno, ' ', a.a_materno) AS alumno,
                           CONCAT(a.grado, a.grupo) AS grupo,
                           t.nombre AS tutor
                    FROM cita c
                    LEFT JOIN alumnos a ON a.matricula = c.matricula_alumno
                    LEFT JOIN tutor t ON t.id_tutor = c.id_tutor
                    WHERE c.estatus IN ('Realizada', 'Reprogramada', 'Rechazada')
                    ORDER BY c.fecha DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except pymysql.MySQLError as error:
            print(f"Error al consultar el historial: {error}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def obtener_solicitudes():
        """Citas que el tutor pidió y todavía no tienen fecha, la más antigua primero."""
        conexion = obtener_conexion()
        if conexion is None:
            return []
        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT c.id_cita, c.num_folio, c.motivo,
                           a.matricula, a.carrera,
                           CONCAT(a.nombre, ' ', a.a_paterno, ' ', a.a_materno) AS alumno,
                           CONCAT(a.grado, a.grupo) AS grupo,
                           t.nombre AS tutor
                    FROM cita c
                    LEFT JOIN alumnos a ON a.matricula = c.matricula_alumno
                    LEFT JOIN tutor t ON t.id_tutor = c.id_tutor
                    WHERE c.estatus = 'Solicitada'
                    ORDER BY c.id_cita ASC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except pymysql.MySQLError as error:
            print(f"Error al consultar las solicitudes: {error}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def agendar(id_cita, fecha):
        """Le pone fecha y hora a una solicitud y la pasa a 'Agendada'.
        Solo cambia citas que siguen como 'Solicitada'. Regresa True si se actualizó."""
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = """
                    UPDATE cita
                    SET fecha = %s, estatus = 'Agendada'
                    WHERE id_cita = %s AND estatus = 'Solicitada'
                """
                cursor.execute(sql, (fecha, id_cita))
                actualizadas = cursor.rowcount
            conexion.commit()
            return actualizadas == 1
        except pymysql.MySQLError as error:
            print(f"Error al agendar la cita: {error}")
            conexion.rollback()
            return False
        finally:
            conexion.close()
            
    
    @staticmethod
    def reprogramar(id_cita, nueva_fecha):
        conexion = obtener_conexion()

        if conexion is None:
            return False, "No hay conexión con la base de datos"

        try:
            with conexion.cursor() as cursor:
                # Comprobar que la cita existe y sigue agendada
                cursor.execute(
                    """
                    SELECT id_psicologa
                    FROM cita
                    WHERE id_cita = %s
                    AND estatus = 'Agendada'
                    """,
                    (id_cita,)
                )

                cita = cursor.fetchone()

                if cita is None:
                    return False, "La cita ya no está agendada"

                # Verificar que el nuevo horario esté libre
                cursor.execute(
                    """
                    SELECT id_cita
                    FROM cita
                    WHERE fecha = %s
                    AND id_psicologa = %s
                    AND id_cita != %s
                    AND estatus IN ('Agendada', 'Reprogramada')
                    LIMIT 1
                    """,
                    (nueva_fecha, cita["id_psicologa"], id_cita)
                )

                if cursor.fetchone() is not None:
                    return False, "Ya existe una cita en ese horario"

                # Actualizar fecha y hora de la cita
                cursor.execute(
                    """
                    UPDATE cita
                    SET fecha = %s
                    WHERE id_cita = %s
                    AND estatus = 'Agendada'
                    """,
                    (nueva_fecha, id_cita)
                )

                if cursor.rowcount != 1:
                    conexion.rollback()
                    return False, "No se pudo actualizar la cita"

            conexion.commit()
            return True, None

        except pymysql.MySQLError as error:
            conexion.rollback()
            print(f"Error al reprogramar: {error}")
            return False, "No se pudo reprogramar la cita"

        finally:
            conexion.close()


    @staticmethod
    def agendar_directamente(datos_alumno, fecha, motivo, id_psicologa):
        """Crea una cita para un alumno nuevo o existente."""
        matricula = datos_alumno["matricula"]
        conexion = obtener_conexion()

        if conexion is None:
            return None, "No hay conexión con la base de datos"

        try:
            with conexion.cursor() as cursor:
                # Comprobar si ya existe una cita en esa fecha y hora
                cursor.execute(
                    """
                SELECT id_cita
                FROM cita
                WHERE fecha = %s
                AND estatus IN ('Agendada', 'Reprogramada')
                LIMIT 1
                """,
                    (fecha,),
                )
                if cursor.fetchone() is not None:
                    return None, "Ya existe una cita agendada en ese horario"
                # Buscar al alumno y obtener su tutor
            # Buscar si el alumno ya existe y conservar su tutor
                cursor.execute(
                    """
                    SELECT id_tutor
                    FROM alumnos
                    WHERE matricula = %s
                    """,
                    (matricula,),
                )
                alumno = cursor.fetchone()
                id_tutor = alumno["id_tutor"] if alumno is not None else None
                # Si el alumno ya existe, actualizar sus datos
                if alumno is not None:
                    cursor.execute(
                        """
                        UPDATE alumnos
                        SET nombre = %s,
                            a_paterno = %s,
                            a_materno = %s,
                            grado = %s,
                            grupo = %s,
                            carrera = %s
                        WHERE matricula = %s
                        """,
                        (
                            datos_alumno["nombre"],
                            datos_alumno["a_paterno"],
                            datos_alumno["a_materno"],
                            datos_alumno["grado"],
                            datos_alumno["grupo"],
                            datos_alumno["carrera"],
                            matricula,
                        ),
                    )
                # Si el alumno no existe, registrarlo
                if alumno is None:
                    # Registrar al alumno si todavía no existe
                    cursor.execute(
                        """
                    INSERT INTO alumnos
                    (matricula, nombre, a_paterno, a_materno,
                    grado, grupo, carrera, id_tutor)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)
                    """,
                        (
                            matricula,
                            datos_alumno["nombre"],
                            datos_alumno["a_paterno"],
                            datos_alumno["a_materno"],
                            datos_alumno["grado"],
                            datos_alumno["grupo"],
                            datos_alumno["carrera"],
                        ),
                    )

                # Guardar el estado de la transacción antes de intentar crear la cita
                cursor.execute("SAVEPOINT antes_de_cita")
                # Generar un folio único
                for _ in range(5):
                    folio = secrets.token_hex(4)

                    try:
                        cursor.execute(
                            """
                                INSERT INTO cita
                                (num_folio, fecha, estatus, motivo,
                                matricula_alumno, id_tutor, id_psicologa)
                                VALUES (%s, %s, 'Agendada', %s, %s, %s, %s)
                                """,
                            (folio, fecha, motivo, matricula, id_tutor, id_psicologa),
                        )

                        conexion.commit()
                        return folio, None

                    except pymysql.err.IntegrityError as error:
                        # Reintentar solo si el folio está duplicado
                        if error.args[0] != 1062 or "num_folio" not in str(error).lower():
                            raise

                        # Deshacer solo el intento de insertar la cita
                        cursor.execute("ROLLBACK TO SAVEPOINT antes_de_cita")

                        # Volver a intentar con otro folio
                        continue

            # Deshacer todos los cambios si no se pudo crear la cita
            conexion.rollback()
            return None, "No se pudo generar un folio único"

        except pymysql.MySQLError as error:
            conexion.rollback()
            print(f"Error al agendar directamente: {error}")
            return None, "No se pudo registrar la cita"

        finally:
            conexion.close()

    @staticmethod
    def rechazar(id_cita):
        """Marca una solicitud como 'Rechazada' y le pone la fecha de hoy
        para que salga hasta arriba en el Historial. Solo si seguía como 'Solicitada'.
        """
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = """
                    UPDATE cita
                    SET estatus = 'Rechazada', fecha = NOW()
                    WHERE id_cita = %s AND estatus = 'Solicitada'
                """
                cursor.execute(sql, (id_cita,))
                actualizadas = cursor.rowcount
            conexion.commit()
            return actualizadas == 1
        except pymysql.MySQLError as error:
            print(f"Error al rechazar la cita: {error}")
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @staticmethod
    def solicitar(id_tutor, motivo, alumno):
        """Crea una solicitud de cita (estatus 'Solicitada', sin fecha).
        Si el alumno no existe, lo registra con los datos que escribió el tutor.
        'alumno' es un diccionario con: matricula, nombre, a_paterno, a_materno,
        grado, grupo y carrera.
        Regresa (folio, None) si salió bien, o (None, mensaje) si no."""
        conexion = obtener_conexion()
        if conexion is None:
            return None, "No hay conexión con la base de datos"
        try:
            with conexion.cursor() as cursor:
                # 1) ¿Ya existe ese alumno?
                cursor.execute(
                    "SELECT id_tutor FROM alumnos WHERE matricula = %s",
                    (alumno["matricula"],),
                )
                existente = cursor.fetchone()

                if existente is None:
                    cursor.execute(
                        """INSERT INTO alumnos (matricula, nombre, a_paterno, a_materno,
                                                grado, grupo, carrera, id_tutor)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            alumno["matricula"],
                            alumno["nombre"],
                            alumno["a_paterno"],
                            alumno["a_materno"],
                            alumno["grado"],
                            alumno["grupo"],
                            alumno["carrera"],
                            id_tutor,
                        ),
                    )
                elif existente["id_tutor"] != id_tutor:
                    conexion.rollback()
                    return None, "Esa matrícula ya está registrada con otro tutor"

                # 2) La psicóloga (el sistema tiene una sola)
                cursor.execute(
                    "SELECT id_psicologa FROM psicologa ORDER BY id_psicologa LIMIT 1"
                )
                psicologa = cursor.fetchone()
                if psicologa is None:
                    conexion.rollback()
                    return None, "No hay una psicóloga registrada"

                # 3) La cita, con un folio aleatorio (se reintenta si se repite)
                for _ in range(5):
                    folio = secrets.token_hex(4)
                    try:
                        cursor.execute(
                            """INSERT INTO cita (num_folio, fecha, estatus, motivo,
                                                 matricula_alumno, id_tutor, id_psicologa)
                               VALUES (%s, NULL, 'Solicitada', %s, %s, %s, %s)""",
                            (
                                folio,
                                motivo,
                                alumno["matricula"],
                                id_tutor,
                                psicologa["id_psicologa"],
                            ),
                        )
                        conexion.commit()
                        return folio, None
                    except pymysql.err.IntegrityError as error:
                        if error.args[0] != 1062:
                            raise

                conexion.rollback()
                return None, "No se pudo generar un folio, intenta de nuevo"
        except pymysql.MySQLError as error:
            print(f"Error al solicitar la cita: {error}")
            conexion.rollback()
            return None, "No se pudo guardar la solicitud"
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_folio(folio):
        """Busca una cita por su folio y regresa solo lo que puede ver el alumno
        (sin motivo, resumen ni recomendaciones). Regresa None si no existe."""
        conexion = obtener_conexion()
        if conexion is None:
            return None
        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT c.fecha, c.estatus,
                           CONCAT(a.nombre, ' ', a.a_paterno) AS alumno,
                           t.nombre AS tutor, t.telefono AS telefono_tutor,
                           u.edificio, u.docencia AS nombre_edificio,
                           u.salon, u.referencia
                    FROM cita c
                    LEFT JOIN alumnos a ON a.matricula = c.matricula_alumno
                    LEFT JOIN tutor t ON t.id_tutor = c.id_tutor
                    LEFT JOIN ubicacion u ON u.id_ubicacion = c.id_ubicacion
                    WHERE c.num_folio = %s
                """
                cursor.execute(sql, (folio,))
                return cursor.fetchone()
        except pymysql.MySQLError as error:
            print(f"Error al consultar el folio: {error}")
            return None
        finally:
            conexion.close()

    @staticmethod
    def marcar_realizada(id_cita, resumen, recomendacion):
        """Marca una cita como realizada y guarda su seguimiento."""

        if not resumen.strip() or not recomendacion.strip():
            return False

        conexion = obtener_conexion()

        if conexion is None:
            return False

        try:
            with conexion.cursor() as cursor:

                # Cambiar el estado de la cita
                cursor.execute(
                    """
                    UPDATE cita
                    SET estatus = 'Realizada'
                    WHERE id_cita = %s
                    AND estatus = 'Agendada'
                """,
                    (id_cita,),
                )

                if cursor.rowcount != 1:
                    conexion.rollback()
                    return False

                # Guardar resumen y recomendación
                cursor.execute(
                    """
                    INSERT INTO seguimiento
                        (id_cita, resumen, recomendacion)
                    VALUES (%s, %s, %s)
                """,
                    (id_cita, resumen, recomendacion),
                )

            conexion.commit()
            return True

        except pymysql.MySQLError as error:
            print(f"Error al marcar cita realizada: {error}")
            conexion.rollback()
            return False

        finally:
            conexion.close()

    @staticmethod
    def obtener_seguimientos():
        """Obtiene las citas realizadas con su seguimiento."""

        conexion = obtener_conexion()

        if conexion is None:
            return []

        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        c.id_cita,
                        c.fecha,
                        a.matricula,
                        a.carrera,
                        a.grado,
                        a.grupo,
                        CONCAT(
                            a.nombre, ' ',
                            a.a_paterno, ' ',
                            a.a_materno
                        ) AS alumno,
                        s.resumen,
                        s.recomendacion,
                        s.requiere_mas_sesiones
                    FROM seguimiento s
                    INNER JOIN cita c
                        ON c.id_cita = s.id_cita
                    INNER JOIN alumnos a
                        ON a.matricula = c.matricula_alumno
                    WHERE c.estatus = 'Realizada'
                    ORDER BY c.fecha DESC
                """
                )

                return cursor.fetchall()

        except pymysql.MySQLError as error:
            print(f"Error al obtener seguimientos: {error}")
            return []

        finally:
            conexion.close()

    @staticmethod
    def actualizar_mas_sesiones(id_cita, respuesta):
        """Guarda si el alumno requiere más sesiones."""

        if respuesta not in ("Por definir", "Sí", "No"):
            return False

        conexion = obtener_conexion()

        if conexion is None:
            return False

        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE seguimiento
                    SET requiere_mas_sesiones = %s
                    WHERE id_cita = %s
                """,
                    (respuesta, id_cita),
                )

                if cursor.rowcount == 0:
                    cursor.execute(
                        "SELECT id_cita FROM seguimiento WHERE id_cita = %s", (id_cita,)
                    )
                    if cursor.fetchone() is None:
                        conexion.rollback()
                        return False

            conexion.commit()
            return True

        except pymysql.MySQLError as error:
            print(f"Error al actualizar más sesiones: {error}")
            conexion.rollback()
            return False

        finally:
            conexion.close()

    @staticmethod
    def agendar_otra_cita(id_cita_anterior, fecha):
        """Crea una nueva cita para un alumno que ya fue atendido."""

        conexion = obtener_conexion()

        if conexion is None:
            return None, "No hay conexión con la base de datos"

        try:
            with conexion.cursor() as cursor:

                # Buscar los datos de la cita anterior
                cursor.execute(
                    """
                    SELECT
                        matricula_alumno,
                        id_tutor,
                        id_psicologa,
                        motivo
                    FROM cita
                    WHERE id_cita = %s
                    AND estatus = 'Realizada'
                """,
                    (id_cita_anterior,),
                )

                cita_anterior = cursor.fetchone()

                if cita_anterior is None:
                    return None, "La cita anterior no es válida"

                # Verificar que el horario esté disponible
                cursor.execute(
                    """
                    SELECT id_cita
                    FROM cita
                    WHERE id_psicologa = %s
                    AND fecha = %s
                    AND estatus = 'Agendada'
                    LIMIT 1
                """,
                    (cita_anterior["id_psicologa"], fecha),
                )

                if cursor.fetchone() is not None:
                    return None, "La psicóloga ya tiene una cita en ese horario"

                # Crear un folio nuevo
                for intento in range(5):
                    folio = secrets.token_hex(4)

                    try:
                        cursor.execute(
                            """
                            INSERT INTO cita (
                                num_folio,
                                fecha,
                                estatus,
                                motivo,
                                matricula_alumno,
                                id_tutor,
                                id_psicologa
                            )
                            VALUES (
                                %s, %s, 'Agendada',
                                %s, %s, %s, %s
                            )
                        """,
                            (
                                folio,
                                fecha,
                                "Sesión de seguimiento",
                                cita_anterior["matricula_alumno"],
                                cita_anterior["id_tutor"],
                                cita_anterior["id_psicologa"],
                            ),
                        )

                        conexion.commit()
                        return folio, None

                    except pymysql.err.IntegrityError as error:
                        if error.args[0] != 1062:
                            raise

                conexion.rollback()
                return None, "No se pudo generar un folio"

        except pymysql.MySQLError as error:
            print(f"Error al agendar otra cita: {error}")
            conexion.rollback()
            return None, "No se pudo agendar la cita"

        finally:
            conexion.close()


if __name__ == "__main__":
    nueva = Cita(
        "F001", "2026-10-15 10:00:00", "Pendiente", "Primera cita", "2024001", 2, 1
    )
    print("Guardado:", nueva.guardar())
    for c in Cita.obtener_todos():
        print(c.id_cita, c.num_folio, c.estatus)
