# Agenda Psico UTE

Sistema web desarrollado para dar seguimiento a las citas de psicología de la Universidad Tecnológica Gral. Mariano Escobedo (UTE), facilitando la comunicación entre tutores, alumnos y la psicóloga.

## Integrantes

- Nestor Josue Ramirez Salas
- Habacuc Israel Loredo Hernandez

## Tecnologías utilizadas

- Python
- Flask
- MariaDB
- PyMySQL
- Werkzeug
- HTML
- CSS
- JavaScript
- Figma
- Git y GitHub

## Funcionalidades

### Psicóloga

- Inicio de sesión.
- Gestión de tutores.
- Consulta de alumnos.
- Agendar, rechazar y reprogramar citas.
- Calendario semanal.
- Historial de citas.
- Registro de recomendaciones y seguimiento.
- Agendamiento directo de citas.

### Tutor

- Inicio de sesión.
- Solicitud de citas.
- Consulta de sus alumnos.
- Consulta de recomendaciones.
- Calendario semanal.
- Seguimiento de citas.

### Alumno

- Acceso mediante folio.
- Consulta del estado de su cita.
- Consulta de fecha, hora y ubicación.

## Requisitos de instalación

- Python 3
- MariaDB
- Git
- Navegador web

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Nestor-UTE/Agenda_Psico_UTE.git
cd Agenda_Psico_UTE
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

Activar en Linux:

```bash
source venv/bin/activate
```

Activar en Windows (CMD):

```cmd
venv\Scripts\activate.bat
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Importar la base de datos

```bash
mariadb -u TU_USUARIO -p < database/agenda_psico_ute.sql
```

La instalación del script original está pendiente
de una prueba de restauración completa.

### 5. Configurar la conexión

Crear o configurar el archivo config.py con los
datos locales de MariaDB y la clave secreta de Flask.

Ejemplo de configuración:

```python
from secrets import token_hex

DB_CONFIG = {
    "host": "localhost",
    "user": "TU_USUARIO",
    "password": "TU_CONTRASENA",
    "database": "agenda_psico_ute"
}

SECRET_KEY = token_hex(32)
```

No subir credenciales reales a GitHub.

### 6. Ejecutar el sistema

```bash
python app.py
```

Abrir en el navegador:

http://127.0.0.1:5000

El servidor se ejecuta en modo de desarrollo local.

Para iniciar sesión se requiere una cuenta registrada
con su contraseña almacenada mediante hash.

## Estructura del proyecto

```text
Agenda_Psico_UTE/
├── controllers/
├── database/
├── models/
├── sistema-psicologia/
│   └── docs/
├── static/
│   ├── css/
│   ├── img/
│   └── js/
├── templates/
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

## Documentación técnica

- [Diagrama de clases UML](sistema-psicologia/docs/clases.md)
- [Diagrama de flujo](sistema-psicologia/docs/clases_y_flujos.md)
- [Casos de uso](sistema-psicologia/docs/casos_de_uso.md)
- [Diagrama de integración](sistema-psicologia/docs/diagrama_integracion.md)
- [Diagrama de secuencia](sistema-psicologia/docs/secuencia_login.md)
- [POO y excepciones](sistema-psicologia/docs/poo_y_excepciones.md)
- [Casos de prueba](sistema-psicologia/docs/casos_de_prueba.md)
- [Evidencias SQL](sistema-psicologia/docs/evidencias_sql.md)
- [Memoria de evidencias](sistema-psicologia/docs/memoria_evidencias.md)

## Base de datos de pruebas

Se cuenta con una base de datos independiente que
contiene 120 registros ficticios para demostrar
las operaciones SQL solicitadas en la materia
de Base de Datos.

- [Respaldo SQL](database/agenda_psico_ute_pruebas.sql)
- [Ejercicios SQL](database/ejercicios_sql.sql)

Esta base no debe utilizarse para almacenar
información real de los alumnos.

## Proyecto académico

Proyecto Integrador I
Ingeniería en Tecnologías de la Información
e Innovación Digital - UTE, 2026.