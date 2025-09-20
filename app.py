# import streamlit as st
# import pickle
# import requests
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import os

# # -------------------------------
# # App Configuration
# # -------------------------------
# st.set_page_config(
#     page_title="Movie Recommender",
#     page_icon="🎬",
#     layout="wide"
# )

# # -------------------------------
# # Data Loading
# # -------------------------------
# @st.cache_data
# def load_movies():
#     """Load movie list from pickle file"""
#     try:
#         with open('model/movie_list.pkl', 'rb') as f:
#             movies = pickle.load(f)
#         return pd.DataFrame(movies)
#     except Exception as e:
#         st.error(f"Error loading movie list: {e}")
#         return None

# @st.cache_data
# def generate_similarity_matrix():
#     """Generate similarity matrix from movie data"""
#     try:
#         movies_df = pd.read_csv('model/tmdb_5000_movies.csv')
#         movies_df['overview'] = movies_df['overview'].fillna('')
#         movies_df['genres'] = movies_df['genres'].fillna('')
#         movies_df['tags'] = movies_df['overview'] + ' ' + movies_df['genres']

#         cv = CountVectorizer(max_features=3000, stop_words='english')
#         vectors = cv.fit_transform(movies_df['tags']).toarray()
#         similarity = cosine_similarity(vectors)

#         return similarity
#     except Exception as e:
#         st.error(f"Error generating similarity matrix: {e}")
#         return None

# # -------------------------------
# # Helper Functions
# # -------------------------------
# def fetch_poster(movie_id):
#     """Fetch movie poster from TMDB API"""
#     api_key = os.getenv("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")  # Fallback API key
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
#         response = requests.get(url, timeout=5)
#         data = response.json()
#         poster_path = data.get('poster_path')
#         if poster_path:
#             return f"https://image.tmdb.org/t/p/w500/{poster_path}"
#     except Exception:
#         pass
#     return "https://via.placeholder.com/500x750/cccccc/666666?text=No+Poster"

# def recommend(movie, movies_df, similarity):
#     """Get top 5 movie recommendations"""
#     try:
#         movie_matches = movies_df[movies_df['title'] == movie]
#         if movie_matches.empty:
#             return [], []

#         index = movie_matches.index[0]
#         distances = similarity[index]
#         movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#         recommended_movie_names = []
#         recommended_movie_posters = []

#         for i, _ in movies_list:
#             movie_title = movies_df.iloc[i]['title']
#             if 'movie_id' in movies_df.columns:
#                 movie_id = movies_df.iloc[i]['movie_id']
#             elif 'id' in movies_df.columns:
#                 movie_id = movies_df.iloc[i]['id']
#             else:
#                 movie_id = 0

#             recommended_movie_names.append(movie_title)
#             recommended_movie_posters.append(fetch_poster(movie_id))

#         return recommended_movie_names, recommended_movie_posters
#     except Exception as e:
#         st.error(f"Error generating recommendations: {e}")
#         return [], []

# # -------------------------------
# # Main App
# # -------------------------------
# def main():
#     # Header
#     st.title('🎬 Movie Recommender System')

#     # Load movie data
#     movies_df = load_movies()
#     if movies_df is None:
#         st.error("❌ Could not load movie database. Please check your files.")
#         st.stop()

#     # Generate similarity matrix
#     similarity = generate_similarity_matrix()
#     if similarity is None:
#         st.error("❌ Could not create recommendation engine.")
#         st.stop()

#     # Interface
#     col1, col2 = st.columns([3, 1])

#     with col1:
#         st.subheader('🎯 Select a Movie')
#         selected_movie_name = st.selectbox(
#             'Choose a movie you like:',
#             movies_df['title'].values,
#             help="Select any movie to get 5 similar recommendations"
#         )

#     with col2:
#         st.subheader('⚙️ Settings')
#         show_posters = st.checkbox('Show movie posters', value=True)

#     # Get recommendations
#     if st.button('🔍 Get Recommendations', type="primary", use_container_width=True):
#         if selected_movie_name:
#             with st.spinner('Finding similar movies...'):
#                 recommended_movie_names, recommended_movie_posters = recommend(
#                     selected_movie_name, movies_df, similarity
#                 )

#             if recommended_movie_names:
#                 st.subheader(f'🎬 Movies Similar to "{selected_movie_name}"')

#                 if show_posters:
#                     cols = st.columns(5)
#                     for i, (movie, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
#                         with cols[i]:
#                             st.image(poster, use_container_width=True)
#                             st.write(f"**{movie}**")
#                 else:
#                     for i, movie in enumerate(recommended_movie_names, 1):
#                         st.write(f"**{i}.** {movie}")
#             else:
#                 st.error("❌ Could not generate recommendations. Please try another movie.")

#     # Footer
#     st.markdown("---")
#     st.markdown("*Created by ❤️ Hari Om*")

# if __name__ == "__main__":
#     main()






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

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #FF4B4B;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 18px;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .movie-card {
        padding: 10px;
        border-radius: 12px;
        background-color: #fafafa;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    .movie-card img {
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Data Loading
# -------------------------------
@st.cache_data
def load_movies():
    try:
        with open('model/movie_list.pkl', 'rb') as f:
            movies = pickle.load(f)
        return pd.DataFrame(movies)
    except Exception as e:
        st.error(f"Error loading movie list: {e}")
        return None

@st.cache_data
def generate_similarity_matrix():
    try:
        movies_df = pd.read_csv('model/tmdb_5000_movies.csv')
        movies_df['overview'] = movies_df['overview'].fillna('')
        movies_df['genres'] = movies_df['genres'].fillna('')
        movies_df['tags'] = movies_df['overview'] + ' ' + movies_df['genres']

        cv = CountVectorizer(max_features=3000, stop_words='english')
        vectors = cv.fit_transform(movies_df['tags']).toarray()
        similarity = cosine_similarity(vectors)
        return similarity
    except Exception as e:
        st.error(f"Error generating similarity matrix: {e}")
        return None

# -------------------------------
# Helper Functions
# -------------------------------
def fetch_poster(movie_id):
    api_key = os.getenv("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except:
        pass
    return "https://via.placeholder.com/500x750/cccccc/666666?text=No+Poster"

def recommend(movie, movies_df, similarity):
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
    st.markdown('<div class="main-title">🎬 Movie Recommender System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Discover movies similar to your favorites</div>', unsafe_allow_html=True)

    movies_df = load_movies()
    if movies_df is None:
        st.error("❌ Could not load movie database.")
        st.stop()

    similarity = generate_similarity_matrix()
    if similarity is None:
        st.error("❌ Could not create recommendation engine.")
        st.stop()

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
        show_posters = st.checkbox('Show posters', value=True)

    # Get recommendations
    if st.button('🔍 Get Recommendations', type="primary", use_container_width=True):
        if selected_movie_name:
            recommended_movie_names, recommended_movie_posters = recommend(
                selected_movie_name, movies_df, similarity
            )

            if recommended_movie_names:
                st.markdown(f"<h3 style='margin-top:20px;'>✨ Movies Similar to <i>{selected_movie_name}</i></h3>", unsafe_allow_html=True)

                if show_posters:
                    cols = st.columns(5)
                    for i, (movie, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
                        with cols[i]:
                            st.markdown(f"""
                                <div class="movie-card">
                                    <img src="{poster}" width="100%">
                                    <b>{movie}</b>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    for i, movie in enumerate(recommended_movie_names, 1):
                        st.write(f"**{i}.** {movie}")
            else:
                st.warning("⚠️ No recommendations found. Try another movie.")

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#888;'>Created by ❤️ Hari Om</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
