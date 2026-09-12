<div align="center">

# 🇮🇳 Standards Saathi (मानक साथी)
### *Next-Gen AI Technical Advisor & Verification Hub for Indian Standards (IS Codes) and BIS Regulations*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-0467DF?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-384d%20MiniLM-FFA000?style=for-the-badge)](https://www.sbert.net)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.1%20%7C%20Compound-f55036?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>Bilingual Conversational RAG • Dual Voice Assistant (STT + TTS) • Clause-Level Citations • ISI / HUID / CRS Verification • MSME 80% Subsidy Hub • 7-Step BIS Certification Roadmap • Dynamic Standard Ingestion</b>
</p>

[Key Features](#-key-features) • [Tech Stack](#-tech-stack) • [System Architecture](#-system-architecture) • [Ingested Indian Standards](#-ingested-indian-standards) • [Getting Started](#-getting-started) • [Running the Application](#-running-the-application) • [API Reference](#-api-reference) • [Example Queries](#-example-queries-to-try) • [Project Structure](#-project-structure)

---

</div>

## 📌 Overview

**Standards Saathi (मानक साथी)** is an enterprise-grade, high-performance Retrieval-Augmented Generation (RAG) system engineered for engineers, architects, quality control (QC) managers, manufacturers, contractors, MSMEs, and Indian consumers. It provides authoritative, clause-accurate technical guidance on **Bureau of Indian Standards (BIS)** codes, **Quality Control Orders (QCOs)**, **ISI Certification Schemes**, **Gold Hallmarking (HUID)**, and **statutory MSME concessions**.

Whether determining permissible heavy metal limits in drinking water (*IS 10500*), designing high-strength or self-compacting concrete mixes (*IS 10262 / IS 456*), checking sub-zero Charpy impact toughness for structural steel (*IS 2062*), or verifying manufacturer license authenticity, Standards Saathi delivers verified technical answers with exact clause citations, similarity metrics, and official BIS purchase links in sub-seconds.

---

## 🚀 Key Features

### 1. 🌐 Full Bilingual Experience (English & हिंदी)
* **One-Click Real-Time Language Switch (`EN | हिं`)**: Seamlessly toggles all UI labels, action cards, chips, modal text, and placeholders between English and Hindi (Devanagari script).
* **Bilingual LLM Synthesis**: Contextual prompt conditioning ensures the LLM synthesizes technical responses in fluent English or natural Hindi (हिंदी / Hinglish) tailored for technical and non-technical stakeholders alike.

### 2. 🎙️ Dual Voice Assistant (STT & TTS)
* **Voice Input (Speech-to-Text)**: Powered by the Web Speech API (`webkitSpeechRecognition`) with dynamic locale switching (`hi-IN` / `en-IN`), visual pulsing indicator, and continuous listening safeguards.
* **Audio Read Aloud (Text-to-Speech)**: Integrated browser speech synthesis (`window.speechSynthesis`) allows users to listen to any technical response aloud in Hindi or English with a single click.

### 3. 📄 Clause-Level Citations & Direct Purchase Links
* Every generated response provides exact source attribution:
  ```markdown
  📄 IS_1239_Part_1_2004.pdf, Page 5, Section 8.0 | 🔗 Purchase: https://www.standardsbis.in
  ```
* Expandable accordion cards reveal retrieved clause text, section numbers, and vector similarity match percentages (up to 100%).

### 4. 🛡️ BIS License & Hallmark Verification Portal
* **ISI License (CM/L)**: Validates 7-to-8 digit manufacturer license numbers against BIS standard schemas.
* **Gold HUID Code**: Verifies 6-digit alphanumeric hallmark identifiers to protect consumers against counterfeit jewellery.
* **Electronics CRS (R-Number)**: Validates Compulsory Registration Scheme 8-digit registrations for lithium batteries, power banks, adapters, and smart devices under MeitY regulations.
* Direct integration hooks to official **BIS Care App** verification flows.

### 5. 📋 Interactive 7-Step BIS Certification Guide
* Comprehensive end-to-end certification roadmap:
  1. **Standard & Scheme Identification** (Scheme-I ISI vs Scheme-II CRS, QCO check)
  2. **In-House SIT Testing Laboratory Setup** (Calibrated equipment & QC staffing)
  3. **e-BIS Manakonline Application Submission** (Form-V, Udyam certificate, factory layout)
  4. **Factory Audit & Inspection** (Infrastructure, manufacturing line, QC verification)
  5. **Sample Drawing & Independent NABL/BIS Lab Testing** (Counter-sample verification)
  6. **Grant of BIS License (CM/L Number)** (Legal authorization to affix ISI Mark)
  7. **Market Surveillance & Annual Renewal** (Periodic audits and license renewal)
* **Cost Estimates & Timelines**: Detailed breakdown (₹20,000–₹80,000 net; 30–60 days).
* Direct links to **e-BIS Manakonline**, **BIS Lab Directory (LIMS)**, **Fee Structure**, and **QCO Tracker**.

### 6. 🏢 MSME 80% Concession & Compliance Hub
* Explains statutory concessions granted by the Ministry of Consumer Affairs & MSME Ministry:
  * **80% Concession** on BIS Application and Annual Marking/License fees for Micro Enterprises.
  * **50% Concession** for Small Enterprises and Startups.
  * **50% Testing Subsidy** for product testing in BIS-recognized labs.
  * **30-Day Fast-Track** approval path under the Simplified Conformity Assessment Scheme.

### 7. 📚 Searchable Indian Standards Catalog
* Interactive catalog with category-based filtering (**Civil & Structural**, **Mechanical & Metallurgy**, **Electrotechnical**, **Chemical & Water Quality**, **Fire & Life Safety**, **Precious Metals & Hallmarking**).
* View full standard summaries, departments, revision history, and direct purchase links.

### 8. 🔐 Admin Portal & Dynamic Standard Ingestion
* Password-protected administration panel.
* **Runtime Vector Ingestion**: Ingest new custom Indian Standards (*Standard Number, Title, Category, Summary, Clauses*) directly into the live FAISS index with immediate vector rebuilding—zero server restarts required.
* Dynamic Groq API Key management with live status feedback.

### 9. 📊 Dual Frontend Experience
* **Modern Web Application (FastAPI + Tailwind CSS + Vanilla JS)**: Sleek, responsive, mobile-first Material 3 UI with Indian tricolor palette accents.
* **Streamlit Analytics Dashboard (`app.py`)**: Standalone data exploration dashboard featuring live vector index telemetry, session counters, query history download (`.txt`/Markdown), and parameter sliders (Top-K, Temperature, Model override).

---

## 🛠️ Tech Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI & Uvicorn** | Asynchronous high-throughput REST API server with Pydantic validation |
| **Secondary Dashboard** | **Streamlit (v1.40+)** | Multi-tab analytics UI with session state, sidebar telemetry, and dynamic widgets |
| **Vector Database** | **FAISS (`faiss-cpu` v1.8+)** | Dense vector index with `IndexFlatIP` and L2 normalized cosine similarity search |
| **Embeddings** | **Sentence Transformers (v3.0+)** | `all-MiniLM-L6-v2` generating 384-dimensional dense semantic embeddings |
| **LLM Inference** | **Groq Cloud API** | Ultra-low latency inference running `llama-3.1-8b-instant`, `groq/compound-mini`, `openai/gpt-oss-20b` |
| **Frontend UI** | **Tailwind CSS + Material Symbols** | Responsive Material 3 design, custom color tokens, glassmorphism, Devanagari typography |
| **Voice Processing** | **Web Speech API** | Client-side SpeechRecognition (STT) and SpeechSynthesis (TTS) |
| **Markdown Parsing** | **Marked.js** | Client-side Markdown rendering with tables, code blocks, and blockquotes |
| **Environment / Config** | **python-dotenv & Pydantic** | Secure secret management for API keys and administrator credentials |

---

## 🏗️ System Architecture

```
                                  ┌──────────────────────────────────────────────────────────┐
                                  │                     CLIENT INTERFACES                    │
                                  │                                                          │
                                  │   ┌────────────────────────┐  ┌───────────────────────┐  │
                                  │   │ Modern Web UI (HTML5)  │  │  Streamlit Dashboard  │  │
                                  │   │ TailwindCSS + WebSpeech│  │      (`app.py`)       │  │
                                  │   └───────────┬────────────┘  └───────────┬───────────┘  │
                                  └───────────────┼───────────────────────────┼──────────────┘
                                                  │ HTTP / JSON               │ Direct Python Call
                                                  ▼                           ▼
                                  ┌──────────────────────────────────────────────────────────┐
                                  │                  FASTAPI BACKEND SERVER                  │
                                  │                      (`server.py`)                       │
                                  │                                                          │
                                  │   • POST /api/chat           • GET  /api/standards       │
                                  │   • POST /api/standards      • POST /api/admin/auth      │
                                  │   • POST /api/config         • Static File Server (/)    │
                                  └─────────────────────────────┬────────────────────────────┘
                                                                │
                                                                ▼
                                  ┌──────────────────────────────────────────────────────────┐
                                  │                 STANDARDS RAG ENGINE                     │
                                  │                    (`rag_engine.py`)                     │
                                  └──────────────┬────────────────────────────┬──────────────┘
                                                 │                            │
                     ┌───────────────────────────┴──────────┐                 │
                     ▼                                      ▼                 ▼
      ┌─────────────────────────────┐        ┌─────────────────────┐   ┌─────────────────────────────┐
      │    Sentence Transformers    │        │  FAISS Vector Index │   │       Groq Cloud API        │
      │     (all-MiniLM-L6-v2)      │───────▶│    (IndexFlatIP)    │   │  (Llama 3.1 8B Instant /    │
      │  384-dim Dense Embeddings   │        │ Normalized Vectors  │   │     Compound Fallback)      │
      └─────────────────────────────┘        └──────────┬──────────┘   └──────────────┬──────────────┘
                                                        │                             │
                                                        │ Top-K Chunks + Metadata     │ LLM Synthesis
                                                        └──────────────┬──────────────┘
                                                                       │
                                                                       ▼
                                                       ┌───────────────────────────────┐
                                                       │  Synthesized Response Cards   │
                                                       │  • Direct Answer & Markdown   │
                                                       │  • Clause-Level Citations     │
                                                       │  • Related Standards & URLs   │
                                                       │  • Audio Read-Aloud (TTS)     │
                                                       └───────────────────────────────┘
```

---

## 📦 Ingested Indian Standards

The knowledge base in [`sample_data.py`](sample_data.py) comes pre-loaded with curated, clause-indexed Indian Standards spanning critical engineering, safety, and consumer sectors:

| Standard Number | Category | Title / Scope | Key Clauses Covered |
| :--- | :--- | :--- | :--- |
| **IS 2720 (Part 1):1983** | Civil & Geotechnical | Methods of Test for Soils — Preparation of Dry Soil Samples | Cl 2.0 (Apparatus: Mallet, Pulverizer, Sieves, Oven), Cl 3.0 (Drying limit <60°C for organic/calcareous soils), Table 1 (Sample quantities for LL/PL, CBR, Compaction, Sieve analysis) |
| **IS 10262:2019** | Civil & Structural | Concrete Mix Proportioning — Guidelines (Second Revision) | Cl 4.2 (Target strength formula $f'_{ck} = f_{ck} + 1.65S$ or $f_{ck} + X$), Table 4 (Water content), Table 5 (Coarse aggregate volume), High-Strength M65–M100 (Table 8/9), SCC slump flow (SF1–SF3, L-Box, V-Funnel), Mass concrete (40/80/150 mm) |
| **IS 456:2000** *(Amend. 1–5)* | Civil & Structural | Plain and Reinforced Concrete — Code of Practice | Cl 5.0 & Table 1 (Water permissible limits: pH >= 6.0, Chlorides, Sulphates), Table 2 (Grades M10–M100), Table 5 (Exposure durability, min cement, max w/c), Table 11.3.1 (Formwork stripping times), Cl 26 (Reinforcement detailing & cover), Section 5 (Limit state design) |
| **IS 1417:2016** | Precious Metals | Gold & Gold Alloys — Fineness and Marking Specification | Table 1 (Purity grades: 24K/999, 22K/916, 18K/750, 14K/585), Cl 4.1.1 (Cadmium limit <= 0.02%, PGM <= 0.05%), Cl 5.0 (Mandatory hallmarking symbols & -2 ppt tolerance) |
| **IS 1239 (Part 1):2004** | Mechanical & Piping | Steel Tubes, Tubulars and Other Wrought Steel Fittings | Cl 6.0 (ERW/HFS manufacturing, Carbon <= 0.20%, Mn <= 1.30%), Tables 3/4/5 (Light/Medium/Heavy classes & color bands), Cl 13.0 (5 MPa / 50 bar hydrostatic pressure test, flattening/bend tests) |
| **IS 2062:2011** | Metallurgical & Steel | Hot Rolled Medium and High Tensile Structural Steel | Tables 1 & 2 (9 Grades: E250 to E650, Qualities A, BR, B0, C), Table 1 (Carbon Equivalent formula & micro-alloying), Cl 12.0 (Charpy V-notch impact toughness >= 27J at 0°C/-20°C, Y-groove crackability) |
| **IS 10500:2012** | Chemical & Water Quality | Drinking Water — Specification (Second Revision) | Table 1 (Organoleptic: pH 6.5–8.5, TDS <= 500 mg/L, Turbidity <= 1 NTU), Table 3 (Heavy metals: Lead <= 0.01 mg/L, Arsenic <= 0.01 mg/L, Mercury <= 0.001 mg/L), Table 6 (Bacteriological: 0 CFU E. coli) |
| **IS 1786:2008** | Structural Reinforcement | High Strength Deformed Steel Bars (TMT Rebars) | Table 3 (Fe 415, Fe 500, Fe 500D ductile seismic grade, Fe 550D, Fe 600, Yield stress, TS/YS ratio, Elongation criteria) |
| **IS 1293:2019** | Electrotechnical | Plugs and Socket-Outlets up to 250V / 16A | Cl 13.1 (Mandatory child safety shutters on live/neutral pins, terminal temperature rise <= 45 K, 750°C glow wire flammability test, QCO mandate) |
| **IS 732:2019** | Electrotechnical | Code of Practice for Electrical Wiring Installations | Cl 5.2 (Voltage drop limits: 3% lighting / 5% power, Continuous earthing per IS 3043, Mandatory 30mA RCD / RCCB shock protection) |
| **IS 15820:2009** | Consumer Protection | Assaying and Hallmarking Centres — General Requirements | Cl 5.1 (3 Mandatory hallmarking marks: BIS logo, Purity/fineness e.g. 22K916, 6-digit laser engraved alphanumeric HUID code) |
| **IS 2189:2008** | Fire & Life Safety | Automatic Fire Detection and Alarm System | Cl 6.2 (Smoke detector coverage 50 m², 7.5 m spacing; Heat detectors 30 m²; Manual Call Points at 1.4 m height; 65–75 dBA sounders) |
| **IS 16046:2018 / IEC 62133** | Electronics & Batteries | Secondary Cells & Batteries Containing Alkaline/Lithium | Cl 8.3 (Thermal abuse test at 130°C, External short-circuit at 55°C, Overcharge test, Forced mechanical indent test, Mandatory MeitY CRS R-Number) |
| **BIS Act 2016 & Schemes** | Conformity Assessment | BIS Certification Schemes, ISI Mark, CRS & MSME Rules | 7-Step Certification Roadmap, Scheme-I (ISI Mark), Scheme-II (CRS), FMCS, BIS Care App, 80% Micro MSME discount, 50% Small enterprise discount |

---

## ⚡ Getting Started

### Prerequisites
* **Python**: `3.10`, `3.11`, or `3.12`
* **Git**
* **Groq API Key** (Free tier available at [console.groq.com](https://console.groq.com)) — *Optional; high-precision offline fallback mode activates automatically if no API key is configured.*

### 1. Clone the Repository
```bash
git clone https://github.com/shivam-1919/Standards-saathi.git
cd Standards-saathi
```

### 2. Set Up a Python Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
python -m venv .venv
.\.venv\Scripts\activate.bat

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note for Linux / Docker / Cloud Deployments**: Ensure `libgomp1` is installed for FAISS (`apt-get install -y libgomp1` or refer to [`packages.txt`](packages.txt)).

### 4. Configure Environment Variables
Copy the example environment file and configure your credentials:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
ADMIN_PASSWORD=admin123
```

---

## 🖥️ Running the Application

### Option A: Modern Web Application (Recommended)
Launches the asynchronous FastAPI backend serving the rich, bilingual single-page frontend with voice assistant, live search, verification tools, and administrative controls:
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser and navigate to: **[http://localhost:8000](http://localhost:8000)**

---

### Option B: Streamlit Analytics Dashboard
Launches the standalone multi-tab Python analytics dashboard with live vector store diagnostics and metrics:
```bash
streamlit run app.py
```
Open your browser and navigate to: **[http://localhost:8501](http://localhost:8501)**

---

## 📡 API Reference

The FastAPI server exposes standardized REST endpoints documented interactively via OpenAPI / Swagger at **`http://localhost:8000/docs`**.

### 1. `POST /api/chat`
Executes FAISS vector similarity search and Groq LLM response generation with citation assembly.

* **Request Body**:
  ```json
  {
    "query": "What are the permissible limits for TDS, pH, and Lead in drinking water under IS 10500?",
    "top_k": 3,
    "temperature": 0.2,
    "language": "English",
    "chat_history": [
      {"role": "user", "content": "Hello Saathi"},
      {"role": "assistant", "content": "Namaste! How can I assist you with Indian Standards today?"}
    ]
  }
  ```

* **Response Body**:
  ```json
  {
    "answer": "**Direct Answer**\nUnder IS 10500:2012, the acceptable pH limit is 6.5–8.5 (no relaxation), the acceptable TDS limit is 500 mg/L (max 2000 mg/L in absence of alternate source), and the maximum limit for Lead (Pb) is 0.01 mg/L.\n\n**Sources:**\n- 📄 IS_10500_2012.pdf, Page 2, Section 4.1 | 🔗 Purchase: https://www.standardsbis.in\n- 📄 IS_10500_2012.pdf, Page 3, Section 4.3 | 🔗 Purchase: https://www.standardsbis.in",
    "raw_answer": "...",
    "citations": [
      {
        "standard_number": "IS 10500:2012",
        "title": "Drinking Water — Specification",
        "clause_id": "Table 1 / Clause 4.1",
        "clause_title": "Organoleptic and Physical Parameters",
        "similarity_score": 0.895,
        "page_number": 2,
        "section_number": "Section 4.1",
        "filename": "IS_10500_2012.pdf",
        "purchase_url": "https://www.standardsbis.in/gemini/detail/IS_10500_2012",
        "full_content": "Table 1 defines essential physical parameters..."
      }
    ],
    "sources_text": "📄 IS_10500_2012.pdf, Page 2, Section 4.1 | 🔗 Purchase: https://www.standardsbis.in",
    "related_standards": ["IS 3025:2014", "IS 13428:2005", "IS 14543:2004"],
    "is_fallback": false,
    "model": "groq/compound-mini (Groq)"
  }
  ```

---

### 2. `GET /api/standards`
Returns the complete list of Indian Standards, metadata, and clauses indexed in the system.

---

### 3. `POST /api/standards`
Dynamically indexes a new custom Indian Standard and rebuilds the FAISS vector index in real time.

* **Request Body**:
  ```json
  {
    "standard_number": "IS 1786:2008",
    "title": "High Strength Deformed Steel Bars for Concrete Reinforcement",
    "category": "Civil & Structural Engineering",
    "status": "Active Mandatory QCO",
    "summary": "Specifies Fe 415, Fe 500, Fe 500D rebar requirements.",
    "clauses": [
      {
        "clause_id": "Clause 4.1",
        "clause_title": "Mechanical Properties",
        "content": "Fe 500D requires minimum 0.2% proof stress of 500 N/mm² and min elongation of 16.0%.",
        "keywords": ["Fe 500D", "rebar", "seismic"]
      }
    ]
  }
  ```

* **Response Body**:
  ```json
  {
    "status": "success",
    "message": "Standard IS 1786:2008 ingested successfully.",
    "total_chunks_indexed": 48
  }
  ```

---

### 4. `POST /api/admin/auth`
Validates administrator passwords to unlock configuration and custom standard ingestion tools.

* **Request Body**: `{"password": "admin123"}`
* **Response Body**: `{"status": "success", "message": "Authenticated"}`

---

### 5. `POST /api/config`
Dynamically updates the active Groq API key at runtime.

* **Request Body**: `{"groq_api_key": "gsk_..."}`
* **Response Body**: `{"status": "success", "message": "API key updated."}`

---

## 💬 Example Queries to Try

| Domain | English Query | Hindi Query (हिंदी) |
| :--- | :--- | :--- |
| **Water Quality** | "What are the acceptable limits for TDS, pH, and Lead under IS 10500?" | "IS 10500 के अनुसार पीने के पानी में TDS, pH और लेड (Lead) की अधिकतम सीमा क्या है?" |
| **Concrete & Structures** | "What is the target mean compressive strength formula in IS 10262:2019 for M40 concrete?" | "IS 10262 के तहत M40 कंक्रीट के लिए Target Mean Strength का फॉर्मूला क्या है?" |
| **Structural Steel** | "What are the impact toughness requirements for Grade E250 Quality C steel under IS 2062?" | "IS 2062 में स्ट्रक्चरल स्टील के लिए Charpy Impact Test और -20°C पर क्या नियम हैं?" |
| **Electrical Safety** | "What are the mandatory child safety shutter and temperature rise rules in IS 1293:2019?" | "IS 1293:2019 के तहत 6A और 16A सॉकेट में चाइल्ड सेफ्टी शटर के क्या नियम हैं?" |
| **Gold Jewellery** | "What are the 3 mandatory marks on hallmarked gold jewellery and how to verify HUID?" | "सोने के गहनों पर 3 अनिवार्य हॉलमार्क और 6-अंकीय HUID कोड को कैसे चेक करें?" |
| **BIS Certification** | "What is the step-by-step process and cost for getting a BIS ISI mark license?" | "BIS ISI मार्क लाइसेंस लेने की 7-चरणीय प्रक्रिया और MSME के लिए फीस में क्या छूट है?" |
| **MSME Benefits** | "How does a micro enterprise claim an 80% fee concession on BIS certification?" | "सूक्ष्म उद्यमों (Micro MSMEs) को BIS आवेदन और लाइसेंस शुल्क में 80% छूट कैसे मिलती है?" |

---

## 📂 Project Structure

```
Standards-saathi/
├── static/
│   ├── index.html            # Single-Page Web UI (Material 3, Tailwind CSS, STT/TTS, Verification)
│   └── logo.svg              # Standards Saathi Official SVG Emblem
├── app.py                    # Streamlit Multi-Tab Analytics Dashboard Application
├── server.py                 # FastAPI Asynchronous REST API & Static File Server
├── rag_engine.py             # Core RAG Pipeline (SentenceTransformers, FAISS IndexFlatIP, Groq LLM)
├── sample_data.py            # Pre-loaded Knowledge Base (Curated IS Codes, Clauses, Citations & Metadata)
├── requirements.txt          # Python Dependencies (FastAPI, Streamlit, FAISS, Sentence-Transformers, Groq)
├── packages.txt              # System Level Packages (libgomp1 for FAISS on Linux/Cloud)
├── .env.example              # Environment Configuration Template
├── .gitignore                # Git Exclusions (.env, .venv, __pycache__)
└── README.md                 # Project Documentation
```

---

## 🔒 Security & Privacy

* **No Hardcoded Keys**: All API keys and administrator passwords reside in environment variables (`.env`) or Streamlit secrets (`st.secrets`).
* **Input Sanitization**: User inputs are sanitized before vector embedding and LLM prompt assembly.
* **Strict Verification**: License and HUID verifications follow strict regex formats matching official BIS and Bureau of Indian Standards schemas.

---

## 🛡️ License & Disclaimer

* **License**: This project is distributed under the [MIT License](LICENSE).
* **Regulatory Disclaimer**: *Standards Saathi (मानक साथी) is an independent AI technical assistant designed to facilitate reference, education, and fast navigation of Indian Standards (IS Codes) and BIS guidelines. For official regulatory enforcement, legal tenders, and statutory certification, always refer directly to the gazette notifications published by the [Bureau of Indian Standards (BIS)](https://www.bis.gov.in) and [e-BIS Manakonline](https://www.manakonline.in).*

---

<div align="center">
  <sub>Built with pride for Indian Standards, Quality Assurance, and Atmanirbhar Bharat 🇮🇳</sub>
</div>
