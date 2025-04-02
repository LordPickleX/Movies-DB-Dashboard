import streamlit as st
import matplotlib.pyplot as plt
import neo4j
from pymongo import MongoClient
from scripts import database
from scripts.mongo_queries import *
from scripts.neo4j_queries import *
import numpy as np
import random

global selected_question
global db
global fichier

def connect_neo4j():
    URI = "bolt://neo4j:7687"
    AUTH = ("neo4j", "password")
    print("Connecting to Neo4j")

    with neo4j.GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("Successfully connected to Neo4j")
        return driver

# Une fois le dataset choisi, tu vas récupérer les collections disponibles
def get_collections(db_name):
    client = MongoClient("mongodb://root:test@mongodb:27017")
    db = client[db_name]
    return db.list_collection_names()

# Afficher les données de la collection sélectionnée
def display_collection_data(collection):
    data = pd.DataFrame(list(collection.find()))  # Récupérer toutes les données de la collection
    st.write(data)

def get_random_actor(session):
    # Récupérer tous les acteurs dans la base de données Neo4j
    query = """
    MATCH (a:Actor)
    RETURN a.name AS actor_name
    """
    result = session.run(query).data()
    
    # Sélectionner un acteur aléatoire
    actor_names = [record['actor_name'] for record in result]
    random_actor = random.choice(actor_names)
    
    return random_actor

def analyse_collaboration(collaborations):
    """Analyse les collaborations pour déterminer leur succès commercial et critique."""
    # Analyse pour déterminer s'il y a succès commercial ou critique
    for analysis in collaborations:
        if analysis["MoyenneRevenu"] > 500:  # Un seuil arbitraire pour un "grand succès commercial"
            analysis["Succès Commercial"] = "Oui"
        else:
            analysis["Succès Commercial"] = "Non"
        
        if analysis["MoyenneMetascore"] >= 70:  # Un seuil arbitraire pour un "bon score critique"
            analysis["Succès Critique"] = "Oui"
        else:
            analysis["Succès Critique"] = "Non"
    
    return collaborations




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
        "Evolution of average movie duration per decade",
        "Actor with most movie appearances",
        "Actors who have starred in movies with Anne Hathaway",
        "Actor with highest total movie revenue",
        "Average movie votes",
        "Most represented movie genre",
        "Movies featuring actors you've worked with",
        "Director with most unique actors",
        "Most connected movies (shared actors)",
        "Top 5 actors with most different directors",
        "Movie recommendation based on actor's past genres",
        "Director influence network based on genre similarities",
        "Shortest path between two actors",
        "Actor community detection (Louvain algorithm)",
        "Movies with common genres but different directors",
        "Movie recommendations based on actor's preferences",
        "Director competition based on films released in the same year",
        "Frequent collaborations between directors and actors, and their success"
    ]

        for i in range(1,31):
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
        
        neo4j_driver=connect_neo4j()
        with neo4j_driver.session() as session:
            clean_neo4j(session)
        
        # Stocker la session Neo4j dans `st.session_state`
        st.session_state.neo4j_session = neo4j_driver.session()
            
        # Charger les données CSV dans Neo4j
        load_csv_data(neo4j_driver, "data/movies.films.csv")

        print("Importation des données terminée.")






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
    
    neo4j_session = st.session_state.neo4j_session

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
        
    elif query_choice == "Actor with most movie appearances":
        result = actor_with_most_movies(neo4j_session)
        st.write(f"Actor with most appearances: **{result[0]['actor']}** ({result[0]['movie_count']} movies)")

    elif query_choice == "Actors who have starred in movies with Anne Hathaway":
        result = actors_with_anne_hathaway(neo4j_session)
        actors_list = [actor['actor'] for actor in result]
        st.write("Actors who starred with Anne Hathaway:", ", ".join(actors_list))

    elif query_choice == "Actor with highest total movie revenue":
        result = actor_with_highest_revenue(neo4j_session)
        st.write(f"Actor with highest total revenue: **{result[0]['actor']}** (${result[0]['total_revenue']}M)")

    elif query_choice == "Average movie votes":
        result = average_movie_votes(neo4j_session)
        st.write(f"Average movie votes: **{result[0]['avg_votes']:.2f}**")

    elif query_choice == "Most represented movie genre":
        result = most_represented_genre(neo4j_session)
        st.write(f"Genre le plus représenté : {result[0]['genre']} ({result[0]['count']} films)")
