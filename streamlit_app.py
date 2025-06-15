import streamlit as st
from recommender import recommend_books
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("sqlite:///src/data/books.db")
df = pd.read_sql("SELECT title FROM books", engine)
titles = sorted(df['title'].unique().tolist())

st.set_page_config(page_title="📚 Book Recommender", layout="centered")

st.title("📚 Book Recommendation Engine")
st.markdown("Select a book title to get similar book recommendations based on content.")

# Autocomplete dropdown instead of text_input
title_input = st.selectbox("Choose a Book Title", titles, index=0)

# Slider for number of recommendations
top_n = st.slider("How many recommendations?", min_value=1, max_value=10, value=5)

# Recommend button
if st.button("Get Recommendations"):
    with st.spinner("Finding similar books..."):
        result = recommend_books(title_input, top_n)
        if isinstance(result, str):
            st.warning(result)
        else:
            st.success(f"Books similar to: *{title_input}*")
            st.table(result)

