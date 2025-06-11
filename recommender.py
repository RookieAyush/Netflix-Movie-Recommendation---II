import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Load data
df = pd.read_csv('netflix_titles.csv')
df['description'] = df['description'].fillna('')
df['listed_in'] = df['listed_in'].fillna('')
df['release_year'] = df['release_year'].fillna(0).astype(str)
df['text'] = df['title'] + ' ' + df['description'] + ' ' + df['listed_in'] + ' ' + df['release_year']

# Generate BERT embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['text'].tolist(), show_progress_bar=True)

def recommend(query):
    query = query.lower().strip()
    
    # Search by year
    if query.isdigit() and len(query) == 4:
        year_matches = df[df['release_year'] == query]
        return year_matches[['title', 'listed_in', 'description', 'release_year']].sample(n=min(15, len(year_matches)))
    
    # Search by genre or partial title
    match_df = df[df['text'].str.lower().str.contains(query)]
    if not match_df.empty:
        # BERT-based similarity search
        query_vec = model.encode([query])
        sims = cosine_similarity(query_vec, embeddings).flatten()
        top_indices = sims.argsort()[-15:][::-1]
        return df.iloc[top_indices][['title', 'listed_in', 'description', 'release_year']]
    
    return pd.DataFrame()  # Return empty DataFrame if nothing matched

# OMDb API setup
OMDB_API_KEY = "8df3a7d2"  # Replace with your API key

def fetch_poster(title):
    title = title.split(":")[0].strip().replace("&", "and")
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get('Response') == 'True' and data.get("Poster") != "N/A":
        return data.get('Poster')
    else:
        return "https://via.placeholder.com/160x240.png?text=No+Image"
