import pandas as pd
from fastapi import FastAPI
import psycopg2

#fonction de connexion à la bdd
def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="postgresql_bdd",
        user="user",
        password="password"
    )
    return connection

api= FastAPI()

# création des fichiers sources de données pour les tables produits et prix
@api.post("/creation_fichiers_sources")
def create_file():
    df = pd.read_csv('https://query.data.world/s/b6r62f3bsjalbhxttweer2cqzszmbv')
    # construction du dataframe des prix de produits
    df_price = df[['id', 'prices.amountMax', 'prices.amountMin', 'prices.availability',
           'prices.condition', 'prices.currency', 'prices.dateSeen',
           'prices.isSale', 'prices.merchant', 'prices.shipping',
           'prices.sourceURLs']]
    #renommage de la colonne id en id_product
    df_price.rename(columns = {'id':'product_id','prices.amountMax':'amountMax','prices.amountMin':'amountMin','prices.availability':'availability',
                               'prices.condition':'condition','prices.currency':'currency','prices.dateSeen':'dateSeen','prices.isSale':'.isSale',
                               'prices.merchant':'merchant','prices.shipping':'shipping','prices.sourceURLs':'sourceURLs'}, inplace = True)
    # contruction du data frame des caractéristiques des produits
    df_product = df[['id', 'asins', 'brand', 'categories', 'dateAdded',
           'dateUpdated', 'imageURLs', 'keys', 'manufacturer',
           'manufacturerNumber', 'name', 'primaryCategories', 'sourceURLs','weight']]
    df_product.rename(columns = {'id':'product_id'}, inplace = True)
    # écriture des fichiers sources des bases de données
    df.to_csv('bdd.csv', sep=";", index=False)
    df_price.to_csv('tb_prix.csv', sep=";", index=False)
    df_product.to_csv('tb_produits.csv', sep=";", index=False)
    return "Les fichiers sources ont été créés avec succès"

# Endpoint création de la base de données et de la tables produit et prix
@api.post("/creation_des_tables")
def create_database():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE bdd;")
        cursor.execute ("USE bdd;")
        cursor.execute('''CREATE TABLE products (
                        id INT NOT NULL AUTO_INCREMENT,
                        product_id VARCHAR(255),
                        asins VARCHAR(255),
                        brand VARCHAR(255),
                        categories VARCHAR(255),
                        dateAdded VARCHAR(255),
                        dateUpdated VARCHAR(255),
                        imageURLs VARCHAR(255),
                        keys VARCHAR(255),
                        manufacturer VARCHAR(255),
                        manufacturerNumber VARCHAR(255),
                        name VARCHAR(255),
                        primaryCategories VARCHAR(255),
                        sourceURLs VARCHAR(255),
                        weight VARCHAR(255),
                        PRIMARY KEY (id)
                        );''')
        cursor.execute('''CREATE TABLE prices (
                        id INT NOT NULL AUTO_INCREMENT,
                        product_id VARCHAR(255),
                        amountMax FLOAT,
                        amountMin FLOAT,
                        availability VARCHAR(255),
                        condition VARCHAR(255),
                        currency VARCHAR(3),
                        dateSeen DATETIME,
                        isSale VARCHAR(255),
                        merchant VARCHAR(255),
                        shipping VARCHAR(255),
                        sourceURLs VARCHAR(255),
                        PRIMARY KEY (id),
                        FOREIGN KEY (product_id) REFERENCES products(product_id)
                        );''')
        connection.commit()
        return {"success": True}
    except Exception as e:
        connection.rollback()
        return {"success": False, "error": str(e)}
    finally:
        cursor.close()
        connection.close()

# Enpoint injection des données
@api.post("/injection_des_donnees")
def load_data():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''LOAD DATA INFILE 'bdd_produits.csv'
                          INTO TABLE products
                          FIELDS TERMINATED BY ','
                          ENCLOSED BY '"'
                          LINES TERMINATED BY '\n'
                          IGNORE 1 ROWS
                          (product_id,asins,brand,categories,dateAdded,dateUpdated,imageURLs,keys,manufacturer,manufacturerNumber,name,primaryCategories,sourceURLs,weight);''')
        cursor.execute('''LOAD DATA INFILE 'bdd_prix.csv'
                          INTO TABLE prices
                          FIELDS TERMINATED BY ','
                          ENCLOSED BY '"'
                          LINES TERMINATED BY '\n'
                          IGNORE 1 ROWS
                          (product_id, amountMax, amountMin, availability, condition, currency, dateSeen, isSale, merchant, shipping, sourceURLs);''')
        connection.commit()
        return {"success": True}
    except Exception as e:
        connection.rollback()
        return {"success": False, "error": str(e)}
    finally:
        cursor.close()
        connection.close()

# Endpoint de requêtes sur la base de données:
@api.post("/requetes_sur_la_bdd")
def request_data():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''SELECT product_id, manufacturer, availability, amountMin
                       from bdd
                       INNER JOIN products.product_id=prices.product_id;''')
        connection.commit()
        return {"success": True}
    except Exception as e:
        connection.rollback()
        return {"success": False, "error": str(e)}
    finally:
        cursor.close()
        connection.close()
