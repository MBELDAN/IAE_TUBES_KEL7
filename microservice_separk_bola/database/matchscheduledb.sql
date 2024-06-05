-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 03, 2024 at 11:03 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `matchscheduledb`
--
CREATE DATABASE IF NOT EXISTS `matchscheduledb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `matchscheduledb`;

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('6cbc203311c4');

-- --------------------------------------------------------

--
-- Table structure for table `match_schedules`
--

CREATE TABLE IF NOT EXISTS `match_schedules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_date` date NOT NULL,
  `team_home_id` int NOT NULL,
  `team_away_id` int NOT NULL,
  `stadium_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `stadium_id` (`stadium_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `match_schedules`
--

INSERT INTO `match_schedules` (`id`, `match_date`, `team_home_id`, `team_away_id`, `stadium_id`) VALUES
(1, '2023-06-01', 1, 2, 1),
(2, '2024-07-01', 1, 3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `stadiums`
--

CREATE TABLE IF NOT EXISTS `stadiums` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `capacity` int DEFAULT NULL,
  `address` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stadiums`
--

INSERT INTO `stadiums` (`id`, `name`, `capacity`, `address`) VALUES
(1, 'New Stadium', 50000, '123 Stadium Road'),
(3, 'Jakarta International Stadion', 60000, 'Jakarta');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `match_schedules`
--
ALTER TABLE `match_schedules`
  ADD CONSTRAINT `match_schedules_ibfk_1` FOREIGN KEY (`stadium_id`) REFERENCES `stadiums` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
