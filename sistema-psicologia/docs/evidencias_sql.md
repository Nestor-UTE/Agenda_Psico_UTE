# Evidencias de Base de Datos - Agenda Psico UTE

**Tarea:** T24
**Fecha:** 25/11/2026
**Motor:** MariaDB 13.0.2

## 1. Base de datos de pruebas

Se creó la base agenda_psico_ute_pruebas para
realizar los ejercicios académicos con datos
ficticios, sin modificar la base del sistema.

## 2. Estructura y registros

| Tabla | Tipos de datos | Registros |
|---|---:|---:|
| Tutor | 4 | 20 |
| Alumnos | 4 | 20 |
| Psicologa | 4 | 20 |
| Cita | 4 | 20 |
| Seguimiento | 4 | 20 |
| Ubicacion | 4 | 20 |
| Total | | 120 |

## 3. Restricciones implementadas

- PRIMARY KEY
- FOREIGN KEY
- NOT NULL
- UNIQUE
- DEFAULT
- CHECK

## 4. Resultados de las operaciones

| Operación | Resultado |
|---|---|
| ALTER TABLE | Estructura final comprobada |
| UPDATE relacional | 5 tutores actualizados |
| UPDATE lógico | 5 alumnos actualizados |
| DELETE relacional | 2 registros eliminados |
| DELETE lógico | 2 registros eliminados |
| ROLLBACK | 20 seguimientos recuperados en total |
| WHERE y AND | 20 registros encontrados |
| LIKE | 20 tutores encontrados |
| BETWEEN | 10 citas encontradas |
| INNER JOIN | 20 alumnos relacionados con tutores |
| GROUP BY y COUNT | 20 citas realizadas |
| AVG, MAX y MIN | 45 minutos |
| Respaldo SQL | Exportado correctamente |

## 5. Archivos de evidencia

- database/agenda_psico_ute_pruebas.sql
- database/ejercicios_sql.sql

## 6. Conclusión

Se comprobó el funcionamiento de las operaciones
SQL utilizando datos ficticios. Las pruebas
permitieron verificar las relaciones, los tipos
de datos y las consultas de la base de datos.

Los cambios se realizaron únicamente en la base
de pruebas para no afectar el sistema original.

Queda pendiente comprobar la restauración del
respaldo y grabar el video explicativo.