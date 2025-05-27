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

# Create journals file if not present
JOURNAL_FILE = "journals.json"
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w") as f:
        json.dump([], f)
if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
