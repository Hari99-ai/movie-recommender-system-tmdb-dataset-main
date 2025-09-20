import streamlit as st
import pickle
import requests
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# -------------------------------
# App Configuration
# -------------------------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# -------------------------------
# Data Loading
# -------------------------------
@st.cache_data
def load_movies():
    """Load movie list from pickle file"""
    try:
        with open('model/movie_list.pkl', 'rb') as f:
            movies = pickle.load(f)
        return pd.DataFrame(movies)
    except Exception as e:
        st.error(f"Error loading movie list: {e}")
        return None

@st.cache_data
def generate_similarity_matrix():
    """Generate similarity matrix from movie data"""
    try:
        movies_df = pd.read_csv('model/tmdb_5000_movies.csv')
        movies_df['overview'] = movies_df['overview'].fillna('')
        movies_df['genres'] = movies_df['genres'].fillna('')
        movies_df['tags'] = movies_df['overview'] + ' ' + movies_df['genres']

        with st.spinner('Creating movie vectors...'):
            cv = CountVectorizer(max_features=3000, stop_words='english')
            vectors = cv.fit_transform(movies_df['tags']).toarray()

        with st.spinner('Calculating movie similarities...'):
            similarity = cosine_similarity(vectors)

        return similarity
    except Exception as e:
        st.error(f"Error generating similarity matrix: {e}")
        return None

# -------------------------------
# Helper Functions
# -------------------------------
def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API"""
    api_key = os.getenv("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")  # Fallback API key
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception as e:
        st.warning(f"Poster fetch failed: {e}")
    return "https://via.placeholder.com/500x750/cccccc/666666?text=No+Poster"

def recommend(movie, movies_df, similarity):
    """Get top 5 movie recommendations"""
    try:
        movie_matches = movies_df[movies_df['title'] == movie]
        if movie_matches.empty:
            return [], []

        index = movie_matches.index[0]
        distances = similarity[index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movie_names = []
        recommended_movie_posters = []

        for i, _ in movies_list:
            movie_title = movies_df.iloc[i]['title']
            if 'movie_id' in movies_df.columns:
                movie_id = movies_df.iloc[i]['movie_id']
            elif 'id' in movies_df.columns:
                movie_id = movies_df.iloc[i]['id']
            else:
                movie_id = 0

            recommended_movie_names.append(movie_title)
            recommended_movie_posters.append(fetch_poster(movie_id))

        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return [], []

# -------------------------------
# Main App
# -------------------------------
def main():
    # Header
    st.title('🎬 Movie Recommender System')
    st.markdown("*Find movies similar to your favorites*")

    # Load movie data
    with st.spinner('Loading movie database...'):
        movies_df = load_movies()

    if movies_df is None:
        st.error("❌ Could not load movie database. Please check your files.")
        st.stop()

    st.success(f"✅ Loaded {len(movies_df)} movies")

    # Generate similarity matrix
    with st.spinner('Setting up recommendation engine...'):
        similarity = generate_similarity_matrix()

    if similarity is None:
        st.error("❌ Could not create recommendation engine.")
        st.stop()

    st.success("✅ Recommendation engine ready!")

    # Interface
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader('🎯 Select a Movie')
        selected_movie_name = st.selectbox(
            'Choose a movie you like:',
            movies_df['title'].values,
            help="Select any movie to get 5 similar recommendations"
        )

    with col2:
        st.subheader('⚙️ Settings')
        show_posters = st.checkbox('Show movie posters', value=True)

    # Get recommendations
    if st.button('🔍 Get Recommendations', type="primary", use_container_width=True):
        if selected_movie_name:
            with st.spinner('Finding similar movies...'):
                recommended_movie_names, recommended_movie_posters = recommend(
                    selected_movie_name, movies_df, similarity
                )

            if recommended_movie_names:
                st.subheader(f'🎬 Movies Similar to "{selected_movie_name}"')

                if show_posters:
                    cols = st.columns(5)
                    for i, (movie, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
                        with cols[i]:
                            st.image(poster, use_container_width=True)
                            st.write(f"**{movie}**")
                else:
                    for i, movie in enumerate(recommended_movie_names, 1):
                        st.write(f"**{i}.** {movie}")
            else:
                st.error("❌ Could not generate recommendations. Please try another movie.")

    # Footer
    st.markdown("---")
    st.markdown("*Created by ❤️Hari Om*")

if __name__ == "__main__":
    main()

