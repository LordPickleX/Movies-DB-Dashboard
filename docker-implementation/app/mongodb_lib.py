from pymongo import MongoClient
import json

def connect_mongo(uri, db_name):
    """ Connexion à MongoDB """
    client = MongoClient(uri)
    return client,client[db_name]

def clean_mongodb(collection):
    """Supprime toutes les données d'une collection MongoDB déjà connectée"""
    # Supprimer toutes les données dans la collection
    result = collection.delete_many({})
    
    print(f"{result.deleted_count} documents supprimés de la collection.")

def import_json(db, collection_name, json_file):
    """Importer un fichier JSON dans une collection MongoDB en gérant les erreurs de format"""
    try:
        collection = db[collection_name]
        # clean_mongodb(collection)
        with open(json_file, 'r', encoding='utf-8') as file:
            first_char = file.read(1)
            file.seek(0)  # Revenir au début du fichier

            if first_char == "[":  
                # Cas où le JSON est une liste
                data = json.load(file)
                collection.insert_many(data)
            else:
                # Lire ligne par ligne (pour JSON mal formé)
                data = []
                for line in file:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"⚠️ Ligne ignorée (JSON invalide) : {line.strip()} -> {e}")

                if data:
                    collection.insert_many(data)
                    print(f"✅ Importation réussie de {len(data)} documents dans '{collection_name}' !")
                else:
                    print("❌ Aucun document valide n'a été importé.")

    except Exception as e:
        print(f"❌ Erreur lors de l'importation JSON : {e}")

def display_documents(db, collection_name, limit=3):
    """Afficher les X premiers documents d'une collection MongoDB"""
    try:
        collection = db[collection_name]
        documents = collection.find().limit(limit)
        print(f"📌 Affichage des {limit} premiers documents de '{collection_name}':")
        for doc in documents:
            print(doc)
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage des documents : {e}")