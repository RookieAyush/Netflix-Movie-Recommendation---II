import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Load data
df = pd.read_csv('netflix_titles.csv')
df = df[['title', 'description', 'listed_in', 'release_year']].dropna(subset=['description', 'listed_in'])
df['text'] = df['description'] + " " + df['listed_in']

# Load pre-trained BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight and fast

# Compute embeddings
embeddings = model.encode(df['text'].tolist(), show_progress_bar=True)

# BERT-based recommendation
def recommend(query, top_n=10):
    query_embed = model.encode([query])
    similarities = cosine_similarity(query_embed, embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][1:top_n+1]

    return df.iloc[top_indices][['title', 'release_year', 'listed_in', 'description']]

# OMDb poster fetching
OMDB_API_KEY = "8df3a7d2"  # 🔁 Replace with your actual OMDb key

def fetch_poster(title):
    title = title.split(":")[0].strip().replace("&", "and")
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get('Response') == 'True' and data.get('Poster') != "N/A":
        return data.get('Poster')
    else:
        return "https://via.placeholder.com/160x240.png?text=No+Image"
