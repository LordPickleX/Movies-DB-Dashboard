
"""
def create_actor_relationship_neo(driver, movie_title, genre_name):
    with driver.session() as session:
        session.run("
            MATCH (m:Movie {title: $movie_title})
            MERGE (a:Genre {name: $genre_name})
            MERGE (a)-[:ACTED_IN]->(m)
        " movie_title=movie_title, genre_name=genre_name)

"""
def create_genre_relationship_neo(driver, movie_title, genre_name):
    toto,coco =driver.execute_query(
        "MATCH (p:Person {age: $age}) RETURN p.name AS name",
        age=42,
        database_="neo4j",
    )
    
def clean_neo4j(session):
    """Supprime tous les nœuds et relations dans Neo4j avec une session déjà ouverte"""
    # Supprimer toutes les relations
    session.run("MATCH ()-[r]->() DELETE r")
    print("Toutes les relations ont été supprimées.")
    
    # Supprimer tous les nœuds
    session.run("MATCH (n) DELETE n")
    print("Tous les nœuds ont été supprimés.")
    
def execute_neo4j_query(driver, query):
    """Exécute une requête Cypher sur Neo4j"""
    with driver.session() as session:
        result = session.run(query, {})
        return [record.data() for record in result]

def create_film_node(tx, film):
    """ Créer un noeud Film dans Neo4j """
    query = (
        "CREATE (f:Film {id: $id, title: $title, year: $year, votes: $votes, "
        "revenue: $revenue, rating: $rating, director: $director, metascore: $metascore})"
    )
    tx.run(query, 
           id=film["_id"],
           title=film["title"], 
           year=film["year"], 
           votes=film["Votes"], 
           revenue=film["Revenue (Millions)"], 
           rating=film["rating"], 
           director=film["Director"],
           metascore=film["Metascore"])

def create_actor_node(tx, actor_name):
    """ Créer un noeud Actor dans Neo4j """
    query = "CREATE (a:Actor {name: $name})"
    tx.run(query, name=actor_name)

def create_actor_relationship(tx, actor_name, film_title):
    """ Créer une relation 'A joué' entre un acteur et un film """
    query = (
        "MATCH (a:Actor {name: $actor_name}), (f:Film {title: $film_title}) "
        "MERGE (a)-[:ACTED_IN]->(f)"
    )
    tx.run(query, actor_name=actor_name, film_title=film_title)

def create_actor_node_movies(tx):
    """Créer des noeuds de type Actor pour tous les membres du projet et les relier au film spécifié."""
    # Liste des acteurs à ajouter
    actors = ["Vincent VACCAREZZA", "Erwan BRETECHER", "Evan THIBAULT"]
    film_title = "Guardians of the Galaxy"  # Le film de notre choix
    
    for actor_name in actors:
        tx.run("""
            MERGE (a:Actor {name: $actor_name})  // Créer ou trouver l'acteur
            WITH a
            MATCH (f:Film {title: $film_title})  // Trouver le film par son titre
            MERGE (a)-[:ACTED_IN]->(f)  // Créer une relation ACTED_IN entre l'acteur et le film
        """, actor_name=actor_name, film_title=film_title)

def create_director_node(tx, director_name):
    """ Créer un noeud Realisateur (Director) à partir du champ Director sans relation """
    tx.run("""
        MERGE (d:Director {name: $director_name})
        """, director_name=director_name)
    
def create_director_relationship(tx, director_name, film_title):
    """Créer la relation DIRECTED entre un réalisateur et un film"""
    query = """
    MATCH (d:Director {name: $director_name}), (f:Film {title: $film_title})
    MERGE (d)-[:DIRECTED]->(f)
    """
    tx.run(query, director_name=director_name, film_title=film_title)
    
def create_genre_relationship(tx, film_title, genres):
    """Créer et relier les genres aux films"""
    query = """
    MATCH (f:Film {title: $film_title})
    UNWIND $genres AS genre
    MERGE (g:Genre {name: genre})
    MERGE (f)-[:BELONGS_TO]->(g)
    """
    tx.run(query, film_title=film_title, genres=genres)

