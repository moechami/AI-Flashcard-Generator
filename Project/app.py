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

#Session state for card, first initialize
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "question_side" not in st.session_state:
    st.session_state.question_side = True

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

            #turn list to flat so you can look up by question, answer index for card
            flat_flashcards = []
            for _, cards in all_flashcards:
                flat_flashcards.extend(cards)
            st.session_state.flashcards = flat_flashcards
            st.session_state.index = 0

#functions to be executed when clicked on respective button
def next_card():
    if st.session_state.index < len(st.session_state.flashcards) - 1:
        st.session_state.index += 1
        st.session_state.question_side = True
def flip_card():
    st.session_state.question_side = not st.session_state.question_side
def previous_card():
    if st.session_state.index > 0:
        st.session_state.index -= 1
        st.session_state.question_side = True

#Review flashcard section
if st.session_state.flashcards:
    st.markdown("🧠 Flashcard Review")
    #Define current card as the first card
    curr_card = st.session_state.flashcards[st.session_state.index]

    #Question or Answer title based on the card's side
    st.write("Question:" if st.session_state.question_side else "Answer:")
    st.info(curr_card['question'] if st.session_state.question_side else curr_card['answer'])

    #Previous, flip, and next buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("⬅️ Previous", on_click=previous_card, disabled=st.session_state.index == 0)
    with col2:
        st.button("🔁 Flip", on_click=flip_card)
    with col3:
        st.button("Next ➡️", on_click=next_card,
                  disabled=st.session_state.index == len(st.session_state.flashcards) - 1)