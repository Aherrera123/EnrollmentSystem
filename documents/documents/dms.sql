-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 09, 2025 at 05:25 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dms`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `AccountID` varchar(255) NOT NULL,
  `UName` varchar(255) DEFAULT NULL,
  `PWord` varchar(255) DEFAULT NULL,
  `AccType` varchar(255) DEFAULT NULL,
  `Status` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`AccountID`, `UName`, `PWord`, `AccType`, `Status`) VALUES
('AhNQbZjj', 'carlooo', '$2y$10$dZQYZjoeuxSZ2Wqbw4V7UeSO/.kvQsYVcJc8ipdgzBe.Tj0MvebBW', 'Admin', '1'),
('m0y911ls', 'admin', '$2y$10$bIXgfdtuGsFPAAv/nEyF1ulU6irGZYt.qOBOz..fbocbpt0V/fQMS', 'Admin', '1'),
('N6X7Gk6z', 'test@gmail.com', '$2y$10$O6siurL2H4GfaCmeiiBKy.pr5Gw.KU6CokMoP0OpClA4ZW9snLYUq', 'Admin', '1'),
('tC0RSf5e', 'carlo', '$2y$10$MK4YQMeYV7NsvgH86n4m7OEPO0s6DNJdWvbRTj0FvoWLcioVhLtqS', 'Admin', '1');

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `AdminID` varchar(255) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `AccountID` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`AdminID`, `Name`, `AccountID`) VALUES
('2x57lPdX', 'Username', 'N6X7Gk6z'),
('9ZBCoYab', NULL, 'AhNQbZjj'),
('fMWzctFg', 'Carlo James Musa Del Valle', 'tC0RSf5e'),
('gTrat1of', NULL, 'm0y911ls');

-- --------------------------------------------------------

--
-- Table structure for table `files`
--

CREATE TABLE `files` (
  `FileID` varchar(255) NOT NULL,
  `FileName` varchar(255) DEFAULT NULL,
  `FileSize` float DEFAULT NULL,
  `FilePath` varchar(255) DEFAULT NULL,
  `DateUploaded` varchar(255) DEFAULT NULL,
  `FolderID` varchar(255) DEFAULT NULL,
  `AccountID` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `files`
--

INSERT INTO `files` (`FileID`, `FileName`, `FileSize`, `FilePath`, `DateUploaded`, `FolderID`, `AccountID`) VALUES
('FILE_2LZ1WDTM', 'QRCode.png', 2229, '../../uploads/9zhMUaWk/QRCode.png', '2025-01-09 19:32:38', '9zhMUaWk', 'm0y911ls'),
('FILE_JICY3ZUN', 'placehold.co.png', 7809, '../../uploads/STfaIeRh/placehold.co.png', '2025-01-09 04:17:32', 'STfaIeRh', 'N6X7Gk6z'),
('FILE_LPE136XU', 'QRCode (4).png', 2283, '../../uploads/IKitsrFM/QRCode (4).png', '2025-01-09 20:14:40', 'IKitsrFM', 'm0y911ls'),
('FILE_ZMNIA794', 'QR.png', 2163, '../../uploads/tGFrB9kY/QRCode (3).png', '2025-01-09 21:17:53', 'tGFrB9kY', 'N6X7Gk6z');

-- --------------------------------------------------------

--
-- Table structure for table `folders`
--

CREATE TABLE `folders` (
  `FolderID` varchar(255) NOT NULL,
  `FolderName` varchar(255) DEFAULT NULL,
  `FolderPath` varchar(255) DEFAULT NULL,
  `Category` varchar(255) DEFAULT NULL,
  `Contractor` varchar(255) DEFAULT NULL,
  `Project` varchar(255) DEFAULT NULL,
  `ContractAmount` decimal(15,2) DEFAULT NULL,
  `CheckNo` varchar(50) DEFAULT NULL,
  `PaymentNature` varchar(255) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Amount` decimal(15,2) DEFAULT NULL,
  `FundingSource` varchar(255) DEFAULT NULL,
  `ContractEffectivity` date DEFAULT NULL,
  `ContractDuration` int(11) DEFAULT NULL,
  `ContractExpiry` date DEFAULT NULL,
  `ExpiryExtension` date DEFAULT NULL,
  `DateCreated` varchar(255) DEFAULT NULL,
  `AccountID` varchar(255) DEFAULT NULL,
  `subcategory` varchar(255) DEFAULT 'COA'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `folders`
--

