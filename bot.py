from flask_cors import CORS
from openai import OpenAI
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

def load_style_data():
    with open("dataset.txt.rtf", "r", encoding="utf-8") as file:
        return file.read()

# Load environment variables from .env
load_dotenv()

# Flask setup
app = Flask(__name__)
CORS(app, origins=["https://pranshubot.netlify.app"]

# OpenAI API Client Initialization
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Concise Texting Style
style_data = load_style_data()

def chat_with_gpt(incoming_message):
    """Generates a response mimicking Pranshu's texting style while minimizing token usage."""
    messages = [
        {"role": "system", "content": style_data},
        {"role": "user", "content": incoming_message}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6,  
        max_tokens=200  
    )

    return response.choices[0].message.content.strip()

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/chat', methods=['POST'])
def chat():
    """Receives messages from a POST request and returns the chatbot response."""
    data = request.json
    incoming_message = data.get('message', '').strip()

    if not incoming_message:
        return jsonify({"error": "No message received"}), 400

    chat_reply = chat_with_gpt(incoming_message)
    return jsonify({"response": chat_reply})

if __name__ == '__main__':
    app.run(debug=True)
