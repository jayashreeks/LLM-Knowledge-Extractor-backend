from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.db import (Analysis)
from database.db import get_db
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from ai_generator import process_with_llm
from ai_generator import extract_keywords

router = APIRouter()

# Pydantic models for API
class TextPayload(BaseModel):
    text: str = Field(..., min_length=1)

class AnalysisResponse(BaseModel):
    summary: str
    title: Optional[str]
    topics: Optional[List[str]]
    sentiment: Optional[str]
    keywords: Optional[List[str]]


# API Endpoints
@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(payload: TextPayload, db: Session = Depends(get_db)):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    # 1. Process with LLM for summary and structured data
    llm_results = await process_with_llm(payload.text)

    # 2. Extract keywords using NLTK
    keywords = extract_keywords(payload.text)
    # keywords= ["sample"]
    
    # 3. Store in the database
    new_analysis = Analysis(
        text=payload.text,
        summary=llm_results["summary"],
        title=llm_results["title"],
        topics=llm_results["topics"],
        sentiment=llm_results["sentiment"],
        keywords=keywords,
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return new_analysis

@router.get("/search", response_model=List[AnalysisResponse])
def search_analyses(topic: Optional[str] = None, keyword: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Analysis)
    
    if topic:
        # Search for the topic within the JSON topics column
        # Using a simple LIKE query on the string representation of the JSON
        query = query.filter(Analysis.topics.like(f"%{topic}%"))
    
    if keyword:
        # Search for the keyword within the JSON keywords column
        query = query.filter(Analysis.keywords.like(f"%{keyword}%"))

    analyses = query.all()
    return analyses