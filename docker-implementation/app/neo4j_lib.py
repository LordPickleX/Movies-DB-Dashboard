from neo4j import GraphDatabase

def connect_neo4j(uri, user, password):
    """ Connexion à Neo4j """
    return GraphDatabase.driver(uri, auth=(user, password))

def clean_neo4j(session):
    """Supprime tous les nœuds et relations dans Neo4j avec une session déjà ouverte"""
    # Supprimer toutes les relations
    session.run("MATCH ()-[r]->() DELETE r")
    print("Toutes les relations ont été supprimées.")
    
    # Supprimer tous les nœuds
    session.run("MATCH (n) DELETE n")
    print("Tous les nœuds ont été supprimés.")

def create_film_node(tx, film):
    """ Créer un noeud Film dans Neo4j """
    query = (
        "CREATE (f:Film {id: $id, title: $title, year: $year, votes: $votes, "
        "revenue: $revenue, rating: $rating, director: $director})"
    )
    tx.run(query, 
           id=film["_id"],
           title=film["title"], 
           year=film["year"], 
           votes=film["Votes"], 
           revenue=film["Revenue (Millions)"], 
           rating=film["rating"], 
           director=film["Director"])

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

def create_actor_node_movies(tx, actor_name, film_title):
    """Créer un noeud Actor pour chaque acteur et les relier au film spécifié"""
    tx.run("""
        MERGE (a:Actor {name: $actor_name})
        WITH a
        MATCH (f:Film {title: $film_title})
        MERGE (a)-[:ACTED_IN]->(f)
    """, actor_name=actor_name, film_title=film_title)

def create_director_node(tx, director_name):
    """ Créer un noeud Realisateur (Director) à partir du champ Director sans relation """
    tx.run("""
        MERGE (d:Director {name: $director_name})
        """, director_name=director_name)

def load_csv_data(driver, csv_file_path):
    """Charger les données du fichier CSV dans Neo4j"""
    with driver.session() as session:
        # Lire le fichier CSV et traiter chaque ligne
        with open(csv_file_path, "r", encoding="utf-8") as file:
            # Lire chaque ligne du CSV et convertir en dictionnaire
            import csv
            reader = csv.DictReader(file)
            for row in reader:
                # Créer un film
                session.write_transaction(create_film_node, row)
                
                # Créer des acteurs
                actors = row["Actors"].split(",")  # Séparer les acteurs par virgules
                for actor in actors:
                    actor_name = actor.strip()  # Supprimer les espaces inutiles
                    session.write_transaction(create_actor_node, actor_name)
                    session.write_transaction(create_actor_relationship, actor_name, row["title"])
                    # Créer des noeuds Actor et les lier au film
                    session.write_transaction(create_actor_node_movies, actor_name, row["title"])

                # Créer un réalisateur
                session.write_transaction(create_director_node, row["Director"])