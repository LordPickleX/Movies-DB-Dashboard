import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from bson import ObjectId
import neo4j
from scripts import database
from scripts.mongo_queries import *
from scripts.neo4j_queries import *

# MongoDB interaction in Streamlit
def mongo_test():
    db = database.connect_mongodb()

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
        plt.figure(figsize=(8, 5))
        plt.bar(genre_data["_id"], genre_data["count"])
        plt.xlabel("Genre")
        plt.ylabel("Count")
        plt.title("Number of Movies by Genre")
        st.pyplot()
    else:
        st.warning("No genre data found!")


# Neo4j: Simplified for testing
def neo4j_test():
    driver = database.connect_neo4j()
    create_genre_relationship_neo(driver, 'Star Wars', 'Action')
    print("Creation successful")


# Run Streamlit application
if __name__ == "__main__":
    st.title("Movie Database Admin Dashboard")
    mongo_test()