"""
Strictly Compliant Word Document (.docx) Generator for PageSage AI Software Project Report.
Follows ECMA-376 / ISO 29500 element ordering strictly so Microsoft Word, Google Docs, 
LibreOffice, and mobile viewers open it with zero warnings or corruption errors.
"""

import os
import zipfile
import html

def escape_xml(text):
    if text is None:
        return ""
    return html.escape(str(text), quote=True)

class StrictDocxBuilder:
    def __init__(self):
        self.body_elements = []

    def add_page_break(self):
        self.body_elements.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def add_title(self, text):
        p = f'''
        <w:p>
          <w:pPr>
            <w:spacing w:before="360" w:after="200"/>
            <w:jc w:val="center"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:color w:val="1F4E79"/>
              <w:sz w:val="48"/>
            </w:rPr>
            <w:t>{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        '''
        self.body_elements.append(p)

    def add_subtitle(self, text, bold=True, center=True):
        jc = '<w:jc w:val="center"/>' if center else ''
        b_tag = '<w:b/>' if bold else ''
        p = f'''
        <w:p>
          <w:pPr>
            <w:spacing w:before="100" w:after="160"/>
            {jc}
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              {b_tag}
              <w:color w:val="262626"/>
              <w:sz w:val="28"/>
            </w:rPr>
            <w:t>{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        '''
        self.body_elements.append(p)

    def add_heading_1(self, text):
        # Strict OpenXML: pBdr must appear BEFORE spacing and jc
        p = f'''
        <w:p>
          <w:pPr>
            <w:pBdr>
              <w:bottom w:val="single" w:sz="12" w:space="4" w:color="1F4E79"/>
            </w:pBdr>
            <w:spacing w:before="360" w:after="140"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:color w:val="1F4E79"/>
              <w:sz w:val="32"/>
            </w:rPr>
            <w:t>{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        '''
        self.body_elements.append(p)

    def add_heading_2(self, text):
        p = f'''
        <w:p>
          <w:pPr>
            <w:spacing w:before="240" w:after="100"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:color w:val="2F5597"/>
              <w:sz w:val="26"/>
            </w:rPr>
            <w:t>{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        '''
        self.body_elements.append(p)

    def add_paragraph(self, text, justify=True, italic=False, bold=False):
        jc = '<w:jc w:val="both"/>' if justify else ''
        i_tag = '<w:i/>' if italic else ''
        b_tag = '<w:b/>' if bold else ''
        p = f'''
        <w:p>
          <w:pPr>
            <w:spacing w:before="60" w:after="120" w:line="280" w:lineRule="auto"/>
            {jc}
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              {b_tag}
              {i_tag}
              <w:color w:val="262626"/>
              <w:sz w:val="22"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        '''
        self.body_elements.append(p)

    def add_bullet(self, bold_prefix, text):
        p = f'''
        <w:p>
          <w:pPr>
            <w:spacing w:before="40" w:after="60"/>
            <w:ind w:left="480" w:hanging="240"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:color w:val="1F4E79"/>
              <w:sz w:val="22"/>
            </w:rPr>
            <w:t>• </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:color w:val="1F4E79"/>
              <w:sz w:val="22"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape_xml(bold_prefix)} </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:color w:val="262626"/>
              <w:sz w:val="22"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        '''
        self.body_elements.append(p)

    def add_code_block(self, code_text):
        lines = code_text.strip().split("\n")
        elements = []
        for line in lines:
            elements.append(f'''
            <w:p>
              <w:pPr>
                <w:shd w:val="clear" w:color="auto" w:fill="F4F4F4"/>
                <w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>
                <w:ind w:left="240" w:right="240"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
                  <w:color w:val="333333"/>
                  <w:sz w:val="18"/>
                </w:rPr>
                <w:t xml:space="preserve">{escape_xml(line)}</w:t>
              </w:r>
            </w:p>
            ''')
        self.body_elements.append(''.join(elements))

    def add_table(self, headers, rows):
        tbl_xml = [
            '<w:tbl>',
            '<w:tblPr>',
            '<w:tblW w:w="0" w:type="auto"/>',
            '<w:tblBorders>',
            '<w:top w:val="single" w:sz="6" w:space="0" w:color="D3D3D3"/>',
            '<w:left w:val="single" w:sz="6" w:space="0" w:color="D3D3D3"/>',
            '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="D3D3D3"/>',
            '<w:right w:val="single" w:sz="6" w:space="0" w:color="D3D3D3"/>',
            '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>',
            '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>',
            '</w:tblBorders>',
            '</w:tblPr>'
        ]

        # Header Row
        tbl_xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
        for h in headers:
            tbl_xml.append(f'''
            <w:tc>
              <w:tcPr>
                <w:shd w:val="clear" w:color="auto" w:fill="1F4E79"/>
              </w:tcPr>
              <w:p>
                <w:pPr>
                  <w:spacing w:before="60" w:after="60"/>
                  <w:jc w:val="center"/>
                </w:pPr>
                <w:r>
                  <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:b/>
                    <w:color w:val="FFFFFF"/>
                    <w:sz w:val="20"/>
                  </w:rPr>
                  <w:t>{escape_xml(h)}</w:t>
                </w:r>
              </w:p>
            </w:tc>
            ''')
        tbl_xml.append('</w:tr>')

        # Data Rows
        for idx, row in enumerate(rows):
            bg = 'F9FBFD' if idx % 2 == 1 else 'FFFFFF'
            tbl_xml.append('<w:tr>')
            for c_idx, cell in enumerate(row):
                jc_val = "center" if (c_idx == 0 or str(cell) == "Pass") and len(str(cell)) < 12 else "left"
                status_color = "008000" if str(cell) == "Pass" else "262626"
                bold_tag = "<w:b/>" if str(cell) == "Pass" or c_idx == 0 else ""
                tbl_xml.append(f'''
                <w:tc>
                  <w:tcPr>
                    <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
                  </w:tcPr>
                  <w:p>
                    <w:pPr>
                      <w:spacing w:before="40" w:after="40"/>
                      <w:jc w:val="{jc_val}"/>
                    </w:pPr>
                    <w:r>
                      <w:rPr>
                        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                        {bold_tag}
                        <w:color w:val="{status_color}"/>
                        <w:sz w:val="19"/>
                      </w:rPr>
                      <w:t>{escape_xml(cell)}</w:t>
                    </w:r>
                  </w:p>
                </w:tc>
                ''')
            tbl_xml.append('</w:tr>')

        tbl_xml.append('</w:tbl>')
        self.body_elements.append(''.join(tbl_xml))

    def save(self, filepath):
        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

        doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

        styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:color w:val="262626"/>
        <w:sz w:val="22"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
