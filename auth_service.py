"""
Authentication Service for PageSage AI Book Assistant.
Handles user registration, credential hashing, and SQLite persistence.
"""

import os
import sqlite3
from typing import Dict, Any, Optional, Tuple
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "pagesage_users.db")

def get_db_connection() -> sqlite3.Connection:
    """Create and return a database connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and seed default demo account if needed."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if demo account exists
        cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@pagesage.com",))
        if not cursor.fetchone():
            demo_hash = generate_password_hash("pagesage123")
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                ("Alex Reader", "demo@pagesage.com", demo_hash)
            )
        conn.commit()

# Ensure table exists on import
init_db()

def register_user(name: str, email: str, password: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Register a new user account. Returns (user_dict, error_message)."""
    name = (name or "").strip()
    email = (email or "").strip().lower()
    password = (password or "").strip()

    if not name or len(name) < 2:
        return None, "Name must be at least 2 characters long."
    if not email or "@" not in email or "." not in email:
        return None, "Please provide a valid email address."
    if not password or len(password) < 6:
        return None, "Password must be at least 6 characters long."

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Check for existing email
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                return None, "An account with this email address already exists."

            hashed = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, hashed)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return {
                "id": user_id,
                "name": name,
                "email": email
            }, None
    except Exception as e:
        return None, f"Database error during registration: {str(e)}"

def authenticate_user(email: str, password: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Verify credentials and return user record if valid."""
    email = (email or "").strip().lower()
    password = (password or "").strip()

    if not email or not password:
        return None, "Email and password are required."

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if not row:
                return None, "Invalid email or password."

            if not check_password_hash(row["password_hash"], password):
                return None, "Invalid email or password."

            return {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"]
            }, None
    except Exception as e:
        return None, f"Authentication error: {str(e)}"

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Fetch user record by ID."""
    if user_id == 0:
        return {"id": 0, "name": "Guest Bibliophile", "email": "guest@pagesage.com"}
        
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return {"id": row["id"], "name": row["name"], "email": row["email"]}
    except Exception:
        pass
    return None
