import os
from google import genai
from dotenv import load_dotenv
from typing import Dict
from fastapi import HTTPException
import json
import spacy
from collections import Counter
from typing import Optional, List, Dict
from pydantic import BaseModel

load_dotenv()
# Load the spaCy model once at startup
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    exit()

class AnalysisSchema(BaseModel):
    summary: str
    title: str
    topics: list[str]
    sentiment: str

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

async def process_with_llm(text: str) -> Dict:
    
    prompt = f"""
    You are a text analysis assistant. Your task is to analyze the following block of text.
    First, generate a concise summary of 1-2 sentences.
    Second, extract structured metadata as a JSON object.
    
    The JSON object must contain the following keys:
    - "summary": A 1 to 2 sentence brief summary of the text.
    - "title": The title of the text, if one is clearly present. If not, use null.
    - "topics": A list of exactly 3 key topics from the text.
    - "sentiment": The overall sentiment of the text, which must be 'positive', 'neutral', or 'negative'.

    Example output format:
    
    ```json
    {{
      "title": "Example Title",
      "topics": ["topic 1", "topic 2", "topic 3"],
      "sentiment": "positive"
    }}
    ```
    
    Text to analyze:
    {text}
    """

    try:
        # response = model.generate_content(prompt)
        # full_output = response.text.strip()

        response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt,
                        config={
                            "response_mime_type": "application/json",
                            "response_schema": AnalysisSchema,
                        },
                    )
        
        
        print("AI Response:",json.loads(response.text)) # json.loads(response.text)
        return json.loads(response.text)
    except Exception as e:
        print(f"LLM API failure: {e}")
        raise HTTPException(status_code=500, detail="LLM API is currently unavailable.")
    
# Helper function for keyword extraction
def extract_keywords(text: str, top_n: int = 3) -> List[str]:
    doc = nlp(text)
    
    # Filter for common nouns only
    common_nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    
    # Count the frequency of each noun
    noun_counts = Counter(common_nouns)
    
    # Return the most common nouns
    return [noun for noun, count in noun_counts.most_common(top_n)]