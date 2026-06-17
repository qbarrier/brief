import sqlite3
import import_data
import analyse_brief

print("Hello World !")

### CREATION/CONNEXION A LA BDD ###
conn = sqlite3.connect('/var/lib/sqlite/brief.db')
cursor = conn.cursor()

### CREATION DES TABLES ###
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS magasins(
        id_magasin INTEGER PRIMARY KEY,
        ville TEXT,
        nombre_de_salaries INTEGER);

     CREATE TABLE IF NOT EXISTS produits(
        nom TEXT,
        id_reference_produit TEXT PRIMARY KEY,
        prix REAL,
        stock INTEGER); 

     CREATE TABLE IF NOT EXISTS ventes(
        id_vente INTEGER PRIMARY KEY,
        date TEXT,
        id_reference_produit TEXT,
        quantite INTEGER,
        id_magasin INTEGER,
        FOREIGN KEY(id_magasin) REFERENCES magasins(id_magasin),
        FOREIGN KEY(id_reference_produit) REFERENCES produits(id_reference_produit)
        UNIQUE(date, id_reference_produit, id_magasin));
                     
    CREATE TABLE IF NOT EXISTS ventes_par_produit(
        nom TEXT,
        id_reference_produit TEXT PRIMARY KEY,
        nombre_vendu INTEGER,
        recette_produit REAL,
        FOREIGN KEY(id_reference_produit) REFERENCES produits(id_reference_produit));

    CREATE TABLE IF NOT EXISTS ventes_par_region(
        ville TEXT,
        id_magasin INTEGER PRIMARY KEY,
        nombre_de_transaction INTEGER,
        recette_ville REAL,
        FOREIGN KEY(id_magasin) REFERENCES magasins(id_magasin));
                     
     CREATE TABLE IF NOT EXISTS ca_total(
        id INTEGER PRIMARY KEY,
        nombre_de_transaction INTEGER,
        ca_total REAL);      
    
               """)

import_data.main(conn)
analyse_brief.main(conn)

### COMMIT ET CLOSE ###
conn.commit()
conn.close()