import streamlit as st
from matplotlib import pyplot as plt
from scripts import database
from scripts.mongo_queries import *


def number_of_movies():
    options = []
    for i in range(1970, 2026):
        options.append(str(i))
    start_year, end_year = st.select_slider(

        "Select a range",
        options=options,

        value=("1970", "2025"),
    )
    st.write("You selected wavelengths between", start_year, "and", end_year)
    db = database.connect_mongodb(db_name="movies")


    fig, ax = plt.subplots()
    #st.subheader("Movies by Genre")
    #fig, ax = plt.subplots(figsize=(8, 5))
    #print(movies_per_year_range(db, start_year, end_year))
    data = pd.DataFrame(movies_per_year_range(db, start_year, end_year))
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

    result = most_movies_year_range(db, start_year, end_year)
    st.write(f"Year with the most releases: **{result[0]['_id']}** ({result[0]['count']} movies)")

    result = avg_votes_2007_range(db, start_year, end_year)
    st.write("Average votes for movies from", start_year, " to ", end_year, f": **{result[0]['avg_votes']:.2f}**")

    result = avg_score_2007_range(db, start_year, end_year)
    st.write("Average Metascore for movies from", start_year, " to ", end_year, f": **{result[0]['avg_score']:.2f}**")




if __name__ == "__main__":
    st.title("Movie Database Admin Dashboard")
    number_of_movies()