def load_csv_data(driver, csv_file_path):
    """Charger les données du fichier CSV dans Neo4j"""
    with driver.session() as session:
        
        session.write_transaction(create_actor_node_movies)
        
        # Lire le fichier CSV et traiter chaque ligne
        with open(csv_file_path, "r", encoding="utf-8") as file:
            # Lire chaque ligne du CSV et convertir en dictionnaire
            import csv
            reader = csv.DictReader(file)
            for row in reader:
                film_title = row["title"].strip()

                # Créer le film
                session.write_transaction(create_film_node, row)
                
                # Ajouter les genres du film
                # Nettoyage et séparation des genres
                genres = [genre.strip() for genre in row["genre"].split(",")]
    
                for genre_name in genres:
                    genre = [g.strip() for g in genres]  # Nettoyage des espaces
                    session.write_transaction(create_genre_relationship, film_title, genre)

                # Ajouter les acteurs et leurs relations avec le film
                actors = row["Actors"].split(",")
                for actor in actors:
                    actor_name = actor.strip()
                    if actor_name:  # Éviter les valeurs vides
                        session.write_transaction(create_actor_node, actor_name)
                        session.write_transaction(create_actor_relationship, actor_name, film_title)

                # Ajouter le réalisateur et sa relation avec le film
                director_name = row["Director"].strip()
                if director_name:
                    session.write_transaction(create_director_node, director_name)
                    session.write_transaction(create_director_relationship, director_name, film_title)
                
                
                
                
# Fonctions pour les question neo4j

def actor_with_most_movies(session):
    query = """
    MATCH (a:Actor)
    RETURN a.name AS actor, COUNT { (a)-[:ACTED_IN]->(:Film) } AS movie_count
    ORDER BY movie_count DESC
    LIMIT 1
    """
    return session.run(query).data()

def actors_with_anne_hathaway(session):
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)<-[:ACTED_IN]-(anne:Actor {name: 'Anne Hathaway'})
    RETURN DISTINCT a.name AS actor
    """
    return session.run(query).data()

def actor_with_highest_revenue(session):
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
    WHERE f.revenue IS NOT NULL
    RETURN a.name AS actor, SUM(toInteger(f.revenue)) AS total_revenue
    ORDER BY total_revenue DESC
    LIMIT 1
    """
    return session.run(query).data()

def average_movie_votes(session):
    query = """
    MATCH (f:Film)
    WHERE f.votes IS NOT NULL
    RETURN AVG(toInteger(f.votes)) AS avg_votes
    """
    return session.run(query).data()

def most_represented_genre(session):
    """Retourne le genre de film le plus représenté dans la base Neo4j."""
    query = """
    MATCH (f:Film)-[:BELONGS_TO]->(g:Genre)
    RETURN g.name AS genre, COUNT(f) AS count
    ORDER BY count DESC
    LIMIT 1
    """
    return session.run(query).data()

def movies_with_my_colleagues(session, my_name):
    query = """
    MATCH (me:Actor {name: $my_name})-[:ACTED_IN]->(f1:Film)<-[:ACTED_IN]-(colleague:Actor),
          (colleague)-[:ACTED_IN]->(f2:Film)
    WHERE NOT (me)-[:ACTED_IN]->(f2)
    RETURN DISTINCT f2.title AS title
    """
    return session.run(query, my_name=my_name).data()

def director_with_most_unique_actors(session):    
    query = """
    MATCH (d:Director)-[:DIRECTED]->(f:Film)<-[:ACTED_IN]-(a:Actor)
    RETURN d.name AS director, COUNT(DISTINCT a) AS actor_count
    ORDER BY actor_count DESC
    LIMIT 1
    """  
    return session.run(query).data()

def most_connected_movies(session):
    query = """
    MATCH (f:Film)<-[:ACTED_IN]-(a:Actor)-[:ACTED_IN]->(other:Film)
    WHERE f <> other
    RETURN f.title AS movie, COUNT(DISTINCT other) AS connections
    ORDER BY connections DESC
    """
    return session.run(query).data()

