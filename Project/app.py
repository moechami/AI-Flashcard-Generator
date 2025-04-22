# app.py

import streamlit as st
from pdf_extractor import extract_text_from_pdf
from flashcard_gen import generate_flashcards_from_text
import random
import pandas as pd
import io

st.set_page_config(page_title="AI Flashcard Generator", page_icon="🧠")
st.title("🧠 AI Flashcard Generator")
st.write("Upload a PDF, and we'll extract the content and create flashcards using AI.")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF file here", type=["pdf"])

# Card settings
num_cards = st.slider("How many flashcards per page?", min_value=1, max_value=5, value=3)

#Session state for card, first initialize
if "flashcards" not in st.session_state:    #initialize flashcard list for modes
    st.session_state.flashcards = []
if "index" not in st.session_state:         #initialize index for flashcard list
    st.session_state.index = 0
if "question_side" not in st.session_state: #check if flashcard is on question side
    st.session_state.question_side = True
if "entered_answer" not in st.session_state:  #initialize user answer as empty
    st.session_state.entered_answer = ""
if "result" not in st.session_state:        #result of entered answer is blank on session start
    st.session_state.result = ""
if "number_correct" not in st.session_state:    #number of correct cards answered
    st.session_state.number_correct = 0
if "answered" not in st.session_state:      #keeps track of whether the card in test mode has already been answered
    st.session_state.answered = False

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

            #Exporting generated flashcards into csv file for download
            export = pd.DataFrame(st.session_state.flashcards)
            buffer = io.StringIO()
            export.to_csv(buffer, index = False)
            csv_data = buffer.getvalue()

            st.download_button(label="📥 Download Flashcards as CSV", data=csv_data,
                               file_name="flashcards.csv", mime="text/csv")

#functions to be executed when clicked on respective button
def next_card():
    if st.session_state.index < len(st.session_state.flashcards) - 1:
        st.session_state.index += 1
        st.session_state.question_side = True
        st.session_state.entered_answer = ""
        st.session_state.result = ""
        st.session_state.answered = False

def flip_card():
    st.session_state.question_side = not st.session_state.question_side

def previous_card():
    if st.session_state.index > 0:
        st.session_state.index -= 1
        st.session_state.question_side = True
        st.session_state.entered_answer = ""
        st.session_state.result = ""
        st.session_state.answered = False

def shuffle_cards():
    random.shuffle(st.session_state.flashcards)
    st.session_state.index = 0
    st.session_state.question_side = True
    st.session_state.number_correct = 0
    st.session_state.entered_answer = ""
    st.session_state.result = ""
    st.session_state.answered = False

def check_entered_answer():
    if st.session_state.answered:
        return

    correct_answer = st.session_state.flashcards[st.session_state.index]['answer']
    user_input = st.session_state.entered_answer.strip().lower()
    correct = correct_answer.strip().lower()

    if user_input == correct:
        st.session_state.result = "✅ Correct!"
        st.session_state.number_correct += 1
    else:
        st.session_state.result = f"❌ Incorrect. The correct answer is: {correct_answer}"

    st.session_state.answered = True

def reset_test():
    st.session_state.index = 0
    st.session_state.entered_answer = ""
    st.session_state.result = ""
    st.session_state.answered = False
    st.session_state.number_correct = 0

mode = st.radio("Choose a mode:", ["Review Mode", "Test Mode"], horizontal=True)

if st.session_state.flashcards:
    #Define current card as the first card
    curr_card = st.session_state.flashcards[st.session_state.index]
    if mode == "Review Mode":
        # Review flashcard section
        st.markdown("🧠 Flashcard Review")
        #Question or Answer title based on the card's side
        st.write("Question:" if st.session_state.question_side else "Answer:")
        #write the question or the answer of the flashcard based on what side it is on, keep track of number of cards
        st.info(curr_card['question'] if st.session_state.question_side else curr_card['answer'])
        st.write(f"({st.session_state.index + 1} / {len(st.session_state.flashcards) + 1})")

        #Previous, flip, and next buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("⬅️ Previous", on_click=previous_card, disabled=st.session_state.index == 0)
        with col2:

            st.button("🔁 Flip", on_click=flip_card, key='1')

            st.button("🔀 Shuffle", on_click=shuffle_cards, key='2')
        with col3:
            st.button("Next ➡️", on_click=next_card,
                  disabled=st.session_state.index == len(st.session_state.flashcards) - 1)



    elif mode == "Test Mode":
        #Testing knowledge mode
        st.markdown("🧠 Test Your Knowledge")
        st.write("Question:")
        #Question is written, prompts user for their reponse
        st.info(curr_card['question'])
        st.text_input("Your Answer", key = "entered_answer")
        st.button("Check Answer", on_click=check_entered_answer)
        #progress in terms of which card user is on out of the total cards
        st.write(f"({st.session_state.index + 1} / {len(st.session_state.flashcards) + 1})")
        #user can traverse cards similar to review mode
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("⬅️ Previous", on_click=previous_card, disabled=st.session_state.index == 0)
        with col3:
            st.button("Next ➡️", on_click=next_card,
                  disabled=st.session_state.index == len(st.session_state.flashcards) - 1)
        with col2:
            st.button("🔀 Shuffle", on_click=shuffle_cards)
        if st.session_state.result:
            st.markdown(st.session_state.result)
        #keep track of progress for number of correct answers out of the total flashcard set
        st.write(f"Number of correct answers: {st.session_state.number_correct}")
        total = st.session_state.index + 1 if st.session_state.index + 1 <= len(st.session_state.flashcards) else len(st.session_state.flashcards)
        score = int((st.session_state.number_correct / total) * 100) if total > 0 else 0
        st.progress(score)
        st.caption(f'Score: {score}%')
        #reset in case user wants to start over
        st.button("🔄 Reset Test Progress", on_click=reset_test)