</w:styles>'''

        body_inner = "".join(self.body_elements)
        doc_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {body_inner}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as docx:
            docx.writestr('[Content_Types].xml', content_types)
            docx.writestr('_rels/.rels', rels)
            docx.writestr('word/_rels/document.xml.rels', doc_rels)
            docx.writestr('word/styles.xml', styles)
            docx.writestr('word/document.xml', doc_xml)


def build_complete_report(filepath):
    doc = StrictDocxBuilder()

    # =========================================================================
    # PAGE 1: TITLE PAGE (Kept as is, as requested by user)
    # =========================================================================
    doc.add_title("SOFTWARE PROJECT REPORT")
    doc.add_subtitle("B.Tech 2nd Year – Computer Science and Engineering(Data Science)", bold=True)
    doc.add_subtitle("Academic Session: 2026–2027", bold=False)
    doc.add_paragraph("\n\n\n\n", justify=False)
    doc.add_subtitle("Project Title: [Enter the Title of the Project]", bold=True)
    doc.add_paragraph("\n\n\n", justify=False)
    doc.add_subtitle("Submitted by:", bold=True)
    doc.add_subtitle("1. Student Name – Roll No.", bold=False)
    doc.add_paragraph("\n\n\n", justify=False)
    doc.add_subtitle("Department of Computer Science and Engineering (Data Science)", bold=True)
    doc.add_subtitle("[College/Institute Name]", bold=False)
    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    doc.add_heading_1("TABLE OF CONTENTS")
    toc_items = [
        ("1.", "Abstract", "3"),
        ("2.", "Introduction", "4"),
        ("3.", "Problem Statement", "5"),
        ("4.", "Objectives of the Project", "6"),
        ("5.", "Scope of the Project", "7"),
        ("6.", "Tools and Technologies Used", "8"),
        ("7.", "System Requirements", "9"),
        ("8.", "System Design", "10"),
        ("9.", "Database Design", "12"),
        ("10.", "Implementation", "14"),
        ("11.", "Testing", "17"),
        ("12.", "Results and Screenshots", "19"),
        ("13.", "Limitations", "21"),
        ("14.", "Future Scope", "22"),
        ("15.", "Conclusion", "23"),
        ("16.", "References", "24"),
        ("Appendix", "System Architecture & API Specifications", "25")
    ]
    doc.add_table(["Sl. No.", "Chapter Title", "Page No."], toc_items)
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: ABSTRACT
    # =========================================================================
    doc.add_heading_1("CHAPTER 1: ABSTRACT")
    doc.add_paragraph(
        "PageSage is an intelligent, full-stack conversational AI book assistant and reading companion "
        "engineered to transform literature exploration. In an age of digital information saturation, readers "
        "frequently confront choice paralysis, scattered reading logs, and the persistent frustration of accidental plot "
        "spoilers on social platforms. PageSage addresses these challenges through a dual-intelligence architecture that "
        "combines state-of-the-art Google Gemini Cloud AI (via dynamic ModelService discovery) with a high-fidelity "
        "offline literary intelligence engine and real-time Open Library REST API integration."
    )
    doc.add_paragraph(
        "The application provides tailored book recommendations by emotional mood, genre, and trope; offers chapter "
        "and plot summaries safeguarded by an interactive, click-to-reveal Spoiler Shield; formulates stimulating book "
        "club discussion questions; and constructs comprehensive series reading orders for intricate fantasy and sci-fi universes. "
        "Additionally, an interactive client-side Bookshelf manager enables readers to seamlessly categorize books into 'Want to Read', "
        "'Currently Reading', and 'Finished' with one-click Markdown export. Developed using Python 3, Flask, HTML5, "
        "CSS3, and vanilla JavaScript, PageSage delivers an aesthetic Dark Academia responsive interface, verified by a 15-test "
        "automated test suite and deployed to production cloud environments."
    )
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: INTRODUCTION
    # =========================================================================
    doc.add_heading_1("CHAPTER 2: INTRODUCTION")
    doc.add_heading_2("2.1 Background of the Project")
    doc.add_paragraph(
        "Literature serves as an essential medium for cognitive enrichment, empathy development, and human knowledge transmission. "
        "However, with millions of books published annually across traditional presses and self-publishing channels, modern readers "
        "face an unprecedented volume of literary content. Traditional keyword-based search engines and commercial book portals "
        "frequently offer static, advertising-driven lists that fail to capture the nuanced subjective criteria readers care about—such "
        "as pacing, emotional tone, specific literary tropes, character chemistry, and moral ambiguity."
    )
    doc.add_heading_2("2.2 Why This Project is Needed")
    doc.add_paragraph(
        "Readers require an intuitive, intelligent dialogue partner that acts like an erudite librarian. PageSage is designed "
        "to simulate a deep, interactive consultation with an expert bibliophile. Whether a reader is searching for a fast-paced "
        "hard sci-fi with an unlikely friendship, a cozy mystery for a rainy evening, or the exact chronological starting point for "
        "Brandon Sanderson's Cosmere saga, PageSage delivers tailored, contextual, and structured literary guidance."
    )
    doc.add_heading_2("2.3 How the Application Works")
    doc.add_paragraph(
        "PageSage operates as a lightweight, single-page web application. The frontend communicates asynchronously with a "
        "Python Flask REST API backend. When a user submits a query, the Literary Agent determines the optimal model path, invokes "
        "Google's Gemini Generative API (or falls back to its internal NLP heuristic engine), extracts structured book metadata, "
        "and renders rich interactive book cards alongside formatted Markdown dialogue."
    )
    doc.add_heading_2("2.4 Target Audience")
    doc.add_paragraph("The primary beneficiaries and target user groups for PageSage include:")
    doc.add_bullet("Casual & Avid Readers:", "Individuals seeking personalized book discoveries tailored to their mood and reading pace.")
    doc.add_bullet("Book Club Moderators:", "Organizers seeking thought-provoking discussion questions, pacing analyses, and meeting ideas.")
    doc.add_bullet("Students & Researchers:", "Scholars analyzing character motivations, literary devices, and historical themes in classic literature.")
    doc.add_bullet("Series Enthusiasts:", "Fans of massive speculative universes seeking clear chronological vs. publication reading orders.")
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: PROBLEM STATEMENT
    # =========================================================================
    doc.add_heading_1("CHAPTER 3: PROBLEM STATEMENT")
    doc.add_paragraph(
        "Despite the wide availability of online book databases and review aggregators, the digital reading experience suffers from "
        "several fundamental shortcomings:"
    )
    doc.add_bullet("Choice Paralysis & Rigid Categorization:", "Conventional book platforms categorize titles strictly by broad genres "
                   "(e.g., 'Fiction', 'Fantasy'), ignoring user-centric emotional nuances such as 'uplifting survival against all odds' "
                   "or 'witty enemies-to-lovers with high intellectual stakes'.")
    doc.add_bullet("Accidental Spoiler Exposure:", "Readers seeking plot premises or character breakdowns frequently encounter major twists, "
                   "murder culprits, and climactic endings inadvertently in online reviews, destroying the reading experience.")
    doc.add_bullet("Scattered Reading Logs:", "Readers rely on disparate spreadsheets or complex commercial platforms requiring heavyweight logins "
                   "just to save a title they recently discovered.")
    doc.add_bullet("Lack of Interactive Literary Discourse:", "Static websites offer one-way reviews rather than dynamic discussions about character "
                   "arcs, moral dilemmas, and narrative symbolism.")
    doc.add_heading_2("3.1 Proposed Solution")
    doc.add_paragraph(
        "PageSage resolves these challenges by uniting modern generative AI with respectful reading controls. Its active Spoiler Shield "
        "quarantines critical plot revelations behind click-to-reveal components, its Bookshelf tracker maintains lightweight local persistence, "
        "and its conversational agent translates subjective reader inquiries into curated, richly presented recommendations."
    )
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: OBJECTIVES OF THE PROJECT
    # =========================================================================
    doc.add_heading_1("CHAPTER 4: OBJECTIVES OF THE PROJECT")
    doc.add_paragraph("The primary technical and operational objectives of the PageSage project are:")
    doc.add_bullet("Objective 1 - Responsive Web Platform:", "Design and implement an aesthetic, responsive single-page web interface "
                   "featuring Dark Academia and Light themes accessible across mobile phones, tablets, and desktop devices.")
    doc.add_bullet("Objective 2 - Dual-AI Architecture:", "Engineer a resilient dual-intelligence backend integrating Google Gemini Cloud AI "
                   "(with automated ModelService discovery) and an offline literary reasoning engine for 100% operational reliability.")
    doc.add_bullet("Objective 3 - Spoiler Shield Implementation:", "Develop an active spoiler protection system that programmatically hides "
                   "critical narrative turns, character deaths, and endings behind interactive HTML5 details containers.")
    doc.add_bullet("Objective 4 - Interactive Bookshelf Tracker:", "Implement a client-side reading tracker supporting 'Want to Read', "
                   "'Currently Reading', and 'Finished' shelves with localStorage persistence and one-click Markdown (.md) export.")
    doc.add_bullet("Objective 5 - Live Metadata Integration:", "Connect with the Open Library REST API to dynamically fetch real-world book covers, "
                   "publication years, ratings, and author metadata.")
    doc.add_bullet("Objective 6 - Quality Assurance & Deployment:", "Construct an automated unit testing suite (achieving 100% pass across 15 tests) "
                   "and deploy the production application to Render cloud hosting with Gunicorn WSGI.")
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: SCOPE OF THE PROJECT
    # =========================================================================
    doc.add_heading_1("CHAPTER 5: SCOPE OF THE PROJECT")
    doc.add_paragraph(
        "The project encompasses a comprehensive suite of literary exploration and data management capabilities:"
    )
    doc.add_bullet("User Authentication & Profile Management:", "Secure registration, login with hashed credentials (PBKDF2/SHA256 via Werkzeug), session preservation, guest entry, and one-click demo login.")
    doc.add_bullet("Conversational Book Assistant:", "Natural language Q&A regarding plots, characters, historical contexts, and writing styles.")
    doc.add_bullet("Mood & Trope Filtering:", "Dynamic recommendation generation matching nuanced reader prompts with literary elements.")
    doc.add_bullet("Spoiler Protection Controller:", "Instant toggle switch protecting readers from uninvited climax disclosures.")
    doc.add_bullet("Interactive Book Cards:", "Visual display cards embedded directly in chat responses with cover images, ratings, and direct '+ Add to Shelf' controls.")
    doc.add_bullet("Multi-Tab Bookshelf:", "Client-side library management allowing users to cycle books through reading stages and monitor shelf counters.")
    doc.add_bullet("Book Club Assistant:", "Instant formulation of multi-perspective discussion questions, ethical dilemma prompts, and host suggestions.")
    doc.add_bullet("Reading Order Guides:", "Curated timelines and entry routes for sprawling multi-novel sagas (Sanderson's Cosmere, Herbert's Dune).")
    doc.add_bullet("Production Cloud Accessibility:", "Public deployment via Gunicorn and Render, allowing seamless access across any network-enabled device.")
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: TOOLS AND TECHNOLOGIES USED
    # =========================================================================
    doc.add_heading_1("CHAPTER 6: TOOLS AND TECHNOLOGIES USED")
    doc.add_paragraph("The following table enumerates the software tools, libraries, and frameworks utilized in developing PageSage:")
    tech_table = [
        ["Python 3.14", "Core programming language for backend server and business logic."],
        ["Flask 3.1", "Micro web framework providing REST API endpoints and routing."],
        ["Google Gemini API", "Cloud generative language model (gemini-3.8-flash) for deep reasoning."],
        ["Open Library REST API", "Public API used for dynamic book cover lookups and bibliographical data."],
        ["HTML5", "Semantic markup for single-page application structure and modal dialogs."],
        ["CSS3 (Custom Theme)", "Responsive styling, Dark Academia aesthetic, and CSS variables."],
        ["JavaScript (ES6+)", "Client-side event handling, asynchronous Fetch API, and localStorage management."],
        ["Marked.js", "Client-side library for parsing and rendering rich Markdown in chat bubbles."],
        ["Lucide Icons", "Lightweight, scalable vector icon set for interface navigation."],
        ["Gunicorn 21.2", "Production-grade WSGI HTTP Server for cloud deployment."],
        ["Git & GitHub", "Distributed version control system and remote repository hosting."],
        ["Render", "Cloud Application Platform for automated CI/CD and public hosting."],
        ["VS Code", "Integrated Development Environment for code editing and debugging."]
    ]
    doc.add_table(["Technology / Tool", "Specific Purpose in Project"], tech_table)
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: SYSTEM REQUIREMENTS
    # =========================================================================
    doc.add_heading_1("CHAPTER 7: SYSTEM REQUIREMENTS")
    doc.add_heading_2("7.1 Hardware Requirements")
    doc.add_bullet("Processor:", "Intel Core i3 / AMD Ryzen 3 (1.8 GHz) or higher.")
    doc.add_bullet("Random Access Memory (RAM):", "Minimum 4 GB (8 GB recommended for optimal multi-tab browsing).")
    doc.add_bullet("Storage Space:", "Minimum 500 MB available local disk storage.")
    doc.add_bullet("Network Interface:", "Standard Wi-Fi / Ethernet adapter (required for cloud API interactions and public deployment).")

    doc.add_heading_2("7.2 Software Requirements")
    doc.add_bullet("Operating System:", "Windows 10/11, macOS Monterey+, or Ubuntu Linux 20.04+.")
    doc.add_bullet("Python Runtime:", "Python 3.10 or higher (tested on Python 3.14.3).")
    doc.add_bullet("Web Browser:", "Google Chrome 110+, Mozilla Firefox 110+, Microsoft Edge 110+, or Safari 16+.")
    doc.add_bullet("Dependencies:", "Flask >= 3.0.0, requests >= 2.31.0, gunicorn >= 21.2.0.")
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: SYSTEM DESIGN
    # =========================================================================
    doc.add_heading_1("CHAPTER 8: SYSTEM DESIGN")
    doc.add_heading_2("8.1 Application Workflow")
    doc.add_paragraph("The architectural workflow of PageSage is illustrated below:")
    doc.add_code_block(
"""[User Interface (Browser)]
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
[User Reads & Interacts]"""
    )
    doc.add_heading_2("8.2 Main Modules")
    doc.add_bullet("1. Dialogue & Presentation Module:", "Manages asynchronous user input, Markdown parsing via Marked.js, auto-expanding textareas, and theme toggling.")
    doc.add_bullet("2. Dual-AI Literary Agent:", "Oversees intent classification (recommendations, summaries, book club guides, reading orders), manages Gemini REST requests, and implements automatic ModelService discovery.")
    doc.add_bullet("3. Spoiler Shield Subsystem:", "Conditionally structures plot summaries with HTML5 collapsible containers based on the active state of the user's spoiler preference.")
    doc.add_bullet("4. Bookshelf & Persistence Module:", "Facilitates full CRUD operations for book tracking directly within the browser's localStorage, complete with Markdown export.")
    doc.add_bullet("5. Book Metadata Service:", "Provides local database queries, fuzzy string matching across curated literature, and Open Library REST lookups.")
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 9: DATABASE DESIGN
    # =========================================================================
    doc.add_heading_1("CHAPTER 9: DATABASE DESIGN")
    doc.add_heading_2("9.1 Storage Architecture")
    doc.add_paragraph(
        "PageSage employs a robust multi-tiered data architecture: a persistent SQLite relational database (pagesage_users.db) "
        "for secure user authentication, an in-memory structured knowledge store for literary heuristics, and client-side localStorage "
        "for responsive, zero-latency personal bookshelf tracking."
    )
    doc.add_heading_2("9.2 User Accounts Schema (SQLite Database)")
    users_schema = [
        ["id", "INTEGER PRIMARY KEY", "Unique auto-incrementing user identification number."],
        ["name", "TEXT NOT NULL", "Full display name of the registered reader."],
        ["email", "TEXT UNIQUE NOT NULL", "Unique registered email address used for login."],
        ["password_hash", "TEXT NOT NULL", "Cryptographic password hash generated via PBKDF2:SHA256."],
        ["created_at", "TIMESTAMP", "Account creation timestamp (DEFAULT CURRENT_TIMESTAMP)."]
    ]
    doc.add_table(["Field Name", "Data Type", "Description"], users_schema)

    doc.add_heading_2("9.3 Curated Literature Schema (Server-Side In-Memory)")
    server_schema = [
        ["id", "String (Slug)", "Unique alphanumeric identifier (e.g., 'project-hail-mary')."],
        ["title", "String", "Full official book title."],
        ["author", "String", "Author name(s)."],
        ["year", "Integer", "Original publication year."],
        ["genre", "String", "Primary literary genre."],
        ["tropes", "Array [String]", "Key storytelling tropes (e.g., 'unlikely friendship')."],
        ["mood", "Array [String]", "Emotional tone tags (e.g., 'optimistic', 'tense')."],
        ["rating", "Float", "Average reader rating out of 5.0."],
        ["pages", "Integer", "Standard edition page count."],
        ["description", "Text", "Spoiler-free premise and narrative hook."],
        ["spoiler_summary", "Text", "Full narrative breakdown and twist resolution."],
        ["themes", "Array [String]", "Central literary themes and motifs."],
        ["characters", "Array [Object]", "Dossier of main characters and their roles."],
        ["discussion_questions", "Array [String]", "Curated questions for book club debate."],
        ["read_alikes", "Array [String]", "Curated list of complementary recommended works."]
    ]
    doc.add_table(["Field Name", "Data Type", "Description"], server_schema)

    doc.add_heading_2("9.3 Bookshelf Schema (Client-Side LocalStorage)")
    client_schema = [
        ["want", "JSON Array [Book]", "Array of book objects marked as 'Want to Read'."],
        ["reading", "JSON Array [Book]", "Array of book objects currently being read."],
        ["finished", "JSON Array [Book]", "Array of book objects completed by the user."]
    ]
    doc.add_table(["Key Name", "Data Type", "Description"], client_schema)

    doc.add_heading_2("9.4 CRUD Operations")
    doc.add_bullet("Create (Insert):", "Clicking '+ Add' on any book card writes the item into the designated shelf in localStorage.")
    doc.add_bullet("Read (Select):", "The shelf tabs dynamically render book thumbnails, authors, and titles with instantaneous counter updates.")
    doc.add_bullet("Update:", "Users can cycle books between 'Want', 'Reading', and 'Finished' states via the one-touch cycle button.")
    doc.add_bullet("Delete:", "Clicking the trash icon instantly removes the targeted book from storage.")
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 10: IMPLEMENTATION
    # =========================================================================
    doc.add_heading_1("CHAPTER 10: IMPLEMENTATION")
    doc.add_heading_2("10.1 Backend API Implementation (app.py)")
    doc.add_paragraph(
        "The Flask backend exposes clean, stateless REST endpoints supporting JSON payloads. Below is the primary chat endpoint handler:"
    )
    doc.add_code_block(
"""@app.route("/api/chat", methods=["POST"])
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
    return jsonify(response)"""
    )
    doc.add_heading_2("10.2 Dynamic Gemini Model Discovery (literary_agent.py)")
    doc.add_paragraph(
        "To prevent 404 errors caused by API deprecations, PageSage dynamically interrogates Google's ModelService at runtime:"
    )
    doc.add_code_block(
"""def _discover_model(self, api_key: str) -> List[str]:
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
    return discovered or ["v1beta/models/gemini-2.0-flash"]"""
    )
    doc.add_heading_2("10.3 Spoiler Shield Implementation")
    doc.add_paragraph(
        "When the spoiler shield is active, critical disclosures are wrapped inside an HTML5 details tag with styled summary borders:"
    )
    doc.add_code_block(
"""if spoiler_shield:
    text += \"\"\"
<details class="spoiler-box">
  <summary>⚠️ <strong>Click to reveal spoiler-heavy plot details & ending</strong></summary>
  <p>\"\"\" + book["spoiler_summary"] + \"\"\"</p>
</details>\"\"\""""
    )
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 11: TESTING
    # =========================================================================
    doc.add_heading_1("CHAPTER 11: TESTING")
    doc.add_paragraph(
        "The project includes a comprehensive automated unit and integration test suite (test_app.py) validating backend routes, "
        "intent recognition, user authentication, and data structures. All 21 tests execute with a 100% pass rate:"
    )
    test_results = [
        ["1", "Curated Library Integrity", "Library contains >5 books with complete schema fields", "Verified 12+ books with all attributes", "Pass"],
        ["2", "Local Book Search", "Accurate fuzzy title search for 'Project Hail Mary'", "Book matched with author Andy Weir", "Pass"],
        ["3", "Genre & Mood Filtering", "Filter books by 'Science Fiction' genre", "Sci-Fi list returned successfully", "Pass"],
        ["4", "Book Retrieval by ID", "Fetch specific book record for 'dune'", "Dune object retrieved with full details", "Pass"],
        ["5", "Spoiler Shield (Active)", "Plot twist concealed behind details spoiler-box", "HTML spoiler-box present in output", "Pass"],
        ["6", "Spoiler Shield (Disabled)", "Direct, unshielded climax and ending discussion", "Full ending details returned in prose", "Pass"],
        ["7", "Book Club Question Gen", "Formulate targeted questions for 'The Great Gatsby'", "Formatted questions & host tips returned", "Pass"],
        ["8", "Series Reading Order", "Generate Sanderson Cosmere reading timeline", "Structured reading guide returned", "Pass"],
        ["9", "Trope Recommendation", "Suggest cozy mystery based on user prompt", "Curated titles with tropes returned", "Pass"],
        ["10", "Demo User Authentication", "Verify demo@pagesage.com / pagesage123", "User authenticated with ID & display name", "Pass"],
        ["11", "Invalid Password Rejection", "Attempt login with incorrect password", "Authentication rejected with error message", "Pass"],
        ["12", "User Account Registration", "Register new reader with hashed password", "Record inserted into SQLite users database", "Pass"],
        ["13", "Duplicate Email Guard", "Prevent registering duplicate email address", "Registration blocked with existing email error", "Pass"],
        ["14", "Unauthenticated Redirect", "Unauthenticated request to '/' redirects", "HTTP 302 Redirect to /login", "Pass"],
        ["15", "Login Interface Route", "HTTP GET /login renders authentication view", "HTTP 200 with Sign In & Sign Up tabs", "Pass"],
        ["16", "Guest Entry Flow", "HTTP POST /api/auth/guest sets guest session", "HTTP 200 with Guest Bibliophile profile", "Pass"],
        ["17", "User Logout Flow", "HTTP GET /logout clears session", "HTTP 302 Redirect to /login", "Pass"],
        ["18", "System Status Endpoint", "HTTP GET /api/status returns online status", "HTTP 200 with JSON status: online", "Pass"],
        ["19", "Curated Catalogue API", "HTTP GET /api/curated returns book list", "HTTP 200 with JSON book array", "Pass"],
        ["20", "Book Details API", "HTTP GET /api/book/dune returns book metadata", "HTTP 200 with title 'Dune'", "Pass"],
        ["21", "Chat API Validation", "HTTP POST /api/chat with valid inquiry", "HTTP 200 with text & book cards", "Pass"]
    ]
    doc.add_table(["Test No.", "Feature Tested", "Expected Result", "Actual Result", "Status"], test_results)
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 12: RESULTS AND SCREENSHOTS
    # =========================================================================
    doc.add_heading_1("CHAPTER 12: RESULTS AND SCREENSHOTS")
    doc.add_paragraph(
        "This chapter presents the operational user interface of PageSage. Students can attach visual captures into the designated figures:"
    )
    doc.add_heading_2("Figure 1: Welcome & Landing Interface")
    doc.add_paragraph("Shows the responsive Dark Academia workspace, featuring guided inquiry pills, the AI engine indicator, and the bookshelf sidebar.")
    doc.add_paragraph("[ Insert Screenshot of Home Screen / Welcome Interface Here ]", italic=True)

    doc.add_heading_2("Figure 2: Conversational Dialogue & Interactive Book Cards")
    doc.add_paragraph("Displays the conversational response stream with rich markdown typography and interactive book cards with cover art and '+ Add' buttons.")
    doc.add_paragraph("[ Insert Screenshot of Chat Dialogue with Book Cards Here ]", italic=True)

    doc.add_heading_2("Figure 3: Active Spoiler Shield Mechanism")
    doc.add_paragraph("Demonstrates the click-to-reveal spoiler protection box shielding climactic plot revelations and twist endings.")
    doc.add_paragraph("[ Insert Screenshot of Click-to-Reveal Spoiler Box Here ]", italic=True)

    doc.add_heading_2("Figure 4: My Bookshelf Reading Tracker")
    doc.add_paragraph("Illustrates the interactive multi-shelf tracker showcasing categorized titles under 'Want to Read', 'Reading', and 'Read'.")
    doc.add_paragraph("[ Insert Screenshot of Bookshelf Sidebar & Export Action Here ]", italic=True)

    doc.add_heading_2("Figure 5: Configuration & Preferences Modal")
    doc.add_paragraph("Shows the settings dialog where users configure Google Gemini API credentials and favorite genres.")
    doc.add_paragraph("[ Insert Screenshot of Settings & Preferences Modal Here ]", italic=True)
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 13: LIMITATIONS
    # =========================================================================
    doc.add_heading_1("CHAPTER 13: LIMITATIONS")
    doc.add_paragraph("While PageSage achieves its core objectives, several operational constraints exist:")
    doc.add_bullet("1. Cloud API Rate Limits:", "Google Gemini free-tier keys impose requests-per-minute (RPM) constraints, which may cause temporary throttling during high-volume usage.")
    doc.add_bullet("2. External Network Dependency for Images:", "Displaying live Open Library book covers requires an active internet connection; in offline sandboxed environments, placeholder covers are rendered.")
    doc.add_bullet("3. Browser-Bound Storage:", "Bookshelf data stored in browser localStorage is specific to that device and browser, lacking cross-device synchronization without a central account login.")
    doc.add_bullet("4. Scope Boundary on Copyrighted Content:", "PageSage provides analysis, commentary, and summaries, but does not distribute or host full copyrighted e-book manuscripts.")
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 14: FUTURE SCOPE
    # =========================================================================
    doc.add_heading_1("CHAPTER 14: FUTURE SCOPE")
    doc.add_paragraph("The PageSage architecture can be expanded in several valuable directions:")
    doc.add_bullet("User Accounts & Cloud Database:", "Integrate PostgreSQL / Supabase authentication to synchronize reading lists seamlessly across web and mobile platforms.")
    doc.add_bullet("RAG Vector Database (Retrieval-Augmented Generation):", "Incorporate FAISS or ChromaDB with sentence embeddings to allow Q&A across user-uploaded e-book files (EPUB/PDF).")
    doc.add_bullet("Audio Integration & Text-to-Speech:", "Add speech-to-text voice queries and AI audiobook narrator voices for hands-free reading assistance.")
    doc.add_bullet("Social Reading Groups:", "Enable collaborative book clubs where members share synchronized reading schedules, annotations, and ratings.")
    doc.add_bullet("Native Mobile Apps:", "Package the frontend using Flutter or React Native for native distribution on iOS and Android app stores.")
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 15: CONCLUSION
    # =========================================================================
    doc.add_heading_1("CHAPTER 15: CONCLUSION")
    doc.add_paragraph(
        "PageSage successfully demonstrates how modern Data Science and Artificial Intelligence technologies can be synthesized "
        "with elegant software engineering to enrich human literary discovery. By solving the dual challenges of choice paralysis "
        "and inadvertent plot spoilers, the platform offers an indispensable companion for readers, students, and book clubs."
    )
    doc.add_paragraph(
        "Throughout this project, foundational competencies were developed in Python full-stack engineering, REST API architecture, "
        "dynamic cloud LLM integration, automated unit testing, client-side state persistence, and cloud production deployment. "
        "All stated project objectives were fully achieved, providing a production-ready, extensible platform with broad real-world utility."
    )
    doc.add_page_break()

    # =========================================================================
    # CHAPTER 16: REFERENCES
    # =========================================================================
    doc.add_heading_1("CHAPTER 16: REFERENCES")
    doc.add_bullet("1. Flask Documentation:", "Pallets Projects. Flask Web Development Documentation. https://flask.palletsprojects.com/")
    doc.add_bullet("2. Google AI Studio & Gemini API:", "Google DeepMind. Gemini API Reference & Model Documentation. https://aistudio.google.com/")
    doc.add_bullet("3. Open Library Developer Portal:", "Internet Archive. Open Library REST APIs for Books & Covers. https://openlibrary.org/developers/api")
    doc.add_bullet("4. MDN Web Docs:", "Mozilla Developer Network. HTML5 Details, CSS Grid, and Fetch API Specifications. https://developer.mozilla.org/")
    doc.add_bullet("5. Gunicorn WSGI Documentation:", "Arboretum Gunicorn Team. Python WSGI HTTP Server. https://gunicorn.org/")
    doc.add_bullet("6. Marked.js:", "Christopher Jeffrey. Marked - A fast JavaScript Markdown parser. https://marked.js.org/")
    doc.add_page_break()

    # =========================================================================
    # APPENDIX: ARCHITECTURE & API CONTRACT
    # =========================================================================
    doc.add_heading_1("APPENDIX: SYSTEM SPECIFICATIONS")
    doc.add_heading_2("Project Directory Tree")
    doc.add_code_block(
"""book-assistant-ai/
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
        └── app.js          # Client State, Chat Logic, & Bookshelf CRUD"""
    )
    doc.add_heading_2("REST API Contracts")
    doc.add_bullet("POST /api/chat:", "Accepts { message, conversation_history, api_key, spoiler_shield, preferences }. Returns { text, book_cards, engine, model }.")
    doc.add_bullet("GET /api/status:", "Returns { status: 'online', name: 'PageSage', version: '1.0.0', books_count: int }.")
    doc.add_bullet("GET /api/curated:", "Returns complete curated JSON catalogue filtered by optional genre/mood query params.")
    doc.add_bullet("GET /api/book/<id>:", "Returns full bibliographical and analytical dossier for a targeted book.")

    doc.save(filepath)
    print(f"Report successfully saved to {filepath}")

if __name__ == "__main__":
    out = r"C:\Users\rouna\.gemini\antigravity\scratch\book-assistant-ai\PageSage_AI_Project_Report.docx"
    build_complete_report(out)
