import json
from pymongo import MongoClient

# Remplacez par votre URI MongoDB Atlas
uri = "mongodb+srv://user_test:s1bAihIRaBXuUCdL@projetnosql.tv8d9.mongodb.net/?appName=projetnosql"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Sélection de la base de données et de la collection
db = client["nom_de_votre_base"]  # Remplacez par votre base de données
collection = db["nom_de_votre_collection"]  # Remplacez par votre collection

# Charger les données du fichier JSON
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # Charger le JSON en tant que liste de dictionnaires

# Insérer les données dans MongoDB
if isinstance(data, list):  # Vérifie si le fichier contient une liste de documents
    result = collection.insert_many(data)
    print(f"{len(result.inserted_ids)} documents insérés avec succès !")
else:
    result = collection.insert_one(data)
    print(f"Document inséré avec l'ID : {result.inserted_id}")

# Fermer la connexion
client.close()
