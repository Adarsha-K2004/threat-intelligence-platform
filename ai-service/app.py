from flask import Flask
from services.groq_client import generate_response
from middleware.input_sanitizer import sanitize_input
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import jsonify

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

@app.errorhandler(429)
def rate_limit_handler(e):
    return jsonify({
        "status": "error",
        "message": "Too many requests. Please try again later."
    }), 429

@app.route("/")
def home():
    return "AI Service Running"

@app.route("/test")
@limiter.limit("30 per minute")
def test():
    try:
        prompt = "Explain AI in simple words"

        # Sanitize input
        clean_prompt, error = sanitize_input(prompt)

        if error:
            return {
                "status": "error",
                "message": error
            }, 400

        result = generate_response(clean_prompt)

        return {
            "status": "success",
            "data": {
                "prompt": clean_prompt,
                "response": result
            }
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
