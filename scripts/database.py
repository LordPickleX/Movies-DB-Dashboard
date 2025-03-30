from pymongo import MongoClient
import neo4j
import pandas as pd

from pymongo import MongoClient

def connect_mongodb_db(db_name):
    # Connexion à MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]  # Connexion à la base de données
    print("Connected to MongoDB : ", db_name)
    return db  # Retourner l'objet MongoDB, pas le DataFrame ici

def connect_neo4j():
    URI = "neo4j+s://657cbcf3.databases.neo4j.io"
    AUTH = ("neo4j", "ztAxWgivGNDCkrawRWBE3UjG27VKlh2VRzopi2-6aZs")
    print("Connecting to Neo4j")

    with neo4j.GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("Successfully connected to Neo4j")
        return driver