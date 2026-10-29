import pymysql
import secrets
from database.conexion import obtener_conexion

class Cita:
    def __init__(self,num_folio, fecha, estatus, motivo, matricula_alumno, id_tutor, id_psicologa, id_cita= None):
        self.id_cita = id_cita
        self.num_folio = num_folio
        self.fecha = fecha
        self.estatus = estatus
        self.motivo = motivo
        self.matricula_alumno = matricula_alumno
        self.id_tutor= id_tutor
        self.id_psicologa = id_psicologa

    def guardar(self):
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = ("INSERT INTO cita (num_folio, fecha, estatus, motivo, matricula_alumno, id_tutor, id_psicologa) VALUES (%s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(sql,(self.num_folio, self.fecha, self.estatus, self.motivo, self.matricula_alumno, self.id_tutor, self.id_psicologa),)
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
            return[]
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM cita")
                filas = cursor.fetchall()
            return [
                Cita(f["num_folio"], f["fecha"], f["estatus"], f["motivo"], f["matricula_alumno"], f["id_tutor"], f["id_psicologa"], f["id_cita"])
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
                    SELECT c.id_cita, c.num_folio, c.fecha, c.estatus,
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
    def rechazar(id_cita):
        """Marca una solicitud como 'Rechazada' y le pone la fecha de hoy
        para que salga hasta arriba en el Historial. Solo si seguía como 'Solicitada'."""
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
                cursor.execute("SELECT id_tutor FROM alumnos WHERE matricula = %s",
                               (alumno["matricula"],))
                existente = cursor.fetchone()

                if existente is None:
                    cursor.execute(
                        """INSERT INTO alumnos (matricula, nombre, a_paterno, a_materno,
                                                grado, grupo, carrera, id_tutor)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (alumno["matricula"], alumno["nombre"], alumno["a_paterno"],
                         alumno["a_materno"], alumno["grado"], alumno["grupo"],
                         alumno["carrera"], id_tutor))
                elif existente["id_tutor"] != id_tutor:
                    conexion.rollback()
                    return None, "Esa matrícula ya está registrada con otro tutor"

                # 2) La psicóloga (el sistema tiene una sola)
                cursor.execute("SELECT id_psicologa FROM psicologa ORDER BY id_psicologa LIMIT 1")
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
                            (folio, motivo, alumno["matricula"], id_tutor,
                             psicologa["id_psicologa"]))
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

if __name__ == "__main__":
    nueva = Cita("F001", "2026-10-15 10:00:00", "Pendiente", "Primera cita", "2024001", 2, 1)
    print("Guardado:", nueva.guardar())
    for c in Cita.obtener_todos():
        print(c.id_cita, c.num_folio, c.estatus)