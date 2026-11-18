"""
Book Service for PageSage AI Book Assistant.
Provides access to curated literary database and live Open Library API integration.
"""

import requests
import re
from typing import List, Dict, Any, Optional

# Curated High-Quality Literary Database
CURATED_BOOKS: List[Dict[str, Any]] = [
    {
        "id": "project-hail-mary",
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "year": 2021,
        "genre": "Science Fiction",
        "tropes": ["lone survivor", "unlikely friendship", "first contact", "hard sci-fi", "saving humanity"],
        "mood": ["humorous", "optimistic", "intellectual", "tense", "heartwarming"],
        "cover_url": "https://covers.openlibrary.org/b/id/10522956-M.jpg",
        "rating": 4.8,
        "pages": 496,
        "description": "Ryland Grace is the sole survivor on a desperate, last-chance mission—and if he fails, humanity and the earth itself are doomed. Except right now, he doesn't even remember his own name.",
        "spoiler_summary": "Ryland remembers he was sent on the Hail Mary ship to find an answer to the Astrophage extinction threat. He encounters Rocky, an intelligent alien spider-like engineer whose species is facing the exact same doom. They work together, forge a deep bond of friendship, and Ryland chooses to sacrifice his return trip to Earth to rescue Rocky's dying ship, eventually settling on Rocky's homeworld as a beloved science teacher.",
        "themes": ["scientific ingenuity", "cross-species friendship", "self-sacrifice", "resilience"],
        "characters": [
            {"name": "Ryland Grace", "role": "Middle school science teacher turned astronaut"},
            {"name": "Rocky", "role": "Eridian engineer and Ryland's extraterrestrial companion"},
            {"name": "Eva Stratt", "role": "Determined global administrator with unlimited authority"}
        ],
        "discussion_questions": [
            "How does humor serve as a survival mechanism for Ryland throughout his isolation?",
            "What does Rocky and Ryland's communication development say about universal languages like math and music?",
            "Was Stratt justified in using coercive authoritarian methods to ensure humanity's survival?"
        ],
        "read_alikes": ["The Martian by Andy Weir", "Children of Time by Adrian Tchaikovsky", "Bobiverse by Dennis E. Taylor", "Contact by Carl Sagan"]
    },
    {
        "id": "dune",
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "genre": "Science Fiction",
        "tropes": ["chosen one deconstruction", "feudal space empire", "desert survival", "political intrigue", "ecology"],
        "mood": ["epic", "philosophical", "dark", "intricate", "mystical"],
        "cover_url": "https://covers.openlibrary.org/b/id/11153218-M.jpg",
        "rating": 4.7,
        "pages": 688,
        "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world where the only thing of value is the 'spice' melange.",
        "spoiler_summary": "After House Atreides is betrayed and massacred by House Harkonnen and Emperor Shaddam IV, Paul and his mother Jessica escape into the deep desert. Paul integrates with the Fremen, embraces the religious myth seeded by the Bene Gesserit, and becomes Muad'Dib. He uses sandworm power and spice control to overthrow the Emperor, but realizes his victory unleashes an unstoppable galactic jihad in his name.",
        "themes": ["dangers of charismatic leaders", "ecological balance", "religious manipulation", "colonialism"],
        "characters": [
            {"name": "Paul Atreides", "role": "Protagonist, duke's son, and prophesied Kwisatz Haderach"},
            {"name": "Lady Jessica", "role": "Bene Gesserit concubine to Duke Leto and Paul's mother"},
            {"name": "Baron Vladimir Harkonnen", "role": "Ruthless head of House Harkonnen"},
            {"name": "Chani", "role": "Fremen warrior and Paul's lover"}
        ],
        "discussion_questions": [
            "Herbert famously intended Dune as a warning against messianic figures. How does Paul struggle against his fate?",
            "In what ways does Arrakis's ecology shape Fremen culture and philosophy?",
            "How does the Bene Gesserit's multi-generational breeding program reflect real-world eugenics and political power?"
        ],
        "read_alikes": ["Foundation by Isaac Asimov", "Hyperion by Dan Simmons", "Red Rising by Pierce Brown", "The Left Hand of Darkness by Ursula K. Le Guin"]
    },
    {
        "id": "the-silent-patient",
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "year": 2019,
        "genre": "Mystery & Thriller",
        "tropes": ["unreliable narrator", "shocking twist", "psychological mind games", "obsession"],
        "mood": ["tense", "suspenseful", "dark", "mysterious"],
        "cover_url": "https://covers.openlibrary.org/b/id/8816790-M.jpg",
        "rating": 4.4,
        "pages": 336,
        "description": "Alicia Berenson's life is seemingly perfect. A famous painter married to an in-demand fashion photographer, she lives in a grand house. Then, one evening, she shoots her husband five times in the face and never speaks another word.",
        "spoiler_summary": "Theo Faber, the forensic psychotherapist trying to get Alicia to talk, is secretly the intruder who broke into Alicia's home. Theo had discovered his own wife was having an affair with Alicia's husband, Gabriel. Theo broke in to confront Gabriel and tie them up, leaving a gun. Alicia shot Gabriel out of feelings of ultimate betrayal. Alicia figures out Theo's identity, so Theo overdoses her with morphine to keep her quiet, though she leaves a hidden diary entry exposing him.",
        "themes": ["childhood trauma", "silence as defense", "projection", "obsession and revenge"],
        "characters": [
            {"name": "Alicia Berenson", "role": "Famous painter accused of murder who refuses to speak"},
            {"name": "Theo Faber", "role": "Criminal psychotherapist obsessed with uncovering her motive"},
            {"name": "Gabriel Berenson", "role": "Alicia's murdered husband"}
        ],
        "discussion_questions": [
            "How did the dual timeline mislead you throughout the narrative?",
            "What role does Greek mythology (specifically the Alcestis myth) play in Alicia's silence?",
            "Did Theo actually want to cure Alicia or merely silence her?"
        ],
        "read_alikes": ["Gone Girl by Gillian Flynn", "The Maidens by Alex Michaelides", "The Guest List by Lucy Foley", "Rock Paper Scissors by Alice Feeney"]
    },
    {
        "id": "the-seven-husbands-of-evelyn-hugo",
        "title": "The Seven Husbands of Evelyn Hugo",
        "author": "Taylor Jenkins Reid",
        "year": 2017,
        "genre": "Historical Fiction & Romance",
        "tropes": ["old Hollywood glamour", "forbidden love", "framing story", "hidden secrets"],
        "mood": ["glamorous", "emotional", "nostalgic", "bittersweet"],
        "cover_url": "https://covers.openlibrary.org/b/id/8750849-M.jpg",
        "rating": 4.6,
        "pages": 400,
        "description": "Aging and reclusive Hollywood movie icon Evelyn Hugo is finally ready to tell the truth about her glamorous and scandalous life. But when she chooses unknown magazine reporter Monique Grant, no one is more astounded than Monique herself.",
        "spoiler_summary": "Evelyn reveals that while she had seven marriages with men for career advancement, image preservation, or convenience, the true love of her life was fellow actress Celia St. James. Furthermore, Evelyn reveals why she picked Monique: Monique's father died in a car crash decades ago that Harry Cameron (Evelyn's best friend and platonic husband) caused while drunk; Evelyn had moved Harry into the passenger seat to protect his reputation. Evelyn hands Monique the tell-all biography rights before choosing to end her life on her own terms.",
        "themes": ["authenticity vs. public persona", "LGBTQ+ identity in mid-century Hollywood", "the cost of ambition", "unconditional love"],
        "characters": [
            {"name": "Evelyn Hugo", "role": "Legendary Hollywood star with a guarded past"},
            {"name": "Celia St. James", "role": "Talented actress and Evelyn's enduring true love"},
            {"name": "Harry Cameron", "role": "Studio producer and Evelyn's loyal confidant"},
            {"name": "Monique Grant", "role": "Ambitious young journalist selected to write Evelyn's memoir"}
        ],
        "discussion_questions": [
            "Was Evelyn a good person, a ruthless survivor, or both?",
            "How does the novel portray the price of visibility and fame for women and queer people in mid-century America?",
            "Did Evelyn's confession give Monique closure or burden her?"
        ],
        "read_alikes": ["Daisy Jones & The Six by Taylor Jenkins Reid", "City of Girls by Elizabeth Gilbert", "The Paris Wife by Paula McLain", "Lessons in Chemistry by Bonnie Garmus"]
    },
    {
        "id": "atomic-habits",
        "title": "Atomic Habits",
        "author": "James Clear",
        "year": 2018,
        "genre": "Self-Growth & Psychology",
        "tropes": ["habit loops", "incremental gains", "identity change", "practical framework"],
        "mood": ["motivating", "practical", "insightful", "clear"],
        "cover_url": "https://covers.openlibrary.org/b/id/12885611-M.jpg",
        "rating": 4.8,
        "pages": 320,
        "description": "No matter your goals, Atomic Habits offers a proven framework for improving--every day. James Clear reveals practical strategies that will teach you exactly how to form good habits, break bad ones, and master the tiny behaviors that lead to remarkable results.",
        "spoiler_summary": "The core thesis is that tiny 1% improvements compound into massive long-term transformations. The 4 Laws of Behavior Change are: (1) Make it obvious, (2) Make it attractive, (3) Make it easy, and (4) Make it satisfying (and their opposites for bad habits). Focus on identity-based habits ('I am a runner') rather than outcome-based goals.",
        "themes": ["compounding progress", "identity shift", "environmental design", "systems over goals"],
        "characters": [
            {"name": "James Clear", "role": "Author, researcher, and productivity practitioner"}
        ],
        "discussion_questions": [
            "Why is changing your environment often more effective than relying on sheer willpower?",
            "How can identity-based habits overcome the frustration of delayed gratification?",
            "Which of the 4 laws of behavior change have you found most applicable in your own routine?"
        ],
        "read_alikes": ["Deep Work by Cal Newport", "The Power of Habit by Charles Duhigg", "Tiny Habits by BJ Fogg", "Thinking, Fast and Slow by Daniel Kahneman"]
    },
    {
        "id": "the-great-gatsby",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "genre": "Classics & Literary Fiction",
        "tropes": ["unrequited love", "roaring twenties", "the American Dream decay", "wealth and privilege"],
        "mood": ["elegiac", "cynical", "lyrical", "haunting"],
        "cover_url": "https://covers.openlibrary.org/b/id/7222246-M.jpg",
        "rating": 4.2,
        "pages": 180,
        "description": "The novel chronicles an era that Fitzgerald himself dubbed the 'Jazz Age'. Following the mysterious millionaire Jay Gatsby and his passion and obsession for the beautiful former debutante Daisy Buchanan.",
        "spoiler_summary": "Daisy accidentally strikes and kills Myrtle Wilson with Gatsby's yellow roadster. Gatsby takes the blame to protect Daisy. Tom Buchanan directs Myrtle's distraught husband George to Gatsby's mansion, where George shoots Gatsby dead in his swimming pool and kills himself. Only Nick Carraway, Gatsby's father, and one partygoer attend Gatsby's funeral, while Daisy and Tom leave carelessly without consequence.",
        "themes": ["corruption of the American dream", "hollowness of the upper class", "idealized romantic delusion", "time and memory"],
        "characters": [
            {"name": "Jay Gatsby", "role": "Enigmatic, newly rich host driven by longing for Daisy"},
            {"name": "Nick Carraway", "role": "Tolerant, moral narrator observing East and West Egg"},
            {"name": "Daisy Buchanan", "role": "Careless, alluring aristocratic woman Gatsby adores"},
            {"name": "Tom Buchanan", "role": "Brutal, arrogant old-money heir"}
        ],
        "discussion_questions": [
            "Is Gatsby's love for Daisy genuine, or is she merely a symbol of wealth and social status?",
            "How does Nick's narration walk the line between participating in the hedonism and passing moral judgment?",
            "What does the green light at the end of Daisy's dock symbolize throughout Gatsby's evolution?"
        ],
        "read_alikes": ["Tender Is the Night by F. Scott Fitzgerald", "The Sun Also Rises by Ernest Hemingway", "Passing by Nella Larsen", "The Age of Innocence by Edith Wharton"]
    },
    {
        "id": "1984",
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian & Classics",
        "tropes": ["totalitarian surveillance", "rebellion against the system", "forbidden romance", "thought control"],
        "mood": ["bleak", "paranoia-inducing", "philosophical", "chilling"],
        "cover_url": "https://covers.openlibrary.org/b/id/11181822-M.jpg",
        "rating": 4.6,
        "pages": 328,
        "description": "Winston Smith lives in a dystopian world where the Party and its omnipresent leader, Big Brother, control every aspect of life. Working at the Ministry of Truth, Winston begins keeping a forbidden secret diary.",
        "spoiler_summary": "Winston and Julia carry out their secret love affair and attempt to join the rumored Brotherhood through party official O'Brien. O'Brien reveals he is an agent of the Thought Police and arrests them. Winston is systematically tortured in Room 101, broken by his deepest terror (rats), and betrays Julia. The novel ends with Winston thoroughly brainwashed, sitting at the Chestnut Tree Cafe, realizing that he finally loves Big Brother.",
        "themes": ["totalitarian surveillance", "manipulation of language (Newspeak)", "destruction of truth and history", "erasure of individuality"],
        "characters": [
            {"name": "Winston Smith", "role": "Ministry of Truth employee harboring rebellious thoughts"},
            {"name": "Julia", "role": "Pragmatic sensual rebel who becomes Winston's lover"},
            {"name": "O'Brien", "role": "Inner Party member posing as a dissident to trap Winston"},
            {"name": "Big Brother", "role": "The symbolic, omnipotent figurehead of the Party"}
        ],
        "discussion_questions": [
            "Why is the manipulation of language (Newspeak) so vital to the Party's maintenance of absolute power?",
            "How does Orwell's concept of 'Doublethink' resonate with modern media and political discourse?",
            "Was Winston's defeat inevitable from the very moment he purchased the diary?"
        ],
        "read_alikes": ["Brave New World by Aldous Huxley", "Fahrenheit 451 by Ray Bradbury", "The Handmaid's Tale by Margaret Atwood", "Darkness at Noon by Arthur Koestler"]
    },
    {
        "id": "mistborn-the-final-empire",
        "title": "Mistborn: The Final Empire",
        "author": "Brandon Sanderson",
        "year": 2006,
        "genre": "Fantasy",
        "tropes": ["heist crew", "unique magic system", "dark lord already won", "mentor and apprentice", "rebellion"],
        "mood": ["exhilarating", "gritty", "clever", "epic"],
        "cover_url": "https://covers.openlibrary.org/b/id/8316348-M.jpg",
        "rating": 4.7,
        "pages": 541,
        "description": "For a thousand years the ash fell and no flowers bloomed. For a thousand years the Skaa slaved in misery. For a thousand years the Lord Ruler ruled with an iron fist. Then a half-skaa thief named Kelsier discovered he was Mistborn.",
        "spoiler_summary": "Kelsier assembles a crew to rob the Lord Ruler's atium reserves and overthrow the thousand-year empire. Kelsier sacrifices his life publicly to become a martyr and spark the Skaa rebellion. Vin realizes the Lord Ruler's secret: he is using both Allomancy and Feruchemy to maintain eternal youth. Vin draws on the mists themselves to strip away the Lord Ruler's Feruchemical metalminds, causing him to age rapidly and die, leaving the empire in chaotic liberation.",
        "themes": ["hope against tyranny", "found family", "the cost of rebellion", "trust and betrayal"],
        "characters": [
            {"name": "Vin", "role": "Street urchin who discovers immense Mistborn allomantic powers"},
            {"name": "Kelsier", "role": "Charismatic rebel leader known as the Survivor of Hathsin"},
            {"name": "Elend Venture", "role": "Philosophical nobleman who desires egalitarian reform"},
            {"name": "The Lord Ruler", "role": "Immortal tyrant reigning for a millennium"}
        ],
        "discussion_questions": [
            "How does Sanderson use the Allomantic magic system to ground action and tactical stakes?",
            "Was Kelsier's intentional martyrdom a noble sacrifice or calculated manipulation?",
            "How does Vin's trust issues evolve as she transitions from street thief to high-society spy?"
        ],
        "read_alikes": ["The Way of Kings by Brandon Sanderson", "The Lies of Locke Lamora by Scott Lynch", "The Name of the Wind by Patrick Rothfuss", "Six of Crows by Leigh Bardugo"]
    },
    {
        "id": "the-thursday-murder-club",
        "title": "The Thursday Murder Club",
        "author": "Richard Osman",
        "year": 2020,
        "genre": "Mystery & Cozy Crime",
        "tropes": ["elderly sleuths", "retirement village", "witty banter", "unsolved cold cases"],
        "mood": ["charming", "witty", "heartwarming", "clever"],
        "cover_url": "https://covers.openlibrary.org/b/id/10427845-M.jpg",
        "rating": 4.5,
        "pages": 400,
        "description": "In a peaceful retirement village, four unlikely friends meet weekly in the Jigsaw Room to investigate unsolved crimes. When a local property developer is found dead, the Thursday Murder Club find themselves in the middle of their first live case.",
        "spoiler_summary": "Property developer Tony Curran and later Ian Ventham are murdered. The seniors unearth tangled histories of drug deals, cemetery land, and family feuds. Bogdan, a friendly builder, killed Tony Curran over a past murder, while Penny (a former police detective and club founder now comatose) had killed a rapist decades earlier. Elizabeth guides justice with gentle empathy for moral nuance.",
        "themes": ["aging and vitality", "grief and mortality", "friendship in later life", "morality vs. legalism"],
        "characters": [
            {"name": "Elizabeth Best", "role": "Shrewd former secret intelligence agent and group mastermind"},
            {"name": "Joyce Meadowcroft", "role": "Warm, observant retired nurse and diary keeper"},
            {"name": "Ron Ritchie", "role": "Fiery former union activist with a heart of gold"},
            {"name": "Ibrahim Arif", "role": "Meticulous, soft-spoken retired psychiatrist"}
        ],
        "discussion_questions": [
            "How does Osman balance lighthearted English wit with poignant reflections on dementia and loss?",
            "Why is retirement age portrayed as an investigative superpower rather than a limitation?",
            "Did the members of the club make the right moral choice regarding the true culprits?"
        ],
        "read_alikes": ["The Maid by Nita Prose", "Vera Wong's Unsolicited Advice for Murderers by Jesse Q. Sutanto", "Magpie Murders by Anthony Horowitz", "A Man Called Ove by Fredrik Backman"]
    },
    {
        "id": "pride-and-prejudice",
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "year": 1813,
        "genre": "Classics & Romance",
        "tropes": ["enemies to lovers", "class differences", "witty repartee", "first impressions"],
        "mood": ["delightful", "romantic", "sharp-witted", "satirical"],
        "cover_url": "https://covers.openlibrary.org/b/id/10543666-M.jpg",
        "rating": 4.7,
        "pages": 432,
        "description": "A romantic novel of manners written by Jane Austen in 1813. The novel follows the character development of Elizabeth Bennet, the dynamic protagonist of the book who learns about the repercussions of hasty judgments.",
        "spoiler_summary": "After initially detesting Mr. Darcy for his aristocratic snobbery and believing Wickham's slander, Elizabeth receives Darcy's explanatory letter. When her sister Lydia runs away with Wickham, Darcy secretly pays off Wickham's debts and arranges their wedding to save the Bennet family from ruin. Elizabeth realizes she loves Darcy, rejects Lady Catherine's demands, and happily accepts Darcy's renewed proposal.",
        "themes": ["misjudgment and prejudice", "social class and financial independence", "matrimony vs. true affection", "growth through humility"],
        "characters": [
            {"name": "Elizabeth Bennet", "role": "Spirited, intelligent second Bennet daughter"},
            {"name": "Fitzwilliam Darcy", "role": "Wealthy, aristocratic landowner whose outward pride masks integrity"},
            {"name": "Jane Bennet", "role": "Sweet-natured, trusting elder sister"},
            {"name": "George Wickham", "role": "Charming militia officer who conceals deceitful motives"}
        ],
        "discussion_questions": [
            "How do both Elizabeth and Darcy represent both pride and prejudice throughout their courtship?",
            "What does Austen's portrayal of Charlotte Lucas's pragmatic marriage say about 19th-century female agency?",
            "How does humor and irony function as social critique in Austen's dialogue?"
        ],
        "read_alikes": ["Emma by Jane Austen", "Jane Eyre by Charlotte Brontë", "North and South by Elizabeth Gaskell", "Sense and Sensibility by Jane Austen"]
    }
]

