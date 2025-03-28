from pymongo import MongoClient
import json

def connect_mongo(uri, db_name):
    """ Connexion à MongoDB """
    client = MongoClient(uri)
    return client[db_name]

def import_json(db, collection_name, json_file):
    """ Importer un fichier JSON dans une collection MongoDB """
    collection = db[collection_name]
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)
    print(f"Importation réussie dans la collection '{collection_name}'.")

def display_documents(db, collection_name, limit=3):
    """ Afficher les 3 premiers documents d'une collection """
    collection = db[collection_name]
    for doc in collection.find().limit(limit):
        print(doc)