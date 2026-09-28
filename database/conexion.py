import pymysql
from config import DB_CONFIG


def obtener_conexion():
    try:
        conexion = pymysql.connect(
            **DB_CONFIG,
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conexion
    except pymysql.MySQLError as error:
        print(f"Error al conectar con la base de datos: {error}")
        return None


if __name__ == "__main__":
    conexion = obtener_conexion()
    if conexion:
        print("Conexión exitosa")
        conexion.close()