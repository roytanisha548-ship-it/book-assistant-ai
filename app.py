"""
PageSage - AI Book Assistant
Flask Web Application & API Server.
"""

import os
from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from literary_agent import LiteraryAgent
from book_service import (
    CURATED_BOOKS,
    search_open_library,
    search_local_books,
    get_book_by_id,
    get_recommendations_by_mood_or_genre
)
from auth_service import register_user, authenticate_user, get_user_by_id

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "pagesage-secret-session-key-2026")
agent = LiteraryAgent()

@app.route("/")
def index():
    """Render the primary single-page application interface if authenticated."""
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template(
        "index.html",
        user_name=session.get("user_name", "Bibliophile"),
        user_email=session.get("user_email", "")
    )

@app.route("/login")
def login_page():
    """Render the login and registration interface."""
    if "user_id" in session:
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/api/auth/login", methods=["POST"])
def auth_login_endpoint():
    """Authenticate user with email and password."""
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    user, error = authenticate_user(email, password)
    if error or not user:
        return jsonify({"success": False, "error": error or "Invalid credentials"}), 400

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]
    return jsonify({"success": True, "user": user})

@app.route("/api/auth/register", methods=["POST"])
def auth_register_endpoint():
    """Register a new reader account."""
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    user, error = register_user(name, email, password)
    if error or not user:
        return jsonify({"success": False, "error": error or "Registration failed"}), 400

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]
    return jsonify({"success": True, "user": user})

@app.route("/api/auth/guest", methods=["POST"])
def auth_guest_endpoint():
    """Instant login as guest bibliophile."""
    session["user_id"] = 0
    session["user_name"] = "Guest Bibliophile"
    session["user_email"] = "guest@pagesage.com"
    return jsonify({
        "success": True,
        "user": {
            "id": 0,
            "name": "Guest Bibliophile",
            "email": "guest@pagesage.com"
        }
    })

@app.route("/logout")
@app.route("/api/auth/logout", methods=["GET", "POST"])
def auth_logout_endpoint():
    """Clear session and redirect to login page."""
    session.clear()
    if request.path.startswith("/api/"):
        return jsonify({"success": True, "message": "Logged out successfully"})
    return redirect(url_for("login_page"))

@app.route("/api/auth/me", methods=["GET"])
def auth_me_endpoint():
    """Return currently active user profile."""
    if "user_id" in session:
        return jsonify({
            "authenticated": True,
            "user": {
                "id": session.get("user_id"),
                "name": session.get("user_name"),
                "email": session.get("user_email")
            }
        })
    return jsonify({"authenticated": False, "user": None})

@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    """Handle chat messages with the AI Literary Agent."""
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    
    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400
        
    conversation_history = data.get("conversation_history", [])
    api_key = data.get("api_key", "").strip()
    spoiler_shield = data.get("spoiler_shield", True)
    preferences = data.get("preferences", {})

    try:
        response = agent.chat(
            message=message,
            conversation_history=conversation_history,
            api_key=api_key,
            spoiler_shield=spoiler_shield,
            user_preferences=preferences
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({
            "error": "Failed to process chat query",
            "details": str(e)
        }), 500

@app.route("/api/search", methods=["GET"])
def search_endpoint():
    """Search for books using Open Library and curated internal library."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])
    
    results = search_open_library(query, limit=8)
    return jsonify(results)

@app.route("/api/curated", methods=["GET"])
def curated_endpoint():
    """Return the curated list of popular books."""
    genre = request.args.get("genre")
    mood = request.args.get("mood")
    trope = request.args.get("trope")
    
    if genre or mood or trope:
        books = get_recommendations_by_mood_or_genre(genre=genre, mood=mood, trope=trope)
    else:
        books = CURATED_BOOKS
    return jsonify(books)

@app.route("/api/book/<book_id>", methods=["GET"])
def book_detail_endpoint(book_id):
    """Retrieve details for a specific book."""
    book = get_book_by_id(book_id)
    if not book:
        # Try search
        matches = search_local_books(book_id)
        if matches:
            book = matches[0]
            
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

@app.route("/api/status", methods=["GET"])
def status_endpoint():
    """Check system status and configuration."""
    return jsonify({
        "status": "online",
        "name": "PageSage AI Book Assistant",
        "version": "1.0.0",
        "gemini_env_key_set": bool(os.environ.get("GEMINI_API_KEY")),
        "curated_books_count": len(CURATED_BOOKS)
    })

@app.route("/download-report", methods=["GET"])
def download_report():
    """Serve the generated Word document directly as a browser download."""
    doc_path = os.path.join(os.path.dirname(__file__), "PageSage_AI_Project_Report.docx")
    if os.path.exists(doc_path):
        return send_file(
            doc_path,
            as_attachment=True,
            download_name="PageSage_AI_Project_Report.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    return jsonify({"error": "Report file not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"📖 Starting PageSage AI Book Assistant on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
