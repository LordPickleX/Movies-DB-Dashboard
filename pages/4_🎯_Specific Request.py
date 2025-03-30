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

global selected_question

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

def specific_request():

    db_name = "movies"
    db = database.connect_mongodb(db_name)
    # Menu déroulant pour choisir une requête


    if selected_question == "None":
        st.write("Please select a request on left sidebar")
        return
    query_choice = selected_question[3:]
    # Exécuter la requête sélectionnée

    st.subheader(query_choice, divider=True)

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
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(data["_id"], data["count"])
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Movies")
        ax.set_title("Number of Movies per Year")

        st.pyplot(fig)

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


if __name__ == "__main__":
    st.title("Movie Database Specific Request")
    init()
    specific_request()
