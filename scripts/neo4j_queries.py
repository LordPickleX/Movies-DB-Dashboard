
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