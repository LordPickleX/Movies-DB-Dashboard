import streamlit as st
from matplotlib import pyplot as plt
from scripts import database
from scripts.mongo_queries import *
from pymongo import MongoClient


with st.sidebar:
    # Liste des bases de données disponibles
    db_list = ["movies", "your_other_datasets"]  # Ajoute les autres datasets ici

    # Sélectionner la base de données
    db_name = st.selectbox("Choose Database", db_list)

    # Une fois le dataset choisi, tu vas récupérer les collections disponibles
    def get_collections(db_name):
        client = MongoClient("mongodb://root:test@mongodb:27017")
        db = client[db_name]
        return db.list_collection_names()

    # Sélectionner la collection selon la base choisie
    collection_list = get_collections(db_name)
    fichier = st.selectbox("Choose Collection", collection_list)

    # Connexion à la base et la collection sélectionnée
    db = database.connect_mongodb_db(db_name)

# Afficher les données de la collection sélectionnée
def display_collection_data(collection):
    data = pd.DataFrame(list(collection.find()))  # Récupérer toutes les données de la collection
    st.write(data)


        









def number_of_movies():
    #db = database.connect_mongodb(db_name, fichier_name)

    # db = database.connect_mongodb(db_name=db_name, fichier_name=collection)

    #print(db.head())

    #print("✅ Connexion réussie à MongoDB avec", db_name, "->", fichier_name)
    #print(db.find_one())

    options = []
    for i in range(1970, 2026):
        options.append(str(i))
    start_year, end_year = st.select_slider(

        "Select a range",
        options=options,

        value=("1970", "2025"),
    )
    st.write("You selected wavelengths between", start_year, "and", end_year)



    fig, ax = plt.subplots()
    #st.subheader("Movies by Genre")
    #fig, ax = plt.subplots(figsize=(8, 5))
    #print(movies_per_year_range(db, start_year, end_year))
    data = pd.DataFrame(movies_per_year_range(db, start_year, end_year,fichier))
    print("📊 Données récupérées :", data)  # Ajoute ce print pour voir les données
    if data.empty:
        st.write("No data available")
        return
    #plt.figure(figsize=(10, 5))
    #plt.bar(data["_id"], data["count"])
    ax.bar(data["_id"], data["count"])
    #plt.xlabel("Year")
    ax.set_xlabel("Year")
    #plt.ylabel("Number of Movies")
    ax.set_ylabel("Number of Movies")
    #plt.title("Number of Movies per Year")
    ax.set_title("Number of Movies per Year")

    st.pyplot(fig)

    result = most_movies_year_range(db, start_year, end_year,fichier)
    st.write(f"Year with the most releases: **{result[0]['_id']}** ({result[0]['count']} movies)")

    result = avg_votes_2007_range(db, start_year, end_year,fichier)
    st.write("Average votes for movies from", start_year, " to ", end_year, f": **{result[0]['avg_votes']:.2f}**")

    result = avg_score_2007_range(db, start_year, end_year,fichier)
    st.write("Average Metascore for movies from", start_year, " to ", end_year, f": **{result[0]['avg_score']:.2f}**")

    # Quel est le film qui a généré le plus de revenu.

    result = highest_revenue_movie_range(db, start_year, end_year,fichier)[0]
    print(result)
    st.write(f"Highest revenue movie: **{result['title']}** (${result['Revenue (Millions)']}M)")



if __name__ == "__main__":
    st.title("Movie Database Admin Dashboard")
    number_of_movies()
