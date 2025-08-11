import streamlit as st
from recommender import recommend, fetch_poster

st.set_page_config(page_title="Netflix Recommender", layout="wide")
st.markdown("<h1 style='color:red;'>🍿 Netflix Recommendation Engine</h1>", unsafe_allow_html=True)
# Header and CSS for responsive tile layout
'''
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
            
    except Exception as e:
        st.error(f"Something went wrong: {e}")
'''


import math
import streamlit.components.v1 as components

# CSS (strong selectors + responsive)
css = """
<style>
.tile-container{
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 16px !important;
  width: 100%;
  box-sizing: border-box;
}
.movie-tile{
  position: relative;
  width: 100%;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0,0,0,0.12);
}
.movie-tile img{
  display: block;
  width: 100%;
  height: 260px;               /* fixed height so tiles align */
  object-fit: cover;
}
.movie-info{
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.75);
  color: #fff;
  padding: 10px;
  transform: translateY(100%);
  transition: transform 0.25s ease-in-out;
  font-size: 13px;
  box-sizing: border-box;
}
.movie-tile:hover .movie-info{
  transform: translateY(0);
}

/* responsive fallbacks */
@media (max-width: 1000px){
  .tile-container{ grid-template-columns: repeat(3, minmax(0,1fr)); }
}
@media (max-width: 700px){
  .tile-container{ grid-template-columns: repeat(2, minmax(0,1fr)); }
}
@media (max-width: 420px){
  .tile-container{ grid-template-columns: 1fr; }
}
</style>
"""

# Build the inner HTML in one go (important)
items_html = ""
for _, row in results.iterrows():
    poster_url = fetch_poster(str(row['title']))  # ensure string
    description = str(row['description']) if not pd.isna(row['description']) else ""
    items_html += f"""
    <div class="movie-tile">
      <img src="{poster_url}" alt="{str(row['title'])} poster">
      <div class="movie-info">
        <strong>{str(row['title'])}</strong><br>
        <b>Year:</b> {str(row['release_year'])}<br>
        <b>Genre:</b> {str(row['listed_in'])}<br>
        <p>{description[:200]}...</p>
      </div>
    </div>
    """


html = css + "<div class='tile-container'>" + items_html + "</div>"

# Option A: single st.markdown injection
st.markdown(html, unsafe_allow_html=True)

# Option B: more reliable — render inside a component iframe and set height
# rows = math.ceil(len(results)/4)
# height = rows * 320 + 50
# components.html(html, height=height, scrolling=True)
