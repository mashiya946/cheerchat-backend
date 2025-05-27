import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import cohere

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Journaling file
JOURNAL_FILE = "journals.json"
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w") as f:
        json.dump([], f)

# 🔥 Add your chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    try:
        response = co.chat(
            message=message,
            model="command-r-plus",
            temperature=0.6
        )
        reply = response.text.strip()
    except Exception as e:
        reply = f"Sorry, something went wrong. ({str(e)})"

    return jsonify({"reply": reply})

# Optional: journaling route (you can add more)
@app.route("/journal", methods=["POST"])
def save_journal():
    entry = request.json.get("text", "")
    with open(JOURNAL_FILE, "r") as f:
        data = json.load(f)
    data.append(entry)
    with open(JOURNAL_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "saved"})

# ✅ Run the app with the correct host + port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