def search_local_books(query: str) -> List[Dict[str, Any]]:
    """Search the curated internal book database."""
    query_lower = query.lower().strip()
    words = [w for w in re.split(r'\W+', query_lower) if len(w) > 2]
    
    scored_books = []
    for b in CURATED_BOOKS:
        score = 0
        title_lower = b["title"].lower()
        author_lower = b["author"].lower()
        genre_lower = b["genre"].lower()
        tropes_str = " ".join(b["tropes"]).lower()
        mood_str = " ".join(b["mood"]).lower()
        desc_str = b["description"].lower()
        
        # Exact title or author match gives high score
        if query_lower in title_lower:
            score += 15
        if query_lower in author_lower:
            score += 12
        if query_lower in genre_lower:
            score += 8
        if query_lower in tropes_str or query_lower in mood_str:
            score += 6

        # Check word overlaps
        for w in words:
            if w in title_lower:
                score += 5
            if w in author_lower:
                score += 4
            if w in genre_lower:
                score += 3
            if w in tropes_str:
                score += 3
            if w in mood_str:
                score += 2
            if w in desc_str:
                score += 1
                
        if score > 0:
            scored_books.append((score, b))
            
    scored_books.sort(key=lambda x: x[0], reverse=True)
    return [b for score, b in scored_books]


