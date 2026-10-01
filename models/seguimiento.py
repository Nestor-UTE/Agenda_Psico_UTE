import pymysql
from database.conexion import obtener_conexion

class Seguimiento:
    def __init__(self, recomendacion, resumen, id_cita= None):
        self.id_cita = id_cita
        self.recomendacion = recomendacion
        self.resumen = resumen

    def guardar(self):
        conexion = obtener_conexion()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO seguimiento (id_cita, recomendacion, resumen) VALUES (%s, %s, %s)"
                cursor.execute(sql, (self.id_cita, self.recomendacion, self.resumen))
            conexion.commit()
            return True
        except pymysql.MySQLError as error:
            print(f"Error al guardar el seguimiento: {error}")
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
                cursor.execute("SELECT * FROM seguimiento")
                filas = cursor.fetchall()
            return [
                Seguimiento(recomendacion=f["recomendacion"], resumen=f["resumen"], id_cita=f["id_cita"])
                for f in filas
            ]
        except pymysql.MySQLError as error:
            print(f"Error al mostrar el seguimiento: {error}")
            return []
        finally:
            conexion.close()

if __name__ == "__main__":
    nuevo = Seguimiento("Se recomienda seguimiento mensual", "Primera sesión, sin incidentes", id_cita=1)
    print("Guardado:", nuevo.guardar())
    for s in Seguimiento.obtener_todos():
        print(s.id_cita, s.recomendacion)