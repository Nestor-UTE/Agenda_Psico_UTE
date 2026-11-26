# Diagrama de integración - Agenda Psico UTE

Este diagrama muestra cómo se comunican los usuarios, la interfaz web, el backend y la base de datos del sistema.

```mermaid
flowchart TD
    T[Tutor]
    P[Psicóloga]
    A[Alumno]

    T --> F
    P --> F
    A --> F

    subgraph Frontend
        F["Interfaz web<br/>HTML, CSS y JavaScript"]
    end

    subgraph Backend
        B[Python y Flask - app.py]
        S[Autenticación y sesiones]
        M[Modelos de clases]
        C[Manejo de excepciones]

        B <--> S
        B <--> M
        M --> C
    end

    subgraph Base_de_datos
        D[(MariaDB)]
    end

    F <-->|Peticiones HTTP y respuestas| B
    M <-->|Consultas SQL| D

    style F fill:#367f7c,color:#fff
    style B fill:#367f7c,color:#fff
    style D fill:#367f7c,color:#fff
```

## Funcionamiento de la integración

- Frontend: muestra las pantallas y recibe las acciones de los usuarios.
- Backend: procesa las solicitudes, valida los datos y controla los permisos.
- Modelos: organizan la lógica del sistema mediante programación orientada a objetos.
- Base de datos: almacena alumnos, tutores, psicólogas, citas, seguimientos y ubicaciones.
- Manejo de excepciones: permite controlar errores durante las operaciones del sistema.