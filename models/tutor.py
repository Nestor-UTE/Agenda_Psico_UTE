import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from database.conexion import obtener_conexion


class Tutor:
    def __init__(self, nombre, telefono, correo, contrasena, id_tutor=None):
        self.id_tutor = id_tutor
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.contrasena = contrasena  # aquí siempre va el HASH, nunca la contraseña real

    @classmethod
    def nuevo(cls, nombre, telefono, correo, contrasena_plana):
        """Crea un tutor nuevo convirtiendo la contraseña en hash."""
        return cls(nombre, telefono, correo, generate_password_hash(contrasena_plana))

    def verificar_contrasena(self, contrasena_plana):
        """Devuelve True si la contraseña escrita coincide con el hash guardado."""
        return check_password_hash(self.contrasena, contrasena_plana)

    def guardar(self):
        """Inserta el tutor en la BD. Devuelve True si salió bien."""
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO tutor (nombre, telefono, correo, contrasena) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (self.nombre, self.telefono, self.correo, self.contrasena))
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
    def buscar_por_correo(correo):
        """Busca un tutor por su correo. Devuelve el objeto o None si no existe."""
        conexion = obtener_conexion()
        if conexion is None:
            return None
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM tutor WHERE correo = %s", (correo,))
                fila = cursor.fetchone()
            if fila is None:
                return None
            return Tutor(fila["nombre"], fila["telefono"], fila["correo"], fila["contrasena"], fila["id_tutor"])
        except pymysql.MySQLError as error:
            print(f"Error al buscar tutor: {error}")
            return None
        finally:
            conexion.close()

    @staticmethod
    def obtener_todos():
        """Regresa una lista con todos los tutores."""
        conexion = obtener_conexion()
        if conexion is None:
            return []
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM tutor")
                filas = cursor.fetchall()
            return [
                Tutor(f["nombre"], f["telefono"], f["correo"], f["contrasena"], f["id_tutor"])
                for f in filas
            ]
        except pymysql.MySQLError as error:
            print(f"Error al consultar tutores: {error}")
            return []
        finally:
            conexion.close()


if __name__ == "__main__":
    nuevo = Tutor.nuevo("Tutor Prueba", "8112345678", "tutor1@ute.edu.mx", "clave123")
    print("Guardado:", nuevo.guardar())

    encontrado = Tutor.buscar_por_correo("tutor1@ute.edu.mx")
    print("Clave correcta:", encontrado.verificar_contrasena("clave123"))
    print("Clave incorrecta:", encontrado.verificar_contrasena("otra"))