def top_5_actors_with_most_directors(session):
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)<-[:DIRECTED]-(d:Director)
    RETURN a.name AS actor, COUNT(DISTINCT d) AS director_count
    ORDER BY director_count DESC
    LIMIT 5
    """
    return session.run(query).data()

def recommend_movie_for_actor(session, actor_name):
    """Recommande des films à un acteur en fonction des genres des films dans lesquels il a joué."""
    query = """
    MATCH (a:Actor {name: $actor_name})-[:ACTED_IN]->(f:Film)-[:BELONGS_TO]->(g:Genre),
          (other_f:Film)-[:BELONGS_TO]->(g)
    WHERE NOT (a)-[:ACTED_IN]->(other_f)
    RETURN DISTINCT other_f.title AS recommended_movie, COUNT(g) AS common_genres
    ORDER BY common_genres DESC
    LIMIT 5
    """
    result = session.run(query, actor_name=actor_name).data()
    return result

def create_influence_relationship(session):
    """Crée une relation INFLUENCED_BY entre réalisateurs partageant au moins 2 genres en commun."""
    query = """
    MATCH (d1:Director)-[:DIRECTED]->(f1:Film)-[:BELONGS_TO]->(g:Genre),
          (d2:Director)-[:DIRECTED]->(f2:Film)-[:BELONGS_TO]->(g)
    WHERE d1 <> d2
    WITH d1, d2, COUNT(DISTINCT g) AS shared_genres
    WHERE shared_genres >= 2
    MERGE (d1)-[:INFLUENCED_BY]->(d2)
    """
    session.run(query)

def shortest_path_between_actors(session, actor1, actor2):
    query = """
    MATCH p=shortestPath((a1:Actor {name: $actor1})-[:ACTED_IN*]-(a2:Actor {name: $actor2}))
    RETURN [n IN nodes(p) | n.name] AS path
    """
    return session.run(query, actor1=actor1, actor2=actor2).data()

def detect_actor_communities(session):
    """Détecte les communautés d'acteurs en utilisant l'algorithme Louvain de Neo4j GDS."""
    create_graph_query = """
    CALL gds.graph.project(
        'myGraph',
        ['Actor', 'Film'],
        {ACTED_IN: {orientation: 'UNDIRECTED'}}
    )
    """
    session.run(create_graph_query)

    louvain_query = """
    CALL gds.louvain.stream('myGraph')
    YIELD nodeId, communityId
    MATCH (a:Actor) WHERE id(a) = nodeId
    RETURN a.name AS actor, communityId
    ORDER BY communityId
    """
    result = session.run(louvain_query)
    
    return [record for record in result]

def get_movies_with_common_genres_but_different_directors(session):
    """Retourne les films ayant des genres en commun mais des réalisateurs différents."""
    query = """
    MATCH (f1:Film)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(f2:Film),
          (d1:Director)-[:DIRECTED]->(f1),
          (d2:Director)-[:DIRECTED]->(f2)
    WHERE f1 <> f2 AND d1 <> d2 
    RETURN f1.title AS Film1, d1.name AS Director1, 
           f2.title AS Film2, d2.name AS Director2, 
           g.name AS Genre
    LIMIT 100
    """
    return session.run(query)

def recommend_movies_based_on_actor(session, acteur="Chris Pratt"):
    query = """
    MATCH (a:Actor {name: $acteur})-[:ACTED_IN]->(f:Film)<-[:BELONGS_TO]->(g:Genre)
    WITH DISTINCT a, collect(DISTINCT g.name) AS genres_pref
    UNWIND genres_pref AS genre
    MATCH (rec:Film)<-[:BELONGS_TO]->(g2:Genre)
    WHERE g2.name = genre AND NOT EXISTS {
        MATCH (a)-[:ACTED_IN]->(rec)
    }
    RETURN DISTINCT rec.title AS Recommended_Film, genre AS Genre, a.name AS Actor
    LIMIT 10
    """
    
    # Exécution de la requête dans la session
    return session.run(query, {"acteur": acteur})

def create_director_competition(session):
    """Créer une relation de 'concurrence' entre les réalisateurs ayant réalisé des films similaires la même année."""
    query = """
    MATCH (r1:Director)-[:DIRECTED]->(f1:Film)<-[:BELONGS_TO]->(g1:Genre),
          (r2:Director)-[:DIRECTED]->(f2:Film)<-[:BELONGS_TO]->(g2:Genre)
    WHERE r1 <> r2 AND g1.name = g2.name AND f1.year = f2.year
    MERGE (r1)-[:CONCURRENCE]->(r2)
    """
    
    # Exécution de la requête dans la session
    session.run(query)
    return "Concurrence relationships have been created between directors."

def collaborations_frequentes(session):
    """Exécute la requête pour récupérer les collaborations fréquentes entre un acteur et un réalisateur."""
    query = """
    MATCH (r:Director)-[:DIRECTED]->(f:Film)<-[:ACTED_IN]-(a:Actor)
    WHERE f.revenue IS NOT NULL AND f.metascore IS NOT NULL  
    AND trim(f.revenue) <> "" AND trim(f.metascore) <> ""
    WITH r.name AS Realisateur, f.title AS Film, 
        toFloat(f.revenue) AS Revenu, toFloat(f.metascore) AS Metascore, a.name AS Acteur
    WHERE Revenu IS NOT NULL AND Metascore IS NOT NULL
    RETURN Acteur, Realisateur, COLLECT(DISTINCT Film) AS Films, 
        AVG(Revenu) AS MoyenneRevenu, 
        AVG(Metascore) AS MoyenneMetascore
    ORDER BY MoyenneRevenu DESC
    LIMIT 100
    """
    
    return session.run(query)