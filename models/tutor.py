
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from database.conexion import obtener_conexion


class Tutor:
    def __init__(self, nombre, telefono, correo, contrasena,
                 id_tutor=None, cuatrimestre=None, grupo=None, carrera=None):
        self.id_tutor = id_tutor
        self.nombre = nombre
        self.telefono = telefono or None
        self.correo = correo
        self.contrasena = contrasena
        self.cuatrimestre = cuatrimestre
        self.grupo = grupo
        self.carrera = carrera

    @classmethod
    def nuevo(cls, nombre, telefono, correo, contrasena_plana,
              cuatrimestre=None, grupo=None, carrera=None):
        """Crea un tutor y convierte su contraseña en hash."""
        return cls(
            nombre, telefono, correo,
            generate_password_hash(contrasena_plana),
            cuatrimestre=cuatrimestre,
            grupo=grupo,
            carrera=carrera
        )

    def verificar_contrasena(self, contrasena_plana):
        """Comprueba la contraseña del tutor."""
        return check_password_hash(self.contrasena, contrasena_plana)

    def guardar(self):
        """Guarda el tutor en MariaDB."""
        conexion = obtener_conexion()

        if conexion is None:
            return False

        try:
            with conexion.cursor() as cursor:
                sql = """
                    INSERT INTO tutor
                    (nombre, telefono, correo, contrasena,
                     cuatrimestre, grupo, carrera)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(sql, (
                    self.nombre,
                    self.telefono,
                    self.correo,
                    self.contrasena,
                    self.cuatrimestre,
                    self.grupo,
                    self.carrera
                ))

                self.id_tutor = cursor.lastrowid

            conexion.commit()
            return True

        except pymysql.MySQLError as error:
            print(f"Error al guardar tutor: {error}")
            conexion.rollback()
            return False

        finally:
            conexion.close()

    @staticmethod
    def desde_fila(fila):
        """Convierte una fila de MariaDB en un objeto Tutor."""
        return Tutor(
            nombre=fila["nombre"],
            telefono=fila["telefono"],
            correo=fila["correo"],
            contrasena=fila["contrasena"],
            id_tutor=fila["id_tutor"],
            cuatrimestre=fila["cuatrimestre"],
            grupo=fila["grupo"],
            carrera=fila["carrera"]
        )

    @staticmethod
    def buscar_por_correo(correo):
        """Busca un tutor por correo."""
        conexion = obtener_conexion()

        if conexion is None:
            return None

        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM tutor WHERE correo = %s",
                    (correo,)
                )
                fila = cursor.fetchone()

                if fila is None:
                    return None

                return Tutor.desde_fila(fila)

        except pymysql.MySQLError as error:
            print(f"Error al buscar tutor: {error}")
            return None

        finally:
            conexion.close()

    
    @staticmethod
    def buscar_por_id(id_tutor):
        """Busca un tutor por su ID para poder editarlo."""
        conexion = obtener_conexion()

        if conexion is None:
            return None

        try:
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM tutor WHERE id_tutor = %s"
                cursor.execute(sql, (id_tutor,))
                fila = cursor.fetchone()

                if fila is None:
                    return None

                return Tutor.desde_fila(fila)

        except pymysql.MySQLError as error:
            print(f"Error al buscar tutor por ID: {error}")
            return None

        finally:
            conexion.close()


    def actualizar(self):
        """Actualiza los datos de un tutor en MariaDB."""
        conexion = obtener_conexion()

        if conexion is None:
            return False

        try:
            with conexion.cursor() as cursor:
                sql = """
                    UPDATE tutor
                    SET nombre = %s,
                        telefono = %s,
                        correo = %s,
                        cuatrimestre = %s,
                        grupo = %s,
                        carrera = %s
                    WHERE id_tutor = %s
                """

                cursor.execute(sql, (
                    self.nombre,
                    self.telefono or None,
                    self.correo,
                    self.cuatrimestre,
                    self.grupo,
                    self.carrera,
                    self.id_tutor
                ))

            conexion.commit()
            return True

        except pymysql.MySQLError as error:
            print(f"Error al actualizar tutor: {error}")
            conexion.rollback()
            return False

        finally:
            conexion.close()


    @staticmethod
    def eliminar_por_id(id_tutor):
        """Elimina un tutor solo si no tiene alumnos ni citas relacionadas."""

        conexion = obtener_conexion()

        if conexion is None:
            return False, "No se pudo conectar con MariaDB"

        try:
            with conexion.cursor() as cursor:

                # Comprobar si tiene alumnos registrados
                cursor.execute(
                    "SELECT COUNT(*) AS total FROM alumnos WHERE id_tutor = %s",
                    (id_tutor,)
                )

                alumnos = cursor.fetchone()["total"]

                if alumnos > 0:
                    return False, "No puedes eliminar un tutor que tiene alumnos asignados"

                # Comprobar si tiene citas registradas
                cursor.execute(
                    "SELECT COUNT(*) AS total FROM cita WHERE id_tutor = %s",
                    (id_tutor,)
                )

                citas = cursor.fetchone()["total"]

                if citas > 0:
                    return False, "No puedes eliminar un tutor que tiene citas registradas"

                # Eliminar solamente si no tiene relaciones
                cursor.execute(
                    "DELETE FROM tutor WHERE id_tutor = %s",
                    (id_tutor,)
                )

                eliminado = cursor.rowcount

            conexion.commit()

            if eliminado == 0:
                return False, "El tutor no existe"

            return True, "Tutor eliminado correctamente"

        except pymysql.MySQLError as error:
            print(f"Error al eliminar tutor: {error}")
            conexion.rollback()
            return False, "No se pudo eliminar el tutor"

        finally:
            conexion.close()



    @staticmethod
    def obtener_todos():
        """Obtiene todos los tutores."""
        conexion = obtener_conexion()

        if conexion is None:
            return []

        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM tutor")
                filas = cursor.fetchall()

                return [
                    Tutor.desde_fila(fila)
                    for fila in filas
                ]

        except pymysql.MySQLError as error:
            print(f"Error al consultar tutores: {error}")
            return []

        finally:
            conexion.close()

    @staticmethod
    def obtener_resumen():
        """Consulta los tutores y sus alumnos asignados."""
        conexion = obtener_conexion()

        if conexion is None:
            return []

        try:
            with conexion.cursor() as cursor:

                sql = """
                    SELECT
                        t.id_tutor,
                        t.nombre,
                        t.correo,
                        t.telefono,
                        t.cuatrimestre,
                        t.grupo,
                        t.carrera,
                        GROUP_CONCAT(
                            DISTINCT CONCAT(a.grado, a.grupo)
                            ORDER BY a.grado, a.grupo
                            SEPARATOR ', '
                        ) AS grupos,
                        COUNT(a.matricula) AS total_alumnos
                    FROM tutor t
                    LEFT JOIN alumnos a
                        ON a.id_tutor = t.id_tutor
                    GROUP BY
                        t.id_tutor,
                        t.nombre,
                        t.correo,
                        t.telefono,
                        t.cuatrimestre,
                        t.grupo,
                        t.carrera
                    ORDER BY t.nombre
                """


                cursor.execute(sql)
                return cursor.fetchall()

        except pymysql.MySQLError as error:
            print(f"Error al consultar el resumen de tutores: {error}")
            return []

        finally:
            conexion.close()
