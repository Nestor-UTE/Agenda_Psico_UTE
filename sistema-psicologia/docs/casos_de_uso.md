# Diagrama de Casos de Uso

```mermaid
graph TD
    Tutor((Tutor))
    Psicologa((Psicologa))

    subgraph Sistema de Agenda Psicologica UTE
        UC1[Iniciar Sesion / Autenticarse]
        UC2[Consultar Resumen de Grupos y Alumnos]
        UC3[Solicitar Cita para Alumno]
        UC4[Consultar Solicitudes de Citas Pendientes]
        UC5[Gestionar Agenda de Citas Proximas]
        UC6[Consultar Historial de Citas Cerradas]
        UC7[Registrar Seguimiento y Recomendaciones]
        UC8[Registrar y Administrar Alumnos]
    end

    Tutor --> UC1
    Tutor --> UC2
    Tutor --> UC3

    Psicologa --> UC1
    Psicologa --> UC4
    Psicologa --> UC5
    Psicologa --> UC6
    Psicologa --> UC7
    Psicologa --> UC8