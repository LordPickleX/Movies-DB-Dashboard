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
    db = database.connect_mongodb(db_name)

    # Input form for adding movie details
    with st.form(key="movie_form"):
        id = st.text_input("ID")
        title = st.text_input("Title")
        genre = st.text_input("Genre")
        description = st.text_input("Description")
        director = st.text_input("Director")
        actors = st.text_input("Actors (comma separated)")
        year = st.number_input("Year", min_value=1900, max_value=2025, step=1)
        runtime = st.text_input("Runtime")
        rating = st.number_input("Rating", min_value=0.0, max_value=10.0)
        votes = st.number_input("Votes")
        revenue = st.number_input("Revenue (Millions)")
        metascore = st.number_input("Metascore")

        submit_button = st.form_submit_button("Add Movie")

        if submit_button:
            film = {
                "_id": id,
                "title": title,
                "genre": genre,
                "Description": description,
                "Director": director,
                "Actors": actors.split(","),
                "year": year,
                "Runtime": runtime,
                "rating": rating,
                "Votes": votes,
                "Revenue (Millions)": revenue,
                "Metascore": metascore,
            }
            insert_movie(db, film)
            st.success("Movie added successfully!")

    # Display current movies
    st.subheader("All Movies in Database")
    #affiche_mongo(db)

    # Delete Movie section with selectable fields (ID, title, genre, etc.)
    delete_field = st.selectbox("Select Field for Deleting Movie", ["ID", "Title", "Genre"])
    delete_value = st.text_input(f"Enter {delete_field} to Delete")
    if st.button("Delete Movie"):
        if delete_value:
            if delete_field == "ID":
                delete_movie(db, delete_field,delete_value)  # Assuming ID field
            elif delete_field == "Title":
                delete_movie(db, delete_field,delete_value)  # Assuming Title field
            elif delete_field == "Genre":
                delete_movie(db, delete_field,delete_value)  # Assuming Genre field
            st.success(f"Movie with {delete_field}: '{delete_value}' deleted successfully!")
        else:
            st.warning(f"Please enter a {delete_field} to delete.")

    # Search Movie section with selectable fields (ID, title, genre, etc.)
    search_field = st.selectbox("Select Field for Searching Movie", ["ID", "Title", "Genre"])
    search_value = st.text_input(f"Enter {search_field} to Search")
    if st.button("Search Movie"):
        if search_value:
            if search_field == "ID":
                movies = find_movies(db, "_id", search_value)  # Searching by ID
            elif search_field == "Title":
                movies = find_movies(db, "title", search_value)  # Searching by Title
            elif search_field == "Genre":
                movies = find_movies(db, "genre", search_value)  # Searching by Genre
            if movies:
                st.write(f"Found {len(movies)} movie(s) matching '{search_value}':")
                for movie in movies:
                    st.write(f"**{movie['title']}** ({movie['year']})")
                    st.write(f"Genre: {movie['genre']}")
                    st.write(f"Description: {movie['Description']}")
                    st.write(f"Director: {movie['Director']}")
                    st.write(f"Actors: {movie['Actors']}")
                    st.write(f"Rating: {movie['rating']} | Votes: {movie['Votes']} | Revenue: {movie['Revenue (Millions)']}M | Metascore: {movie['Metascore']}")
            else:
                st.warning(f"No movie found with {search_field}: '{search_value}'.")
        else:
            st.warning(f"Please enter a {search_field} to search.")

    # Display movie count by genre
    genre_count = db.films.aggregate([
        {"$unwind": "$genre"},  # Handle multiple genres per movie
        {"$group": {"_id": "$genre", "count": {"$sum": 1}}}
    ])
    genre_data = pd.DataFrame(list(genre_count))

    if not genre_data.empty:
        st.subheader("Movies by Genre")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(genre_data["_id"], genre_data["count"])
        ax.set_xlabel("Genre")
        ax.set_ylabel("Count")
        ax.set_title("Number of Movies by Genre")
        ax.set_xticklabels(genre_data["_id"], rotation=90)
        st.pyplot(fig)
    else:
        st.warning("No genre data found!")
    # Menu déroulant pour choisir une requête
    query_choice: object = st.selectbox("Choose a query:", [
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
    ])

    # Exécuter la requête sélectionnée
    if query_choice == "Year with most movie releases":
        result = most_movies_year(db)
        st.write(f"Year with the most releases: **{result[0]['_id']}** ({result[0]['count']} movies)")

    elif query_choice == "Number of movies after 1999":
        result = count_movies_after_1999(db)
        st.write(f"Movies released after 1999: **{result}**")

    elif query_choice == "Average votes for movies in 2007":
        result = avg_votes_2007(db)
        st.write(f"Average votes for movies in 2007: **{result[0]['avg_votes']:.2f}**")

    elif query_choice == "Movies per year (Histogram)":
        data = pd.DataFrame(movies_per_year(db))
        plt.figure(figsize=(10, 5))
        plt.bar(data["_id"], data["count"])
        plt.xlabel("Year")
        plt.ylabel("Number of Movies")
        plt.title("Number of Movies per Year")
        st.pyplot()

    elif query_choice == "Available movie genres":
        result = distinct_genres(db)
        genres = []
        #print(result)
        for i in result:
            for j in i.split(','):
                genres.append(j)
        #print(genres)
        genres = np.unique(genres)
        st.write("Genres available:", ", ".join(genres))

    elif query_choice == "Highest revenue movie":
        result = highest_revenue_movie(db)[0]
        print(result)
        st.write(f"Highest revenue movie: **{result['title']}** (${result['Revenue (Millions)']}M)")

    elif query_choice == "Directors with more than 5 movies":
        result = directors_with_more_than_5_movies(db)
        st.table(pd.DataFrame(result))

    elif query_choice == "Highest revenue genre (on average)":
        result = most_profitable_genre(db)[0]
        st.write(f"Highest earning genre on average: **{result['_id']}** (${result['avg_revenue']:.2f}M)")

    elif query_choice == "Top 3 rated movies per decade":
        result = top_movies_by_decade(db)
        for item in result:
            st.write(f"**{item['decade']}s**:")
            for movie in item['top_movies']:
                # Check if both 'title' and 'rating' are present and not None
                if 'title' in movie and 'rating' in movie and movie['title'] and movie['rating'] is not None:
                    st.write(f"- {movie['title']} ({movie['rating']}/10)")


    elif query_choice == "Longest movie per genre":
        result = longest_movie_by_genre(db)
        df = pd.DataFrame(result)
        df.rename(columns={"_id": "Genre", "longest_film": "Title", "Runtime (Minutes)": "Duration"}, inplace=True)
        st.table(df)


    elif query_choice == "View: Movies with Metascore > 80 and Revenue > 50M":
        create_high_rated_profitable_movies_view(db)
        st.write("View created for high-rated movies!")

    elif query_choice == "Correlation: Runtime vs Revenue":
        correlation = correlation_runtime_revenue(db)
        st.write(f"Correlation coefficient (Runtime vs Revenue): **{correlation:.2f}**")

    elif query_choice == "Evolution of average movie duration per decade":
        data = pd.DataFrame(avg_runtime_by_decade(db))
        plt.figure(figsize=(10, 5))
        plt.plot(data["_id"], data["avg_runtime"], marker="o")
        plt.xlabel("Decade")
        plt.ylabel("Average Runtime (min)")
        plt.title("Average Movie Duration per Decade")
        st.pyplot()


# Neo4j: Simplified for testing
def neo4j_test():
    driver = database.connect_neo4j()
    create_genre_relationship_neo(driver, 'Star Wars', 'Action')
    print("Creation successful")



def init():
    with st.sidebar:
        st.header("Specific Selection")
        api_options = ["None"]
        for i in range(1,31):
            api_options.append("Question " + str(i))
        #api_options = ("Question 1", "Question 2")
        selected_api = st.selectbox(
            label="Choose a specific question:",
            options=api_options,
        )


# Run Streamlit application
if __name__ == "__main__":
    st.title("Movie Database Admin Dashboard")
    mongo_test()
    init()

