"""
Literary Agent for PageSage AI Book Assistant.
Provides dual-mode intelligence:
1. Google Gemini API integration (via direct REST API) when API key is provided.
2. Built-in Offline Literary Intelligence Engine with natural intent parsing,
   rich book recommendations, spoiler shields, and literary analysis.
"""

import os
import json
import re
import requests
from typing import Dict, Any, List, Optional
from book_service import (
    CURATED_BOOKS,
    search_local_books,
    search_open_library,
    get_book_by_id,
    get_recommendations_by_mood_or_genre
)

SYSTEM_PROMPT = """You are PageSage, a world-class literary companion, bibliophile, and expert book assistant.
Your knowledge spans classic literature, contemporary fiction, genre fiction (Sci-Fi, Fantasy, Thrillers, Romance, Horror), non-fiction, philosophy, and poetry.

Your Personality:
- Warm, erudite, enthusiastic about reading, insightful, and attentive to reader tastes.
- Tailor suggestions to the reader's preferred pacing, emotional tone, tropes, and reading level.
- When summarizing or discussing plots, ALWAYS respect the user's spoiler preference:
  - If spoiler protection is requested, provide a compelling premise without ruining twists. If you must mention a twist, wrap it in a spoiler tag: `[SPOILER: your spoiler text here]`.
  - If spoilers are allowed, provide an in-depth analysis of the climax, thematic resolution, and twists.
- When recommending books, format each recommendation clearly with:
  - **Title** by Author (Year)
  - *The Vibe / Pitch*: 1-2 punchy sentences.
  - *Why You'll Love It*: How it matches what the user asked for.
  - *Key Tropes & Themes*: Short bullet tags.
- At the end of your response, when mentioning specific books, include a hidden JSON comment block with the books so the UI can render rich interactive book cards:
<!-- BOOKS: [{"title": "Title", "author": "Author"}] -->
"""

