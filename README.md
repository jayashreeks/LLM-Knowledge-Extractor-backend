## LLM-Knowledge-Extractor-backend
This is a full-stack web application designed to analyze text and provide structured insights. It features a FastAPI backend for powerful text processing with a Large Language Model (LLM) and a modern React frontend for a clean, intuitive user interface.

###**Key Features**
**Intelligent Text Analysis**: Processes text to generate a title, a concise summary, sentiment, topics, and keywords.

**Search Functionality**: Allows users to search for and retrieve past analysis results based on topics.

**Modern UI**: A responsive and visually appealing user interface built with React, Vite, and custom CSS for a seamless user experience.

####**Tech Stack**
Backend: Python, FastAPI, uvicorn, SQLAlchemy, google-genai

Frontend: React, Vite, JavaScript, CSS

Package Management: uv for the backend

#####Getting Started
Follow these steps to set up and run the project locally.

1. Backend Setup
Navigate to the backend directory.

Bash

cd backend
2. Install all Python dependencies using uv.

Bash

uv sync
3. Start the backend server. The API will be available at http://localhost:8000.

Bash

uvicorn app:app --reload

Description: Searches for analyses by a specific topic.

Query Parameters: topic (string)

Response: A list of analysis objects.

####**API Reference**
POST /analyze
Analyzes a block of text and saves the result to the database.

URL: http://localhost:8000/analyze

Request Body: {"text": "Your text to analyze."}

Response: {"title": "...", "summary": "...", "sentiment": "...", "topics": ["..."], "keywords": ["..."]}

GET /search?topic={query}
Searches the database for past analyses containing the specified topic.

URL: http://localhost:8000/search?topic=climate

Query Parameter: topic (string)

Response: A list of analysis objects.
