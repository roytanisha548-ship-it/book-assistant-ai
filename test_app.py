"""
Unit and Integration Tests for PageSage AI Book Assistant.
Covers literary service, agents, authentication, and endpoints.
"""

import unittest
import json
import time
from app import app
from book_service import (
    search_local_books,
    get_book_by_id,
    get_recommendations_by_mood_or_genre,
    CURATED_BOOKS
)
from literary_agent import LiteraryAgent
from auth_service import register_user, authenticate_user, get_user_by_id

class TestBookService(unittest.TestCase):
    def test_curated_books_not_empty(self):
        self.assertGreater(len(CURATED_BOOKS), 5)
        for b in CURATED_BOOKS:
            self.assertIn("title", b)
            self.assertIn("author", b)
            self.assertIn("genre", b)
            self.assertIn("description", b)
            self.assertIn("spoiler_summary", b)

    def test_search_local_books(self):
        results = search_local_books("Project Hail Mary")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["title"], "Project Hail Mary")
        self.assertEqual(results[0]["author"], "Andy Weir")

    def test_search_by_genre_or_mood(self):
        scifi = get_recommendations_by_mood_or_genre(genre="Science Fiction")
        self.assertTrue(any("Science Fiction" in b["genre"] for b in scifi))

    def test_get_book_by_id(self):
        book = get_book_by_id("dune")
        self.assertIsNotNone(book)
        self.assertEqual(book["title"], "Dune")

class TestLiteraryAgent(unittest.TestCase):
    def setUp(self):
        self.agent = LiteraryAgent()

    def test_offline_summary_with_spoiler_shield(self):
        res = self.agent.chat(
            message="Summarize Project Hail Mary",
            spoiler_shield=True
        )
        self.assertIn("text", res)
        self.assertIn("spoiler-box", res["text"])
        self.assertIn("Project Hail Mary", res["text"])
        self.assertGreater(len(res["book_cards"]), 0)

    def test_offline_summary_without_spoiler_shield(self):
        res = self.agent.chat(
            message="Explain the ending of The Silent Patient",
            spoiler_shield=False
        )
        self.assertIn("text", res)
        self.assertIn("The Silent Patient", res["text"])
        self.assertIn("Theo Faber", res["text"])

    def test_offline_book_club_guide(self):
        res = self.agent.chat(
            message="Give me book club discussion questions for The Great Gatsby"
        )
        self.assertIn("Discussion Questions", res["text"])
        self.assertIn("Great Gatsby", res["text"])

    def test_offline_reading_order(self):
        res = self.agent.chat(
            message="What is the reading order for Brandon Sanderson Cosmere?"
        )
        self.assertIn("Mistborn", res["text"])
        self.assertIn("Stormlight", res["text"])

    def test_offline_recommendations(self):
        res = self.agent.chat(
            message="Recommend some cozy mysteries or atmospheric detective books"
        )
        self.assertIn("Recommendations", res["text"])
        self.assertGreater(len(res["book_cards"]), 0)

class TestAuthentication(unittest.TestCase):
    def test_demo_user_authentication(self):
        user, err = authenticate_user("demo@pagesage.com", "pagesage123")
        self.assertIsNone(err)
        self.assertIsNotNone(user)
        self.assertEqual(user["email"], "demo@pagesage.com")

    def test_invalid_password(self):
        user, err = authenticate_user("demo@pagesage.com", "wrongpassword")
        self.assertIsNone(user)
        self.assertIn("Invalid", err)

    def test_new_user_registration(self):
        unique_email = f"reader_{int(time.time())}@example.com"
        user, err = register_user("Jane Austen Fan", unique_email, "securepass123")
        self.assertIsNone(err)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "Jane Austen Fan")

        # Duplicate registration should fail
        dup_user, dup_err = register_user("Jane Clone", unique_email, "anotherpass")
        self.assertIsNone(dup_user)
        self.assertIn("already exists", dup_err)

class TestFlaskEndpoints(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_unauthenticated_index_redirects(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.headers["Location"])

    def test_login_page_renders(self):
        resp = self.client.get("/login")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Sign In", resp.data)
        self.assertIn(b"PageSage", resp.data)

    def test_guest_login_flow(self):
        resp = self.client.post("/api/auth/guest")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["user"]["name"], "Guest Bibliophile")

        # Now / should succeed
        index_resp = self.client.get("/")
        self.assertEqual(index_resp.status_code, 200)
        self.assertIn(b"Guest Bibliophile", index_resp.data)

    def test_demo_login_flow(self):
        payload = {"email": "demo@pagesage.com", "password": "pagesage123"}
        resp = self.client.post(
            "/api/auth/login",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data["success"])

        # Check me endpoint
        me_resp = self.client.get("/api/auth/me")
        me_data = json.loads(me_resp.data)
        self.assertTrue(me_data["authenticated"])

        # Logout
        logout_resp = self.client.get("/logout")
        self.assertEqual(logout_resp.status_code, 302)

    def test_status_route(self):
        resp = self.client.get("/api/status")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "online")
        self.assertGreater(data["curated_books_count"], 0)

    def test_curated_route(self):
        resp = self.client.get("/api/curated")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_book_detail_route(self):
        resp = self.client.get("/api/book/dune")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["title"], "Dune")

    def test_chat_endpoint_success(self):
        payload = {
            "message": "What should I read if I love space exploration and witty characters?",
            "spoiler_shield": True
        }
        resp = self.client.post(
            "/api/chat",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn("text", data)
        self.assertIn("book_cards", data)

    def test_chat_endpoint_empty_message(self):
        resp = self.client.post(
            "/api/chat",
            data=json.dumps({"message": ""}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

if __name__ == "__main__":
    unittest.main()
