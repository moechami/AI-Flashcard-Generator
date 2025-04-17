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