def search_open_library(query: str, limit: int = 6) -> List[Dict[str, Any]]:
    """
    Search Open Library API for books matching query.
    Falls back gracefully to local database on timeout or network disconnect.
    """
    try:
        url = f"https://openlibrary.org/search.json?q={requests.utils.quote(query)}&limit={limit}"
        resp = requests.get(url, timeout=3.5)
        if resp.status_code == 200:
            data = resp.json()
            docs = data.get("docs", [])
            results = []
            for d in docs:
                cover_id = d.get("cover_i")
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None
                authors = d.get("author_name", ["Unknown Author"])
                results.append({
                    "id": d.get("key", "").replace("/works/", ""),
                    "title": d.get("title", "Untitled"),
                    "author": ", ".join(authors[:2]),
                    "year": d.get("first_publish_year", "N/A"),
                    "genre": ", ".join(d.get("subject", [])[:3]) if d.get("subject") else "General",
                    "tropes": d.get("subject", [])[:4],
                    "mood": [],
                    "cover_url": cover_url,
                    "rating": round(d.get("ratings_average", 4.3), 1) if d.get("ratings_average") else 4.2,
                    "pages": d.get("number_of_pages_median") or "350",
                    "description": d.get("first_sentence", {}).get("value", "") or f"A celebrated work by {', '.join(authors[:1])}.",
                    "openlibrary_key": d.get("key")
                })
            if results:
                return results
    except Exception:
        # Network disconnected, timeout, or sandboxed environment
        pass
    
    # Fallback to local curated search
    return search_local_books(query)


def get_book_by_id(book_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve full book information by ID."""
    for b in CURATED_BOOKS:
        if b["id"] == book_id or book_id in b["title"].lower():
            return b
    return None


def get_recommendations_by_mood_or_genre(genre: Optional[str] = None, mood: Optional[str] = None, trope: Optional[str] = None) -> List[Dict[str, Any]]:
    """Filter curated books by mood, genre, or trope."""
    matches = []
    for b in CURATED_BOOKS:
        match = True
        if genre and genre.lower() not in b["genre"].lower():
            match = False
        if mood and not any(mood.lower() in m.lower() for m in b["mood"]):
            match = False
        if trope and not any(trope.lower() in t.lower() for t in b["tropes"]):
            match = False
        if match:
            matches.append(b)
    return matches if matches else CURATED_BOOKS[:4]
