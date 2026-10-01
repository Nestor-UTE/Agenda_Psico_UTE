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

if __name__ == "__main__":
    nuevo = Alumnos("2024001", "Alumno Prueba", "Pérez", "López", 2, "A", "TICs", id_tutor=2)
    print("Guardado:", nuevo.guardar())
    for a in Alumnos.obtener_todos():
        print(a.matricula, a.nombre, a.id_tutor)