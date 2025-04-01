from mongodb_lib import connect_mongo, clean_mongodb, import_json, display_documents
from neo4j_lib import connect_neo4j, clean_neo4j, execute_neo4j_query, load_csv_data
import json

# liste des querry cypher :
cypher_queries = [
    # 1. Acteur ayant joué dans le plus grand nombre de films
    """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
    RETURN a.name AS acteur, COUNT(f) AS nombre_de_films
    ORDER BY nombre_de_films DESC
    LIMIT 1
    """,

    # 2. Acteurs ayant joué dans des films où Anne Hathaway a également joué
    """
    MATCH (anne:Actor {name: "Anne Hathaway"})-[:ACTED_IN]->(f:Film)<-[:ACTED_IN]-(co_actor)
    RETURN DISTINCT co_actor.name AS acteur
    """,

    # 3. Acteur ayant joué dans des films totalisant le plus de revenus
    """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
    WITH a, SUM(f.revenue) AS total_revenu
    RETURN a.name AS acteur, total_revenu
    ORDER BY total_revenu DESC
    LIMIT 1
    """,

    # 4. Moyenne des votes
    """
    MATCH (f:Film)
    RETURN AVG(f.votes) AS moyenne_votes
    """,

    # 5. Genre le plus représenté
    """
    MATCH (f:Film)
    WITH SPLIT(f.genre, ",") AS genres
    UNWIND genres AS genre
    RETURN genre, COUNT(*) AS nombre_de_films
    ORDER BY nombre_de_films DESC
    LIMIT 1
    """,

    # 6. Films dans lesquels les acteurs ayant joué avec toi ont aussi joué
    """
    MATCH (me:Actor {name: "Votre Nom"})-[:ACTED_IN]->(f:Film)<-[:ACTED_IN]-(co_actor),
          (co_actor)-[:ACTED_IN]->(otherFilm)
    WHERE NOT (me)-[:ACTED_IN]->(otherFilm)
    RETURN DISTINCT otherFilm.title AS film_recommandé
    """,

    # 7. Réalisateur ayant travaillé avec le plus grand nombre d’acteurs distincts
    """
    MATCH (d:Director)-[:DIRECTED]->(f:Film)<-[:ACTED_IN]-(a:Actor)
    RETURN d.name AS realisateur, COUNT(DISTINCT a) AS nombre_acteurs
    ORDER BY nombre_acteurs DESC
    LIMIT 1
    """,

    # 8. Films les plus connectés (ayant le plus d’acteurs en commun avec d'autres films)
    """
    MATCH (f1:Film)<-[:ACTED_IN]-(a:Actor)-[:ACTED_IN]->(f2:Film)
    WHERE f1 <> f2
    RETURN f1.title AS film, COUNT(DISTINCT a) AS nombre_acteurs_communs
    ORDER BY nombre_acteurs_communs DESC
    LIMIT 5
    """,

    # 9. Top 5 des acteurs ayant joué avec le plus de réalisateurs différents
    """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)<-[:DIRECTED]-(d:Director)
    RETURN a.name AS acteur, COUNT(DISTINCT d) AS nombre_realisateurs
    ORDER BY nombre_realisateurs DESC
    LIMIT 5
    """,

    # 10. Recommander un film à un acteur en fonction des genres des films où il a joué
    """
    MATCH (a:Actor {name: "Nom de l'acteur"})-[:ACTED_IN]->(f:Film)
    WITH a, COLLECT(DISTINCT f.genre) AS genres_pref
    MATCH (rec:Film)
    WHERE ANY(g IN genres_pref WHERE g IN SPLIT(rec.genre, ","))
    AND NOT EXISTS {
        MATCH (a)-[:ACTED_IN]->(rec)
    }
    RETURN DISTINCT rec.title AS film_recommandé
    LIMIT 5
    """,

    # 11. Créer une relation INFLUENCE_PAR entre réalisateurs avec genres similaires
    """
    MATCH (d1:Director)-[:DIRECTED]->(f1:Film), (d2:Director)-[:DIRECTED]->(f2:Film)
    WHERE d1 <> d2 AND f1.genre = f2.genre
    MERGE (d1)-[:INFLUENCED_BY]->(d2)
    """,

    # 12. Trouver le chemin le plus court entre deux acteurs
    """
    MATCH p=shortestPath((a1:Actor {name: "Tom Hanks"})-[:ACTED_IN*]-(a2:Actor {name: "Scarlett Johansson"}))
    RETURN p
    """,

    # 13. Détection des communautés d’acteurs avec Louvain
    """
    CALL gds.louvain.stream('actor-graph')
    YIELD nodeId, communityId
    MATCH (a:Actor) WHERE id(a) = nodeId
    RETURN communityId, COLLECT(a.name) AS acteurs_par_communauté
    ORDER BY SIZE(acteurs_par_communauté) DESC
    LIMIT 5
    """
]

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
    
    for querry in cypher_queries:
        execute_neo4j_query(neo4j_driver,querry)
    
    neo4j_driver.close()
    print("Fermeture connexion Neo4j")
    
except Exception as e:
    print(f"❌ Erreur de connexion à Neo4j : {e}")