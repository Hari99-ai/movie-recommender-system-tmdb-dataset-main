from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
import requests

app = Flask(__name__)

# TMDB API key
API_KEY = "0d4416864237a443599eb466486f9763"

# Load pickle files
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Reset index for safety
movies = movies.reset_index(drop=True)


# Function to fetch poster from TMDB
import requests

API_KEY = "0d4416864237a443599eb466486f9763"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)  # set timeout
        response.raise_for_status()  # raise HTTP error if any
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.ConnectionError:
        print("⚠️ No Internet connection. Returning default poster.")
        return "https://via.placeholder.com/500x750?text=Offline"
    except requests.exceptions.Timeout:
        print("⚠️ Request timed out. Returning default poster.")
        return "https://via.placeholder.com/500x750?text=Timeout"
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie_title):
    if movie_title not in movies['title'].values:
        return []
    
    # Get index of the movie
    idx = movies[movies['title'] == movie_title].index[0]
    distances = similarity[idx]
    
    # Get top 5 similar movies (excluding the movie itself)
    movie_indices = sorted(
        list(enumerate(distances)), 
        reverse=True, 
        key=lambda x: x[1]
    )[1:6]
    
    recommendations = []
    for i in movie_indices:
        movie_id = movies.iloc[i[0]]["id"]   # ✅ use "id" instead of "movie_id"
        recommendations.append({
            "title": movies.iloc[i[0]]["title"],
            "poster": fetch_poster(movie_id)
        })
    
    return recommendations



@app.route('/')
def home():
    return render_template('index.html')  # create index.html inside templates folder


@app.route('/recommend', methods=['POST'])
def recommend_movies():
    movie_name = request.form['movie']
    recommendations = recommend(movie_name)
    return render_template('index.html', movie=movie_name, recommendations=recommendations)


# API endpoint
@app.route('/api/recommend', methods=['GET'])
def api_recommend():
    movie_name = request.args.get('movie')
    recommendations = recommend(movie_name)
    return jsonify({
        "movie": movie_name,
        "recommendations": recommendations
    })


if __name__ == "__main__":
    app.run(debug=True)