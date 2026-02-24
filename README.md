## AI Chatbot with Multi-Conversation Memory

A full-stack AI chatbot built using Flask, SQLite, and multiple LLM backends.

Supports both:

• Local LLM using TinyLlama (via Ollama)  
• Cloud LLM using Groq API  

Includes persistent multi-conversation memory and a modern UI.

## Features

• Multi-conversation chat system  
• Persistent chat history using SQLite  
• Local LLM support using TinyLlama (Ollama)  
• Cloud LLM support using Groq API  
• Modern sidebar UI  
• Conversation switching  
• Delete and clear conversations  
• Fast and lightweight  
• Secure API key management using .env

## Tech Stack

Backend:
• Python  
• Flask  
• SQLite  

LLM Backends:
• TinyLlama (via Ollama, local inference)  
• Groq API (cloud inference)

Frontend:
• HTML  
• CSS  
• JavaScript

## Multiple Backend Support

This project includes two versions:

• app_local.py → Uses TinyLlama via Ollama (runs locally)  
• app.py → Uses Groq API (cloud version, deployment-ready)

This demonstrates flexibility between local and cloud LLM architectures.

## How it works

Flask handles user requests, stores conversations in SQLite, and sends messages to TinyLlama via Ollama for generating responses.

## Run locally

Install dependencies:

pip install -r requirements.txt

Start Ollama:

ollama run tinyllama

Run app:

python app.py