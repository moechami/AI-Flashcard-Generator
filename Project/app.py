# app.py

import streamlit as st
from pdf_extractor import extract_text_from_pdf
from flashcard_gen import generate_flashcards_from_text

st.set_page_config(page_title="AI Flashcard Generator", page_icon="🧠")
st.title("🧠 AI Flashcard Generator")
st.write("Upload a PDF, and we'll extract the content and create flashcards using AI.")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF file here", type=["pdf"])

# Card settings
num_cards = st.slider("How many flashcards per page?", min_value=1, max_value=5, value=3)

if uploaded_file:
    with st.spinner("🔍 Extracting and cleaning text from PDF..."):
        pages = extract_text_from_pdf(uploaded_file)

    st.success(f"✅ Extracted and cleaned text from {len(pages)} page(s).")

    if st.button("⚡ Generate Flashcards"):
        all_flashcards = []

        with st.spinner("🧠 Generating flashcards with AI..."):
            for i, chunk in enumerate(pages):
                cards = generate_flashcards_from_text(chunk, num_cards=num_cards)
                if cards:
                    all_flashcards.append((i + 1, cards))

        if not all_flashcards:
            st.error("No flashcards were generated. Please try with a different PDF.")
        else:
            st.success("🎉 Flashcards generated successfully!")

            for page_num, cards in all_flashcards:
                st.markdown(f"### 📄 Page {page_num}")
                for idx, card in enumerate(cards, 1):
                    with st.expander(f"Q{idx}: {card['question']}"):
                        st.markdown(f"**Answer:** {card['answer']}")
