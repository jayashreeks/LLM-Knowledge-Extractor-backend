# LLM-Knowledge-Extractor-backend

Overview
This is a full-stack application designed to analyze text and provide structured analysis. It consists of a FastAPI backend for processing text with a Large Language Model (LLM) and a React frontend for user interaction and displaying the results.

Features
Text Analysis: Analyzes text to generate a title, a summary, a list of topics, keywords, and sentiment.

Search Functionality: Allows users to search for previously analyzed text by topic.

Modern UI: A clean, responsive user interface built with React.

Backend (backend/)
The backend is a FastAPI application that handles all text processing and data persistence.

Prerequisites
Python 3.12 or higher.

uv (Universal Installer)

Setup
Navigate to the backend directory:

Bash

cd backend
Install dependencies using uv:

Bash

uv sync
Run the application with Uvicorn:

Bash

uvicorn app:app --reload
The server will run on http://localhost:8000.

API Endpoints
POST /analyze

Description: Analyzes a given text.

Request Body:

JSON

{
  "text": "The text to be analyzed."
}
Response:

JSON

{
  "title": "...",
  "summary": "...",
  "topics": ["...", "..."],
  "keywords": ["...", "..."],
  "sentiment": "..."
}
GET /search?topic={query}

Description: Searches for analyses by a specific topic.

Query Parameters: topic (string)

Response: A list of analysis objects.
