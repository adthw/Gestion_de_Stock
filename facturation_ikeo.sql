-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8081
-- Generation Time: Jan 10, 2022 at 02:06 PM
-- Server version: 5.7.24
-- PHP Version: 7.4.16

CREATE DATABASE IF NOT EXISTS `FACTURATION_IKEO` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `FACTURATION_IKEO`;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `facturation_ikeo`
--

-- --------------------------------------------------------

--
-- Table structure for table `calendrier`
--

CREATE TABLE `calendrier` (
  `date_calendrier` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `calendrier`
--

INSERT INTO `calendrier` (`date_calendrier`) VALUES
('2018-06-15 00:00:00'),
('2018-06-23 00:00:00'),
('2018-06-28 00:00:00'),
('2018-07-01 00:00:00'),
('2018-07-04 00:00:00'),
('2018-07-12 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE `clients` (
  `id_client` int(11) NOT NULL,
  `nom_client` varchar(50) NOT NULL,
  `adresse_client` varchar(30) NOT NULL,
  `ville_client` varchar(30) NOT NULL,
  `pays_client` varchar(30) NOT NULL,
  `id_types` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`id_client`, `nom_client`, `adresse_client`, `ville_client`, `pays_client`, `id_types`) VALUES
(1, 'Bo Meuble', 'Place Vendôme', 'Paris', 'France', 1),
(2, 'Mobel', 'Porte de Brandebourg', 'Berlin', 'Allemagne', 1),
(3, 'Bo Meuble', 'Rue Jean Jaurès', 'Brest', 'France', 1),
(4, 'Tout A La Maison', 'Rue de la Bastille', 'Paris', 'France', 1),
(5, 'Bo Meuble', 'Avenue des Trois Dragons', 'Barcelone', 'Espagne', 1),
(6, 'The Wolrd Compagny', 'Oxford street', 'Londres', 'Angleterre', 2),
(7, 'The Best Greatest Beautifulest Furniture', 'Coven Gargen', 'Londres', 'Angleterre', 1);

-- --------------------------------------------------------

--
-- Table structure for table `commander`
--

CREATE TABLE `commander` (
  `id_commander` int(11) NOT NULL,
  `id_produit` int(11) NOT NULL,
  `id_facture` int(11) NOT NULL,
  `quantite_commander` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `commander`
--

INSERT INTO `commander` (`id_commander`, `id_produit`, `id_facture`, `quantite_commander`) VALUES
(1, 1, 1, 20),
(2, 2, 1, 30),
(3, 3, 1, 10),
(4, 8, 2, 25),
(5, 4, 2, 32),
(6, 3, 3, 80),
(7, 5, 3, 70),
(8, 6, 3, 60),
(9, 4, 3, 60),
(10, 9, 3, 120),
(11, 7, 3, 90),
(12, 1, 4, 10),
(13, 2, 4, 10),
(14, 6, 4, 30),
(15, 1, 5, 25),
(16, 7, 5, 34),
(17, 2, 6, 40),
(18, 5, 6, 38),
(19, 6, 6, 54),
(20, 4, 7, 20),
(21, 5, 7, 34),
(22, 6, 7, 45);

-- --------------------------------------------------------

--
-- Table structure for table `factures`
--

CREATE TABLE `factures` (
  `id_facture` int(11) NOT NULL,
  `numero_facture` varchar(30) NOT NULL,
  `date_calendrier` datetime NOT NULL,
  `id_client` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `factures`
--

INSERT INTO `factures` (`id_facture`, `numero_facture`, `date_calendrier`, `id_client`) VALUES
(1, 'MSQ291', '2018-06-15 00:00:00', 1),
(2, 'MSQ292', '2018-06-23 00:00:00', 3),
(3, 'MSQ293', '2018-06-23 00:00:00', 6),
(4, 'MSQ294', '2018-06-28 00:00:00', 1),
(5, 'MSQ295', '2018-07-01 00:00:00', 4),
(6, 'MSQ296', '2018-07-04 00:00:00', 7),
(7, 'MSQ297', '2018-07-12 00:00:00', 2);

-- --------------------------------------------------------

--
-- Table structure for table `produire`
--

CREATE TABLE `produire` (
  `id_produire` int(11) NOT NULL,
  `id_usine` int(11) NOT NULL,
  `id_produit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `produire`
--

INSERT INTO `produire` (`id_produire`, `id_usine`, `id_produit`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 1, 2),
(4, 2, 2),
(5, 1, 3),
(6, 3, 3),
(7, 3, 4),
(8, 1, 5),
(9, 3, 5),
(10, 2, 5),
(11, 1, 6),
(12, 3, 5),
(13, 2, 7),
(14, 3, 7),
(15, 3, 8),
(16, 3, 7);

-- --------------------------------------------------------

--
-- Table structure for table `produits`
--

CREATE TABLE `produits` (
  `id_produit` int(11) NOT NULL,
  `ref_produit` varchar(10) NOT NULL,
  `nom_produit` varchar(30) NOT NULL,
  `description_produit` varchar(500) NOT NULL,
  `statut_produit` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `produits`
--

INSERT INTO `produits` (`id_produit`, `ref_produit`, `nom_produit`, `description_produit`, `statut_produit`) VALUES
(1, 'OANT72', 'Knutsen', 'Table basse pour poser les bières', 0),
(2, 'OANT34', 'Moen', 'Chaise haute de bar', 1),
(3, 'OANT67', 'Eide', 'Porte-serviettes pour 100 serviettes', 0),
(4, 'LXAL34', 'Gulbrandsen', 'Lit nuage en lévitation', 0),
(5, 'LXAL56', 'Naess', 'Table 128 convives', 0),
(6, 'LXAL 78', 'Lund', 'Bureau-cafetière électrique', 0),
(7, 'LXAL12', 'Dahl', 'Tiroir à ronds de serviette', 1),
(8, 'OANT90', 'Ruud', 'Bureau-lit conbiné', 0),
(9, 'OANT12', 'Apfelgluk', 'Panier à chien (ou à chat)', 0);

-- --------------------------------------------------------

--
-- Table structure for table `types`
--

CREATE TABLE `types` (
  `id_types` int(11) NOT NULL,
  `nom_types` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `types`
--

INSERT INTO `types` (`id_types`, `nom_types`) VALUES
(1, 'Magasin'),
(2, 'Centrale d\'achat');

-- --------------------------------------------------------

--
-- Table structure for table `usines`
--

CREATE TABLE `usines` (
  `id_usine` int(11) NOT NULL,
  `nom_usine` varchar(30) NOT NULL,
  `adresse_usine` varchar(30) NOT NULL,
  `ville_usine` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `usines`
--

INSERT INTO `usines` (`id_usine`, `nom_usine`, `adresse_usine`, `ville_usine`) VALUES
(1, 'Harald', 'Quai Pipervika', 'Oslo'),
(2, 'Sverre', 'Rue Strangehagen', 'Bergen'),
(3, 'Olaf', 'Place Nidaros', 'Trondheim');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `calendrier`
--
ALTER TABLE `calendrier`
  ADD PRIMARY KEY (`date_calendrier`);

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`id_client`),
  ADD KEY `id_types` (`id_types`);

--
-- Indexes for table `commander`
--
ALTER TABLE `commander`
  ADD PRIMARY KEY (`id_commander`),
  ADD KEY `id_produit` (`id_produit`),
  ADD KEY `id_facture` (`id_facture`);

--
-- Indexes for table `factures`
--
ALTER TABLE `factures`
  ADD PRIMARY KEY (`id_facture`),
  ADD KEY `id_client` (`id_client`),
  ADD KEY `date_calendrier` (`date_calendrier`);

--
-- Indexes for table `produire`
--
ALTER TABLE `produire`
  ADD PRIMARY KEY (`id_produire`),
  ADD KEY `id_produit` (`id_produit`),
  ADD KEY `id_usine` (`id_usine`);

--
-- Indexes for table `produits`
--
ALTER TABLE `produits`
  ADD PRIMARY KEY (`id_produit`);

--
-- Indexes for table `types`
--
ALTER TABLE `types`
  ADD PRIMARY KEY (`id_types`);

--
-- Indexes for table `usines`
--
ALTER TABLE `usines`
  ADD PRIMARY KEY (`id_usine`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `clients`
--
ALTER TABLE `clients`
  MODIFY `id_client` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `commander`
--
ALTER TABLE `commander`
  MODIFY `id_commander` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `factures`
--
ALTER TABLE `factures`
  MODIFY `id_facture` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `produire`
--
ALTER TABLE `produire`
  MODIFY `id_produire` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `produits`
--
ALTER TABLE `produits`
  MODIFY `id_produit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `types`
--
ALTER TABLE `types`
  MODIFY `id_types` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `usines`
--
ALTER TABLE `usines`
  MODIFY `id_usine` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `clients`
--
ALTER TABLE `clients`
  ADD CONSTRAINT `clients_ibfk_1` FOREIGN KEY (`id_types`) REFERENCES `types` (`id_types`);

--
-- Constraints for table `commander`
--
ALTER TABLE `commander`
  ADD CONSTRAINT `commander_ibfk_1` FOREIGN KEY (`id_produit`) REFERENCES `produits` (`id_produit`),
  ADD CONSTRAINT `commander_ibfk_2` FOREIGN KEY (`id_facture`) REFERENCES `factures` (`id_facture`);

--
-- Constraints for table `factures`
--
ALTER TABLE `factures`
  ADD CONSTRAINT `factures_ibfk_1` FOREIGN KEY (`id_client`) REFERENCES `clients` (`id_client`),
  ADD CONSTRAINT `factures_ibfk_2` FOREIGN KEY (`date_calendrier`) REFERENCES `calendrier` (`date_calendrier`);

--
-- Constraints for table `produire`
--
ALTER TABLE `produire`
  ADD CONSTRAINT `produire_ibfk_1` FOREIGN KEY (`id_produit`) REFERENCES `produits` (`id_produit`),
  ADD CONSTRAINT `produire_ibfk_2` FOREIGN KEY (`id_usine`) REFERENCES `usines` (`id_usine`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
