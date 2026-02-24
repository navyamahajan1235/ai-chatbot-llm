# AI Chatbot with Multi-Conversation Memory

A full-stack AI chatbot built using Flask, SQLite, and TinyLlama (via Ollama).  
Supports multiple conversations with persistent chat history.

## Features

- Multi-conversation chat system
- Persistent chat history using SQLite
- Local LLM integration using TinyLlama
- Modern sidebar UI
- Conversation switching
- Delete and clear conversations
- Fast and lightweight

## Tech Stack

Backend:
- Python
- Flask
- SQLite

Frontend:
- HTML
- CSS
- JavaScript

AI:
- TinyLlama
- Ollama

## How it works

Flask handles user requests, stores conversations in SQLite, and sends messages to TinyLlama via Ollama for generating responses.

## Run locally

Install dependencies:

pip install -r requirements.txt

Start Ollama:

ollama run tinyllama

Run app:

python app.py