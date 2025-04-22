# AI-Flashcard-Generator
First Commit – Project Initialization (Mohammad El-Chami)

    Created project directory and initialized a Python virtual environment using venv.

    Added a requirements.txt file listing all core and optional dependencies:

        pdfplumber, openai, langchain, streamlit, tiktoken, nltk, pinecone, faiss-cpu, PyMuPDF

    Install all packages within your virtual environment via:

    pip install -r requirements.txt

Second Commit - Project Prototype Setup (Mohammad El-Chami)

    Built the first working prototype of the app:
    
        Streamlit frontend loads and renders (simple and clean UI)
        PDF file upload works (200MB max)
        Extracts text (still messy) from uploaded PDFs using `pdfplumber`
        
    Created the `extractor/` file to handle simple PDF parsing
    
    Defined task responsibilities for the rest of the team

Third commit- PDF extractor file modification (ali ramadan)
   initial changes to the code, just fixing up what me and the team talked about. 
   i modified the pdf extractor pyhton file to improve the current code. 

Fourth commit- PDF extractor file second modification (ali ramadan)
    Finishing what me and my team discussed about cleaning up the pdf file extraction and adding some extra features.
    
Fifth Commit – Flashcard Generator Integration (Mohammad El-Chami)

Built the core AI flashcard generation logic using OpenAI + LangChain:

    Added generator/flashcard_gen.py

    Integrated langchain-openai with prompt templates using ChatPromptTemplate

    Ensured consistent JSON output

sixth commit- app.py changes (ali ramadan)
    I made changes to the app.py file to format everything better for streamlit, this way it can look more professional and works better with everything else.

Seventh commit (made before sixth commit) (Ghina Albabbili):
Created flashcard_display.py in order to display the flashcards in a window using the tkinter library. Implementation is in progress, sample buttons, text, and user input boxes provide framework for later changes. TODO-create separate pages

Eighth commit (Ghina Albabbili)-
-Deletes: flashcard_display.py
    Tkinter library not necessary, everything done in streamlit
-Changes made to app.py
    Define session state for card in order to flip between question and answer side, go to previous card, go to next card
    Define functions for what to do on clicks of buttons: next_card(), flip_card(), previous_card() 
    Change flashcards to a flat list to traverse by their question, answer values
    Create flashcard review with above features

Ninth commit (Ghina Albabbili)-
-Changes made to app.py
    Creation of test mode- adding buttons, definitions, number of correct answer tracker
    Allows for user answer input to be checked against correct answer
    Progress view and reset button
    Creating toggle menu between review mode and test mode- ux update