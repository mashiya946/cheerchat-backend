import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import cohere

# Load .env and Cohere key
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Ensure journal file exists
JOURNAL_FILE = "journals.json"
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w") as f:
        json.dump([], f)

# Root route (optional)
@app.route("/")
def home():
    return "CheerChat backend is running 💙"

# /chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    try:
        response = co.chat(
            message=message,
            model="command-r-plus",
            temperature=0.6,
            chat_history=[],
            prompt_truncation="auto",
            preamble="""
You are CheerChat 💙 — a kind, supportive AI built by a teenager to help other teens with their mental health and daily struggles.

If someone asks “Who built you?”, reply: “I was built by a teenager just like you.”

If someone asks “What are your uses?”, say: “I help teens struggling with emotions like stress, sadness, or anxiety. I offer emotional support, motivation, breathing exercises, journaling, and even homework help!”

Always be kind, warm, supportive, and honest.
"""
        )
        reply = response.text.strip()
    except Exception as e:
        reply = f"Sorry, something went wrong. ({str(e)})"

    return jsonify({"reply": reply})

# Optional: journal endpoint
@app.route("/journal", methods=["POST"])
def save_journal():
    entry = request.json.get("text", "")
    with open(JOURNAL_FILE, "r") as f:
        data = json.load(f)
    data.append(entry)
    with open(JOURNAL_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "saved"})

# Required for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
