import pymysql
from database.conexion import obtener_conexion

class Tutor:
    def __init__(self, nombre, telefono, correo, id_tutor=None):
        self.id_tutor = id_tutor
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    def guardar(self):
        """Con este apartado inserta y verifca el tutor. Devuelve true si salio bien."""
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO tutor (nombre, telefono, correo) VALUES (%s, %s, %s)"
                cursor.execute(sql, (self.nombre, self.telefono, self.correo))
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
    def obtener_todos():
        """Regresa o muestra una lista de los tutores ."""
        conexion = obtener_conexion()
        if conexion is None:
            return[]
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM tutor")
                filas = cursor.fetchall()
            return [
                Tutor(f["nombre"], f["telefono"], f["correo"], f["id_tutor"])
                for f in filas
            ]
        except pymysql.MySQLError as error:
            print(f"Error al consultar tutores: {error}")
            return []
        finally:
            conexion.close()



