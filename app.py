"""
PageSage - AI Book Assistant
Flask Web Application & API Server.
"""

import os
from flask import Flask, render_template, request, jsonify
from literary_agent import LiteraryAgent
from book_service import (
    CURATED_BOOKS,
    search_open_library,
    search_local_books,
    get_book_by_id,
    get_recommendations_by_mood_or_genre
)

app = Flask(__name__)
agent = LiteraryAgent()

@app.route("/")
def index():
    """Render the primary single-page application interface."""
    return render_template("index.html")

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"📖 Starting PageSage AI Book Assistant on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
