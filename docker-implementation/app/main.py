from mongodb_lib import connect_mongo
from neo4j_lib import connect_neo4j

# Vérification de la connexion à MongoDB
try:
    mongo_db = connect_mongo("mongodb://localhost:27017", "test_db")
    print("✅ Connexion à MongoDB réussie !")
except Exception as e:
    print(f"❌ Erreur de connexion à MongoDB : {e}")

# Vérification de la connexion à Neo4j
try:
    neo4j_driver = connect_neo4j("bolt://localhost:7687", "neo4j", "password")
    print("✅ Connexion à Neo4j réussie !")
    neo4j_driver.close()
except Exception as e:
    print(f"❌ Erreur de connexion à Neo4j : {e}")