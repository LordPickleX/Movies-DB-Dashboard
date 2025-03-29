from pymongo import MongoClient
import neo4j


def connect_mongodb(db_name):
    client = MongoClient("mongodb://localhost:27017/")
    database_name = "project"
    collection_name = "movies"
    #db = client.movies
    db = client[db_name]
    print("Connected to MongoDB : ", db_name)
    return db

def connect_neo4j():
    URI = "neo4j+s://657cbcf3.databases.neo4j.io"
    AUTH = ("neo4j", "ztAxWgivGNDCkrawRWBE3UjG27VKlh2VRzopi2-6aZs")
    print("Connecting to Neo4j")

    with neo4j.GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("Successfully connected to Neo4j")
        return driver