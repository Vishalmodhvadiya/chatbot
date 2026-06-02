
# Chatbot 🤖

An AI-powered chatbot built with FastAPI, Streamlit, and Groq LLM. The project supports interactive conversations with session-based chat history and is deployed using Render and Streamlit Community Cloud.

## Live Demo

https://chatbot-5f7o7njuvfppecweaqlfun.streamlit.app/

## Features

* AI-powered conversations
* Session-based chat history
* FastAPI backend
* Streamlit frontend
* Groq Llama 3.3 model integration
* Cloud deployment with Render and Streamlit

## Tech Stack

* Python
* FastAPI
* Streamlit
* Groq API
* Uvicorn

## Project Structure

```text
app/
tests/
.env.example
.gitignore
README.md
frontend.py
main.py
requirements.txt
```

## Setup

1. Clone the repository

```bash
git clone https://github.com/Vishalmodhvadiya/chatbot.git
cd chatbot
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the backend

```bash
uvicorn main:app --reload
```

5. Run the frontend

```bash
streamlit run frontend.py
```

## Author

Vishal Modhvadiya
