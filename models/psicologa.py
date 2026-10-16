import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from database.conexion import obtener_conexion


class Psicologa:
    def __init__(self, nombre, usuario, contrasena, id_psicologa=None):
        self.id_psicologa = id_psicologa
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena  # aquí siempre va el HASH, nunca la contraseña real

    @classmethod
    def nueva(cls, nombre, usuario, contrasena_plana):
        """Crea una psicóloga nueva convirtiendo la contraseña en hash."""
        return cls(nombre, usuario, generate_password_hash(contrasena_plana))

    def verificar_contrasena(self, contrasena_plana):
        """Devuelve True si la contraseña escrita coincide con el hash guardado."""
        return check_password_hash(self.contrasena, contrasena_plana)

    def guardar(self):
        """Inserta la psicóloga en la BD. Devuelve True si salió bien."""
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO psicologa (nombre, usuario, contrasena) VALUES (%s, %s, %s)"
                cursor.execute(sql, (self.nombre, self.usuario, self.contrasena))
                self.id_psicologa = cursor.lastrowid
            conexion.commit()
            return True
        except pymysql.MySQLError as error:
            print(f"Error al guardar psicologa: {error}")
            conexion.rollback()
            return False
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_usuario(usuario):
        """Busca una psicóloga por su usuario. Devuelve el objeto o None si no existe."""
        conexion = obtener_conexion()
        if conexion is None:
            return None
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM psicologa WHERE usuario = %s", (usuario,))
                fila = cursor.fetchone()
            if fila is None:
                return None
            return Psicologa(fila["nombre"], fila["usuario"], fila["contrasena"], fila["id_psicologa"])
        except pymysql.MySQLError as error:
            print(f"Error al buscar psicologa: {error}")
            return None
        finally:
            conexion.close()

    @staticmethod
    def obtener_todos():
        """Regresa una lista con todas las psicólogas."""
        conexion = obtener_conexion()
        if conexion is None:
            return []
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM psicologa")
                filas = cursor.fetchall()
            return [
                Psicologa(f["nombre"], f["usuario"], f["contrasena"], f["id_psicologa"])
                for f in filas
            ]
        except pymysql.MySQLError as error:
            print(f"Error al consultar psicologa: {error}")
            return []
        finally:
            conexion.close()


if __name__ == "__main__":
    nueva = Psicologa.nueva("Psicóloga Prueba", "psico1", "clave123")
    print("Guardado:", nueva.guardar())

    encontrada = Psicologa.buscar_por_usuario("psico1")
    print("Clave correcta:", encontrada.verificar_contrasena("clave123"))
    print("Clave incorrecta:", encontrada.verificar_contrasena("otra"))