class LiteraryAgent:
    def __init__(self):
        self.default_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.discovered_model: Optional[str] = None

    def _discover_model(self, api_key: str) -> List[str]:
        """
        Dynamically query Google's ModelService to find models that support generateContent
        for this exact API key and project tier.
        """
        if self.discovered_model:
            return [self.discovered_model]

        discovered = []
        for version in ["v1beta", "v1"]:
            try:
                list_url = f"https://generativelanguage.googleapis.com/{version}/models?key={api_key}"
                resp = requests.get(list_url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    models = data.get("models", [])
                    # Filter for models supporting generateContent
                    gen_models = [
                        f"{version}/{m['name']}"
                        for m in models
                        if "generateContent" in m.get("supportedGenerationMethods", [])
                    ]
                    # Prioritize Flash models, then Pro, then others
                    flash_models = [m for m in gen_models if "flash" in m.lower()]
                    other_models = [m for m in gen_models if "flash" not in m.lower()]
                    discovered.extend(flash_models + other_models)
                    if discovered:
                        break
            except Exception:
                pass

        # Static fallback list in case ListModels is blocked
        static_fallbacks = [
            "v1beta/models/gemini-2.0-flash",
            "v1beta/models/gemini-2.5-flash",
            "v1beta/models/gemini-1.5-flash-latest",
            "v1beta/models/gemini-1.5-pro",
            "v1/models/gemini-1.5-flash",
            "v1beta/models/gemini-pro"
        ]
        
        return discovered if discovered else static_fallbacks

    def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        api_key: Optional[str] = None,
        spoiler_shield: bool = True,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user query and return response text, metadata, and book cards.
        """
        active_key = api_key or self.default_api_key
        conversation_history = conversation_history or []

        # If API key is available, attempt Gemini REST API
        if active_key and active_key.strip():
            try:
                gemini_res = self._call_gemini_api(
                    message=message,
                    conversation_history=conversation_history,
                    api_key=active_key.strip(),
                    spoiler_shield=spoiler_shield,
                    user_preferences=user_preferences
                )
                if gemini_res:
                    return gemini_res
            except Exception as e:
                # Fall back to offline agent with notice
                offline_res = self._offline_reasoning(message, spoiler_shield, user_preferences)
                offline_res["notice"] = f"Cloud AI request failed ({str(e)}). Switched to Offline Literary Engine."
                return offline_res

        # Default to high-fidelity Offline Literary Engine
        return self._offline_reasoning(message, spoiler_shield, user_preferences)

    def _call_gemini_api(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        api_key: str,
        spoiler_shield: bool,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Call Gemini REST API with dynamic model discovery and fallback."""
        candidate_paths = self._discover_model(api_key)
        
        # Build contents from history
        contents = []
        
        # Context note about user preferences & spoiler mode
        prefs_note = ""
        if user_preferences:
            fav_genres = ", ".join(user_preferences.get("genres", []))
            fav_authors = ", ".join(user_preferences.get("authors", []))
            prefs_note = f"\nReader profile: Favorite genres: [{fav_genres}]. Favorite authors: [{fav_authors}]."
            
        spoiler_note = "\nSPOILER SHIELD IS ACTIVE. Do NOT reveal major twists, murder culprits, or surprise endings without wrapping in [SPOILER: ...]." if spoiler_shield else "\nSpoilers are permitted: feel free to analyze major twists openly."

        system_instruction_text = SYSTEM_PROMPT + prefs_note + spoiler_note

        for msg in conversation_history[-6:]:
            role = "user" if msg.get("role") == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.get("content", "")}]
            })
            
        contents.append({
            "role": "user",
            "parts": [{"text": message}]
        })

        payload = {
            "system_instruction": {
                "parts": [{"text": system_instruction_text}]
            },
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1800
            }
        }

        headers = {"Content-Type": "application/json"}
        last_error = None

        for path in candidate_paths:
            # path is formatted as: "{version}/{name}" e.g. "v1beta/models/gemini-2.0-flash"
            if path.startswith("http"):
                url = f"{path}:generateContent?key={api_key}"
            else:
                clean_path = path.lstrip("/")
                url = f"https://generativelanguage.googleapis.com/{clean_path}:generateContent?key={api_key}"

            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=12)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        
                        # Cache the working model path for future calls
                        self.discovered_model = path
                        model_name = path.split("/")[-1]
                        
                        # Extract embedded book JSON if present
                        book_cards = []
                        match = re.search(r'<!--\s*BOOKS:\s*(\[.*?\])\s*-->', raw_text, re.DOTALL)
                        if match:
                            try:
                                books_meta = json.loads(match.group(1))
                                for b in books_meta:
                                    title = b.get("title", "")
                                    found = search_local_books(title)
                                    if found:
                                        book_cards.append(found[0])
                                    else:
                                        book_cards.append({
                                            "id": re.sub(r'\W+', '-', title.lower()).strip('-'),
                                            "title": title,
                                            "author": b.get("author", "Various"),
                                            "year": b.get("year", "N/A"),
                                            "genre": "Recommended Read",
                                            "cover_url": None,
                                            "rating": 4.5,
                                            "description": f"Featured literary recommendation by {b.get('author', 'Author')}."
                                        })
                            except Exception:
                                pass
                        
                        clean_text = re.sub(r'<!--\s*BOOKS:.*?-->', '', raw_text, flags=re.DOTALL).strip()
                        return {
                            "text": clean_text,
                            "book_cards": book_cards,
                            "engine": "gemini-cloud",
                            "model": model_name
                        }
                elif resp.status_code in [404, 400]:
                    last_error = f"Gemini API returned status {resp.status_code}: {resp.text}"
                    continue
                else:
                    last_error = f"Gemini API returned status {resp.status_code}: {resp.text}"
            except Exception as e:
                last_error = str(e)
                continue

        raise RuntimeError(last_error or "Failed to connect to an active Gemini model.")

    def _offline_reasoning(
        self,
        query: str,
        spoiler_shield: bool,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Intelligent offline literary reasoning system.
        Analyzes intent, entities, themes, tropes, and returns tailored literary responses.
        """
        q_lower = query.lower()
        
        # 1. Check for specific book queries in our curated library
        matched_books = search_local_books(query)
        primary_book = matched_books[0] if matched_books else None
        
        # Intent: Summary / Plot Explanation
        if any(w in q_lower for w in ["summarize", "summary", "plot", "what is it about", "explain", "synopsis"]):
            if primary_book:
                return self._generate_summary_response(primary_book, spoiler_shield)
                
        # Intent: Book Club / Discussion Questions
        if any(w in q_lower for w in ["book club", "discussion questions", "questions for", "talk about"]):
            if primary_book:
                return self._generate_book_club_response(primary_book)

        # Intent: Character Analysis
        if any(w in q_lower for w in ["character", "who is", "protagonist", "antagonist", "cast"]):
            if primary_book:
                return self._generate_character_response(primary_book)

        # Intent: Reading Order
        if any(w in q_lower for w in ["reading order", "order to read", "where to start", "chronological"]):
            return self._generate_reading_order_response(query)

        # Intent: Read-alikes / "Books like X"
        if any(phrase in q_lower for phrase in ["books like", "similar to", "if i loved", "if you like", "read after"]):
            if primary_book:
                return self._generate_read_alikes_response(primary_book)

        # Intent: Mood / Genre / Trope Recommendations
        genre_keywords = {
            "sci-fi": "Science Fiction", "science fiction": "Science Fiction", "space": "Science Fiction",
            "fantasy": "Fantasy", "magic": "Fantasy",
            "mystery": "Mystery & Thriller", "thriller": "Mystery & Thriller", "crime": "Mystery & Thriller", "detective": "Mystery & Thriller",
            "horror": "Horror", "gothic": "Horror", "spooky": "Horror", "creepy": "Horror",
            "romance": "Romance", "love": "Romance", "dating": "Romance",
            "classic": "Classics", "classics": "Classics", "literature": "Classics",
            "dystopian": "Dystopian", "apocalyptic": "Dystopian",
            "non-fiction": "Self-Growth & Psychology", "habits": "Self-Growth & Psychology", "productivity": "Self-Growth & Psychology"
        }
        
        mood_keywords = {
            "cozy": "charming", "comfort": "heartwarming", "dark": "dark", "grim": "dark",
            "scary": "terrifying", "creepy": "chilling", "spooky": "chilling", "terrifying": "terrifying",
            "funny": "humorous", "witty": "witty", "tense": "tense", "fast-paced": "suspenseful",
            "mind-bending": "philosophical", "deep": "philosophical", "emotional": "emotional"
        }

        detected_genre = next((v for k, v in genre_keywords.items() if k in q_lower), None)
        detected_mood = next((v for k, v in mood_keywords.items() if k in q_lower), None)

        if detected_genre or detected_mood or any(w in q_lower for w in ["recommend", "suggestion", "what to read", "next book", "good books"]):
            return self._generate_recommendation_response(detected_genre, detected_mood, query)

        # General book search / conversational query
        if matched_books:
            return self._generate_book_overview_response(matched_books[:3], query)

        # Default helpful bibliophile response
        return self._generate_general_guidance(query)

    def _generate_summary_response(self, book: Dict[str, Any], spoiler_shield: bool) -> Dict[str, Any]:
        title = book["title"]
        author = book["author"]
        year = book["year"]
        genre = book["genre"]
        desc = book["description"]
        spoiler_text = book["spoiler_summary"]
        themes = ", ".join(book["themes"])

        if spoiler_shield:
            text = f"""### 📖 Overview: *{title}* by {author} ({year})

**Genre**: {genre}  
**Central Themes**: {themes}

#### Premise & Core Conflict
{desc}

---

#### 🛡️ Spoiler Shield Active
Major plot revelations, climactic twists, and the ending have been shielded to protect your reading experience.

<details class="spoiler-box">
<summary>⚠️ <strong>Click to reveal spoiler-heavy plot details & ending</strong></summary>
<p>{spoiler_text}</p>
</details>

*Need character breakdowns, thematic analysis, or reading recommendations like this? Ask me anytime!*
"""
        else:
            text = f"""### 📖 Full Synopsis & Plot Breakdown: *{title}* by {author} ({year})

**Genre**: {genre}  
**Central Themes**: {themes}

#### Premise
{desc}

#### ⚡ Full Narrative & Ending Analysis (Spoilers Unveiled)
{spoiler_text}

#### 🔍 Thematic Significance
The resolution ties directly into the primary themes: *{themes}*. It challenges conventional tropes in the {genre} genre by blending emotional stakes with intellectual inquiry.
"""
        return {
            "text": text,
            "book_cards": [book],
            "engine": "offline-intelligence",
            "model": "PageSage Literary Core"
        }

    def _generate_book_club_response(self, book: Dict[str, Any]) -> Dict[str, Any]:
        title = book["title"]
        author = book["author"]
        questions = book.get("discussion_questions", [
            "How does the setting act as a character in its own right?",
            "Were the protagonist's choices morally justified given their circumstances?",
            "What lasting questions does the ending leave with the reader?"
        ])
        themes = ", ".join(book["themes"])

        q_list = "\n".join([f"{idx+1}. **{q}**" for idx, q in enumerate(questions)])

        text = f"""### 👥 Book Club Discussion Guide: *{title}* by {author}

*A curated set of conversation catalysts designed for lively debate, literary appreciation, and deep reflection.*

**Primary Themes to Explore**: {themes}

---

#### 🗣️ Discussion Questions
{q_list}

#### 💡 Host Tips for the Meeting:
- **Opening Warmup**: Ask each attendee to rate the book on a scale of 1 to 5 stars, describing their experience in just three adjectives.
- **Trope Exploration**: Discuss how *{title}* handles {book.get('tropes', ['its premise'])[0]} compared to traditional works in {book['genre']}.
- **Pairing Idea**: Serve snacks or refreshments inspired by the book's setting!
"""
        return {
            "text": text,
            "book_cards": [book],
            "engine": "offline-intelligence",
            "model": "PageSage Literary Core"
        }

    def _generate_character_response(self, book: Dict[str, Any]) -> Dict[str, Any]:
        title = book["title"]
        characters = book.get("characters", [])
        
        char_md = ""
        for c in characters:
            char_md += f"- **{c['name']}**: {c['role']}\n"

        text = f"""### 🎭 Character Dossier: *{title}*

Here is an analysis of the key figures driving the narrative momentum:

{char_md}

#### Narrative Dynamics
These characters create tension through their conflicting motivations, ethical dilemmas, and distinct worldviews. Their interpersonal friction directly mirrors the broader thematic conflict of {', '.join(book.get('themes', ['the story']))}.
"""
        return {
            "text": text,
            "book_cards": [book],
            "engine": "offline-intelligence",
            "model": "PageSage Literary Core"
        }

    def _generate_read_alikes_response(self, book: Dict[str, Any]) -> Dict[str, Any]:
        title = book["title"]
        author = book["author"]
        read_alikes = book.get("read_alikes", [])
        
        alikes_md = "\n".join([f"- **{item}**" for item in read_alikes])

        text = f"""### 📚 If You Loved *{title}* by {author}...

Here are handcrafted recommendations that capture a similar spirit, narrative pace, or emotional resonance:

{alikes_md}

#### Why These Work:
These titles share *{title}*'s DNA—whether it's the distinctive atmosphere, complex character arcs, or thematic exploration of {', '.join(book.get('themes', ['human nature']))}.

Would you like a spoiler-free premise for any of these?
"""
        # Collect any matching local books
        cards = [book]
        for ra in read_alikes[:2]:
            ra_title = ra.split(" by ")[0]
            matched = search_local_books(ra_title)
            if matched:
                cards.append(matched[0])

        return {
            "text": text,
            "book_cards": cards,
            "engine": "offline-intelligence",
            "model": "PageSage Literary Core"
        }

    def _generate_recommendation_response(self, genre: Optional[str], mood: Optional[str], query: str) -> Dict[str, Any]:
        books = get_recommendations_by_mood_or_genre(genre=genre, mood=mood)
        if not books:
            books = CURATED_BOOKS[:3]

        recs_text = ""
        for b in books[:3]:
            tropes_badge = " • ".join(b.get("tropes", [])[:3])
            recs_text += f"""#### 📖 *{b['title']}* by {b['author']} ({b['year']})
- **The Pitch**: {b['description']}
- **The Vibe**: {', '.join(b.get('mood', ['engrossing']))} | Rating: ⭐ {b['rating']}/5.0
- **Tropes**: `{tropes_badge}`

"""

        header = f"### 🔮 Curated Recommendations for You"
        if genre or mood:
            details = []
            if genre: details.append(f"Genre: **{genre}**")
            if mood: details.append(f"Mood: **{mood}**")
            header += f"\n*Tailored for: {' | '.join(details)}*\n"

        text = f"""{header}

{recs_text}
---
*You can tap **"+ Add to Bookshelf"** on any card below to track it in your Want to Read list!*
"""
        return {
            "text": text,
            "book_cards": books[:3],
            "engine": "offline-intelligence",
            "model": "PageSage Literary Core"
        }

    def _generate_reading_order_response(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()
        if "cosmere" in q_lower or "sanderson" in q_lower:
            text = """### 🌌 Brandon Sanderson's Cosmere Reading Order Guide

The Cosmere is Brandon Sanderson's interconnected fantasy universe. Here are the two best starting paths:

#### Option 1: The Recommended Entry (Mistborn Path)
1. **Mistborn Era 1**:
   - *The Final Empire*
   - *The Well of Ascension*
   - *The Hero of Ages*
2. **Standalone Gems**:
   - *Warbreaker* (vital context before Stormlight Book 2)
   - *Elantris*
3. **The Epic Opus (The Stormlight Archive)**:
   - *The Way of Kings*
   - *Words of Radiance*
   - *Edgedancer* (Novella 2.5)
   - *Oathbringer*
   - *Dawnshard* (Novella 3.5)
   - *Rhythm of War*
   - *Wind and Truth*

#### Option 2: The Direct Epic Entry
Jump directly into *The Way of Kings* if you love massive 1,000+ page worldbuilding with rich cultures and deep history!
"""
            matched = search_local_books("Mistborn")
            return {
                "text": text,
                "book_cards": matched[:1],
                "engine": "offline-intelligence",
                "model": "PageSage Literary Core"
            }
        elif "dune" in q_lower:
            text = """### 🪐 Frank Herbert's *Dune* Reading Order

For the true quintessential experience of Frank Herbert's vision:

1. **Dune** (1965) - *Masterpiece; can be read as a standalone.*
2. **Dune Messiah** (1969) - *The vital deconstruction of the hero's journey.*
3. **Children of Dune** (1976) - *The transformation of Arrakis and the Golden Path begins.*
4. **God Emperor of Dune** (1981) - *Deep philosophical centerpiece set 3,500 years later.*
5. **Heretics of Dune** (1984)
6. **Chapterhouse: Dune** (1985) - *Frank Herbert's final installment.*

*Tip: Reading Books 1–3 offers a complete, brilliant original trilogy arc!*
"""
            matched = search_local_books("Dune")
            return {
                "text": text,
                "book_cards": matched[:1],
                "engine": "offline-intelligence",
                "model": "PageSage Literary Core"
            }
        else:
            return {
                "text": "### 📚 Series Reading Order Guide\n\nWhen starting a new literary series, you typically choose between **Publication Order** (experiencing the world and mysteries exactly as the author unveiled them) and **Internal Chronological Order** (following in-universe history from beginning to end).\n\nWhich specific series would you like a detailed breakdown for? (e.g., *The Lord of the Rings*, *Discworld*, *The Wheel of Time*, *The Witcher*, or *Asimov's Foundation*)?",
                "book_cards": [],
                "engine": "offline-intelligence",
                "model": "PageSage Literary Core"
            }

    def _generate_book_overview_response(self, books: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        b = books[0]
        text = f"""### 📖 *{b['title']}* by {b['author']} ({b['year']})

**Genre**: {b['genre']} | ⭐ **Rating**: {b['rating']}/5.0  
**Tropes**: {', '.join(b.get('tropes', []))}

#### About This Book
{b['description']}

#### Why Readers Recommend It
> *"{b['themes'][0].title()} explored with extraordinary depth and memorable character dynamics."*

**Notable Read-Alikes**:
{', '.join(b.get('read_alikes', ['Various classic works']))}

---
*Would you like a chapter summary, book club questions, or character breakdown for this title?*
"""
        return {
            "text": text,
            "book_cards": books[:2],
            "engine": "offline-intelligence",
            "model": "PageSage Literary Core"
        }

    def _generate_general_guidance(self, query: str) -> Dict[str, Any]:
        text = """### 📚 Welcome to PageSage!

I am your personal AI bibliophile and book assistance companion. Here are some of the ways we can explore literature together:

- 🔮 **Custom Recommendations**: Tell me your mood, favorite movies, or recent books you loved (e.g., *"Recommend a fast-paced sci-fi with an unlikely friendship"*).
- 🛡️ **Spoiler-Free Summaries**: Ask about any book's premise, themes, and pacing with active spoiler shields.
- 👥 **Book Club Guides**: Generate stimulating questions, discussion themes, and meeting ideas.
- 🎭 **Character & Theme Analysis**: Deep-dive into character motivations, symbolism, and literary devices.
- ⚡ **Series Reading Orders**: Discover where to begin complex fantasy and sci-fi universes.

What story or genre is calling to you today?
"""
        return {
            "text": text,
            "book_cards": CURATED_BOOKS[:2],
            "engine": "offline-intelligence",
            "model": "PageSage Literary Core"
        }