INSERT INTO `folders` (`FolderID`, `FolderName`, `FolderPath`, `Category`, `Contractor`, `Project`, `ContractAmount`, `CheckNo`, `PaymentNature`, `Date`, `Amount`, `FundingSource`, `ContractEffectivity`, `ContractDuration`, `ContractExpiry`, `ExpiryExtension`, `DateCreated`, `AccountID`, `subcategory`) VALUES
('9zhMUaWk', 'Folder1', '../folders/9zhMUaWk-Folder1/', 'Goods and Services', '123', '123', 123.00, '123', '123', '2025-01-08', 123.00, '123', '2025-01-16', 123, '2025-01-09', '2025-05-12', '2025-01-09 19:30:13', 'm0y911ls', 'COA'),
('F0oGxsJ1', 'test', '../folders/F0oGxsJ1-test/', 'Infrastructure and Consultancy', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-01-09 12:35:09', 'N6X7Gk6z', 'COA'),
('IKitsrFM', 'Folder 2', '../folders/IKitsrFM-Folder 2/', 'Goods and Services', 'test', 'test', 123.00, '123', '123', '2025-01-09', 123.00, '123', '2025-01-09', 123, '2025-01-09', '2025-05-11', '2025-01-09 19:32:01', 'm0y911ls', 'COA'),
('STfaIeRh', 'Folder1', '../folders/STfaIeRh-Folder1/', 'Goods and Services', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-01-09 04:11:17', 'N6X7Gk6z', 'Inspection Team'),
('tGFrB9kY', 'Folder 3', '../folders/tGFrB9kY-Folder 3/', 'Inspection Team', 'Test', 'Test', 123.00, '123', '123', '2025-01-10', 123.00, '123', '2025-01-09', 123, '2025-01-09', '2025-05-12', '2025-01-09 21:16:42', 'N6X7Gk6z', 'Accounting'),
('ZGkk9Yx3', 'Folder123', '../folders/ZGkk9Yx3-Folder123/', 'Goods and Services', 'Folder123', 'Folder123', 123.00, '123', '123', '2025-01-09', 123.00, '123', '2025-01-17', 5, '2025-01-09', '2025-01-14', '2025-01-09 12:51:38', 'N6X7Gk6z', 'COA');

-- --------------------------------------------------------

--
-- Table structure for table `qr_codes`
--

CREATE TABLE `qr_codes` (
  `QRCodeID` varchar(255) NOT NULL,
  `FolderID` varchar(255) NOT NULL,
  `QRValue` varchar(255) NOT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `qr_codes`
--

INSERT INTO `qr_codes` (`QRCodeID`, `FolderID`, `QRValue`, `CreatedAt`) VALUES
('50X0Xjyn', 'ZGkk9Yx3', '354234d3380cc399d9e113f7e21845f4', '2025-01-09 04:51:38'),
('82z8fCTr', 'tGFrB9kY', 'd73b0a974982047de4e9568a8570d5df', '2025-01-09 13:16:42'),
('p3yRFy5D', 'STfaIeRh', 'cd95741c52b5bd43accb3324a91aa91f', '2025-01-08 20:11:17'),
('UgG7fASC', 'IKitsrFM', '1e2a50e2121eef5346c44ba3a37cdcd9', '2025-01-09 11:32:01'),
('xAUIlogg', '9zhMUaWk', 'f52b3bbd56e4bf354cf06801852b2703', '2025-01-09 11:30:13'),
('xODpJ94I', 'F0oGxsJ1', '7fb51174c10b44a0a3670ee4821e323e', '2025-01-09 04:35:09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`AccountID`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`AdminID`),
  ADD KEY `AccountID` (`AccountID`);

--
-- Indexes for table `files`
--
ALTER TABLE `files`
  ADD PRIMARY KEY (`FileID`),
  ADD KEY `FolderID` (`FolderID`),
  ADD KEY `AccountID` (`AccountID`);

--
-- Indexes for table `folders`
--
ALTER TABLE `folders`
  ADD PRIMARY KEY (`FolderID`),
  ADD KEY `AccountID` (`AccountID`);

--
-- Indexes for table `qr_codes`
--
ALTER TABLE `qr_codes`
  ADD PRIMARY KEY (`QRCodeID`),
  ADD UNIQUE KEY `QRValue` (`QRValue`),
  ADD KEY `FolderID` (`FolderID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin`
--
ALTER TABLE `admin`
  ADD CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`AccountID`) REFERENCES `account` (`AccountID`);

--
-- Constraints for table `files`
--
ALTER TABLE `files`
  ADD CONSTRAINT `files_ibfk_1` FOREIGN KEY (`FolderID`) REFERENCES `folders` (`FolderID`),
  ADD CONSTRAINT `files_ibfk_2` FOREIGN KEY (`AccountID`) REFERENCES `account` (`AccountID`);

--
-- Constraints for table `folders`
--
ALTER TABLE `folders`
  ADD CONSTRAINT `folders_ibfk_1` FOREIGN KEY (`AccountID`) REFERENCES `account` (`AccountID`);

--
-- Constraints for table `qr_codes`
--
ALTER TABLE `qr_codes`
  ADD CONSTRAINT `qr_codes_ibfk_1` FOREIGN KEY (`FolderID`) REFERENCES `folders` (`FolderID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
