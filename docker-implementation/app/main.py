from mongodb_lib import connect_mongo, clean_mongodb, import_json, display_documents
from neo4j_lib import connect_neo4j, clean_neo4j, load_csv_data
import json

# Vérification de la connexion à MongoDB
try:
    client,mongo_db = connect_mongo("mongodb://root:test@mongodb:27017", "entertainment")
    print("✅ Connexion à MongoDB réussie !")
    
    collection = mongo_db["films"]
    clean_mongodb(collection)
    
    # Importation du fichier JSON
    import_json(mongo_db, "films", "movies.json")
    
    # Vérification de l'importation en affichant les 3 premiers documents
    display_documents(mongo_db, "films")
    
    client.close()
    print("Fermeture connexion MongoDB")
    
except Exception as e:
    print(f"❌ Erreur de connexion à MongoDB : {e}")

# Vérification de la connexion à Neo4j
try:
    neo4j_driver = connect_neo4j("bolt://neo4j:7687", "neo4j", "password")
    print("✅ Connexion à Neo4j réussie !")
    
    with neo4j_driver.session() as session:
        clean_neo4j(session)
    
    # Charger les données CSV dans Neo4j
    load_csv_data(neo4j_driver, "movies.films.csv")

    print("Importation des données terminée.")
    
    neo4j_driver.close()
    print("Fermeture connexion Neo4j")
    
except Exception as e:
    print(f"❌ Erreur de connexion à Neo4j : {e}")