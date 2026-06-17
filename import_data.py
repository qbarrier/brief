import sqlite3
import requests
import csv
import io

### FONCTION INSERTION DES DONNESS ###

def ft_insert_data_magasins(row, conn):
    
    # print(f"✓ Inséré: {row['ID Magasin']} - {row['Ville']} - {row['Nombre de salariés']}")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO magasins (id_magasin, ville, nombre_de_salaries)
        VALUES (?, ?, ?)
                """, (row['ID Magasin'], row['Ville'], row['Nombre de salariés']))

### FONCTION INSERTION DES PRODUITS ###

def ft_insert_data_produits(row, conn):
    
    # print(f"✓ Inséré: {row['Nom']} - {row['ID Référence produit']} - {row['Prix']} - {row['Stock']}")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO produits (nom, id_reference_produit, prix, stock)
        VALUES (?, ?, ?, ?)
                """, (row['Nom'], row['ID Référence produit'], row['Prix'], row['Stock']))


### FONCTION INSERTION DES VENTES ###

def ft_insert_data_ventes(row, conn):
    
    # print(f"✓ Inséré: {row['Date']} - {row['ID Référence produit']} - {row['Quantité']} - {row['ID Magasin']}")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO ventes (date, id_reference_produit, quantite, id_magasin)
        VALUES (?, ?, ?, ?)
                """, (row['Date'], row['ID Référence produit'], row['Quantité'], row['ID Magasin']))

### FONCTION REQUEST CSV ###

def ft_request_csv(conn):
    
    ### RECUPERATION CSV MAGASINS ###
    r = requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv")
    r.encoding = 'utf-8'
    # print(r.text)

    ### PARSING EN DICTIONNAIRE ###
    reader = csv.DictReader(io.StringIO(r.text))

    for row in reader:
        # print(row.keys())
        try:
            ft_insert_data_magasins(row, conn)
        except Exception as e:
            print(f"Erreur ligne: {e}")


    ### RECUPERATION CSV PRODUITS ###
    r = requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv")
    r.encoding = 'utf-8'
    # print(r.text)

    ### PARSING EN DICTIONNAIRE ###
    reader = csv.DictReader(io.StringIO(r.text))

    for row in reader:
        # print(row.keys())
        try:
            ft_insert_data_produits(row, conn)
        except Exception as e:
            print(f"Erreur ligne: {e}")


    ### RECUPERATION CSV VENTES ###
    r = requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv")
    r.encoding = 'utf-8'
    # print(r.text)

    ### PARSING EN DICTIONNAIRE ###
    reader = csv.DictReader(io.StringIO(r.text))

    for row in reader:
        # print(row.keys())
        try:
            ft_insert_data_ventes(row, conn)
        except Exception as e:
            print(f"Erreur ligne: {e}")

### MAIN FONCTION ###

def main(conn):

    ### GESTION DES REQUETES ###
    ft_request_csv(conn)


if __name__ == "__main__":
    main()