from flask import Flask
<<<<<<< HEAD
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp
=======
from services.groq_client import generate_response
from middleware.input_sanitizer import sanitize_input
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import jsonify
from flask import request

VALID_TOKEN = "secure-token-123"
>>>>>>> 6006e12 (Day 9: Security sign-off completed — JWT auth, rate limiting, input sanitization (SQL, XSS, prompt injection, PII), validated via Postman and ZAP)

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Service is running"

<<<<<<< HEAD
@app.route("/health")
def health():
    return {"status": "ok"}

# Register all routes
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)
=======

@app.route("/test", methods=["POST"])
@limiter.limit("30 per minute")
def test():
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header or auth_header != f"Bearer {VALID_TOKEN}":
            return jsonify({
                "status": "error",
                "message": "Unauthorized access"
            }), 401

        #  Get JSON data from user
        data = request.get_json()

        prompt = data.get("prompt", "") if data else ""

        #  Sanitize input
        clean_prompt, error = sanitize_input(prompt)

        if error:
            return jsonify({
                "status": "error",
                "message": error
            }), 400

        #  Call AI
        response = generate_response(clean_prompt)

        return jsonify({
            "status": "success",
            "data": {
                "prompt": clean_prompt,
                "response": response
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.after_request
def secure_headers(response):
    # Strong CSP
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self';"
    )

    # Anti-clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # MIME sniffing protection
    response.headers["X-Content-Type-Options"] = "nosniff"

    # XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Remove server info
    response.headers.pop("Server", None)

    return response
>>>>>>> 6006e12 (Day 9: Security sign-off completed — JWT auth, rate limiting, input sanitization (SQL, XSS, prompt injection, PII), validated via Postman and ZAP)

if __name__ == "__main__":
    app.run(port=5000)