from neo4j import GraphDatabase

def connect_neo4j(uri, user, password):
    """ Connexion à Neo4j """
    return GraphDatabase.driver(uri, auth=(user, password))

def create_node(driver, label, properties):
    """ Création d'un nœud dans Neo4j """
    with driver.session() as session:
        query = f"CREATE (n:{label} $props) RETURN n"
        result = session.run(query, props=properties)
        return result.single()[0]

def display_nodes(driver, label):
    """ Afficher les 3 premiers nœuds d'un type donné """
    with driver.session() as session:
        query = f"MATCH (n:{label}) RETURN n LIMIT 3"
        result = session.run(query)
        for record in result:
            print(record["n"])