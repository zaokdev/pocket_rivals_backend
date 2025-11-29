-- MySQL dump 10.13  Distrib 8.4.2-2, for Linux (x86_64)
--
-- Host: localhost    Database: b7nuooaxciymxjhqxjor
-- ------------------------------------------------------
-- Server version	8.4.2-2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*!50717 SELECT COUNT(*) INTO @rocksdb_has_p_s_session_variables FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'performance_schema' AND TABLE_NAME = 'session_variables' */;
/*!50717 SET @rocksdb_get_is_supported = IF (@rocksdb_has_p_s_session_variables, 'SELECT COUNT(*) INTO @rocksdb_is_supported FROM performance_schema.session_variables WHERE VARIABLE_NAME=\'rocksdb_bulk_load\'', 'SELECT 0') */;
/*!50717 PREPARE s FROM @rocksdb_get_is_supported */;
/*!50717 EXECUTE s */;
/*!50717 DEALLOCATE PREPARE s */;
/*!50717 SET @rocksdb_enable_bulk_load = IF (@rocksdb_is_supported, 'SET SESSION rocksdb_bulk_load = 1', 'SET @rocksdb_dummy_bulk_load = 0') */;
/*!50717 PREPARE s FROM @rocksdb_enable_bulk_load */;
/*!50717 EXECUTE s */;
/*!50717 DEALLOCATE PREPARE s */;

--
-- Table structure for table `friend`
--

DROP TABLE IF EXISTS `friend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `friend` (
  `id1` varchar(32) NOT NULL,
  `id2` varchar(32) NOT NULL,
  `id_min` varchar(100) GENERATED ALWAYS AS (least(`id1`,`id2`)) STORED,
  `id_max` varchar(100) GENERATED ALWAYS AS (greatest(`id1`,`id2`)) STORED,
  `approved` tinyint(1) NOT NULL DEFAULT '0',
  `petitioner` varchar(100) NOT NULL,
  UNIQUE KEY `id_min` (`id_min`,`id_max`),
  KEY `id1` (`id1`),
  KEY `id2` (`id2`),
  KEY `petitioner` (`petitioner`),
  CONSTRAINT `friend_ibfk_1` FOREIGN KEY (`id1`) REFERENCES `player` (`id`),
  CONSTRAINT `friend_ibfk_2` FOREIGN KEY (`id2`) REFERENCES `player` (`id`),
  CONSTRAINT `friend_ibfk_3` FOREIGN KEY (`petitioner`) REFERENCES `player` (`id`),
  CONSTRAINT `friend_chk_1` CHECK ((`petitioner` in (`id1`,`id2`)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friend`
--

