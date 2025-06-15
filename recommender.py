import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from decorators import log_calls, timeit, simple_cache


# Load data from SQLite
engine = create_engine("sqlite:///src/data/books.db")
query = """
SELECT books.id, books.title, books.description, genres.name as genre
FROM books
JOIN genres ON books.genre_id = genres.id
"""
df = pd.read_sql(query, engine)

# Combine genre + description
df['text'] = df['genre'].fillna('') + " " + df['description'].fillna('')

# TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['text'])

# Cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Reverse map for title → index lookup
df["lower_title"]=df["title"].str.lower()
title_to_index = pd.Series(df.index, index=df['lower_title']).drop_duplicates()

# Recommendation function
@log_calls
@timeit
@simple_cache
def recommend_books(title, top_n=5):
    title=title.lower().strip()
    if title not in title_to_index:
        return f"❌ Book '{title}' not found in dataset."
    
    idx = title_to_index[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    recommended_books = df.iloc[[i[0] for i in sim_scores]][['title', 'genre']]
    return recommended_books.reset_index(drop=True)

# Example usage
if __name__ == "__main__":
    title_input = "A Light in the Attic"
    print(f"\n📚 Because you liked: {title_input}")
    print(recommend_books(title_input))
