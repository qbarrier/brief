import sqlite3
import requests
import csv
import pandas as pd
import io


### REQUETE INSERT RECETRTE PAR PRODUITS ###

def ft_analyse_produit(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO ventes_par_produit (nom, id_reference_produit, nombre_vendu, recette_produit)
        SELECT produits.nom, ventes.id_reference_produit, SUM(ventes.quantite) AS ombre_vendu, ROUND(SUM(ventes.quantite)*produits.prix, 2) AS recette_produit   FROM produits
        INNER JOIN ventes ON ventes.id_reference_produit=produits.id_reference_produit
        GROUP BY ventes.id_reference_produit;
                """)


### REQUETE INSERT RECETTE PAR MAGASINS ###

def ft_analyse_magasin(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO ventes_par_region (ville, id_magasin, nombre_de_transaction, recette_ville)
        SELECT magasins.ville, ventes.id_magasin, SUM(ventes.quantite) AS nombre_de_transaction, ROUND(SUM(ventes.quantite*produits.prix), 2) FROM magasins
        INNER JOIN ventes ON ventes.id_magasin = magasins.id_magasin
        INNER JOIN produits ON ventes.id_reference_produit=produits.id_reference_produit
        GROUP BY ventes.id_magasin;
                """)


### REQUETE INSERT CHIFFRE D'AFFAIRE ###

def ft_analyse_ca(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO ca_total (id, nombre_de_transaction, ca_total)      
        SELECT 1, SUM(ventes.quantite) AS nombre_de_transaction, ROUND(SUM(ventes.quantite*produits.prix), 2) FROM ventes
        INNER JOIN produits ON ventes.id_reference_produit=produits.id_reference_produit;
                """)

### EXECUTE LA REQUETE INSERT VIA FICHEIR SQL ###

def ft_analyse_sql(conn):
    cursor = conn.cursor()

    with open("analyse.sql", "r") as querry:
        cursor.executescript(querry.read())

### ECRIT LES RESULTAT D'ANNALYSE DANS UN FICHIER DATÉ .TXT ###

def ft_result(conn):

    with open("livrable/result.txt", "w") as f:

        cursor = conn.cursor()

        f.write("- TABLEAU DE RECETTE PAR PRODUITS : \n\n")
        cursor.execute("SELECT * FROM ventes_par_produit;")
        for row in cursor.fetchall():
            f.write(f"Le produit |{row[0]} - {row[1]}| a été vendu |{row[2]:<3}| fois et a recetté |{row[3]:<8}€|\n")
        df = pd.read_sql_query("SELECT * FROM ventes_par_produit;", conn)
        df.to_csv("livrable/ventes_par_produit.csv", index=False)

        f.write("\n- TABLEAU DE RECETTE PAR REGION : \n\n")
        cursor.execute("SELECT * FROM ventes_par_region;")
        for row in cursor.fetchall():
            f.write(f"Le Ville de |{row[0]:^11}| a fait |{row[2]:<3}| transactions et a fait un CA de : |{row[3]:<8}€|\n")
        df = pd.read_sql_query("SELECT * FROM ventes_par_region;", conn)
        df.to_csv("livrable/ventes_par_region.csv", index=False)

        f.write("\n- TABLEAU DU CHIFFRE D'AFFAIRE TOTAL : \n\n")
        cursor.execute("SELECT * FROM ca_total;")
        for row in cursor.fetchall():
            f.write(f"Pour un total de |{row[1]}| transactions le CA total est de : |{row[2]}€|\n")
        df = pd.read_sql_query("SELECT * FROM ca_total;", conn)
        df.to_csv("livrable/ca_total.csv", index=False)

        # print(f.read())
    print("\n -- Vous trouverez le RESULTAT d'analyse, ainsi que les fichiers .csv dans le DOSSIER : /livrable -- \n")

def main(conn):

    ### ANALYSE DES REQUETES ###
    try:
        # ft_analyse_produit(conn) # Ancienne Fonction
        # ft_analyse_magasin(conn) # Ancienne Fonction
        # ft_analyse_ca(conn) # Ancienne Fonction
        ft_analyse_sql(conn)
        ft_result(conn)
    except Exception as e:
        print(f"Erreur ligne: {e}")


if __name__ == "__main__":
    main()