# 📖 PageSage — AI Literary Companion & Book Assistant

An intelligent, aesthetic AI-powered chatbot and reading companion built for bibliophiles, casual readers, and book clubs.

![PageSage Book Assistant](https://images.unsplash.com/photo-1507842229451-7f01be837402?auto=format&fit=crop&q=80&w=1200)

---

## ✨ Features & Capabilities

1. **Dual-Intelligence Architecture**:
   - **Google Gemini Cloud AI**: Powered by `gemini-2.5-flash` for open-ended, deep literary reasoning, bespoke recommendations, and thematic explorations.
   - **Offline Literary Engine**: Instant, high-fidelity literary intelligence engine working out-of-the-box without needing any API keys.
2. **🛡️ Active Spoiler Shield**:
   - Easily toggle spoiler protection.
   - Summaries, plot breakdowns, and character analyses hide major climaxes, twists, and murder culprits behind elegant `<details>` click-to-reveal spoiler shields.
3. **📚 Interactive Bookshelf & Reading Tracker**:
   - Save books directly to **Want to Read**, **Currently Reading**, or **Finished**.
   - Move between shelves with 1 click.
   - Persisted in browser `localStorage`.
   - One-click export to Markdown (`.md`) format.
4. **🔍 Interactive Book Cards**:
   - Rich book cards with cover art, author, publication year, rating badges, and one-click bookshelf addition.
5. **👥 Book Club Assistant**:
   - Generates stimulating discussion questions, pacing assessments, debate catalysts, and themed food/refreshment pairing ideas.
6. **⚡ Series Reading Order Guides**:
   - Chronological vs. Publication order guides for complex fantasy and sci-fi sagas (e.g., Sanderson's Cosmere, Frank Herbert's *Dune*, Tolkien, etc.).
7. **🎨 Modern Dark Academia & Light Themes**:
   - Thoughtfully crafted responsive UI with warm amber highlights, refined typography, and mobile-friendly sidebar navigation.

---

## 🚀 Quick Start

### 1. Requirements
Ensure Python 3.10+ is installed. The required packages are:
```bash
pip install -r requirements.txt
```
*(Flask 3.x and requests are already installed on your system).*

### 2. Launch the Application
Run the Flask server:
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 AI Engine Configuration (Optional Gemini API Key)

PageSage is fully functional right away with its internal offline literary intelligence engine.

If you would like to enable the **Google Gemini 2.5 Flash** model:
1. Tap the **Settings icon** (`⚙️`) in the PageSage sidebar or top card.
2. Paste your Google Gemini API Key into the input field.
3. Click **Save Preferences**.
*(Alternatively, set the environment variable: `set GEMINI_API_KEY=your_key_here` before running `python app.py`)*.

---

## 🧪 Testing

A comprehensive unit and integration test suite is included:
```bash
python -m unittest test_app.py
```
All 15 tests cover intent analysis, spoiler shields, book search, local knowledge bases, and API endpoints.

---

## 📁 Project Structure

```
book-assistant-ai/
├── app.py                  # Flask web server and REST API endpoints
├── book_service.py         # Curated literary database and OpenLibrary search
├── literary_agent.py       # Dual-engine AI (Gemini REST + Offline NLP)
├── requirements.txt        # Python dependencies
├── test_app.py             # 15 Unit & integration tests
├── templates/
│   └── index.html          # Responsive single-page application UI
└── static/
    ├── css/
    │   └── style.css       # Dark Academia and Light responsive styles
    └── js/
        └── app.js          # Client-side state, chat logic, and bookshelf
```
