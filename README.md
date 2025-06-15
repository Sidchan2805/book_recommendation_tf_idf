# Content-Based Book Recommendation System

This is an end-to-end content-based book recommender system built in Python. It scrapes real-world book metadata, stores it in a normalized SQLite database, generates recommendations using TF-IDF + cosine similarity, and exposes the functionality through both a Flask API and a Streamlit frontend.

---

## Features
- Recommend books based on genre and summary similarity
- TF-IDF vectorization and cosine similarity matching
- Relational database with SQLAlchemy (SQLite)
- REST API with Flask
- Web UI using Streamlit
- Decorators for logging, caching, and timing

---

## Project Structure

```
BOOKS RECOMMENDATION/
├── books_with_descriptions.csv       # Scraped data
├── books.db                          # SQLite database
├── scraper.py                        # Scraper script
├── db_loader.py                      # Loads CSV into DB
├── recommender.py                    # Model logic (TF-IDF + cosine)
├── decorators.py                     # Custom decorators
├── flask_app.py                      # Flask API
├── streamlit_app.py                  # Streamlit UI
├── requirements.txt                  # Dependencies
├── .gitignore                        # Git exclusions
└── app.log                           # Log file
```

---

## Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Scrape data
```bash
python scraper.py
```

### 3. Load into database
```bash
python db_loader.py
```

### 4. Test recommendation logic
```bash
python recommender.py
```

### 5. Run Flask API
```bash
python flask_app.py
# Open: http://127.0.0.1:5000/recommend?title=Book%20Title&top_n=5
```

### 6. Run Streamlit App
```bash
streamlit run streamlit_app.py
```

---

## Example API Call

```
GET /recommend?title=The%20Night%20Circus&top_n=3
```

Returns JSON:
```json
[
  { "title": "Soumission", "genre": "Fiction" },
  { "title": "Sharp Objects", "genre": "Mystery" },
  { "title": "The Night Watch", "genre": "Fantasy" }
]
```

---

## Tech Stack
- Python
- BeautifulSoup (scraping)
- SQLAlchemy + SQLite (database)
- Scikit-learn (NLP model)
- Flask (API)
- Streamlit (UI)

