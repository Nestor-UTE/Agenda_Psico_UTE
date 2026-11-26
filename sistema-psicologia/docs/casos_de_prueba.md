# Casos de Prueba del Sistema - Agenda_Psico_UTE

A continuacion se detallan los casos de prueba funcionales y de seguridad para validar el correcto funcionamiento del sistema de gestion de citas psicologicas.

| ID | Modulo / Funcionalidad | Descripcion de la Prueba (Escenario) | Datos de Entrada / Accion | Resultado Esperado | Estatus |
|---|---|---|---|---|---|
| **CP-01** | Autenticacion | Inicio de sesion exitoso de Psicologa. | Usuario y contrasena validos de una psicologa registrada. | El sistema valida las credenciales mediante hash, inicia la sesion y redirige al panel principal de la psicologa. | Aprobado |
| **CP-02** | Autenticacion | Inicio de sesion fallido por contrasena incorrecta (Psicologa). | Usuario valido de psicologa con contrasena erronea. | El sistema rechaza el acceso, muestra un mensaje de error de credenciales y mantiene la vista de login. | Aprobado |
| **CP-03** | Autenticacion | Inicio de sesion exitoso de Tutor. | Correo y contrasena validos de un tutor registrado. | El sistema verifica el hash con `werkzeug.security`, autentica al usuario y redirige a su panel de gestion. | Aprobado |
| **CP-04** | Autenticacion | Inicio de sesion fallido por contrasena incorrecta (Tutor). | Correo valido de tutor con contrasena erronea. | El sistema deniega el acceso y muestra una alerta de error en pantalla. | Aprobado |
| **CP-05** | Seguridad | Control de acceso sin sesion (Ruta protegida). | Intentar acceder directamente a rutas del panel (ej. `/agenda`) escribiendo la URL sin iniciar sesion. | El sistema intercepta la peticion, detecta la ausencia de sesion activa y redirige al formulario de login. | Aprobado |
| **CP-06** | Solicitar cita | Registro exitoso de un nuevo alumno. | Llenado del formulario con matricula, nombre, a_paterno, a_materno, grado, grupo, carrera e id_tutor. | Se ejecuta la consulta parametrizada (`%s`), se realiza el `commit` y el alumno se almacena correctamente en la BD. | Aprobado |
| **CP-07** | Citas | Solicitud de nueva cita por parte del tutor. | Seleccion de alumno, motivo de consulta y envio del formulario de solicitud. | La cita se registra con estatus `'Solicitada'` y queda disponible para revision en el panel de la psicologa. | Aprobado |
| **CP-08** | Citas | Consulta de agenda de citas proximas (Psicologa). | Acceso a la seccion de agenda de la psicologa. | Se ejecuta la consulta con `LEFT JOIN` y `ORDER BY c.fecha ASC`, mostrando las citas agendadas ordenadas de la mas proxima a la mas lejana. | Aprobado |
| **CP-09** | Citas | Consulta de historial de citas cerradas. | Ingreso al historial de atenciones de la psicóloga. | El sistema despliega las citas con estatus `'Realizada'`, `'Reprogramada'` o `'Rechazada'`, ordenadas de forma descendente por fecha. | Aprobado |
| **CP-10** | Seguimiento | Registro de recomendaciones y diagnostico post-sesion. | Guardar el resumen y recomendaciones clinicas asociadas al `id_cita`. | Se ejecuta el `INSERT` en la tabla `seguimiento`, confirmando la transaccion con `commit` y asociandose a la cita correspondiente. | Aprobado |
| **CP-11** | Citas | Agendar una solicitud | Seleccionar fecha y hora de una cita solicitada. | La cita cambia a Agendada y aparece en la Agenda. | Aprobado |
| **CP-12** | Citas | Rechazar una solicitud | Presionar Rechazar en una solicitud. | La cita cambia a Rechazada y aparece en el Historial. | Aprobado |
| **CP-13** | Citas | Reprogramar una cita | Seleccionar una nueva fecha y hora. | La cita se actualiza correctamente en la BD. | Aprobado |
| **CP-14** | Citas | Marcar cita como realizada | Guardar resumen y recomendación de una cita agendada. | La cita cambia a Realizada y aparece en el Historial. | Aprobado |
| **CP-15** | Alumno | Consulta mediante folio válido | Ingresar un folio existente. | Se muestra la información básica de la cita. | Aprobado |
| **CP-16** | Alumno | Consulta mediante folio incorrecto | Ingresar un folio inexistente. | El sistema muestra un mensaje de error. | Por verificar |
| **CP-17** | Seguimiento | Consultar recomendaciones | Ingresar al seguimiento desde el panel del tutor. | Se muestran las recomendaciones sin revelar el resumen interno. | Aprobado |
| **CP-18** | Citas | Agendamiento directo | Registrar una cita desde el panel de Psicología. | Se guarda la cita y se genera un folio único. | Aprobado |
| **CP-19** | Citas | Validación de horario ocupado | Intentar agendar directamente dos citas a la misma hora. | El sistema impide duplicar el horario. | Aprobado |
| **CP-20** | Alumnos | Actualizar alumno existente | Agendar una cita con una matrícula registrada. | Se actualizan sus datos sin duplicar al alumno ni cambiar su tutor. | Aprobado |
| **CP-21** | Filtros | Filtrar registros | Seleccionar filtros de búsqueda disponibles. | Se muestran únicamente los registros que coinciden. | Aprobado |
| **CP-22** | Calendario | Navegación semanal | Cambiar de semana y seleccionar un día. | Se muestran las citas correspondientes. | Por verificar |
| **CP-23** | Seguridad | Separación de información entre tutores | Iniciar sesión con dos cuentas de tutor diferentes. | Cada tutor consulta únicamente sus propios alumnos. | Aprobado |
| **CP-24** | Seguimiento | Agendar otra cita | Indicar que un alumno requiere otra sesión y asignarle fecha y hora. | Se registra una nueva cita asociada al alumno. | Aprobado |
| **CP-25** | Citas | Horario ocupado desde Solicitudes | Intentar agendar una solicitud en un horario ocupado. | El sistema impide duplicar el horario. | Pendiente de corrección |