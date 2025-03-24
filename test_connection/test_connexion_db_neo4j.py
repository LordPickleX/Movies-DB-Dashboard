# # pip3 install neo4j-driver
# # python3 example.py

# from neo4j import GraphDatabase, basic_auth

# driver = GraphDatabase.driver(
#   "bolt://18.233.6.232:7687",
#   auth=basic_auth("neo4j", "crowd-intakes-assistance"))

# cypher_query = '''
# MATCH (n)
# RETURN COUNT(n) AS count
# LIMIT $limit
# '''

# pip3 install neo4j
# python3 example.py

from neo4j import GraphDatabase, basic_auth

# Configuration de la connexion
URI = "bolt://18.233.6.232:7687"
USERNAME = "neo4j"
PASSWORD = "crowd-intakes-assistance"

def test_connection():
    try:
        # Création du driver Neo4j
        driver = GraphDatabase.driver(URI, auth=basic_auth(USERNAME, PASSWORD))
        
        # Vérification de la connexion avec une requête simple
        with driver.session() as session:
            result = session.run("RETURN 1 AS test")
            if result.single()[0] == 1:
                print("✅ Connexion établie avec succès à Neo4j !")
        
        # Exécuter la requête Cypher
        cypher_query = '''
        MATCH (n)
        RETURN COUNT(n) AS count
        LIMIT $limit
        '''
        params = {"limit": 10}

        with driver.session() as session:
            result = session.run(cypher_query, params)
            for record in result:
                print(f"Nombre total de nœuds dans la base : {record['count']}")

    except Exception as e:
        print(f"❌ Erreur de connexion à Neo4j : {e}")

    finally:
        driver.close()
        print("🔌 Connexion fermée.")

# Exécution de la fonction
test_connection()
