import pymysql
from database.conexion import obtener_conexion

class Psicologa:
    def __init__(self,nombre , usuario, contrasena, id_psicologa= None):
        self.id_psicologa = id_psicologa
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena

    def guardar(self):
        """Con este apartado inserta y verifca el psicologa. Devuelve true si salio bien."""
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO psicologa(nombre, usuario, contrasena) VALUES (%s, %s, %s)"
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
    def obtener_todos():
        """Regresa o muestra una lista de los psicologas ."""
        conexion = obtener_conexion()
        if conexion is None:
            return[]
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
    nueva = Psicologa("Psicóloga Prueba", "psico1", "clave123")
    print("Guardado:", nueva.guardar())
    for p in Psicologa.obtener_todos():
        print(p.id_psicologa, p.nombre, p.usuario)