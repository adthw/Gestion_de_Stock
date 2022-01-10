CREATE DATABASE IF NOT EXISTS `FACTURATION_IKEO` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `FACTURATION_IKEO`;

CREATE TABLE `PRODUITS` (
  `id_produit` int(11),
  `ref_produit` VARCHAR(10),
  `nom_produit` VARCHAR(30),
  `description_produit` VARCHAR(500),
  `statut_produit` BOOL,
  PRIMARY KEY (`id_produit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `COMMANDER` (
  `id_produit` int(11),
  `id_facture` int(11),
  `id_commander` INT(11),
  `quantite_commander` INT(11),
  PRIMARY KEY (`id_produit`, `id_facture`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `FACTURES` (
  `id_facture` int(11),
  `numero_facture` VARCHAR(30),
  `date_calendrier` DATE,
  `id_client` int(11),
  PRIMARY KEY (`id_facture`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `PRODUIRE` (
  `id_usine` int(11),
  `id_produit` int(11),
  PRIMARY KEY (`id_usine`, `id_produit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `USINES` (
  `id_usine` int(11),
  `nom_usine` VARCHAR(30),
  `adresse_usine` VARCHAR(30),
  `ville_usine` VARCHAR(30),
  PRIMARY KEY (`id_usine`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `CALENDRIER` (
  `date_calendrier` DATE,
  PRIMARY KEY (`date_calendrier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `CLIENTS` (
  `id_client` int(11),
  `nom_client` VARCHAR(30),
  `adresse_client` VARCHAR(30),
  `ville_client` VARCHAR(30),
  `pays_client` VARCHAR(30),
  `id_types` INT(11),
  PRIMARY KEY (`id_client`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `TYPES` (
  `id_types` INT(11),
  `nom_types` VARCHAR(30),
  PRIMARY KEY (`id_types`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `COMMANDER` ADD FOREIGN KEY (`id_facture`) REFERENCES `FACTURES` (`id_facture`);
ALTER TABLE `COMMANDER` ADD FOREIGN KEY (`id_produit`) REFERENCES `PRODUITS` (`id_produit`);
ALTER TABLE `FACTURES` ADD FOREIGN KEY (`id_client`) REFERENCES `CLIENTS` (`id_client`);
ALTER TABLE `FACTURES` ADD FOREIGN KEY (`date_calendrier`) REFERENCES `CALENDRIER` (`date_calendrier`);
ALTER TABLE `PRODUIRE` ADD FOREIGN KEY (`id_produit`) REFERENCES `PRODUITS` (`id_produit`);
ALTER TABLE `PRODUIRE` ADD FOREIGN KEY (`id_usine`) REFERENCES `USINES` (`id_usine`);
ALTER TABLE `CLIENTS` ADD FOREIGN KEY (`id_types`) REFERENCES `TYPES` (`id_types`);