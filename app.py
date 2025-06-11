'''import streamlit as st
from recommender import recommend, fetch_poster
import math

st.set_page_config(page_title="Netflix Recommender", layout="wide")
st.markdown("<h1 style='color:red;'>🍿 Netflix Recommendation Engine</h1>", unsafe_allow_html=True)

# CSS for hover effects
st.markdown("""
    <style>
    .container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 20px;
    }

    .card {
        position: relative;
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
    }

    .card:hover {
        transform: scale(1.05);
    }

    .poster {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 10px;
    }

    .overlay {
        position: absolute;
        bottom: 0;
        background: rgba(0,0,0,0.8);
        color: white;
        width: 100%;
        transform: translateY(100%);
        transition: transform 0.3s ease;
        padding: 10px;
        font-size: 12px;
    }

    .card:hover .overlay {
        transform: translateY(0%);
    }

    .title {
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Year filter
year = st.slider("Filter by Release Year", min_value=1940, max_value=2025, value=(2010, 2025))

# Input
movie_input = st.text_input("Enter a Netflix title or genre (e.g., Action, Comedy)", "")

if movie_input:
    results = recommend(movie_input)

    if len(results) == 0:
        st.error("Sorry, no matching results found.")
    else:
        results = results[(results['release_year'] >= year[0]) & (results['release_year'] <= year[1])]

        if results.empty:
            st.warning("No titles found for the selected year range.")
        else:
            st.success("Hover over posters to reveal info:")
            html_output = '<div class="container">'
            for _, row in results.iterrows():
                poster = fetch_poster(row['title'])
                title = row['title']
                year = row.get('release_year', 'N/A')
                genre = row['listed_in']
                desc = row['description'][:150] + "..." if row['description'] else "No description"

                html_output += f"""
                <div class="card">
                    <img src="{poster}" alt="{title}" class="poster">
                    <div class="overlay">
                        <div class="title">{title}</div>
                        <div><b>Year:</b> {year}</div>
                        <div><b>Genre:</b> {genre}</div>
                        <div>{desc}</div>
                    </div>
                </div>
                """

            html_output += '</div>'
            st.markdown(html_output, unsafe_allow_html=True) '''




# app.py
import streamlit as st
from recommender import recommend, fetch_poster

st.set_page_config(page_title="Netflix Recommender", layout="wide")
st.markdown("""
    <h1 style='color:red;'>🍿 Netflix Recommendation Engine</h1>
    <style>
    .movie-tile {
        position: relative;
        text-align: center;
        margin: 10px;
        width: 200px;
        display: inline-block;
    }
    .movie-tile img {
        width: 100%;
        height: auto;
        border-radius: 10px;
        transition: 0.3s;
    }
    .movie-info {
        display: none;
        position: absolute;
        background: rgba(0, 0, 0, 0.75);
        color: white;
        padding: 10px;
        border-radius: 10px;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow-y: auto;
    }
    .movie-tile:hover .movie-info {
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

movie_input = st.text_input("Enter a Netflix title, genre, or year", "")

if movie_input:
    try:
        results = recommend(movie_input)
        if results.empty:
            st.error("No results found.")
        else:
            st.markdown("<div style='display: flex; flex-wrap: wrap;'>", unsafe_allow_html=True)
            for _, row in results.iterrows():
                poster_url = fetch_poster(row['title'])
                st.markdown(f"""
                    <div class='movie-tile'>
                        <img src='{poster_url}' alt='Poster'>
                        <div class='movie-info'>
                            <h4>{row['title']}</h4>
                            <p><b>Year:</b> {row['release_year']}</p>
                            <p><b>Genre:</b> {row['listed_in']}</p>
                            <p>{row['description'][:300]}...</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")
