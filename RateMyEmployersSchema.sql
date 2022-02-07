-- MySQL dump 10.13  Distrib 8.0.23, for macos10.15 (x86_64)
--
-- Host: localhost    Database: RateMyEmployers
-- ------------------------------------------------------
-- Server version	8.0.23

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

--
-- Table structure for table `Answers`
--

DROP TABLE IF EXISTS `Answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Answers` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `QId` int DEFAULT NULL,
  `ReviewId` int DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_QId_idx` (`QId`),
  KEY `FK_ReviewId_idx` (`ReviewId`),
  CONSTRAINT `FK_QId` FOREIGN KEY (`QId`) REFERENCES `ReviewQuestions` (`Id`),
  CONSTRAINT `FK_ReviewId` FOREIGN KEY (`ReviewId`) REFERENCES `Review` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `CommentAnswers`
--

DROP TABLE IF EXISTS `CommentAnswers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CommentAnswers` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `AnswerId` int DEFAULT NULL,
  `Comment` text,
  PRIMARY KEY (`Id`),
  KEY `FK_AnswerId_idx` (`AnswerId`),
  CONSTRAINT `FK_Comment_AnswerId` FOREIGN KEY (`AnswerId`) REFERENCES `Answers` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Company`
--

DROP TABLE IF EXISTS `Company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Company` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) DEFAULT NULL,
  `ParentCompany` int DEFAULT NULL,
  `Industry` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_ParentCompany_idx` (`ParentCompany`),
  CONSTRAINT `FK_ParentCompany` FOREIGN KEY (`ParentCompany`) REFERENCES `Company` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Person`
--

DROP TABLE IF EXISTS `Person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Person` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `PrefixId` int DEFAULT NULL,
  `username` varchar(15) DEFAULT NULL,
  `FirstName` varchar(20) DEFAULT NULL,
  `Lname` varchar(20) DEFAULT NULL,
  `SuffixId` int DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `PasswordHash` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_Prefix_idx` (`PrefixId`),
  KEY `FK_Suffix_idx` (`SuffixId`),
  CONSTRAINT `FK_Prefix` FOREIGN KEY (`PrefixId`) REFERENCES `Prefix` (`Id`),
  CONSTRAINT `FK_Suffix` FOREIGN KEY (`SuffixId`) REFERENCES `Suffix` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Prefix`
--

DROP TABLE IF EXISTS `Prefix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Prefix` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Prefix` varchar(5) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `QuestionType`
--

DROP TABLE IF EXISTS `QuestionType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `QuestionType` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Type` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Review`
--

DROP TABLE IF EXISTS `Review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Review` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `PersonId` int DEFAULT NULL,
  `CompanyId` int DEFAULT NULL,
  `CreateTimestamp` datetime DEFAULT NULL,
  `BranchLocation` varchar(100) DEFAULT NULL,
  `YearsOfService` decimal(4,2) DEFAULT NULL,
  `PositionAtCompany` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_PersonId_idx` (`PersonId`),
  KEY `FK_CompanyId_idx` (`CompanyId`),
  CONSTRAINT `FK_CompanyId` FOREIGN KEY (`CompanyId`) REFERENCES `Company` (`Id`),
  CONSTRAINT `FK_PersonId` FOREIGN KEY (`PersonId`) REFERENCES `Person` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ReviewQuestions`
--

DROP TABLE IF EXISTS `ReviewQuestions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ReviewQuestions` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `QTypeId` int DEFAULT NULL,
  `QuestionText` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_QTypeId_idx` (`QTypeId`),
  CONSTRAINT `FK_QTypeId` FOREIGN KEY (`QTypeId`) REFERENCES `QuestionType` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sentences`
--

DROP TABLE IF EXISTS `sentences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sentences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sentence` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `StarAnswers`
--

DROP TABLE IF EXISTS `StarAnswers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StarAnswers` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `AnswerId` int DEFAULT NULL,
  `Answer` int DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_AnswerId_idx` (`AnswerId`),
  CONSTRAINT `FK_Star_AnswerId` FOREIGN KEY (`AnswerId`) REFERENCES `Answers` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Suffix`
--

DROP TABLE IF EXISTS `Suffix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Suffix` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Suffix` varchar(5) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `AI` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-02 21:09:28
