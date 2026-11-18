"""
Generates a styled, printable HTML version of the PageSage project report.
Can be opened in any web browser and printed/saved as PDF or opened in Microsoft Word.
"""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PageSage AI - Software Project Report</title>
<style>
  @page { size: A4; margin: 20mm; }
  body {
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    color: #262626;
    line-height: 1.6;
    max-width: 850px;
    margin: 40px auto;
    padding: 20px;
    background: #fff;
  }
  .page-break { page-break-after: always; }
  h1.title {
    text-align: center;
    color: #1F4E79;
    font-size: 28pt;
    margin-top: 60px;
    margin-bottom: 20px;
  }
  .subtitle {
    text-align: center;
    font-size: 16pt;
    font-weight: bold;
    margin-bottom: 10px;
  }
  .subtitle-regular {
    text-align: center;
    font-size: 14pt;
    margin-bottom: 25px;
    color: #555;
  }
  .spacer { height: 60px; }
  h2.chapter-heading {
    color: #1F4E79;
    font-size: 18pt;
    border-bottom: 2px solid #1F4E79;
    padding-bottom: 6px;
    margin-top: 40px;
    margin-bottom: 16px;
  }
  h3.section-heading {
    color: #2F5597;
    font-size: 14pt;
    margin-top: 24px;
    margin-bottom: 10px;
  }
  p { text-align: justify; margin-bottom: 12px; }
  ul { margin-left: 20px; margin-bottom: 16px; }
  li { margin-bottom: 6px; }
  li strong { color: #1F4E79; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 10pt;
  }
  th {
    background-color: #1F4E79;
    color: white;
    font-weight: bold;
    padding: 8px 10px;
    border: 1px solid #D3D3D3;
    text-align: left;
  }
  td {
    padding: 7px 10px;
    border: 1px solid #D3D3D3;
  }
  tr:nth-child(even) td { background-color: #F9FBFD; }
  .status-pass { color: green; font-weight: bold; text-align: center; }
  pre {
    background-color: #F4F4F4;
    padding: 12px;
    border-radius: 4px;
    font-family: 'Consolas', monospace;
    font-size: 9.5pt;
    line-height: 1.4;
    overflow-x: auto;
    border-left: 4px solid #1F4E79;
  }
  .placeholder {
    font-style: italic;
    color: #777;
    background: #f9f9f9;
    padding: 10px;
    border: 1px dashed #ccc;
    text-align: center;
    margin: 10px 0;
  }
</style>
</head>
<body>

<!-- PAGE 1: TITLE PAGE (Kept as is) -->
<h1 class="title">SOFTWARE PROJECT REPORT</h1>
<div class="subtitle">B.Tech 2nd Year – Computer Science and Engineering(Data Science)</div>
<div class="subtitle-regular">Academic Session: 2026–2027</div>

<div class="spacer"></div>
<div class="subtitle">Project Title: [Enter the Title of the Project]</div>

<div class="spacer"></div>
<div class="subtitle">Submitted by:</div>
<div class="subtitle-regular">1. Student Name – Roll No.</div>

<div class="spacer"></div>
<div class="subtitle">Department of Computer Science and Engineering (Data Science)</div>
<div class="subtitle-regular">[College/Institute Name]</div>

<div class="page-break"></div>

<!-- TABLE OF CONTENTS -->
<h2 class="chapter-heading">TABLE OF CONTENTS</h2>
<table>
  <tr><th>Sl. No.</th><th>Chapter Title</th><th>Page No.</th></tr>
  <tr><td>1.</td><td>Abstract</td><td>3</td></tr>
  <tr><td>2.</td><td>Introduction</td><td>4</td></tr>
  <tr><td>3.</td><td>Problem Statement</td><td>5</td></tr>
  <tr><td>4.</td><td>Objectives of the Project</td><td>6</td></tr>
  <tr><td>5.</td><td>Scope of the Project</td><td>7</td></tr>
  <tr><td>6.</td><td>Tools and Technologies Used</td><td>8</td></tr>
  <tr><td>7.</td><td>System Requirements</td><td>9</td></tr>
  <tr><td>8.</td><td>System Design</td><td>10</td></tr>
  <tr><td>9.</td><td>Database Design</td><td>12</td></tr>
  <tr><td>10.</td><td>Implementation</td><td>14</td></tr>
  <tr><td>11.</td><td>Testing</td><td>17</td></tr>
  <tr><td>12.</td><td>Results and Screenshots</td><td>19</td></tr>
  <tr><td>13.</td><td>Limitations</td><td>21</td></tr>
  <tr><td>14.</td><td>Future Scope</td><td>22</td></tr>
  <tr><td>15.</td><td>Conclusion</td><td>23</td></tr>
  <tr><td>16.</td><td>References</td><td>24</td></tr>
  <tr><td>Appendix</td><td>System Specifications & API Contracts</td><td>25</td></tr>
</table>

<div class="page-break"></div>

<!-- CHAPTER 1: ABSTRACT -->
<h2 class="chapter-heading">CHAPTER 1: ABSTRACT</h2>
<p>
  PageSage is an intelligent, full-stack conversational AI book assistant and reading companion 
  engineered to transform literature exploration. In an age of digital information saturation, readers 
  frequently confront choice paralysis, scattered reading logs, and the persistent frustration of accidental plot 
  spoilers on social platforms. PageSage addresses these challenges through a dual-intelligence architecture that 
  combines state-of-the-art Google Gemini Cloud AI (via dynamic ModelService discovery) with a high-fidelity 
  offline literary intelligence engine and real-time Open Library REST API integration.
</p>
<p>
  The application provides tailored book recommendations by emotional mood, genre, and trope; offers chapter 
  and plot summaries safeguarded by an interactive, click-to-reveal Spoiler Shield; formulates stimulating book 
  club discussion questions; and constructs comprehensive series reading orders for intricate fantasy and sci-fi universes. 
  Additionally, an interactive client-side Bookshelf manager enables readers to seamlessly categorize books into 'Want to Read', 
  'Currently Reading', and 'Finished' with one-click Markdown export. Developed using Python 3, Flask, HTML5, 
  CSS3, and vanilla JavaScript, PageSage delivers an aesthetic Dark Academia responsive interface, verified by a 15-test 
  automated test suite and deployed to production cloud environments.
</p>

<div class="page-break"></div>

<!-- CHAPTER 2: INTRODUCTION -->
<h2 class="chapter-heading">CHAPTER 2: INTRODUCTION</h2>
<h3 class="section-heading">2.1 Background of the Project</h3>
<p>
  Literature serves as an essential medium for cognitive enrichment, empathy development, and human knowledge transmission. 
  However, with millions of books published annually across traditional presses and self-publishing channels, modern readers 
  face an unprecedented volume of literary content. Traditional keyword-based search engines and commercial book portals 
  frequently offer static, advertising-driven lists that fail to capture the nuanced subjective criteria readers care about—such 
  as pacing, emotional tone, specific literary tropes, character chemistry, and moral ambiguity.
</p>
<h3 class="section-heading">2.2 Why This Project is Needed</h3>
<p>
  Readers require an intuitive, intelligent dialogue partner that acts like an erudite librarian. PageSage is designed 
  to simulate a deep, interactive consultation with an expert bibliophile. Whether a reader is searching for a fast-paced 
  hard sci-fi with an unlikely friendship, a cozy mystery for a rainy evening, or the exact chronological starting point for 
  Brandon Sanderson's Cosmere saga, PageSage delivers tailored, contextual, and structured literary guidance.
</p>
<h3 class="section-heading">2.3 How the Application Works</h3>
<p>
  PageSage operates as a lightweight, single-page web application. The frontend communicates asynchronously with a 
  Python Flask REST API backend. When a user submits a query, the Literary Agent determines the optimal model path, invokes 
  Google's Gemini Generative API (or falls back to its internal NLP heuristic engine), extracts structured book metadata, 
  and renders rich interactive book cards alongside formatted Markdown dialogue.
</p>
<h3 class="section-heading">2.4 Target Audience</h3>
<ul>
  <li><strong>Casual & Avid Readers:</strong> Individuals seeking personalized book discoveries tailored to their mood and reading pace.</li>
  <li><strong>Book Club Moderators:</strong> Organizers seeking thought-provoking discussion questions, pacing analyses, and meeting ideas.</li>
  <li><strong>Students & Researchers:</strong> Scholars analyzing character motivations, literary devices, and historical themes in classic literature.</li>
  <li><strong>Series Enthusiasts:</strong> Fans of massive speculative universes seeking clear chronological vs. publication reading orders.</li>
</ul>

<div class="page-break"></div>

<!-- CHAPTER 3: PROBLEM STATEMENT -->
<h2 class="chapter-heading">CHAPTER 3: PROBLEM STATEMENT</h2>
<p>
  Despite the wide availability of online book databases and review aggregators, the digital reading experience suffers from 
  several fundamental shortcomings:
</p>
<ul>
  <li><strong>Choice Paralysis & Rigid Categorization:</strong> Conventional book platforms categorize titles strictly by broad genres, ignoring user-centric emotional nuances.</li>
  <li><strong>Accidental Spoiler Exposure:</strong> Readers seeking premises or character breakdowns frequently encounter major twists inadvertently.</li>
  <li><strong>Scattered Reading Logs:</strong> Disparate spreadsheets or heavyweight commercial platforms requiring logins just to save a title.</li>
  <li><strong>Lack of Interactive Literary Discourse:</strong> Static websites offer one-way reviews rather than dynamic discussions about character arcs and narrative symbolism.</li>
</ul>
<h3 class="section-heading">3.1 Proposed Solution</h3>
<p>
  PageSage resolves these challenges by uniting modern generative AI with respectful reading controls. Its active Spoiler Shield 
  quarantines critical plot revelations behind click-to-reveal components, its Bookshelf tracker maintains lightweight local persistence, 
  and its conversational agent translates subjective reader inquiries into curated, richly presented recommendations.
</p>

<div class="page-break"></div>

<!-- CHAPTER 4: OBJECTIVES -->
<h2 class="chapter-heading">CHAPTER 4: OBJECTIVES OF THE PROJECT</h2>
<ul>
  <li><strong>Objective 1 - Responsive Web Platform:</strong> Design and implement an aesthetic, responsive single-page web interface featuring Dark Academia and Light themes.</li>
  <li><strong>Objective 2 - Dual-AI Architecture:</strong> Engineer a resilient dual-intelligence backend integrating Google Gemini Cloud AI and an offline literary reasoning engine.</li>
  <li><strong>Objective 3 - Spoiler Shield Implementation:</strong> Develop an active spoiler protection system that programmatically hides critical narrative turns behind interactive HTML5 details containers.</li>
  <li><strong>Objective 4 - Interactive Bookshelf Tracker:</strong> Implement a client-side reading tracker supporting 'Want to Read', 'Currently Reading', and 'Finished' shelves with localStorage persistence.</li>
  <li><strong>Objective 5 - Live Metadata Integration:</strong> Connect with the Open Library REST API to dynamically fetch real-world book covers, publication years, and author metadata.</li>
  <li><strong>Objective 6 - Quality Assurance & Deployment:</strong> Construct an automated unit testing suite (100% pass across 15 tests) and deploy the production application to Render cloud hosting.</li>
</ul>

<div class="page-break"></div>

<!-- CHAPTER 5: SCOPE -->
<h2 class="chapter-heading">CHAPTER 5: SCOPE OF THE PROJECT</h2>
<ul>
  <li><strong>Conversational Book Assistant:</strong> Natural language Q&A regarding plots, characters, historical contexts, and writing styles.</li>
  <li><strong>Mood & Trope Filtering:</strong> Dynamic recommendation generation matching nuanced reader prompts with literary elements.</li>
  <li><strong>Spoiler Protection Controller:</strong> Instant toggle switch protecting readers from uninvited climax disclosures.</li>
  <li><strong>Interactive Book Cards:</strong> Visual display cards embedded directly in chat responses with cover images, ratings, and direct '+ Add to Shelf' controls.</li>
  <li><strong>Multi-Tab Bookshelf:</strong> Client-side library management allowing users to cycle books through reading stages and monitor shelf counters.</li>
  <li><strong>Book Club Assistant:</strong> Instant formulation of multi-perspective discussion questions, ethical dilemma prompts, and host suggestions.</li>
  <li><strong>Reading Order Guides:</strong> Curated timelines and entry routes for sprawling multi-novel sagas.</li>
  <li><strong>Production Cloud Accessibility:</strong> Public deployment via Gunicorn and Render, allowing seamless access across any device.</li>
</ul>

<div class="page-break"></div>

<!-- CHAPTER 6: TOOLS AND TECHNOLOGIES -->
<h2 class="chapter-heading">CHAPTER 6: TOOLS AND TECHNOLOGIES USED</h2>
<table>
  <tr><th>Technology / Tool</th><th>Specific Purpose in Project</th></tr>
  <tr><td>Python 3.14</td><td>Core programming language for backend server and business logic.</td></tr>
  <tr><td>Flask 3.1</td><td>Micro web framework providing REST API endpoints and routing.</td></tr>
  <tr><td>Google Gemini API</td><td>Cloud generative language model (gemini-3.8-flash) for deep reasoning.</td></tr>
  <tr><td>Open Library REST API</td><td>Public API used for dynamic book cover lookups and bibliographical data.</td></tr>
  <tr><td>HTML5</td><td>Semantic markup for single-page application structure and modal dialogs.</td></tr>
  <tr><td>CSS3 (Custom Theme)</td><td>Responsive styling, Dark Academia aesthetic, and CSS variables.</td></tr>
  <tr><td>JavaScript (ES6+)</td><td>Client-side event handling, asynchronous Fetch API, and localStorage management.</td></tr>
  <tr><td>Marked.js</td><td>Client-side library for parsing and rendering rich Markdown in chat bubbles.</td></tr>
  <tr><td>Lucide Icons</td><td>Lightweight, scalable vector icon set for interface navigation.</td></tr>
  <tr><td>Gunicorn 21.2</td><td>Production-grade WSGI HTTP Server for cloud deployment.</td></tr>
  <tr><td>Git & GitHub</td><td>Distributed version control system and remote repository hosting.</td></tr>
  <tr><td>Render</td><td>Cloud Application Platform for automated CI/CD and public hosting.</td></tr>
  <tr><td>VS Code</td><td>Integrated Development Environment for code editing and debugging.</td></tr>
</table>

<div class="page-break"></div>

<!-- CHAPTER 7: SYSTEM REQUIREMENTS -->
<h2 class="chapter-heading">CHAPTER 7: SYSTEM REQUIREMENTS</h2>
<h3 class="section-heading">7.1 Hardware Requirements</h3>
<ul>
  <li><strong>Processor:</strong> Intel Core i3 / AMD Ryzen 3 (1.8 GHz) or higher.</li>
  <li><strong>Random Access Memory (RAM):</strong> Minimum 4 GB (8 GB recommended).</li>
  <li><strong>Storage Space:</strong> Minimum 500 MB available local disk storage.</li>
  <li><strong>Network Interface:</strong> Standard Wi-Fi / Ethernet adapter.</li>
</ul>
<h3 class="section-heading">7.2 Software Requirements</h3>
<ul>
  <li><strong>Operating System:</strong> Windows 10/11, macOS Monterey+, or Ubuntu Linux 20.04+.</li>
  <li><strong>Python Runtime:</strong> Python 3.10 or higher.</li>
  <li><strong>Web Browser:</strong> Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari.</li>
  <li><strong>Dependencies:</strong> Flask >= 3.0.0, requests >= 2.31.0, gunicorn >= 21.2.0.</li>
</ul>

<div class="page-break"></div>

<!-- CHAPTER 8: SYSTEM DESIGN -->
<h2 class="chapter-heading">CHAPTER 8: SYSTEM DESIGN</h2>
<h3 class="section-heading">8.1 Application Workflow</h3>
<pre>
[User Interface (Browser)]
       │
       ▼ (1. Submits Book Query / Filter Prompt)
[JavaScript Client Controller (app.js)]
       │
       ▼ (2. HTTP POST /api/chat with History & Spoiler State)
[Flask Application Server (app.py)]
       │
       ▼ (3. Invokes Literary Agent)
[Literary Agent (literary_agent.py)]
       ├───────► Dynamic Model Discovery (ListModels API)
       ├───────► Google Gemini Cloud AI (Primary LLM)
       ├───────► Offline Literary Heuristic Engine (Fallback)
       └───────► Open Library REST API (Book Covers & Metadata)
       │
       ▼ (4. Structured JSON Response: Markdown Text + Book Cards)
[Client Renderer (Marked.js & DOM)]
       │
       ▼ (5. Display Dialogue, Spoiler Shield, & Bookshelf Updates)
[User Reads & Interacts]
</pre>
<h3 class="section-heading">8.2 Main Modules</h3>
<ul>
  <li><strong>Dialogue & Presentation Module:</strong> Manages user input, Markdown parsing, and theme toggling.</li>
  <li><strong>Dual-AI Literary Agent:</strong> Oversees intent classification and manages Gemini REST requests with ModelService discovery.</li>
  <li><strong>Spoiler Shield Subsystem:</strong> Conditionally structures plot summaries with HTML5 collapsible containers.</li>
  <li><strong>Bookshelf & Persistence Module:</strong> Facilitates full CRUD operations for book tracking directly in localStorage.</li>
  <li><strong>Book Metadata Service:</strong> Provides local database queries and Open Library REST lookups.</li>
</ul>

<div class="page-break"></div>

<!-- CHAPTER 9: DATABASE DESIGN -->
<h2 class="chapter-heading">CHAPTER 9: DATABASE DESIGN</h2>
<h3 class="section-heading">9.1 Storage Architecture</h3>
<p>
  PageSage employs a hybrid data architecture: a high-speed curated knowledge store on the backend server for instant literary 
  matching, coupled with client-side localStorage on the browser for privacy-preserving, zero-login personal bookshelf persistence.
</p>
<h3 class="section-heading">9.2 Curated Literature Schema (Server-Side)</h3>
<table>
  <tr><th>Field Name</th><th>Data Type</th><th>Description</th></tr>
  <tr><td>id</td><td>String (Slug)</td><td>Unique alphanumeric identifier (e.g., 'project-hail-mary').</td></tr>
  <tr><td>title</td><td>String</td><td>Full official book title.</td></tr>
  <tr><td>author</td><td>String</td><td>Author name(s).</td></tr>
  <tr><td>year</td><td>Integer</td><td>Original publication year.</td></tr>
  <tr><td>genre</td><td>String</td><td>Primary literary genre.</td></tr>
  <tr><td>tropes</td><td>Array [String]</td><td>Key storytelling tropes (e.g., 'unlikely friendship').</td></tr>
  <tr><td>mood</td><td>Array [String]</td><td>Emotional tone tags (e.g., 'optimistic', 'tense').</td></tr>
  <tr><td>rating</td><td>Float</td><td>Average reader rating out of 5.0.</td></tr>
  <tr><td>pages</td><td>Integer</td><td>Standard edition page count.</td></tr>
  <tr><td>description</td><td>Text</td><td>Spoiler-free premise and narrative hook.</td></tr>
  <tr><td>spoiler_summary</td><td>Text</td><td>Full narrative breakdown and twist resolution.</td></tr>
  <tr><td>themes</td><td>Array [String]</td><td>Central literary themes and motifs.</td></tr>
  <tr><td>characters</td><td>Array [Object]</td><td>Dossier of main characters and their roles.</td></tr>
  <tr><td>discussion_questions</td><td>Array [String]</td><td>Curated questions for book club debate.</td></tr>
  <tr><td>read_alikes</td><td>Array [String]</td><td>Curated list of complementary recommended works.</td></tr>
</table>
<h3 class="section-heading">9.3 Bookshelf Schema (Client-Side LocalStorage)</h3>
<table>
  <tr><th>Key Name</th><th>Data Type</th><th>Description</th></tr>
  <tr><td>want</td><td>JSON Array [Book]</td><td>Array of book objects marked as 'Want to Read'.</td></tr>
  <tr><td>reading</td><td>JSON Array [Book]</td><td>Array of book objects currently being read.</td></tr>
  <tr><td>finished</td><td>JSON Array [Book]</td><td>Array of book objects completed by the user.</td></tr>
</table>

<div class="page-break"></div>

<!-- CHAPTER 10: IMPLEMENTATION -->
<h2 class="chapter-heading">CHAPTER 10: IMPLEMENTATION</h2>
<h3 class="section-heading">10.1 Backend API Implementation (app.py)</h3>
<pre>
@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400
        
    response = agent.chat(
        message=message,
        conversation_history=data.get("conversation_history", []),
        api_key=data.get("api_key", "").strip(),
        spoiler_shield=data.get("spoiler_shield", True),
        user_preferences=data.get("preferences", {})
    )
    return jsonify(response)
</pre>
<h3 class="section-heading">10.2 Dynamic Gemini Model Discovery (literary_agent.py)</h3>
<pre>
def _discover_model(self, api_key: str) -> List[str]:
    discovered = []
    for version in ["v1beta", "v1"]:
        list_url = f"https://generativelanguage.googleapis.com/{version}/models?key={api_key}"
        resp = requests.get(list_url, timeout=5)
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            gen_models = [
                f"{version}/{m['name']}" for m in models
                if "generateContent" in m.get("supportedGenerationMethods", [])
            ]
            flash_models = [m for m in gen_models if "flash" in m.lower()]
            discovered.extend(flash_models + gen_models)
            if discovered: break
    return discovered or ["v1beta/models/gemini-2.0-flash"]
</pre>
<h3 class="section-heading">10.3 Spoiler Shield Implementation</h3>
<pre>
if spoiler_shield:
    text += \"\"\"
&lt;details class="spoiler-box"&gt;
  &lt;summary&gt;⚠️ &lt;strong&gt;Click to reveal spoiler-heavy plot details &amp; ending&lt;/strong&gt;&lt;/summary&gt;
  &lt;p&gt;\"\"\" + book["spoiler_summary"] + \"\"\"&lt;/p&gt;
&lt;/details&gt;\"\"\"
</pre>

<div class="page-break"></div>

<!-- CHAPTER 11: TESTING -->
<h2 class="chapter-heading">CHAPTER 11: TESTING</h2>
<table>
  <tr><th>Test No.</th><th>Feature Tested</th><th>Expected Result</th><th>Actual Result</th><th>Status</th></tr>
  <tr><td>1</td><td>Curated Library Integrity</td><td>Library contains >5 books with complete schema</td><td>Verified 12+ books with all attributes</td><td class="status-pass">Pass</td></tr>
  <tr><td>2</td><td>Local Book Search</td><td>Accurate fuzzy title search for 'Project Hail Mary'</td><td>Book matched with author Andy Weir</td><td class="status-pass">Pass</td></tr>
  <tr><td>3</td><td>Genre & Mood Filtering</td><td>Filter books by 'Science Fiction' genre</td><td>Sci-Fi list returned successfully</td><td class="status-pass">Pass</td></tr>
  <tr><td>4</td><td>Book Retrieval by ID</td><td>Fetch specific book record for 'dune'</td><td>Dune object retrieved with full details</td><td class="status-pass">Pass</td></tr>
  <tr><td>5</td><td>Spoiler Shield (Active)</td><td>Plot twist concealed behind details spoiler-box</td><td>HTML spoiler-box present in output</td><td class="status-pass">Pass</td></tr>
  <tr><td>6</td><td>Spoiler Shield (Disabled)</td><td>Direct, unshielded climax discussion</td><td>Full ending details returned in prose</td><td class="status-pass">Pass</td></tr>
  <tr><td>7</td><td>Book Club Question Gen</td><td>Formulate targeted questions for 'The Great Gatsby'</td><td>Formatted questions & host tips returned</td><td class="status-pass">Pass</td></tr>
  <tr><td>8</td><td>Series Reading Order</td><td>Generate Sanderson Cosmere reading timeline</td><td>Structured reading guide returned</td><td class="status-pass">Pass</td></tr>
  <tr><td>9</td><td>Trope Recommendation</td><td>Suggest cozy mystery based on user prompt</td><td>Curated titles with tropes returned</td><td class="status-pass">Pass</td></tr>
  <tr><td>10</td><td>Web Interface Route (/)</td><td>HTTP GET / returns single-page HTML interface</td><td>HTTP 200 with HTML body</td><td class="status-pass">Pass</td></tr>
  <tr><td>11</td><td>System Status Endpoint</td><td>HTTP GET /api/status returns online status</td><td>HTTP 200 with JSON status: online</td><td class="status-pass">Pass</td></tr>
  <tr><td>12</td><td>Curated Catalogue API</td><td>HTTP GET /api/curated returns book list</td><td>HTTP 200 with JSON book array</td><td class="status-pass">Pass</td></tr>
  <tr><td>13</td><td>Book Details API</td><td>HTTP GET /api/book/dune returns book metadata</td><td>HTTP 200 with title 'Dune'</td><td class="status-pass">Pass</td></tr>
  <tr><td>14</td><td>Chat Endpoint Valid</td><td>HTTP POST /api/chat with valid inquiry</td><td>HTTP 200 with text & book cards</td><td class="status-pass">Pass</td></tr>
  <tr><td>15</td><td>Chat Endpoint Empty</td><td>HTTP POST /api/chat with empty string</td><td>HTTP 400 Bad Request returned</td><td class="status-pass">Pass</td></tr>
</table>

<div class="page-break"></div>

<!-- CHAPTER 12: RESULTS AND SCREENSHOTS -->
<h2 class="chapter-heading">CHAPTER 12: RESULTS AND SCREENSHOTS</h2>
<h3 class="section-heading">Figure 1: Welcome & Landing Interface</h3>
<p>Shows the responsive Dark Academia workspace, featuring guided inquiry pills, the AI engine indicator, and the bookshelf sidebar.</p>
<div class="placeholder">[ Insert Screenshot of Home Screen / Welcome Interface Here ]</div>

<h3 class="section-heading">Figure 2: Conversational Dialogue & Interactive Book Cards</h3>
<p>Displays the conversational response stream with rich markdown typography and interactive book cards with cover art and '+ Add' buttons.</p>
<div class="placeholder">[ Insert Screenshot of Chat Dialogue with Book Cards Here ]</div>

<h3 class="section-heading">Figure 3: Active Spoiler Shield Mechanism</h3>
<p>Demonstrates the click-to-reveal spoiler protection box shielding climactic plot revelations and twist endings.</p>
<div class="placeholder">[ Insert Screenshot of Click-to-Reveal Spoiler Box Here ]</div>

<h3 class="section-heading">Figure 4: My Bookshelf Reading Tracker</h3>
<p>Illustrates the interactive multi-shelf tracker showcasing categorized titles under 'Want to Read', 'Reading', and 'Read'.</p>
<div class="placeholder">[ Insert Screenshot of Bookshelf Sidebar & Export Action Here ]</div>

<h3 class="section-heading">Figure 5: Configuration & Preferences Modal</h3>
<p>Shows the settings dialog where users configure Google Gemini API credentials and favorite genres.</p>
<div class="placeholder">[ Insert Screenshot of Settings & Preferences Modal Here ]</div>

<div class="page-break"></div>

<!-- CHAPTER 13: LIMITATIONS -->
<h2 class="chapter-heading">CHAPTER 13: LIMITATIONS</h2>
<ul>
  <li><strong>1. Cloud API Rate Limits:</strong> Google Gemini free-tier keys impose requests-per-minute constraints.</li>
  <li><strong>2. External Network Dependency for Images:</strong> Displaying live Open Library book covers requires an active internet connection.</li>
  <li><strong>3. Browser-Bound Storage:</strong> Bookshelf data stored in browser localStorage is device and browser-specific.</li>
  <li><strong>4. Scope Boundary on Copyrighted Content:</strong> PageSage provides analysis, commentary, and summaries, but does not host full copyrighted e-book manuscripts.</li>
</ul>

<div class="page-break"></div>

<!-- CHAPTER 14: FUTURE SCOPE -->
<h2 class="chapter-heading">CHAPTER 14: FUTURE SCOPE</h2>
<ul>
  <li><strong>User Accounts & Cloud Database:</strong> Integrate PostgreSQL / Supabase authentication to synchronize reading lists across devices.</li>
  <li><strong>RAG Vector Database:</strong> Incorporate FAISS or ChromaDB with sentence embeddings for Q&A across user-uploaded e-books.</li>
  <li><strong>Audio Integration & Text-to-Speech:</strong> Add speech-to-text queries and AI audiobook narrator voices.</li>
  <li><strong>Social Reading Groups:</strong> Enable collaborative book clubs where members share synchronized reading schedules.</li>
  <li><strong>Native Mobile Apps:</strong> Package the frontend using Flutter or React Native for iOS and Android.</li>
</ul>

<div class="page-break"></div>

<!-- CHAPTER 15: CONCLUSION -->
<h2 class="chapter-heading">CHAPTER 15: CONCLUSION</h2>
<p>
  PageSage successfully demonstrates how modern Data Science and Artificial Intelligence technologies can be synthesized 
  with elegant software engineering to enrich human literary discovery. By solving the dual challenges of choice paralysis 
  and inadvertent plot spoilers, the platform offers an indispensable companion for readers, students, and book clubs.
</p>
<p>
  Throughout this project, foundational competencies were developed in Python full-stack engineering, REST API architecture, 
  dynamic cloud LLM integration, automated unit testing, client-side state persistence, and cloud production deployment. 
  All stated project objectives were fully achieved, providing a production-ready, extensible platform with broad real-world utility.
</p>

<div class="page-break"></div>

<!-- CHAPTER 16: REFERENCES -->
<h2 class="chapter-heading">CHAPTER 16: REFERENCES</h2>
<ul>
  <li><strong>1. Flask Documentation:</strong> Pallets Projects. Flask Web Development Documentation. https://flask.palletsprojects.com/</li>
  <li><strong>2. Google AI Studio & Gemini API:</strong> Google DeepMind. Gemini API Reference & Model Documentation. https://aistudio.google.com/</li>
  <li><strong>3. Open Library Developer Portal:</strong> Internet Archive. Open Library REST APIs for Books & Covers. https://openlibrary.org/developers/api</li>
  <li><strong>4. MDN Web Docs:</strong> Mozilla Developer Network. HTML5 Details, CSS Grid, and Fetch API Specifications. https://developer.mozilla.org/</li>
  <li><strong>5. Gunicorn WSGI Documentation:</strong> Arboretum Gunicorn Team. Python WSGI HTTP Server. https://gunicorn.org/</li>
  <li><strong>6. Marked.js:</strong> Christopher Jeffrey. Marked - A fast JavaScript Markdown parser. https://marked.js.org/</li>
</ul>

<div class="page-break"></div>

<!-- APPENDIX -->
<h2 class="chapter-heading">APPENDIX: SYSTEM SPECIFICATIONS</h2>
<h3 class="section-heading">Project Directory Tree</h3>
<pre>
book-assistant-ai/
├── app.py                  # Primary Flask Application & Routing
├── book_service.py         # Curated Library & Open Library REST Service
├── literary_agent.py       # Dual-AI Engine & Gemini Dynamic Discovery
├── requirements.txt        # Production Dependencies (Flask, Requests, Gunicorn)
├── Procfile                # Cloud Deployment Process Specification
├── test_app.py             # 15 Unit & Integration Tests (100% Pass)
├── README.md               # User Documentation & Quick Start Guide
├── templates/
│   └── index.html          # Responsive Single-Page Application Interface
└── static/
    ├── css/
    │   └── style.css       # Dark Academia Responsive Styling
    └── js/
        └── app.js          # Client State, Chat Logic, & Bookshelf CRUD
</pre>
<h3 class="section-heading">REST API Contracts</h3>
<ul>
  <li><strong>POST /api/chat:</strong> Accepts { message, conversation_history, api_key, spoiler_shield, preferences }. Returns { text, book_cards, engine, model }.</li>
  <li><strong>GET /api/status:</strong> Returns { status: 'online', name: 'PageSage', version: '1.0.0', books_count: int }.</li>
  <li><strong>GET /api/curated:</strong> Returns complete curated JSON catalogue filtered by optional genre/mood query params.</li>
  <li><strong>GET /api/book/&lt;id&gt;:</strong> Returns full bibliographical and analytical dossier for a targeted book.</li>
</ul>

</body>
</html>
"""

with open(r"C:\Users\rouna\.gemini\antigravity\scratch\book-assistant-ai\PageSage_AI_Project_Report.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print("HTML report generated successfully.")
