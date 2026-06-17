-- INSERT VENTES_PAR_PRODUIT
        INSERT OR REPLACE INTO ventes_par_produit (nom, id_reference_produit, nombre_vendu, recette_produit)
        SELECT produits.nom, ventes.id_reference_produit, SUM(ventes.quantite) AS ombre_vendu, ROUND(SUM(ventes.quantite)*produits.prix, 2) AS recette_produit   FROM produits
        INNER JOIN ventes ON ventes.id_reference_produit=produits.id_reference_produit
        GROUP BY ventes.id_reference_produit;

-- INSERT VENTES_PAR_REGION
        INSERT OR REPLACE INTO ventes_par_region (ville, id_magasin, nombre_de_transaction, recette_ville)
        SELECT magasins.ville, ventes.id_magasin, SUM(ventes.quantite) AS nombre_de_transaction, ROUND(SUM(ventes.quantite*produits.prix), 2) FROM magasins
        INNER JOIN ventes ON ventes.id_magasin = magasins.id_magasin
        INNER JOIN produits ON ventes.id_reference_produit=produits.id_reference_produit
        GROUP BY ventes.id_magasin;

-- INSERT CA_TOTAL
        INSERT OR REPLACE INTO ca_total (id, nombre_de_transaction, ca_total)      
        SELECT 1, SUM(ventes.quantite) AS nombre_de_transaction, ROUND(SUM(ventes.quantite*produits.prix), 2) FROM ventes
        INNER JOIN produits ON ventes.id_reference_produit=produits.id_reference_produit;