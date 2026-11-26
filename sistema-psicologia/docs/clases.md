# Diagrama de clases UML - Agenda Psico UTE

El siguiente diagrama representa las clases, atributos, métodos y relaciones implementados en los modelos de Python del sistema.

```mermaid
classDiagram
    direction TB

    class Alumnos {
        +matricula
        +nombre
        +a_paterno
        +a_materno
        +grado
        +grupo
        +carrera
        +id_tutor
        +guardar()
        +obtener_todos()
        +obtener_lista()
        +obtener_estado_por_tutor(id_tutor)
        +obtener_por_matricula_y_tutor(matricula, id_tutor)
        +obtener_por_tutor(id_tutor)
    }

    class Cita {
        +id_cita
        +num_folio
        +fecha
        +estatus
        +motivo
        +matricula_alumno
        +id_tutor
        +id_psicologa
        +guardar()
        +obtener_todos()
        +obtener_agenda()
        +obtener_agenda_por_tutor(id_tutor)
        +contar_solicitudes_por_tutor(id_tutor)
        +obtener_historial()
        +obtener_solicitudes()
        +agendar(id_cita, fecha)
        +reprogramar(id_cita, nueva_fecha)
        +agendar_directamente(datos_alumno, fecha, motivo, id_psicologa)
        +rechazar(id_cita)
        +solicitar(id_tutor, motivo, alumno)
        +obtener_por_folio(folio)
        +marcar_realizada(id_cita, resumen, recomendacion)
        +obtener_seguimientos()
        +actualizar_mas_sesiones(id_cita, respuesta)
        +agendar_otra_cita(id_cita_anterior, fecha)
    }

    class Psicologa {
        +id_psicologa
        +nombre
        +usuario
        +contrasena
        +nueva(nombre, usuario, contrasena_plana)
        +verificar_contrasena(contrasena_plana)
        +guardar()
        +buscar_por_usuario(usuario)
        +obtener_todos()
    }

    class Tutor {
        +id_tutor
        +nombre
        +telefono
        +correo
        +contrasena
        +cuatrimestre
        +grupo
        +carrera
        +nuevo()
        +verificar_contrasena(contrasena_plana)
        +guardar()
        +desde_fila(fila)
        +buscar_por_correo(correo)
        +buscar_por_id(id_tutor)
        +actualizar()
        +eliminar_por_id(id_tutor)
        +obtener_todos()
        +obtener_resumen()
    }

    class Seguimiento {
        +id_cita
        +recomendacion
        +resumen
        +guardar()
        +obtener_todos()
        +obtener_por_tutor(id_tutor)
    }

    Tutor "0..1" -- "0..*" Alumnos : supervisa
    Alumnos "1" -- "0..*" Cita : recibe
    Tutor "0..1" -- "0..*" Cita : solicita
    Psicologa "0..1" -- "0..*" Cita : atiende
    Cita "1" -- "0..1" Seguimiento : genera

    style Alumnos fill:#367f7c,color:#fff
    style Tutor fill:#367f7c,color:#fff
    style Psicologa fill:#367f7c,color:#fff
    style Cita fill:#367f7c,color:#fff
    style Seguimiento fill:#367f7c,color:#fff
```

## Descripción de las clases

- **Alumnos:** administra el registro y la consulta de los estudiantes.
- **Tutor:** administra los tutores, sus datos y su autenticación.
- **Psicologa:** administra la autenticación y los datos de la psicóloga.
- **Cita:** controla las solicitudes, el agendamiento, la reprogramación, los folios y los cambios de estado.
- **Seguimiento:** administra los resúmenes y las recomendaciones de las sesiones.

## Consideraciones

- Las contraseñas se almacenan mediante hash.
- El teléfono del tutor es opcional.
- Un alumno puede estar registrado sin tener un tutor asignado.
- La ubicación se administra desde la base de datos y no cuenta con una clase independiente en Python.