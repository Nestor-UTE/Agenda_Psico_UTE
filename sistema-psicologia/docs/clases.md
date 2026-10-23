# Diagrama de Clases UML

# Diagrama de Clases UML

```mermaid
classDiagram
    class Alumnos {
        +String matricula
        +String nombre
        +String a_paterno
        +String a_materno
        +int grado
        +String grupo
        +String carrera
        +int id_tutor
        +guardar()
        +obtener_todos()$
    }

    class Cita {
        +int id_cita
        +String num_folio
        +DateTime fecha
        +String estatus
        +String motivo
        +String matricula_alumno
        +int id_tutor
        +int id_psicologa
        +guardar()
        +obtener_todos()$+obtener_agenda()$
        +obtener_historial()$+obtener_solicitudes()$
    }

    class Psicologa {
        +int id_psicologa
        +String nombre
        +String usuario
        +String contrasena
        +nueva(nombre, usuario, contrasena_plana)$
        +verificar_contrasena(contrasena_plana)
        +guardar()
        +buscar_por_usuario(usuario)$+obtener_todos()$
    }

    class Tutor {
        +int id_tutor
        +String nombre
        +String telefono
        +String correo
        +String contrasena
        +nuevo(nombre, telefono, correo, contrasena_plana)$
        +verificar_contrasena(contrasena_plana)
        +guardar()
        +buscar_por_correo(correo)$
        +obtener_todos()$+obtener_resumen()$
    }

    class Seguimiento {
        +int id_cita
        +String recomendacion
        +String resumen
        +guardar()
        +obtener_todos()$
    }

    Alumnos "1" -- "*" Cita : solicita
    Tutor "1" -- "*" Alumnos : supervisa
    Psicologa "1" -- "*" Cita : atiende
    Cita "1" -- "0..1" Seguimiento : genera