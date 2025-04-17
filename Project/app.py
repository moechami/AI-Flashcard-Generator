# app.py

import streamlit as st
from pdf_extractor import extract_text_from_pdf

st.title("🧠 Our AI Flashcard Generator!")
st.write("Upload your own PDF, and we'll use our state of the art machine learning model to generate flashcards for you.")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        pages = extract_text_from_pdf(uploaded_file)
    
    st.success(f"Extracted {len(pages)} page(s) of text.")
    