# vérifier l'affichage
    elif query_choice == "Movies featuring actors you've worked with":
        random_actor = get_random_actor(neo4j_session)
        result = movies_with_my_colleagues(neo4j_session, random_actor)
        movie_list = [movie['title'] for movie in result]
        st.write(f"Movies featuring actors you've worked with {random_actor} :", ", ".join(movie_list))

    elif query_choice == "Director with most unique actors":
        result = director_with_most_unique_actors(neo4j_session)
        st.write(f"Director with most unique actors: **{result[0]['director']}** ({result[0]['actor_count']} actors)")

    elif query_choice == "Most connected movies (shared actors)":
        result = most_connected_movies(neo4j_session)
        st.table(pd.DataFrame(result))

    elif query_choice == "Top 5 actors with most different directors":
        result = top_5_actors_with_most_directors(neo4j_session)
        st.table(pd.DataFrame(result))

    elif query_choice == "Movie recommendation based on actor's past genres":
        random_actor = get_random_actor(neo4j_session)  # Sélectionne un acteur aléatoire
        result = recommend_movie_for_actor(neo4j_session, random_actor)

        # Extraire les titres des films recommandés
        movie_titles = [movie['recommended_movie'] for movie in result]
        st.write(f"Recommended movies for {random_actor}:", ", ".join(movie_titles))

    elif query_choice == "Director influence network based on genre similarities":
        result = create_influence_relationship(neo4j_session)
        st.write("Director influence relationships have been created.")

    elif query_choice == "Shortest path between two actors":
        result = shortest_path_between_actors(neo4j_session, "Tom Hanks", "Scarlett Johansson")
        # Prendre le premier chemin s'il y en a plusieurs
        first_path = result[0]["path"]  

        # Filtrer les valeurs NULL (relations) et ne garder que les noms des acteurs
        cleaned_path = [node for node in first_path if node is not None]

        # Afficher sous forme de flèche
        st.write(f"Shortest path: {' → '.join(cleaned_path)}")

    elif query_choice == "Actor community detection (Louvain algorithm)":
        result = detect_actor_communities(neo4j_session)

        # Afficher sous forme de tableau avec Streamlit
        st.write("### Actor Community Detection (Louvain Algorithm)")
        st.table([{"Actor": record["actor"], "Community ID": record["communityId"]} for record in result])
        
    elif query_choice == "Movies with common genres but different directors":
        result = get_movies_with_common_genres_but_different_directors(neo4j_session)
        formatted_result = [{"Film 1": record["Film1"], 
                        "Director 1": record["Director1"], 
                        "Film 2": record["Film2"], 
                        "Director 2": record["Director2"], 
                        "Genre": record["Genre"]} for record in result]
        st.write("Movies with Common Genres but Different Directors")
        st.table(formatted_result)
        
    elif query_choice == "Movie recommendations based on actor's preferences":
        random_actor = get_random_actor(neo4j_session)  # Sélectionne un acteur aléatoire
        result = recommend_movies_based_on_actor(neo4j_session, random_actor)
        formatted_result = [{"Recommended_Film": record["Recommended_Film"], 
             "Genre": record["Genre"], 
             "Actor": record["Actor"]} for record in result]
        st.write(f"Recommended Movies for Actor: {random_actor}")
        st.table(formatted_result)

    elif query_choice == "Director competition based on films released in the same year":
        result = create_director_competition(neo4j_session)
        st.write(result)

    elif query_choice == "Frequent collaborations between directors and actors, and their success":
        result = collaborations_frequentes(neo4j_session)
        formatted_result = [{"Acteur": record["Acteur"],
                            "Realisateur": record["Realisateur"], 
                            "Films": record["Films"], 
                            "MoyenneRevenu": record["MoyenneRevenu"], 
                            "MoyenneMetascore": record["MoyenneMetascore"]} 
                            for record in result]
        analyse=analyse_collaboration(formatted_result)
        st.write("Frequent Collaborations Between Directors and Actors and Their Success")
        st.table(analyse)



if __name__ == "__main__":
    st.title("Movie Database Specific Request")
    init()
    specific_request()
