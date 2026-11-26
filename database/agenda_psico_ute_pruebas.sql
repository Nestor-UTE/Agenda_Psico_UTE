/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.20-13.0.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: agenda_psico_ute_pruebas
-- ------------------------------------------------------
-- Server version	13.0.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Current Database: `agenda_psico_ute_pruebas`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `agenda_psico_ute_pruebas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `agenda_psico_ute_pruebas`;

--
-- Table structure for table `alumnos`
--

DROP TABLE IF EXISTS `alumnos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `alumnos` (
  `matricula` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `a_paterno` varchar(45) NOT NULL,
  `a_materno` varchar(45) NOT NULL,
  `grado` int(11) DEFAULT NULL,
  `grupo` varchar(45) DEFAULT NULL,
  `carrera` varchar(100) DEFAULT NULL,
  `id_tutor` int(11) DEFAULT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  PRIMARY KEY (`matricula`),
  KEY `id_tutor_idx` (`id_tutor`),
  CONSTRAINT `fk_alumnos_tutor` FOREIGN KEY (`id_tutor`) REFERENCES `tutor` (`id_tutor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumnos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `alumnos` WRITE;
/*!40000 ALTER TABLE `alumnos` DISABLE KEYS */;
INSERT INTO `alumnos` VALUES
(260001,'Alumno 1','Prueba','Ejemplo',3,'A','TIID',1,'2026-11-25','Registro ficticio'),
(260002,'Alumno 2','Prueba','Ejemplo',3,'A','TIID',2,'2026-11-25','Registro ficticio'),
(260003,'Alumno 3','Prueba','Ejemplo',3,'A','TIID',3,'2026-11-25','Registro ficticio'),
(260004,'Alumno 4','Prueba','Ejemplo',3,'A','TIID',4,'2026-11-25','Registro ficticio'),
(260005,'Alumno 5','Prueba','Ejemplo',3,'A','TIID',5,'2026-11-25','Registro ficticio'),
(260006,'Alumno 6','Prueba','Ejemplo',3,'A','TIID',6,'2026-11-25','Registro ficticio'),
(260007,'Alumno 7','Prueba','Ejemplo',3,'A','TIID',7,'2026-11-25','Registro ficticio'),
(260008,'Alumno 8','Prueba','Ejemplo',3,'A','TIID',8,'2026-11-25','Registro ficticio'),
(260009,'Alumno 9','Prueba','Ejemplo',3,'A','TIID',9,'2026-11-25','Registro ficticio'),
(260010,'Alumno 10','Prueba','Ejemplo',3,'A','TIID',10,'2026-11-25','Registro ficticio'),
(260011,'Alumno 11','Prueba','Ejemplo',3,'A','TIID',11,'2026-11-25','Registro ficticio'),
(260012,'Alumno 12','Prueba','Ejemplo',3,'A','TIID',12,'2026-11-25','Registro ficticio'),
(260013,'Alumno 13','Prueba','Ejemplo',3,'A','TIID',13,'2026-11-25','Registro ficticio'),
(260014,'Alumno 14','Prueba','Ejemplo',3,'A','TIID',14,'2026-11-25','Registro ficticio'),
(260015,'Alumno 15','Prueba','Ejemplo',3,'A','TIID',15,'2026-11-25','Registro ficticio'),
(260016,'Alumno 16','Prueba','Ejemplo',3,'A','TIID',16,'2026-11-25','Registro ficticio'),
(260017,'Alumno 17','Prueba','Ejemplo',3,'A','TIID',17,'2026-11-25','Registro ficticio'),
(260018,'Alumno 18','Prueba','Ejemplo',3,'A','TIID',18,'2026-11-25','Registro ficticio'),
(260019,'Alumno 19','Prueba','Ejemplo',3,'A','TIID',19,'2026-11-25','Registro ficticio'),
(260020,'Alumno 20','Prueba','Ejemplo',3,'A','TIID',20,'2026-11-25','Registro ficticio');
/*!40000 ALTER TABLE `alumnos` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `cita`
--

DROP TABLE IF EXISTS `cita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cita` (
  `id_cita` int(11) NOT NULL AUTO_INCREMENT,
  `num_folio` varchar(45) NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `estatus` varchar(45) NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `matricula_alumno` int(11) DEFAULT NULL,
  `id_tutor` int(11) DEFAULT NULL,
  `id_psicologa` int(11) DEFAULT NULL,
  `id_ubicacion` int(11) NOT NULL DEFAULT 1,
  `duracion_minutos` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id_cita`),
  UNIQUE KEY `uq_cita_folio` (`num_folio`),
  KEY `id_tutor_idx` (`id_tutor`),
  KEY `id_psicologa_idx` (`id_psicologa`),
  KEY `matricula_alumno_idx` (`matricula_alumno`),
  KEY `fk_cita_ubicacion` (`id_ubicacion`),
  CONSTRAINT `fk_cita_alumno` FOREIGN KEY (`matricula_alumno`) REFERENCES `alumnos` (`matricula`),
  CONSTRAINT `fk_cita_psicologa` FOREIGN KEY (`id_psicologa`) REFERENCES `psicologa` (`id_psicologa`),
  CONSTRAINT `fk_cita_tutor` FOREIGN KEY (`id_tutor`) REFERENCES `tutor` (`id_tutor`),
  CONSTRAINT `fk_cita_ubicacion` FOREIGN KEY (`id_ubicacion`) REFERENCES `ubicacion` (`id_ubicacion`),
  CONSTRAINT `chk_cita_duracion` CHECK (`duracion_minutos` > 0),
  CONSTRAINT `chk_cita_estatus` CHECK (`estatus` in ('Solicitada','Agendada','Realizada','Reprogramada','Rechazada'))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cita`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `cita` WRITE;
/*!40000 ALTER TABLE `cita` DISABLE KEYS */;
INSERT INTO `cita` VALUES
(1,'PRUEBA-0001','2026-10-02 09:00:00','Realizada','Motivo de prueba',260001,1,1,1,45),
(2,'PRUEBA-0002','2026-10-03 09:00:00','Realizada','Motivo de prueba',260002,2,2,2,45),
(3,'PRUEBA-0003','2026-10-04 09:00:00','Realizada','Motivo de prueba',260003,3,3,3,45),
(4,'PRUEBA-0004','2026-10-05 09:00:00','Realizada','Motivo de prueba',260004,4,4,4,45),
(5,'PRUEBA-0005','2026-10-06 09:00:00','Realizada','Motivo de prueba',260005,5,5,5,45),
(6,'PRUEBA-0006','2026-10-07 09:00:00','Realizada','Motivo de prueba',260006,6,6,6,45),
(7,'PRUEBA-0007','2026-10-08 09:00:00','Realizada','Motivo de prueba',260007,7,7,7,45),
(8,'PRUEBA-0008','2026-10-09 09:00:00','Realizada','Motivo de prueba',260008,8,8,8,45),
(9,'PRUEBA-0009','2026-10-10 09:00:00','Realizada','Motivo de prueba',260009,9,9,9,45),
(10,'PRUEBA-0010','2026-10-11 09:00:00','Realizada','Motivo de prueba',260010,10,10,10,45),
(11,'PRUEBA-0011','2026-10-12 09:00:00','Realizada','Motivo de prueba',260011,11,11,11,45),
(12,'PRUEBA-0012','2026-10-13 09:00:00','Realizada','Motivo de prueba',260012,12,12,12,45),
(13,'PRUEBA-0013','2026-10-14 09:00:00','Realizada','Motivo de prueba',260013,13,13,13,45),
(14,'PRUEBA-0014','2026-10-15 09:00:00','Realizada','Motivo de prueba',260014,14,14,14,45),
(15,'PRUEBA-0015','2026-10-16 09:00:00','Realizada','Motivo de prueba',260015,15,15,15,45),
(16,'PRUEBA-0016','2026-10-17 09:00:00','Realizada','Motivo de prueba',260016,16,16,16,45),
(17,'PRUEBA-0017','2026-10-18 09:00:00','Realizada','Motivo de prueba',260017,17,17,17,45),
(18,'PRUEBA-0018','2026-10-19 09:00:00','Realizada','Motivo de prueba',260018,18,18,18,45),
(19,'PRUEBA-0019','2026-10-20 09:00:00','Realizada','Motivo de prueba',260019,19,19,19,45),
(20,'PRUEBA-0020','2026-10-21 09:00:00','Realizada','Motivo de prueba',260020,20,20,20,45);
/*!40000 ALTER TABLE `cita` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `psicologa`
--

DROP TABLE IF EXISTS `psicologa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `psicologa` (
  `id_psicologa` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `usuario` varchar(45) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `fecha_alta` date DEFAULT NULL,
  `activo` enum('Sí','No') DEFAULT 'Sí',
  PRIMARY KEY (`id_psicologa`),
  UNIQUE KEY `uq_psicologa_usuario` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `psicologa`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `psicologa` WRITE;
/*!40000 ALTER TABLE `psicologa` DISABLE KEYS */;
INSERT INTO `psicologa` VALUES
(1,'Psicologa Prueba 1','psicologa1','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(2,'Psicologa Prueba 2','psicologa2','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(3,'Psicologa Prueba 3','psicologa3','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(4,'Psicologa Prueba 4','psicologa4','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(5,'Psicologa Prueba 5','psicologa5','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(6,'Psicologa Prueba 6','psicologa6','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(7,'Psicologa Prueba 7','psicologa7','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(8,'Psicologa Prueba 8','psicologa8','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(9,'Psicologa Prueba 9','psicologa9','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(10,'Psicologa Prueba 10','psicologa10','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(11,'Psicologa Prueba 11','psicologa11','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(12,'Psicologa Prueba 12','psicologa12','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(13,'Psicologa Prueba 13','psicologa13','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(14,'Psicologa Prueba 14','psicologa14','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(15,'Psicologa Prueba 15','psicologa15','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(16,'Psicologa Prueba 16','psicologa16','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(17,'Psicologa Prueba 17','psicologa17','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(18,'Psicologa Prueba 18','psicologa18','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(19,'Psicologa Prueba 19','psicologa19','NO_LOGIN_PRUEBA','2026-11-25','Sí'),
(20,'Psicologa Prueba 20','psicologa20','NO_LOGIN_PRUEBA','2026-11-25','Sí');
/*!40000 ALTER TABLE `psicologa` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `seguimiento`
--

DROP TABLE IF EXISTS `seguimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguimiento` (
  `id_cita` int(11) NOT NULL,
  `recomendacion` mediumtext DEFAULT NULL,
  `resumen` mediumtext DEFAULT NULL,
  `requiere_mas_sesiones` enum('Por definir','Sí','No') NOT NULL DEFAULT 'Por definir',
  `fecha_registro` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_cita`),
  KEY `id_cita_idx` (`id_cita`),
  CONSTRAINT `fk_seguimiento_cita` FOREIGN KEY (`id_cita`) REFERENCES `cita` (`id_cita`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seguimiento`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `seguimiento` WRITE;
/*!40000 ALTER TABLE `seguimiento` DISABLE KEYS */;
INSERT INTO `seguimiento` VALUES
(1,'Recomendacion ficticia 1','Resumen ficticio 1','No','2026-11-25 18:42:29'),
(2,'Recomendacion ficticia 2','Resumen ficticio 2','No','2026-11-25 18:42:29'),
(3,'Recomendacion ficticia 3','Resumen ficticio 3','No','2026-11-25 18:42:29'),
(4,'Recomendacion ficticia 4','Resumen ficticio 4','No','2026-11-25 18:42:29'),
(5,'Recomendacion ficticia 5','Resumen ficticio 5','No','2026-11-25 18:42:29'),
(6,'Recomendacion ficticia 6','Resumen ficticio 6','No','2026-11-25 18:42:29'),
(7,'Recomendacion ficticia 7','Resumen ficticio 7','No','2026-11-25 18:42:29'),
(8,'Recomendacion ficticia 8','Resumen ficticio 8','No','2026-11-25 18:42:29'),
(9,'Recomendacion ficticia 9','Resumen ficticio 9','No','2026-11-25 18:42:29'),
(10,'Recomendacion ficticia 10','Resumen ficticio 10','No','2026-11-25 18:42:29'),
(11,'Recomendacion ficticia 11','Resumen ficticio 11','No','2026-11-25 18:42:29'),
(12,'Recomendacion ficticia 12','Resumen ficticio 12','No','2026-11-25 18:42:29'),
(13,'Recomendacion ficticia 13','Resumen ficticio 13','No','2026-11-25 18:42:29'),
(14,'Recomendacion ficticia 14','Resumen ficticio 14','No','2026-11-25 18:42:29'),
(15,'Recomendacion ficticia 15','Resumen ficticio 15','No','2026-11-25 18:42:29'),
(16,'Recomendacion ficticia 16','Resumen ficticio 16','No','2026-11-25 18:42:29'),
(17,'Recomendacion ficticia 17','Resumen ficticio 17','No','2026-11-25 18:42:29'),
(18,'Recomendacion ficticia 18','Resumen ficticio 18','No','2026-11-25 18:42:29'),
(19,'Recomendacion ficticia 19','Resumen ficticio 19','No','2026-11-25 18:42:29'),
(20,'Recomendacion ficticia 20','Resumen ficticio 20','No','2026-11-25 18:42:29');
/*!40000 ALTER TABLE `seguimiento` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `tutor`
--

DROP TABLE IF EXISTS `tutor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tutor` (
  `id_tutor` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `correo` varchar(45) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `cuatrimestre` int(11) DEFAULT NULL,
  `grupo` varchar(10) DEFAULT NULL,
  `carrera` varchar(100) DEFAULT NULL,
  `fecha_alta` date DEFAULT NULL,
  `activo` enum('Sí','No') DEFAULT 'Sí',
  `observaciones` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_tutor`),
  UNIQUE KEY `uq_tutor_correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tutor`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `tutor` WRITE;
/*!40000 ALTER TABLE `tutor` DISABLE KEYS */;
INSERT INTO `tutor` VALUES
(1,'Tutor Prueba 1',NULL,'tutor1@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(2,'Tutor Prueba 2',NULL,'tutor2@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(3,'Tutor Prueba 3',NULL,'tutor3@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(4,'Tutor Prueba 4',NULL,'tutor4@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(5,'Tutor Prueba 5',NULL,'tutor5@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(6,'Tutor Prueba 6',NULL,'tutor6@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(7,'Tutor Prueba 7',NULL,'tutor7@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(8,'Tutor Prueba 8',NULL,'tutor8@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(9,'Tutor Prueba 9',NULL,'tutor9@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(10,'Tutor Prueba 10',NULL,'tutor10@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(11,'Tutor Prueba 11',NULL,'tutor11@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(12,'Tutor Prueba 12',NULL,'tutor12@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(13,'Tutor Prueba 13',NULL,'tutor13@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(14,'Tutor Prueba 14',NULL,'tutor14@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(15,'Tutor Prueba 15',NULL,'tutor15@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(16,'Tutor Prueba 16',NULL,'tutor16@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(17,'Tutor Prueba 17',NULL,'tutor17@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(18,'Tutor Prueba 18',NULL,'tutor18@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(19,'Tutor Prueba 19',NULL,'tutor19@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL),
(20,'Tutor Prueba 20',NULL,'tutor20@example.com','NO_LOGIN_PRUEBA',3,'A','TIID','2026-11-25','Sí',NULL);
/*!40000 ALTER TABLE `tutor` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `ubicacion`
--

DROP TABLE IF EXISTS `ubicacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ubicacion` (
  `id_ubicacion` int(11) NOT NULL AUTO_INCREMENT,
  `edificio` varchar(10) NOT NULL,
  `docencia` varchar(100) NOT NULL,
  `salon` varchar(10) NOT NULL,
  `referencia` varchar(150) DEFAULT NULL,
  `fecha_revision` date DEFAULT NULL,
  `accesibilidad` enum('Por verificar','Sí','No') DEFAULT 'Por verificar',
  PRIMARY KEY (`id_ubicacion`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ubicacion`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `ubicacion` WRITE;
/*!40000 ALTER TABLE `ubicacion` DISABLE KEYS */;
INSERT INTO `ubicacion` VALUES
(1,'D1','Edificio de prueba','101','Ubicacion ficticia','2026-11-25','Por verificar'),
(2,'D2','Edificio de prueba','102','Ubicacion ficticia','2026-11-25','Por verificar'),
(3,'D3','Edificio de prueba','103','Ubicacion ficticia','2026-11-25','Por verificar'),
(4,'D4','Edificio de prueba','104','Ubicacion ficticia','2026-11-25','Por verificar'),
(5,'D5','Edificio de prueba','105','Ubicacion ficticia','2026-11-25','Por verificar'),
(6,'D6','Edificio de prueba','106','Ubicacion ficticia','2026-11-25','Por verificar'),
(7,'D7','Edificio de prueba','107','Ubicacion ficticia','2026-11-25','Por verificar'),
(8,'D8','Edificio de prueba','108','Ubicacion ficticia','2026-11-25','Por verificar'),
(9,'D9','Edificio de prueba','109','Ubicacion ficticia','2026-11-25','Por verificar'),
(10,'D10','Edificio de prueba','110','Ubicacion ficticia','2026-11-25','Por verificar'),
(11,'D11','Edificio de prueba','111','Ubicacion ficticia','2026-11-25','Por verificar'),
(12,'D12','Edificio de prueba','112','Ubicacion ficticia','2026-11-25','Por verificar'),
(13,'D13','Edificio de prueba','113','Ubicacion ficticia','2026-11-25','Por verificar'),
(14,'D14','Edificio de prueba','114','Ubicacion ficticia','2026-11-25','Por verificar'),
(15,'D15','Edificio de prueba','115','Ubicacion ficticia','2026-11-25','Por verificar'),
(16,'D16','Edificio de prueba','116','Ubicacion ficticia','2026-11-25','Por verificar'),
(17,'D17','Edificio de prueba','117','Ubicacion ficticia','2026-11-25','Por verificar'),
(18,'D18','Edificio de prueba','118','Ubicacion ficticia','2026-11-25','Por verificar'),
(19,'D19','Edificio de prueba','119','Ubicacion ficticia','2026-11-25','Por verificar'),
(20,'D20','Edificio de prueba','120','Ubicacion ficticia','2026-11-25','Por verificar');
/*!40000 ALTER TABLE `ubicacion` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-11-25 18:52:56
