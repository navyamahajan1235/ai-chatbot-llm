from flask import Flask, render_template, request, redirect
import sqlite3
import os
import requests
from dotenv import load_dotenv


load_dotenv()



app = Flask(__name__)

# Function to connect to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            user_message TEXT,
            bot_response TEXT,
            FOREIGN KEY(conversation_id) REFERENCES conversations(id)
        )
    """)

    conn.commit()
    conn.close()

create_table()

# Fake AI function (we will replace later)
def generate_response(message):
    conn = get_db_connection()

    chats = conn.execute(
        "SELECT user_message, bot_response FROM chats ORDER BY id DESC LIMIT 5"
    ).fetchall()

    conn.close()

    context = ""

    for chat in reversed(chats):
        context += f"User: {chat['user_message']}\n"
        context += f"Assistant: {chat['bot_response']}\n"

    context += f"User: {message}\nAssistant:"

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "tinyllama",
        "prompt": context,
        "stream": True
    }

    response = requests.post(url, json=payload, stream=True)

    full_response = ""

    for line in response.iter_lines():
        if line:
            chunk = line.decode("utf-8")
            import json
            data = json.loads(chunk)
            full_response += data.get("response", "")

    response_text = full_response

# Remove unwanted User continuation
    if "User:" in response_text:
        response_text = response_text.split("User:")[0]

# Remove Assistant label
    response_text = response_text.replace("Assistant:", "").strip()

    return response_text

@app.route("/", methods=["GET"])
def index():

    conn = get_db_connection()

    # Get selected conversation_id from URL
    conversation_id = request.args.get("conversation_id")

    # If no conversation selected, get latest one
    if not conversation_id:
        conversation = conn.execute(
            "SELECT * FROM conversations ORDER BY id DESC LIMIT 1"
        ).fetchone()

        if conversation:
            conversation_id = conversation["id"]

    # Load chats of selected conversation
    if conversation_id:
        chats = conn.execute(
            "SELECT * FROM chats WHERE conversation_id = ?",
            (conversation_id,)
        ).fetchall()
    else:
        chats = []

    # Load all conversations for sidebar
    conversations = conn.execute(
        "SELECT * FROM conversations ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        chats=chats,
        conversations=conversations,
        current_conversation=conversation_id
    )

@app.route('/clear', methods=['POST'])
def clear_chat():

    conversation_id = request.form.get("conversation_id")

    conn = get_db_connection()

    # Delete chats of this conversation
    conn.execute(
        "DELETE FROM chats WHERE conversation_id = ?",
        (conversation_id,)
    )

    # Delete conversation itself
    conn.execute(
        "DELETE FROM conversations WHERE id = ?",
        (conversation_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/new_chat", methods=["POST"])
def new_chat():

    conn = get_db_connection()

    cursor = conn.execute(
        "INSERT INTO conversations (title) VALUES (?)",
        ("New Chat",)
    )

    conn.commit()

    new_id = cursor.lastrowid

    conn.close()

    return redirect(f"/?conversation_id={new_id}")

@app.route("/", methods=["POST"])
def send_message():

    message = request.form["message"]
    conversation_id = request.form["conversation_id"]

    bot_response = generate_response(message)

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO chats (conversation_id, user_message, bot_response) VALUES (?, ?, ?)",
        (conversation_id, message, bot_response)
    )
    
    # Check if conversation still has default title
    conversation = conn.execute(
        "SELECT title FROM conversations WHERE id = ?",
        (conversation_id,)
    ).fetchone()

    if conversation["title"] == "New Chat":
        
        # Generate title from first message
        title = message[:30]

        if len(message) > 30:
            title += "..."

        conn.execute(
            "UPDATE conversations SET title = ? WHERE id = ?",
            (title, conversation_id)
        )

    conn.commit()
    conn.close()

    return redirect(f"/?conversation_id={conversation_id}")

if __name__ == '__main__':
    app.run(debug=True)