LOCK TABLES `friend` WRITE;
/*!40000 ALTER TABLE `friend` DISABLE KEYS */;
INSERT INTO `friend` (`id1`, `id2`, `approved`, `petitioner`) VALUES ('T1UT53mFIZXI2X6dinJtiE495Q2u5Um1','Xbh3InnXwqz9S7I0Hq7nt6xZZwOIyJUV',1,'T1UT53mFIZXI2X6dinJtiE495Q2u5Um1'),('T1UT53mFIZXI2X6dinJtiE495Q2u5Um1','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3',1,'T1UT53mFIZXI2X6dinJtiE495Q2u5Um1'),('Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3',1,'Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV'),('Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV','5YLEpbP18yoWucjDWNtTjDUKpi2ZXhkk',1,'Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV'),('5YLEpbP18yoWucjDWNtTjDUKpi2ZXhkk','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3',1,'5YLEpbP18yoWucjDWNtTjDUKpi2ZXhkk'),('Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ',1,'Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV'),('CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3',1,'CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ');
/*!40000 ALTER TABLE `friend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player`
--

DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player` (
  `id` varchar(32) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `last_opened` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player`
--

LOCK TABLES `player` WRITE;
/*!40000 ALTER TABLE `player` DISABLE KEYS */;
INSERT INTO `player` VALUES ('5YLEpbP18yoWucjDWNtTjDUKpi2ZXhkk','test123','test@mail.com','$2b$12$PcXZFk2pGOhDAJumwBrsse.MLFdVLdaG6Hr8cpgwyChUWFToEtX36',NULL),('CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ','kevin123','kevin2@mail.com','$2b$12$oQbQeaHJnCLN45aFAZydXuKrHnHtv10EYzsII4VW7Trm/4s9ltHDW',NULL),('iDsECthhhHTFlP5EbRirApzvwyEB8Voh','cokariz','cokarizzz@mail.com','$2b$12$JvbxGdeDUSsrFGEu3xKx6.yMRafuJsDcG0QpwnVXq78ilvkgbTCVG',NULL),('JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3','Ley73','francisco@mail.com','$2b$12$CHq1FlUdvdLLMviSQO84e.VSFDWFWqv7hkX./fkcpG/mcqY5clhmG',NULL),('POlYYgQUFLkqtfHoWWOEAjNPWTJ54WjX','panchofaller','fran@mail.com','$2b$12$rFac5ysaj2hEbMEpfRI2EeoCbR3pNeFb3jOxwFCD7gi0mn6RCvGDm',NULL),('T1UT53mFIZXI2X6dinJtiE495Q2u5Um1','kebizu','kebizu@mail.com','$2b$12$hKZ1jAecR8GiWy7zs5EN9OZKEA7j9PiH2yAjCRo8cC8ApsDZbH01O',NULL),('Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV','diex1000','diego@mail.com','$2b$12$HHY8eAgUHwX7ic8wryeCe.a3ebBjczWVhgmHI9cL7eZcmC8JuHkAC',NULL);
/*!40000 ALTER TABLE `player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pokeball_history`
--

DROP TABLE IF EXISTS `pokeball_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pokeball_history` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `awarded_pokemon_number` int NOT NULL,
  `opened_at` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pokeball_user` (`user_id`),
  KEY `fk_pokeball_pokemon` (`awarded_pokemon_number`),
  CONSTRAINT `fk_pokeball_pokemon` FOREIGN KEY (`awarded_pokemon_number`) REFERENCES `pokemon_stat` (`pokedex_number`),
  CONSTRAINT `fk_pokeball_user` FOREIGN KEY (`user_id`) REFERENCES `player` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pokeball_history`
--

LOCK TABLES `pokeball_history` WRITE;
/*!40000 ALTER TABLE `pokeball_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `pokeball_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pokemon_owned`
--

DROP TABLE IF EXISTS `pokemon_owned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pokemon_owned` (
  `id` varchar(24) NOT NULL,
  `player_id` varchar(32) NOT NULL,
  `pokedex_number` int NOT NULL,
  `in_team` tinyint(1) NOT NULL DEFAULT '0',
  `obtained_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `mote` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_player` (`player_id`),
  KEY `fk_pokemon` (`pokedex_number`),
  CONSTRAINT `fk_player` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_pokemon` FOREIGN KEY (`pokedex_number`) REFERENCES `pokemon_stat` (`pokedex_number`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pokemon_owned`
--

LOCK TABLES `pokemon_owned` WRITE;
/*!40000 ALTER TABLE `pokemon_owned` DISABLE KEYS */;
INSERT INTO `pokemon_owned` VALUES ('06e7IFREZaSjGWSV1cAZ7Z6Q','5YLEpbP18yoWucjDWNtTjDUKpi2ZXhkk',53,0,'2025-09-29',NULL),('6MeN4OAuiwJYFdhQtnSM1ZNj','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ',120,0,'2025-11-14',NULL),('7bibJu6NkWosKLcC15O2RmZg','T1UT53mFIZXI2X6dinJtiE495Q2u5Um1',4,0,'2025-09-27','fueguito'),('9FnULSmiWxiOFOFOZTTxrisL','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ',3,0,'2025-11-14',NULL),('behdwgHyf6pZJKjQ7Iqbx7zX','POlYYgQUFLkqtfHoWWOEAjNPWTJ54WjX',55,0,'2025-09-27',NULL),('CZEF0laEU9JSccZrEcWqaIz8','Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV',52,0,'2025-09-27',NULL),('eTtICDRmfIjToRAVMGT8khDI','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ',109,0,'2025-09-27',NULL),('i361gJhUEk3g7sJYV5Y4NRLS','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ',89,0,'2025-11-14',NULL),('IYYmXRN3l9l1StIAtszylgvl','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3',32,0,'2025-09-27','El macho'),('jbspMNuwaRwJJFBnLoBAIeFB','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ',18,0,'2025-09-27',NULL),('KNpqNFxTuBiaFVFLlkrlctl3','Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV',63,0,'2025-09-29','jutini'),('LqmrmJ4dQR3AbOG74iMGh5Qy','5YLEpbP18yoWucjDWNtTjDUKpi2ZXhkk',137,0,'2025-09-29',NULL),('nIb14VML0rVE2J11FnpMIvTM','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ',36,0,'2025-11-14',NULL),('NMwC1oDu8RDi8x3glmYpnVh0','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ',150,0,'2025-11-14',NULL),('P60SzQ1KpolVLDhUjTFlragZ','T1UT53mFIZXI2X6dinJtiE495Q2u5Um1',100,0,'2025-09-28',NULL),('rfWqJV73XqNpnEM2atI1M2HK','Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV',141,0,'2025-09-27',NULL),('tN9L1RxFvuyEs2IpqEL7Ac8i','Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV',95,0,'2025-09-27',NULL),('vfih3BH6ORZ6vDuFiszuV59i','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3',15,0,'2025-09-27',NULL),('wohgd1XlUX8KEn78zDNafgGT','POlYYgQUFLkqtfHoWWOEAjNPWTJ54WjX',26,0,'2025-09-27',NULL),('XCiGloYxNx4SktSGdCv4hsWR','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3',128,0,'2025-09-29',NULL),('XlxgYFDQbfYXOrKZO33Cszz4','Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV',3,0,'2025-09-27',NULL);
/*!40000 ALTER TABLE `pokemon_owned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pokemon_stat`
--

DROP TABLE IF EXISTS `pokemon_stat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pokemon_stat` (
  `pokedex_number` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `classification` varchar(50) DEFAULT NULL,
  `base_total` int DEFAULT NULL,
  `type1` varchar(20) NOT NULL,
  `type2` varchar(20) DEFAULT NULL,
  `generation` int DEFAULT NULL,
  `capture_rate` int DEFAULT NULL,
  `is_legendary` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`pokedex_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pokemon_stat`
--

LOCK TABLES `pokemon_stat` WRITE;
/*!40000 ALTER TABLE `pokemon_stat` DISABLE KEYS */;
INSERT INTO `pokemon_stat` VALUES (1,'Bulbasaur','Seed Pokemon',318,'grass','poison',1,45,0),(2,'Ivysaur','Seed Pokemon',405,'grass','poison',1,45,0),(3,'Venusaur','Seed Pokemon',625,'grass','poison',1,45,0),(4,'Charmander','Lizard Pokemon',309,'fire',NULL,1,45,0),(5,'Charmeleon','Flame Pokemon',405,'fire',NULL,1,45,0),(6,'Charizard','Flame Pokemon',634,'fire','flying',1,45,0),(7,'Squirtle','Tiny Turtle Pokemon',314,'water',NULL,1,45,0),(8,'Wartortle','Turtle Pokemon',405,'water',NULL,1,45,0),(9,'Blastoise','Shellfish Pokemon',630,'water',NULL,1,45,0),(10,'Caterpie','Worm Pokemon',195,'bug',NULL,1,255,0),(11,'Metapod','Cocoon Pokemon',205,'bug',NULL,1,120,0),(12,'Butterfree','Butterfly Pokemon',395,'bug','flying',1,45,0),(13,'Weedle','Hairy Pokemon',195,'bug','poison',1,255,0),(14,'Kakuna','Cocoon Pokemon',205,'bug','poison',1,120,0),(15,'Beedrill','Poison Bee Pokemon',495,'bug','poison',1,45,0),(16,'Pidgey','Tiny Bird Pokemon',251,'normal','flying',1,255,0),(17,'Pidgeotto','Bird Pokemon',349,'normal','flying',1,120,0),(18,'Pidgeot','Bird Pokemon',579,'normal','flying',1,45,0),(19,'Rattata','Mouse Pokemon',253,'normal','dark',1,255,0),(20,'Raticate','Mouse Pokemon',413,'normal','dark',1,127,0),(21,'Spearow','Tiny Bird Pokemon',262,'normal','flying',1,255,0),(22,'Fearow','Beak Pokemon',442,'normal','flying',1,90,0),(23,'Ekans','Snake Pokemon',288,'poison',NULL,1,255,0),(24,'Arbok','Cobra Pokemon',448,'poison',NULL,1,90,0),(25,'Pikachu','Mouse Pokemon',320,'electric',NULL,1,190,0),(26,'Raichu','Mouse Pokemon',485,'electric','electric',1,75,0),(27,'Sandshrew','Mouse Pokemon',300,'ground','ice',1,255,0),(28,'Sandslash','Mouse Pokemon',450,'ground','ice',1,90,0),(29,'Nidoran♀','Poison Pin Pokemon',275,'poison',NULL,1,235,0),(30,'Nidorina','Poison Pin Pokemon',365,'poison',NULL,1,120,0),(31,'Nidoqueen','Drill Pokemon',505,'poison','ground',1,45,0),(32,'Nidoran♂','Poison Pin Pokemon',273,'poison',NULL,1,235,0),(33,'Nidorino','Poison Pin Pokemon',365,'poison',NULL,1,120,0),(34,'Nidoking','Drill Pokemon',505,'poison','ground',1,45,0),(35,'Clefairy','Fairy Pokemon',323,'fairy',NULL,1,150,0),(36,'Clefable','Fairy Pokemon',483,'fairy',NULL,1,25,0),(37,'Vulpix','Fox Pokemon',299,'fire','ice',1,190,0),(38,'Ninetales','Fox Pokemon',505,'fire','ice',1,75,0),(39,'Jigglypuff','Balloon Pokemon',270,'normal','fairy',1,170,0),(40,'Wigglytuff','Balloon Pokemon',435,'normal','fairy',1,50,0),(41,'Zubat','Bat Pokemon',245,'poison','flying',1,255,0),(42,'Golbat','Bat Pokemon',455,'poison','flying',1,90,0),(43,'Oddish','Weed Pokemon',320,'grass','poison',1,255,0),(44,'Gloom','Weed Pokemon',395,'grass','poison',1,120,0),(45,'Vileplume','Flower Pokemon',490,'grass','poison',1,45,0),(46,'Paras','Mushroom Pokemon',285,'bug','grass',1,190,0),(47,'Parasect','Mushroom Pokemon',405,'bug','grass',1,75,0),(48,'Venonat','Insect Pokemon',305,'bug','poison',1,190,0),(49,'Venomoth','Poison Moth Pokemon',450,'bug','poison',1,75,0),(50,'Diglett','Mole Pokemon',265,'ground','ground',1,255,0),(51,'Dugtrio','Mole Pokemon',425,'ground','ground',1,50,0),(52,'Meowth','Scratch Cat Pokemon',290,'normal','dark',1,255,0),(53,'Persian','Classy Cat Pokemon',440,'normal','dark',1,90,0),(54,'Psyduck','Duck Pokemon',320,'water',NULL,1,190,0),(55,'Golduck','Duck Pokemon',500,'water',NULL,1,75,0),(56,'Mankey','Pig Monkey Pokemon',305,'fighting',NULL,1,190,0),(57,'Primeape','Pig Monkey Pokemon',455,'fighting',NULL,1,75,0),(58,'Growlithe','Puppy Pokemon',350,'fire',NULL,1,190,0),(59,'Arcanine','Legendary Pokemon',555,'fire',NULL,1,75,0),(60,'Poliwag','Tadpole Pokemon',300,'water',NULL,1,255,0),(61,'Poliwhirl','Tadpole Pokemon',385,'water',NULL,1,120,0),(62,'Poliwrath','Tadpole Pokemon',510,'water','fighting',1,45,0),(63,'Abra','Psi Pokemon',310,'psychic',NULL,1,200,0),(64,'Kadabra','Psi Pokemon',400,'psychic',NULL,1,100,0),(65,'Alakazam','Psi Pokemon',600,'psychic',NULL,1,50,0),(66,'Machop','Superpower Pokemon',305,'fighting',NULL,1,180,0),(67,'Machoke','Superpower Pokemon',405,'fighting',NULL,1,90,0),(68,'Machamp','Superpower Pokemon',505,'fighting',NULL,1,45,0),(69,'Bellsprout','Flower Pokemon',300,'grass','poison',1,255,0),(70,'Weepinbell','Flycatcher Pokemon',390,'grass','poison',1,120,0),(71,'Victreebel','Flycatcher Pokemon',490,'grass','poison',1,45,0),(72,'Tentacool','Jellyfish Pokemon',335,'water','poison',1,190,0),(73,'Tentacruel','Jellyfish Pokemon',515,'water','poison',1,60,0),(74,'Geodude','Rock Pokemon',300,'rock','ground',1,255,0),(75,'Graveler','Rock Pokemon',390,'rock','ground',1,120,0),(76,'Golem','Megaton Pokemon',495,'rock','ground',1,45,0),(77,'Ponyta','Fire Horse Pokemon',410,'fire',NULL,1,190,0),(78,'Rapidash','Fire Horse Pokemon',500,'fire',NULL,1,60,0),(79,'Slowpoke','Dopey Pokemon',315,'water','psychic',1,190,0),(80,'Slowbro','Hermit Crab Pokemon',590,'water','psychic',1,75,0),(81,'Magnemite','Magnet Pokemon',325,'electric','steel',1,190,0),(82,'Magneton','Magnet Pokemon',465,'electric','steel',1,60,0),(83,'Farfetch\'d','Wild Duck Pokemon',377,'normal','flying',1,45,0),(84,'Doduo','Twin Bird Pokemon',310,'normal','flying',1,190,0),(85,'Dodrio','Triple Bird Pokemon',470,'normal','flying',1,45,0),(86,'Seel','Sea Lion Pokemon',325,'water',NULL,1,190,0),(87,'Dewgong','Sea Lion Pokemon',475,'water','ice',1,75,0),(88,'Grimer','Sludge Pokemon',325,'poison','poison',1,190,0),(89,'Muk','Sludge Pokemon',500,'poison','poison',1,75,0),(90,'Shellder','Bivalve Pokemon',305,'water',NULL,1,190,0),(91,'Cloyster','Bivalve Pokemon',525,'water','ice',1,60,0),(92,'Gastly','Gas Pokemon',310,'ghost','poison',1,190,0),(93,'Haunter','Gas Pokemon',405,'ghost','poison',1,90,0),(94,'Gengar','Shadow Pokemon',600,'ghost','poison',1,45,0),(95,'Onix','Rock Snake Pokemon',385,'rock','ground',1,45,0),(96,'Drowzee','Hypnosis Pokemon',328,'psychic',NULL,1,190,0),(97,'Hypno','Hypnosis Pokemon',483,'psychic',NULL,1,75,0),(98,'Krabby','River Crab Pokemon',325,'water',NULL,1,225,0),(99,'Kingler','Pincer Pokemon',475,'water',NULL,1,60,0),(100,'Voltorb','Ball Pokemon',330,'electric',NULL,1,190,0),(101,'Electrode','Ball Pokemon',490,'electric',NULL,1,60,0),(102,'Exeggcute','Egg Pokemon',325,'grass','psychic',1,90,0),(103,'Exeggutor','Coconut Pokemon',530,'grass','psychic',1,45,0),(104,'Cubone','Lonely Pokemon',320,'ground',NULL,1,190,0),(105,'Marowak','Bone Keeper Pokemon',425,'ground','fire',1,75,0),(106,'Hitmonlee','Kicking Pokemon',455,'fighting',NULL,1,45,0),(107,'Hitmonchan','Punching Pokemon',455,'fighting',NULL,1,45,0),(108,'Lickitung','Licking Pokemon',385,'normal',NULL,1,45,0),(109,'Koffing','Poison Gas Pokemon',340,'poison',NULL,1,190,0),(110,'Weezing','Poison Gas Pokemon',490,'poison',NULL,1,60,0),(111,'Rhyhorn','Spikes Pokemon',345,'ground','rock',1,120,0),(112,'Rhydon','Drill Pokemon',485,'ground','rock',1,60,0),(113,'Chansey','Egg Pokemon',450,'normal',NULL,1,30,0),(114,'Tangela','Vine Pokemon',435,'grass',NULL,1,45,0),(115,'Kangaskhan','Parent Pokemon',590,'normal',NULL,1,45,0),(116,'Horsea','Dragon Pokemon',295,'water',NULL,1,225,0),(117,'Seadra','Dragon Pokemon',440,'water',NULL,1,75,0),(118,'Goldeen','Goldfish Pokemon',320,'water',NULL,1,225,0),(119,'Seaking','Goldfish Pokemon',450,'water',NULL,1,60,0),(120,'Staryu','Starshape Pokemon',340,'water',NULL,1,225,0),(121,'Starmie','Mysterious Pokemon',520,'water','psychic',1,60,0),(122,'Mr. Mime','Barrier Pokemon',460,'psychic','fairy',1,45,0),(123,'Scyther','Mantis Pokemon',500,'bug','flying',1,45,0),(124,'Jynx','Humanshape Pokemon',455,'ice','psychic',1,45,0),(125,'Electabuzz','Electric Pokemon',490,'electric',NULL,1,45,0),(126,'Magmar','Spitfire Pokemon',495,'fire',NULL,1,45,0),(127,'Pinsir','Stagbeetle Pokemon',600,'bug',NULL,1,45,0),(128,'Tauros','Wild Bull Pokemon',490,'normal',NULL,1,45,0),(129,'Magikarp','Fish Pokemon',200,'water',NULL,1,255,0),(130,'Gyarados','Atrocious Pokemon',640,'water','flying',1,45,0),(131,'Lapras','Transport Pokemon',535,'water','ice',1,45,0),(132,'Ditto','Transform Pokemon',288,'normal',NULL,1,35,0),(133,'Eevee','Evolution Pokemon',325,'normal',NULL,1,45,0),(134,'Vaporeon','Bubble Jet Pokemon',525,'water',NULL,1,45,0),(135,'Jolteon','Lightning Pokemon',525,'electric',NULL,1,45,0),(136,'Flareon','Flame Pokemon',525,'fire',NULL,1,45,0),(137,'Porygon','Virtual Pokemon',395,'normal',NULL,1,45,0),(138,'Omanyte','Spiral Pokemon',355,'rock','water',1,45,0),(139,'Omastar','Spiral Pokemon',495,'rock','water',1,45,0),(140,'Kabuto','Shellfish Pokemon',355,'rock','water',1,45,0),(141,'Kabutops','Shellfish Pokemon',495,'rock','water',1,45,0),(142,'Aerodactyl','Fossil Pokemon',615,'rock','flying',1,45,0),(143,'Snorlax','Sleeping Pokemon',540,'normal',NULL,1,25,0),(144,'Articuno','Freeze Pokemon',580,'ice','flying',1,3,1),(145,'Zapdos','Electric Pokemon',580,'electric','flying',1,3,1),(146,'Moltres','Flame Pokemon',580,'fire','flying',1,3,1),(147,'Dratini','Dragon Pokemon',300,'dragon',NULL,1,45,0),(148,'Dragonair','Dragon Pokemon',420,'dragon',NULL,1,45,0),(149,'Dragonite','Dragon Pokemon',600,'dragon','flying',1,45,0),(150,'Mewtwo','Genetic Pokemon',780,'psychic',NULL,1,3,1),(151,'Mew','New Species Pokemon',600,'psychic',NULL,1,45,1);
/*!40000 ALTER TABLE `pokemon_stat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade`
--

DROP TABLE IF EXISTS `trade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade` (
  `id` varchar(36) NOT NULL,
  `requester_id` varchar(32) NOT NULL,
  `receiver_id` varchar(32) NOT NULL,
  `requester_pokemon_id` varchar(24) NOT NULL,
  `receiver_pokemon_id` varchar(24) NOT NULL,
  `status` enum('pending','accepted','rejected') DEFAULT 'pending',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `decided_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_trade_requester` (`requester_id`),
  KEY `fk_trade_receiver` (`receiver_id`),
  KEY `fk_trade_requester_pokemon` (`requester_pokemon_id`),
  KEY `fk_trade_receiver_pokemon` (`receiver_pokemon_id`),
  CONSTRAINT `fk_trade_receiver` FOREIGN KEY (`receiver_id`) REFERENCES `player` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_trade_receiver_pokemon` FOREIGN KEY (`receiver_pokemon_id`) REFERENCES `pokemon_owned` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_trade_requester` FOREIGN KEY (`requester_id`) REFERENCES `player` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_trade_requester_pokemon` FOREIGN KEY (`requester_pokemon_id`) REFERENCES `pokemon_owned` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade`
--

LOCK TABLES `trade` WRITE;
/*!40000 ALTER TABLE `trade` DISABLE KEYS */;
INSERT INTO `trade` VALUES ('0881d560-7d3d-41e5-83c6-37ec2eb6cb4d','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3','Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV','jbspMNuwaRwJJFBnLoBAIeFB','rfWqJV73XqNpnEM2atI1M2HK','rejected','2025-09-27 20:10:39','2025-09-27 20:50:55'),('2b90b437-d23f-439e-900d-25ece1b764ad','Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ','jbspMNuwaRwJJFBnLoBAIeFB','KNpqNFxTuBiaFVFLlkrlctl3','accepted','2025-09-29 19:06:44','2025-09-29 19:12:49'),('a64bf0e1-7993-4e30-8c82-9f51aa6e38b8','CV0FK1BJScNyvRIhf8QqxEzgd5zzI1RQ','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3','XCiGloYxNx4SktSGdCv4hsWR','eTtICDRmfIjToRAVMGT8khDI','accepted','2025-09-29 19:12:17','2025-09-29 19:15:09'),('d8eaf1f2-5039-49d8-8705-21c947ad94ce','Xbh3InnXwqz9S7I0Hq7nt6xzZwOIyJUV','JMFVcNrJKnuN3XFhrgHJAYlXXSRxhjG3','eTtICDRmfIjToRAVMGT8khDI','jbspMNuwaRwJJFBnLoBAIeFB','accepted','2025-09-27 20:10:59','2025-09-27 20:42:05');
/*!40000 ALTER TABLE `trade` ENABLE KEYS */;
UNLOCK TABLES;
/*!50112 SET @disable_bulk_load = IF (@is_rocksdb_supported, 'SET SESSION rocksdb_bulk_load = @old_rocksdb_bulk_load', 'SET @dummy_rocksdb_bulk_load = 0') */;
/*!50112 PREPARE s FROM @disable_bulk_load */;
/*!50112 EXECUTE s */;
/*!50112 DEALLOCATE PREPARE s */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-24 14:50:53