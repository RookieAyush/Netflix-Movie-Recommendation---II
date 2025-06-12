import streamlit as st
from recommender import recommend, fetch_poster

st.set_page_config(page_title="Netflix Recommender", layout="wide")
st.markdown("<h1 style='color:red;'>🍿 Netflix Recommendation Engine</h1>", unsafe_allow_html=True)
# Header and CSS for responsive tile layout
st.markdown("""
    <style>
    .tile-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
    }
    .movie-tile {
        position: relative;
        width: 22%;
        margin: 10px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    .movie-tile img {
        width: 100%;
        height: auto;
        border-radius: 10px;
    }
    .movie-info {
        position: absolute;
        bottom: 0;
        background: rgba(0, 0, 0, 0.85);
        color: white;
        padding: 10px;
        width: 100%;
        transform: translateY(100%);
        transition: transform 0.3s ease-in-out;
        font-size: 14px;
    }
    .movie-tile:hover .movie-info {
        transform: translateY(0);
    }
    </style>
""", unsafe_allow_html=True)

# Input
movie_input = st.text_input("Enter how you're feeling or genres you like (e.g. 'romantic comedy', 'mystery adventure')", "")

# Results
if movie_input:
    try:
        results = recommend(movie_input)

        if results.empty:
            st.error("No results found.")
        else:
            st.markdown("<div class='tile-container'>", unsafe_allow_html=True)
            for _, row in results.iterrows():
                poster_url = fetch_poster(row['title'])
                st.markdown(f"""
                    <div class='movie-tile'>
                        <img src="{poster_url}" alt="{row['title']} poster">
                        <div class='movie-info'>
                            <strong>{row['title']}</strong><br>
                            <b>Year:</b> {row['release_year']}<br>
                            <b>Genre:</b> {row['listed_in']}<br>
                            <p>{row['description'][:250]}...</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
