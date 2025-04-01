from pymongo import MongoClient
import neo4j
import pandas as pd

from pymongo import MongoClient

def connect_mongodb_db(db_name):
    # Connexion à MongoDB
    client = MongoClient("mongodb://root:test@mongodb:27017")
    db = client[db_name]  # Connexion à la base de données
    print("Connected to MongoDB : ", db_name)
    return db  # Retourner l'objet MongoDB, pas le DataFrame ici

def connect_neo4j():
    URI = "bolt://neo4j:7687"
    AUTH = ("neo4j", "password")
    print("Connecting to Neo4j")

    with neo4j.GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("Successfully connected to Neo4j")
        return driver