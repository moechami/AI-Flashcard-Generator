from typing import List, Dict
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load OPENAI_API_KEY
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3
)

# The chat prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI tutor that creates JSON flashcards. Only respond with a raw JSON list. Do not include any explanations or markdown formatting."),
    ("human", """Create {num_cards} concise Q&A flashcards from the following text:

{chunk}

Return ONLY a valid JSON array that starts with [ and ends with ].
Each item must be a dictionary with 'question' and 'answer' keys.
Do NOT return markdown, comments, or any explanation. Prioritize Key definitions, processes, and relationships.""")

])

def generate_flashcards_from_text(chunk: str, num_cards: int = 3) -> List[Dict[str, str]]:
    """
    Parameters:
    - chunk (str): The input text to generate flashcards from.
    - num_cards (int): The number of flashcards to generate.

    Returns:
    - List[Dict[str, str]]: A list of flashcards with 'question' and 'answer' keys.
    """
    try:
        formatted_prompt = prompt.format_messages(chunk=chunk, num_cards=num_cards)

        #calls the model
        response = llm.invoke(formatted_prompt)

        #strips the content appropriately
        content = response.content.strip()

        if content.startswith("```json"):
            content = content.removeprefix("```json").removesuffix("```").strip()
        elif content.startswith("```"):
            content = content.removeprefix("```").removesuffix("```").strip()

        if content.startswith('{') and not content.startswith('['):
            content = f"[{content}]"

        flashcards = json.loads(content)

        return flashcards

    except Exception as e:
        print(f"[Error] Flashcard generation failed: {e}")
        return []
