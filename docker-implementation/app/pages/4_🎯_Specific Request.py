import streamlit as st
import matplotlib.pyplot as plt
from pymongo import MongoClient
from scripts import database
from scripts.mongo_queries import *
import numpy as np

global selected_question
global db
global fichier

# Une fois le dataset choisi, tu vas récupérer les collections disponibles
def get_collections(db_name):
    client = MongoClient("mongodb://root:test@mongodb:27017")
    db = client[db_name]
    return db.list_collection_names()

# Afficher les données de la collection sélectionnée
def display_collection_data(collection):
    data = pd.DataFrame(list(collection.find()))  # Récupérer toutes les données de la collection
    st.write(data)


def init():
    with st.sidebar:
        st.header("Specific Selection")
        api_options = ["None"]

        questions = [
        "Year with most movie releases",
        "Number of movies after 1999",
        "Average votes for movies in 2007",
        "Movies per year (Histogram)",
        "Available movie genres",
        "Highest revenue movie",
        "Directors with more than 5 movies",
        "Highest revenue genre (on average)",
        "Top 3 rated movies per decade",
        "Longest movie per genre",
        "View: Movies with Metascore > 80 and Revenue > 50M",
        "Correlation: Runtime vs Revenue",
        "Evolution of average movie duration per decade"
    ]

        for i in range(1,14):
            api_options.append(str(i)+") "+questions[i-1])
        #api_options = ("Question 1", "Question 2")
        global selected_question
        selected_question = st.selectbox(
            label="Choose a specific question:",
            options=api_options,
        )



        # Liste des bases de données disponibles
        db_list = ["movies", "your_other_datasets"]  # Ajoute les autres datasets ici
        # Sélectionner la base de données
        db_name = st.selectbox("Choose Database", db_list)

        # Sélectionner la collection selon la base choisie
        collection_list = get_collections(db_name)
        global fichier
        fichier = st.selectbox("Choose Collection", collection_list)

        # Connexion à la base et la collection sélectionnée
        global db
        db = database.connect_mongodb_db(db_name)






def specific_request():

    #db_name = "movies"
    #fichier = "films"
    #db = database.connect_mongodb(db_name, fichier)
    # Menu déroulant pour choisir une requête


    if selected_question == "None":
        st.write("Please select a request on left sidebar")
        return
    #query_choice = selected_question[3:]
    query_choice = selected_question.split(") ", 1)[1]
    # Exécuter la requête sélectionnée

    st.subheader(query_choice, divider=True)

    if query_choice == "Year with most movie releases":
        result = most_movies_year(db, fichier)
        st.write(f"Year with the most releases: **{result[0]['_id']}** ({result[0]['count']} movies)")

    elif query_choice == "Number of movies after 1999":
        result = count_movies_after_1999(db, fichier)
        st.write(f"Movies released after 1999: **{result}**")

    elif query_choice == "Average votes for movies in 2007":
        result = avg_votes_2007(db, fichier)
        st.write(f"Average votes for movies in 2007: **{result[0]['avg_votes']:.2f}**")

    elif query_choice == "Movies per year (Histogram)":
        data = pd.DataFrame(movies_per_year(db,fichier))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(data["_id"], data["count"])
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Movies")
        ax.set_title("Number of Movies per Year")

        st.pyplot(fig)

    elif query_choice == "Available movie genres":
        result = distinct_genres(db, fichier)
        genres = []
        #print(result)
        for i in result:
            for j in i.split(','):
                genres.append(j)
        #print(genres)
        genres = np.unique(genres)
        st.write("Genres available:", ", ".join(genres))

    elif query_choice == "Highest revenue movie":
        result = highest_revenue_movie(db,fichier)[0]
        print(result)
        st.write(f"Highest revenue movie: **{result['title']}** (${result['Revenue (Millions)']}M)")

    elif query_choice == "Directors with more than 5 movies":
        result = directors_with_more_than_5_movies(db, fichier)
        st.table(pd.DataFrame(result))

    elif query_choice == "Highest revenue genre (on average)":
        result = most_profitable_genre(db,fichier)[0]
        st.write(f"Highest earning genre on average: **{result['_id']}** (${result['avg_revenue']:.2f}M)")

    elif query_choice == "Top 3 rated movies per decade":
        result = top_movies_by_decade(db, fichier)
        for item in result:
            st.write(f"**{item['decade']}s**:")
            for movie in item['top_movies']:
                # Check if both 'title' and 'rating' are present and not None
                if 'title' in movie and 'rating' in movie and movie['title'] and movie['rating'] is not None:
                    st.write(f"- {movie['title']} ({movie['rating']}/10)")


    elif query_choice == "Longest movie per genre":

        result = distinct_genres(db, fichier)

        genres = []

        # print(result)

        for i in result:

            for j in i.split(','):
                genres.append(j)

        # print(genres)

        genres = np.unique(genres)

        result = longest_movie_by_genre(db, fichier)

        genres_dict = {}

        genres_dict2 = {}

        for genre in genres:
            genres_dict[str(genre)] = 0

            genres_dict2[str(genre)] = None

        print(result)

        for movie in result:

            for genre in movie.get("_id").split(','):

                if genres_dict.get(str(genre)) < movie.get("Runtime (Minutes)"):
                    genres_dict[str(genre)] = movie.get("Runtime (Minutes)")

                    genres_dict2[str(genre)] = movie.get("longest_film")

                # print(genre)

        print(genres_dict)

        # unite dicts

        array = []

        for i, key in enumerate(genres_dict.keys()):
            array.append({})

            array[i]["id"] = key

            array[i]["title"] = genres_dict2.get(key)

            array[i]["duration"] = genres_dict.get(key)

        df = pd.DataFrame(array)

        # df = pd.DataFrame.from_dict(genres_dict, orient='index')

        # df.rename(columns={"_id": "Genre", "longest_film": "Title", "Runtime (Minutes)": "Duration"}, inplace=True)

        df.rename(columns={"id": "Genre", "title": "Title", "duration": "Duration"}, inplace=True)

        st.table(df)


    elif query_choice == "View: Movies with Metascore > 80 and Revenue > 50M":
        result = movies_metascore_revenue(db, 80, 50,fichier)
        #print(result)
        #st.write(result)
        #st.write("View created for high-rated movies!")
        df = pd.DataFrame(result)
        df.drop("_id", axis=1, inplace=True)
        st.table(df)


    elif query_choice == "View: Movies with Metascore > 80 and Revenue > 50M":
        create_high_rated_profitable_movies_view(db, fichier)
        st.write("View created for high-rated movies!")

    elif query_choice == "Correlation: Runtime vs Revenue":
        correlation = correlation_runtime_revenue(db, fichier)
        st.write(f"Correlation coefficient (Runtime vs Revenue): **{correlation:.2f}**")

    elif query_choice == "Evolution of average movie duration per decade":
        data = pd.DataFrame(avg_runtime_by_decade(db, fichier))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data["_id"], data["avg_runtime"], marker="o")
        #ax.set_xlabel("Decade")
        #ax.set_ylabel("Movie Duration (min)")
        #ax.set_title("Average Movie Duration per Decade")
        #plt.plot(data["_id"], data["avg_runtime"], marker="o")
        plt.xlabel("Decade")
        plt.ylabel("Average Runtime (min)")
        plt.title("Average Movie Duration per Decade")
        st.pyplot(fig)


if __name__ == "__main__":
    st.title("Movie Database Specific Request")
    init()
    specific_request()
