import pymysql
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

if __name__ == "__main__":
    nueva = Cita("F001", "2026-10-15 10:00:00", "Pendiente", "Primera cita", "2024001", 2, 1)
    print("Guardado:", nueva.guardar())
    for c in Cita.obtener_todos():
        print(c.id_cita, c.num_folio, c.estatus)