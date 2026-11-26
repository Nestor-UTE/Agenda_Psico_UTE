-- Agenda Psico UTE
-- T24: Evidencias de Base de Datos
-- Ejercicios realizados con datos ficticios

USE agenda_psico_ute_pruebas;

-- ALTER: agregar, renombrar, eliminar y volver a agregar
ALTER TABLE tutor ADD COLUMN notas VARCHAR(100);
ALTER TABLE tutor RENAME COLUMN notas TO notas_prueba;
ALTER TABLE tutor DROP COLUMN notas_prueba;
ALTER TABLE tutor ADD COLUMN notas_prueba VARCHAR(100);

-- Limpiar atributo temporal
ALTER TABLE tutor DROP COLUMN notas_prueba;

START TRANSACTION;

-- UPDATE con operador relacional
UPDATE tutor
SET cuatrimestre = 4
WHERE id_tutor <= 5;

-- UPDATE con operador logico
UPDATE alumnos
SET grupo = 'B'
WHERE grado = 3 AND id_tutor <= 5;

-- DELETE con operador relacional
DELETE FROM seguimiento
WHERE id_cita > 18;

-- DELETE con operador logico
DELETE FROM seguimiento
WHERE id_cita = 17 OR id_cita = 18;

-- Verificar cambios
SELECT id_tutor, nombre, cuatrimestre FROM tutor;
SELECT matricula, nombre, grupo FROM alumnos;
SELECT COUNT(*) FROM seguimiento;

ROLLBACK;

-- Consultas SQL
SELECT nombre, carrera, grupo
FROM alumnos
WHERE grado = 3 AND grupo = 'A';

SELECT nombre, correo
FROM tutor
WHERE nombre LIKE 'Tutor%';

SELECT num_folio, fecha, estatus
FROM cita
WHERE id_cita BETWEEN 1 AND 10
ORDER BY fecha DESC;

SELECT a.nombre AS alumno, t.nombre AS tutor
FROM alumnos a
INNER JOIN tutor t ON a.id_tutor = t.id_tutor;

SELECT estatus, COUNT(*) AS total
FROM cita
GROUP BY estatus;

SELECT AVG(duracion_minutos) AS promedio,
       MAX(duracion_minutos) AS maxima,
       MIN(duracion_minutos) AS minima
FROM cita;

-- Verificar tipos de datos
SELECT TABLE_NAME AS tabla,
       COUNT(DISTINCT DATA_TYPE) AS cantidad,
       GROUP_CONCAT(DISTINCT DATA_TYPE) AS tipos
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'agenda_psico_ute_pruebas'
GROUP BY TABLE_NAME;

-- Verificar cantidad de registros
SELECT 'tutor' AS tabla, COUNT(*) AS registros FROM tutor
UNION ALL
SELECT 'alumnos', COUNT(*) FROM alumnos
UNION ALL
SELECT 'psicologa', COUNT(*) FROM psicologa
UNION ALL
SELECT 'cita', COUNT(*) FROM cita
UNION ALL
SELECT 'seguimiento', COUNT(*) FROM seguimiento
UNION ALL
SELECT 'ubicacion', COUNT(*) FROM ubicacion;