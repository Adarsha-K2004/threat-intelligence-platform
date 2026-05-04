from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
import json

recommend_bp = Blueprint("recommend", __name__)


def load_prompt(input_text):
    with open("prompts/recommend.txt", "r") as f:
        template = f.read()
    return template.replace("{input}", input_text)


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.json.get("input")

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    # Step 1: Prepare prompt
    prompt = load_prompt(data)

    # Step 2: Call AI
    response = call_groq(prompt)

    # Step 3: Try to convert AI response → JSON
    try:
        parsed_response = json.loads(response)
    except Exception:
        # fallback if AI returns plain text
        parsed_response = {
            "recommendations": [],
            "raw_output": response
        }

    # Step 4: Return structured output
    return jsonify(parsed_response), 200