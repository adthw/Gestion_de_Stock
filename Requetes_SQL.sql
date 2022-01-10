-- • Afficher les noms et descriptions de tous les produits:

SELECT nom_produit, description_produit FROM produits 

-- • Afficher tous les meubles qui sont abandonnés:

SELECT nom_produit FROM produits WHERE statut_produit='0' 

-- • Effacer le Bo Meuble de brest:

DELETE FROM clients WHERE nom_client='Bo Meuble' AND ville_client ='Brest' 
DELETE FROM clients WHERE nom_client='Bo Meuble' AND adresse_client='Rue Jean Jaurès' AND ville_client ='Brest' AND pays_client='France'

-- • Il y a une erreur sur le nom du meuble Apfelgluk, il faut le réécrire Apfelgluck:

UPDATE produits SET nom_produit = 'Apfelgluck' WHERE ref_produit='OANT12'

-- • Ajouter un nouveau client : Tout à la maison, Place Terreaux, Lyon:

-- Version 1 :
INSERT INTO clients (id_types, nom_client, adresse_client, ville_client, pays_client) VALUES ('1', 'Tout à la maison', 'Place Terreaux', 'Lyon', 'France')

-- Version 2:
INSERT INTO clients (id_types, nom_client, adresse_client, ville_client, pays_client) VALUES ((SELECT id_types FROM types WHERE nom_types='Magasin'), 'Tout à la maison', 'Place Terreaux', 'Lyon', 'France')


-- • Ajouter une nouvelle facture pour le Tout à la maison de Lyon , enregistrée le 28/08/2018, à 18h: (La commande est composé de 18 Naess)     

INSERT INTO calendrier (date_calendrier) VALUES ('2018-08-28 18:00:00')
INSERT INTO factures (numero_facture, date_calendrier, id_client) VALUES ('MSQ298', '2018-08-28 18:00:00', (SELECT id_client FROM clients WHERE nom_client = "Tout à la maison" AND ville_client = "Lyon"))
INSERT INTO commander (id_produit, id_facture, quantite_commander) VALUES ((SELECT id_produit FROM produits WHERE nom_produit = "Naess"), (SELECT id_facture FROM factures WHERE numero_facture = 'MSQ297'), 18)



-- • Retrouver tous les meubles achetés par le Bo Meuble de Paris: (clients, factures, calendrier)
SELECT nom_client,ville_client, id_facture, nom_produit, ref_produit, quantite_commander FROM clients NATURAL JOIN factures NATURAL JOIN commander NATURAL JOIN produits WHERE nom_client='Bo Meuble' AND ville_client='Paris'

-- • Retrouver toutes les factures enregistrées depuis le 1er juillet 2018:

SELECT * FROM facturation_ikeo.calendrier WHERE date_calendrier > '2018-07-01 00:00:00'