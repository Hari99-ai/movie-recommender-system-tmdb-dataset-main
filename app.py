# movie_recommender_streamlit.py

import streamlit as st
import pickle
import pandas as pd
import requests

# --- Load preprocessed data ---
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))
movies = movies.reset_index(drop=True)

# --- TMDB API key ---
API_KEY = "0d4416864237a443599eb466486f9763"

# --- Function to fetch poster ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.ConnectionError:
        return "https://via.placeholder.com/500x750?text=Offline"
    except requests.exceptions.Timeout:
        return "https://via.placeholder.com/500x750?text=Timeout"
    except Exception:
        return "https://via.placeholder.com/500x750?text=Error"

# --- Recommendation function ---
def recommend(movie_title):
    if movie_title not in movies['title'].values:
        return []
    
    idx = movies[movies['title'] == movie_title].index[0]
    distances = similarity[idx]
    
    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]  # top 5 excluding itself
    
    recommendations = []
    for i in movie_indices:
        movie_id = movies.iloc[i[0]]["id"]
        recommendations.append({
            "title": movies.iloc[i[0]]["title"],
            "poster": fetch_poster(movie_id)
        })
    
    return recommendations

# --- Streamlit UI ---
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Custom CSS (for dark theme + gradient effects + hover animation)
st.markdown("""
    <style>
    body {
        background-color: #000;
        color: #fff;
    }
    .main {
        background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
        padding: 20px;
        border-radius: 15px;
    }
    h1, h2, h3 {
        text-align: center;
        font-weight: bold;
        background: linear-gradient(90deg, red, orange, yellow, lime, cyan, blue, violet);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff4b5c, #ffcc00, #33ccff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        filter: brightness(1.2);
    }
    .movie-card {
        transition: transform 0.3s ease, box-shadow 0.3s;
    }
    .movie-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 8px 25px rgba(255,255,255,0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommender System")
st.write("<h3>✨ Get top 5 similar movies with posters!</h3>", unsafe_allow_html=True)

# Movie selection
selected_movie = st.selectbox("Choose a movie:", movies['title'].values)

if st.button("🔍 Recommend"):
    recommendations = recommend(selected_movie)
    
    if recommendations:
        cols = st.columns(5)
        for idx, rec in enumerate(recommendations):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div class="movie-card">
                        <img src="{rec['poster']}" style="border-radius:12px; width:100%; height:300px; object-fit:cover;">
                        <p style="text-align:center; font-weight:bold; margin-top:8px;">⭐ {rec['title']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.error("❌ No recommendations found.")
