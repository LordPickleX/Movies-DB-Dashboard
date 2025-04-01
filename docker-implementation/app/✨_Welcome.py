import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from bson import ObjectId
import neo4j
from scripts import database
from scripts.mongo_queries import *
from scripts.neo4j_queries import *
import numpy as np

# MongoDB interaction in Streamlit

def mongo_test():

    db_name = "movies"
    db = database.connect_mongodb_db(db_name)
    if db is None:
        st.subheader("Unable to connect to MangoDB database", divider="red")
    else:
        st.subheader("Connected to MangoDB database !", divider="green")



# Neo4j: Simplified for testing
def neo4j_test():
    driver = database.connect_neo4j()
    create_genre_relationship_neo(driver, 'Star Wars', 'Action')
    print("Creation successful")






# Run Streamlit application
if __name__ == "__main__":
    st.title("Welcome to Movies DB Dashboard !")
    mongo_test()

