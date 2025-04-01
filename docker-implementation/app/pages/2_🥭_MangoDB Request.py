import streamlit as st
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
        try:
            client = MongoClient("mongodb://root:test@mongodb:27017")
        except Exception as e:
            print(f"❌ Erreur de connexion à MongoDB : {e}")
        db = client[db_name]
        return db.list_collection_names(),db

    # Sélectionner la collection selon la base choisie
    collection_list,mongo_db = get_collections(db_name)
    
    clean_mongodb(mongo_db["films"])
    import_json(mongo_db,"films","data/movies.json")
    
    fichier = st.selectbox("Choose Collection", collection_list)

    # Connexion à la base et la collection sélectionnée
    collection = database.connect_mongodb_db(db_name)

# Afficher les données de la collection sélectionnée
def display_collection_data(collection):
    data = pd.DataFrame(list(collection.find()))  # Récupérer toutes les données de la collection
    st.write(data)


def mongo_test():
    db = database.connect_mongodb_db(db_name)
    info_mongo(db)

    st.subheader(f"Displaying Data from {fichier} Collection")
    display_collection_data(db[fichier])


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
            insert_movie(db,fichier ,film)
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
                delete_movie(db, delete_field,delete_value,fichier)  # Assuming ID field
            elif delete_field == "Title":
                delete_movie(db, delete_field,delete_value,fichier)  # Assuming Title field
            elif delete_field == "Genre":
                delete_movie(db, delete_field,delete_value,fichier)  # Assuming Genre field
            st.success(f"Movie with {delete_field}: '{delete_value}' deleted successfully!")
        else:
            st.warning(f"Please enter a {delete_field} to delete.")

    # Search Movie section with selectable fields (ID, title, genre, etc.)
    search_field = st.selectbox("Select Field for Searching Movie", ["ID", "Title", "Genre"])
    search_value = st.text_input(f"Enter {search_field} to Search")
    if st.button("Search Movie"):
        if search_value:
            if search_field == "ID":
                movies = find_movies(db, "_id", search_value, fichier)  # Searching by ID
            elif search_field == "Title":
                movies = find_movies(db, "title", search_value, fichier)  # Searching by Title
            elif search_field == "Genre":
                movies = find_movies(db, "genre", search_value, fichier)  # Searching by Genre
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


if __name__ == "__main__":
    st.title("MangoDB Database Request ")
    mongo_test()