# 🎬 Movie Recommender System 🍿  

A **content-based movie recommendation system** that suggests similar movies based on your preferences.  
Built with **Python**, **Streamlit**, and **scikit-learn** 🚀  

---

## ✨ Features  

✅ **Movie Database**: 4,800+ movies from TMDB dataset  
🎭 **Content-Based Filtering**: Suggestions based on movie overviews & genres  
⚡ **Dynamic Similarity Matrix**: Generated on-demand for performance  
🖼️ **Movie Posters**: Pulled directly from TMDB API for visual appeal  
💻 **Interactive Web App**: Clean & user-friendly Streamlit interface  

---

## 🚀 Live Demo  

🔗 **[👉 Try the App Here](https://movie-recommender-system-tmdb-dataset-main.streamlit.app)**  

---

## ⚙️ How It Works  

1️⃣ **Data Processing** → Convert movie overviews & genres into numerical vectors  
2️⃣ **Similarity Calculation** → Use cosine similarity between movies  
3️⃣ **Recommendations** → Return top 5 similar movies with posters  

---

## 🛠️ Tech Stack  

- 🐍 **Python 3.x**  
- 🌐 **Streamlit** → Web interface  
- 🧮 **pandas** → Data manipulation  
- 🤖 **scikit-learn** → ML algorithms  
- 🔢 **NumPy** → Numerical computing  
- 🌍 **Requests** → TMDB API calls  

---

## ⚡ Installation  

### 📋 Prerequisites  
- Python **3.7+**  
- `pip` package manager  

### 🏗️ Setup  

```bash
# Clone repository
git clone https://github.com/Hari99-ai/movie-recommender-system-tmdb-dataset-main.git
cd movie-recommender-system-tmdb-dataset-main

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

🌐 Open browser → `http://localhost:8501`

---

## 🎞️ Dataset

📂 **TMDB 5000 Movie Dataset** includes:

* `tmdb_5000_movies.csv` → Movie details (overview, genres, metadata)
* `tmdb_5000_credits.csv` → Cast & crew info
* `movie_list.pkl` → Preprocessed dataset for faster loading

---

## 📂 File Structure

```
movie-recommender-system-tmdb-dataset-main/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── model/
│   ├── movie_list.pkl
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
└── notebooks/
    └── notebook86c26b4f17.ipynb   # Data analysis & preprocessing
```

---

## 🎮 Usage

1. 🎥 **Pick a Movie** → Select from 4,800+ options
2. 🖱️ **Click "Get Recommendations"**
3. 👀 **View Results** → 5 similar movies with posters
4. ⚙️ **Settings** → Toggle poster display on/off

---

## 🔑 API Configuration

🔌 Uses **TMDB API** to fetch posters.
👉 Get your own key from [TMDB](https://www.themoviedb.org/settings/api) for production use.

---

## ☁️ Deployment

### 🔹 Streamlit Cloud (Recommended)

1. Fork repo
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Deploy from GitHub

### 🔹 Local Deployment

```bash
streamlit run app.py --server.port 8501
```

---

## ⚡ Performance Notes

⚠️ **First Load** → 2–3 minutes (matrix generation)
⚡ **Later Uses** → Cached → Instant results
📊 **Dataset Size** → Handles 4,800+ movies efficiently

---

## 🤝 Contributing

1. 🍴 Fork the repo
2. 🌱 Create branch → `git checkout -b feature/new-feature`
3. ✅ Commit → `git commit -am 'Add feature'`
4. 🚀 Push → `git push origin feature/new-feature`
5. 🔁 Open Pull Request

---

## 🔮 Future Enhancements

- [ ] 🤝 Collaborative Filtering
- [ ] ⭐ User Ratings System
- [ ] 🎬 Include Directors & Actors metadata
- [ ] 🔍 Add Search Functionality
- [ ] 💡 Explainable Recommendations

---

## 📜 License

📝 Open-source under [MIT License](LICENSE).

---

## 🙌 Acknowledgments

🎬 **TMDB** → Movie dataset & API
💻 **Streamlit** → Web framework
🧠 **scikit-learn** → Machine Learning

---

## 👤 Contact

👨‍💻 **Created by Hari Om**

🌟 GitHub: [@Hari99-ai](https://github.com/Hari99-ai)
🔗 Project Link: [Movie Recommender System](https://github.com/Hari99-ai/movie-recommender-system-tmdb-dataset-main)

---

✨ *A fun way to explore content-based recommendation systems & modern web deployment!* ✨
