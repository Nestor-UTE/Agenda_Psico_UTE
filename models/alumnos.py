import pymysql
from database.conexion import obtener_conexion

class Alumnos:
    def __init__(self,matricula, nombre, a_paterno, a_materno, grado, grupo, carrera, id_tutor):
        self.matricula = matricula
        self.nombre = nombre
        self.a_paterno = a_paterno
        self.a_materno = a_materno
        self.grado = grado
        self.grupo = grupo
        self.carrera = carrera
        self.id_tutor = id_tutor

    def guardar(self):
        """Con este apartado inserta y verifca el tutor. Devuelve true si salio bien."""
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO alumnos (matricula, nombre, a_paterno, a_materno, grado, grupo, carrera, id_tutor) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (self.matricula, self.nombre, self.a_paterno, self.a_materno, self.grado, self.grupo, self.carrera, self.id_tutor))
                
            conexion.commit()
            return True
        except pymysql.MySQLError as error:
            print(f"Error al guardar alumno: {error}")
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @staticmethod
    def obtener_todos():
        """Regresa o muestra una lista de los Alumnos ."""
        conexion = obtener_conexion()
        if conexion is None:
            return[]
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM alumnos")
                filas = cursor.fetchall()
            return [
                Alumnos(f["matricula"], f["nombre"], f["a_paterno"], f["a_materno"], f["grado"], f["grupo"], f["carrera"], f["id_tutor"])
                for f in filas
            ]
        except pymysql.MySQLError as error:
            print(f"Error al consultar alumnos: {error}")
            return []
        finally:
            conexion.close()


    @staticmethod
    def obtener_lista():
        """Obtiene los alumnos registrados junto con su tutor."""

        conexion = obtener_conexion()

        if conexion is None:
            return []

        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        a.matricula,
                        CONCAT(
                            a.nombre, ' ',
                            a.a_paterno, ' ',
                            COALESCE(a.a_materno, '')
                        ) AS alumno,
                        a.carrera,
                        a.grado,
                        a.grupo,
                        t.nombre AS tutor
                    FROM alumnos a
                    LEFT JOIN tutor t
                        ON a.id_tutor = t.id_tutor
                    ORDER BY a.a_paterno, a.nombre
                """)

                return cursor.fetchall()

        except pymysql.MySQLError as error:
            print(f"Error al obtener lista de alumnos: {error}")
            return []

        finally:
            conexion.close()


    @staticmethod
    def obtener_estado_por_tutor(id_tutor):
        """Obtiene los alumnos del tutor y su cita más reciente."""

        conexion = obtener_conexion()

        if conexion is None:
            return []

        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        a.matricula,
                        a.nombre,
                        a.a_paterno,
                        a.a_materno,
                        CONCAT(
                            a.nombre, ' ',
                            a.a_paterno, ' ',
                            COALESCE(a.a_materno, '')
                        ) AS alumno,
                        a.carrera,
                        a.grado,
                        a.grupo,
                        COALESCE(c.estatus, 'Sin cita') AS estatus,
                        c.id_cita,
                        c.num_folio,
                        c.fecha
                    FROM alumnos a

                    LEFT JOIN cita c
                        ON c.id_cita = (
                            SELECT c2.id_cita
                            FROM cita c2
                            WHERE c2.matricula_alumno = a.matricula
                            AND c2.id_tutor = a.id_tutor
                            ORDER BY c2.id_cita DESC
                            LIMIT 1
                        )

                    WHERE a.id_tutor = %s

                    ORDER BY a.a_paterno, a.nombre
                """, (id_tutor,))

                return cursor.fetchall()

        except pymysql.MySQLError as error:
            print(f"Error al consultar alumnos del tutor: {error}")
            return []

        finally:
            conexion.close()


    @staticmethod
    def obtener_por_matricula_y_tutor(matricula, id_tutor):
        """Busca un alumno que pertenece al tutor actual."""

        conexion = obtener_conexion()

        if conexion is None:
            return None

        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        matricula,
                        nombre,
                        a_paterno,
                        a_materno,
                        carrera,
                        grado,
                        grupo
                    FROM alumnos
                    WHERE matricula = %s
                    AND id_tutor = %s
                    LIMIT 1
                """, (matricula, id_tutor))

                return cursor.fetchone()

        except pymysql.MySQLError as error:
            print(f"Error al buscar alumno: {error}")
            return None

        finally:
            conexion.close()


    @staticmethod
    def obtener_por_tutor(id_tutor):
        """Alumnos asignados a un tutor, para el formulario de solicitar cita.
        Regresa diccionarios con: matricula, nombre, carrera y grupo (ej. 3A)."""
        conexion = obtener_conexion()
        if conexion is None:
            return []
        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT matricula, carrera,
                           CONCAT(nombre, ' ', a_paterno, ' ', a_materno) AS nombre,
                           CONCAT(grado, grupo) AS grupo
                    FROM alumnos
                    WHERE id_tutor = %s
                    ORDER BY a_paterno, a_materno, nombre
                """
                cursor.execute(sql, (id_tutor,))
                return cursor.fetchall()
        except pymysql.MySQLError as error:
            print(f"Error al consultar los alumnos del tutor: {error}")
            return []
        finally:
            conexion.close()

if __name__ == "__main__":
    nuevo = Alumnos("2024001", "Alumno Prueba", "Pérez", "López", 2, "A", "TICs", id_tutor=2)
    print("Guardado:", nuevo.guardar())
    for a in Alumnos.obtener_todos():
        print(a.matricula, a.nombre, a.id_tutor)