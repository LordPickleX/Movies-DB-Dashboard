import streamlit as st
import time
import numpy as np

def number_of_movies():
    options = []
    for i in range(1900, 2026):
        options.append(str(i))
    start_color, end_color = st.select_slider(

        "Select a range",
        options=options,

        value=("1900", "2025"),
    )
    st.write("You selected wavelengths between", start_color, "and", end_color)




if __name__ == "__main__":
    st.title("Movie Database Admin Dashboard")
    number_of_movies()
