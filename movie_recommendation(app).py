import pandas as pd
import numpy as np
from pickle import load
import streamlit as st

# Load Data
path = r"D:\DATA SCIENCE CLASS\Machine Learning\Recommendation model (Netflix)\Netflix\clean_movie.pkl"
movie_detail = load(open(path, "rb"))

path_sim = r"D:\DATA SCIENCE CLASS\Machine Learning\Recommendation model (Netflix)\Netflix\similarity.pkl"
similarity = load(open(path_sim, "rb"))

# Define functions
def get_show_details_by_title(df, title):
    result = df[df['title'] == title]
    if result.empty:
        return []  # Return an empty list if no match is found
    else:
        details = []
        for _, row in result.iterrows():
            details.append({
                "Show ID": row['show_id'],
                "Type": row["type"],
                "Description": row['description'],
                "Cast": row['cast'],
                "Genre": row['listed_in']
            })
        return details


def recommend(movie_name, movies):
    try:
        # Get the index of the given movie
        movie_index = movies[movies["title"] == movie_name].index[0]
        
        # Get the similarity scores for the selected movie
        distances = similarity[movie_index]
        
        # Sort movies by similarity scores in descending order
        sorted_similar_movies = sorted(
            list(enumerate(distances)), key=lambda x: x[1], reverse=True
        )
        
        # Prepare a list of recommended movie titles
        recommended_movies = []
        for i, (index, _) in enumerate(sorted_similar_movies[1:11], start=1):  # Skip the first entry (itself)
            title = movies.iloc[index]["title"]
            recommended_movies.append(title)
        
        return recommended_movies
    
    except IndexError:
        return [f"Error: The movie '{movie_name}' was not found in the dataset."]


# Streamlit App
st.title("Movie Recommendation System")
st.header("A Machine Learning Project")
st.subheader("Recommendation Engine")
st.info("This project is a recommendation engine which will recommend you movies as per your search.")

# Dropdown menu for movie selection
selected_movie = st.selectbox("Movie you want to watch", movie_detail["title"].values)

# Search Button
if st.button("Search"):
    search_results = get_show_details_by_title(movie_detail, selected_movie)
    
    if not search_results:
        st.error(f"No details found for the movie '{selected_movie}'.")
    else:
        # Store in session state for the next step
        st.session_state.search_done = True
        st.session_state.search_results = search_results  # Store search details
        st.write("Details of the selected movie:")
        for result in search_results:
            st.write(f"**Show ID**: {result['Show ID']}")
            st.write(f"**Type**: {result['Type']}")
            st.write(f"**Description**: {result['Description']}")
            st.write(f"**Cast**: {result['Cast']}")
            st.write(f"**Genre**: {result['Genre']}")
            st.write("-" * 50)
            
# Display search results if they exist in session state
if st.session_state.get("search_done", False):
    st.write("Details of the selected movie (stored):")
    for result in st.session_state.get("search_results", []):
        st.write(f"**Show ID**: {result['Show ID']}")
        st.write(f"**Type**: {result['Type']}")
        st.write(f"**Description**: {result['Description']}")
        st.write(f"**Cast**: {result['Cast']}")
        st.write(f"**Genre**: {result['Genre']}")
        st.write("-" * 50)
        
    st.subheader("Hey!! Need some Recommendation, What to watch next")        
    if st.button("Recommend"):
        st.session_state.recommended_results = recommend(selected_movie, movie_detail)

# Show Recommendations
if "recommended_results" in st.session_state and st.session_state.recommended_results:
    selected_movie_from_recommendations = st.selectbox(
        "Choose a recommended movie", st.session_state.recommended_results
    )
    
    # Show details of the selected movie
    if st.button("Details of Recommended Movie"):
        detail_results = get_show_details_by_title(movie_detail, selected_movie_from_recommendations)
        
        if not detail_results:
            st.error(f"No details found for the movie '{selected_movie_from_recommendations}'.")
        else:
            st.write("Details of the recommended movie:")
            for j in detail_results:
                st.write(f"**Show ID**: {j['Show ID']}")
                st.write(f"**Type**: {j['Type']}")
                st.write(f"**Description**: {j['Description']}")
                st.write(f"**Cast**: {j['Cast']}")
                st.write(f"**Genre**: {j['Genre']}")
                st.write("-" * 50)

st.text("by~ Rahul Prasad")
st.markdown(":sunglasses:")

