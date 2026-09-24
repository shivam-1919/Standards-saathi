<div align="center">

# 🇮🇳 Standards Saathi (मानक साथी)
### *Enterprise AI Technical Advisor, Verification Hub & Prompt-Injection Guardrail for Indian Standards (IS Codes) & BIS Regulations*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-0467DF?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-384d%20MiniLM-FFA000?style=for-the-badge)](https://www.sbert.net)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash%20%7C%20Pro-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%20%7C%203.1-f55036?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>5 Indic Languages (EN, HI, TA, BN, MR) • Saral Voice Assistant (Illiterate/Rural Mode) • Clause-Level Citations • ISI / HUID / CRS Verification • 5 Proactive Tools • MSME 80% Subsidy Hub • Multi-Layer Prompt Injection Defense • Admin Security Audit Logs</b>
</p>

[Key Features](#-key-features) • [Tech Stack](#-tech-stack) • [System Architecture](#-system-architecture) • [Ingested Indian Standards](#-ingested-indian-standards) • [Getting Started](#-getting-started) • [Running the Application](#-running-the-application) • [API Reference](#-api-reference) • [Prompt Injection Defense](#-prompt-injection--security-guardrails) • [Example Queries](#-example-queries-to-try) • [Project Structure](#-project-structure)

---

</div>

## 📌 Overview

**Standards Saathi (मानक साथी)** is an enterprise-grade, accessible Retrieval-Augmented Generation (RAG) platform engineered for engineers, architects, MSME entrepreneurs, rural manufacturers, quality control (QC) managers, and Indian citizens. It provides clause-level, citation-backed technical guidance on **Bureau of Indian Standards (BIS)** codes, mandatory **Quality Control Orders (QCOs)**, **ISI Certification Schemes**, **Gold Hallmarking (HUID)**, and statutory **MSME concessions (80% fee subsidies)**.

Standards Saathi supports **5 Indian Languages** (English, Hindi, Tamil, Bengali, Marathi) alongside **Saral Voice Mode (सरल साथी)** for low-literacy users, interactive **5 Proactive Engineering Tools**, a **Multi-Layer Prompt Injection Defense Guardrail**, and an **Admin Security Audit Portal**.

---

## 🚀 Key Features

### 1. 🌐 5 Indian Languages & Native Localization
* **Dynamic 5-Language Switching**: Seamless real-time interface and response translation across:
  - 🇬🇧 **English**
  - 🇮🇳 **Hindi (हिंदी)**
  - 🇮🇳 **Tamil (தமிழ்)**
  - 🇮🇳 **Bengali (বাংলা)**
  - 🇮🇳 **Marathi (मराठी)**
* **Cross-Lingual RAG Retrieval**: Indic domain queries automatically expand into technical English terms for dense FAISS vector matching, followed by structured, localized synthesis in the user's native language.

### 2. 🎙️ Accessible Voice Assistant & Saral Saathi (सरल साथी)
* **Zero Barrier Voice Interaction**: Bidirectional voice assistant using browser **Speech-to-Text (STT)** (`webkitSpeechRecognition`) and **Text-to-Speech (TTS)** (`SpeechSynthesis`) with dynamic locale switching (`en-IN`, `hi-IN`, `ta-IN`, `bn-IN`, `mr-IN`).
* **Play / Stop Audio Controls**: Users can pause or stop speech output instantly at any point.
* **Saral Voice Mode (सरल साथी)**: Specialized conversational mode designed for rural artisans, micro-manufacturers, and low-literacy users, explaining complex compliance rules in clear, spoken-friendly everyday terms.

### 3. 🛡️ Multi-Layer Prompt Injection & Jailbreak Defense
* **Multilingual Direct Override Interception**: Detects and blocks instruction overrides, DAN modes, role-play bypasses, and rule disregard across English, Hindi, Tamil, Bengali, and Marathi.
* **System Prompt & API Key Exfiltration Shield**: Prevents leaking of initial prompts, developer directives, or API credentials (`GEMINI_API_KEY`, `GROQ_API_KEY`).
* **Control Token & Delimiter Sanitization**: Filters adversarial delimiters (`<|system|>`, `[INST]`, ````system````, etc.).
* **Indirect Prompt Injection Sanitization**: Cleans zero-width unicode characters (`\u200B`–`\u200D`, `\uFEFF`) and hidden payloads inside user-submitted tender texts or clause snippets.
* **Statutory Fraud Guardrail**: Blocks requests attempting to forge fake ISI marks, fake licenses, or circumvent mandatory QCOs.
* **Zero False Positives**: Verified against authentic technical standard inquiries.

### 4. 🛠️ 5 Proactive BIS Engineering Tools
1. **📋 Compliance Checklist Generator** (`/api/tools/checklist`): Generates step-by-step checklists for any product or IS code covering QCO mandates, in-house lab equipment, required documents, and 80% MSME fee subsidies.
2. **📑 Tender & Specification Analyzer** (`/api/tools/tender-analyzer`): Ingests tender text or procurement scopes, sanitizes indirect inputs, identifies cited IS codes, flags missing mandatory standards, and outputs compliance recommendations.
3. **🔍 Technical Clause Explainer** (`/api/tools/explain-clause`): Translates dense standard clauses into plain language with 1–2 practical real-world application examples.
4. **💼 MSME 80% Subsidy Hub & Live Calculator**: Calculates net fee savings (80% on application & license fees, 50% on lab testing) based on enterprise Udyam classification.
5. **🎯 4-Step Onboarding Roadmap** (`/api/tools/onboarding-roadmap`): Interactive questionnaire evaluating product type, materials, market scale, and current certifications to generate a customized BIS roadmap.

### 5. 🔍 BIS License, Hallmark & CRS Verification Hub
* **ISI License (CM/L)**: Verifies 7-to-8 digit manufacturer license numbers against BIS standard schemas.
* **Gold HUID Code**: Validates 6-digit alphanumeric laser-engraved hallmark identifiers.
* **Electronics CRS (R-Number)**: Checks 8-digit Compulsory Registration Scheme numbers for lithium batteries, electronics, adapters, and smart devices.

### 6. 🔒 Admin Security Audit Log Portal & Key Management
* **Zero User-Facing API Key Exposure**: All sensitive configurations are shielded behind admin password authentication.
* **Real-Time Security Audit Logs**: Live table logging every intercepted injection attempt with timestamp, category, query snippet, and detected language, with refresh and clear controls.
* **Runtime Vector Ingestion**: Administrators can dynamically ingest new custom Indian Standards into the FAISS index with instant re-indexing.

---

## 🛠️ Tech Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **LLM Inference** | **Google Gemini AI & Groq Cloud** | Multi-agent reasoning via Gemini Flash/Pro and Groq LLaMA 3.3/3.1 models |
| **Vector Database** | **FAISS (`faiss-cpu` v1.8+)** | Dense vector search using `IndexFlatIP` with normalized L2 cosine similarity |
| **Semantic Embeddings** | **Sentence Transformers (v3.0+)** | `all-MiniLM-L6-v2` generating 384-dimensional dense semantic vectors |
| **Backend Server** | **FastAPI & Uvicorn** | Asynchronous high-performance REST API backend with Pydantic validation |
| **Primary Web Interface** | **Single-Page App (HTML5/JS/Tailwind)** | Stitch-inspired civic design, Glassmorphism, Indian Tricolor bar, Web Speech API |
| **Analytics Dashboard** | **Streamlit (v1.40+)** | Standalone multi-tab Python dashboard with live telemetry and vector diagnostics |
| **Voice Processing** | **Web Speech API (STT & TTS)** | Universal client-side speech transcription and synthesis with Play/Stop toggle |
| **Security Guardrails** | **Custom Multi-Layer Defense Engine** | Multilingual regex filters, indirect delimiter sanitization, and audit log telemetry |

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
                                  │   • POST /api/tools/*        • POST /api/admin/auth      │
                                  │   • POST /api/admin/config   • POST /api/admin/security  │
                                  └─────────────────────────────┬────────────────────────────┘
                                                                │
                                                                ▼
                                  ┌──────────────────────────────────────────────────────────┐
                                  │             MULTI-LAYER SECURITY & PROMPT INJECTION      │
                                  │                     DEFENSE GUARDRAIL                    │
                                  │   • Direct Overrides (EN, HI, TA, BN, MR)                │
                                  │   • Exfiltration Shield • Delimiter Sanitization         │
                                  └─────────────────────────────┬────────────────────────────┘
                                                                │ Safe Queries Only
                                                                ▼
                                  ┌──────────────────────────────────────────────────────────┐
                                  │                 STANDARDS RAG ENGINE                     │
                                  │                    (`rag_engine.py`)                     │
                                  └──────────────┬────────────────────────────┬──────────────┘
                                                 │                            │
                     ┌───────────────────────────┴──────────┐                 │
                     ▼                                      ▼                 ▼
      ┌─────────────────────────────┐        ┌─────────────────────┐   ┌─────────────────────────────┐
      │    Sentence Transformers    │        │  FAISS Vector Index │   │    Google Gemini / Groq     │
      │     (all-MiniLM-L6-v2)      │───────▶│    (IndexFlatIP)    │   │   (Multilingual Synthesis   │
      │  384-dim Dense Embeddings   │        │ Normalized Vectors  │   │     & Saral Voice Mode)     │
      └─────────────────────────────┘        └──────────┬──────────┘   └──────────────┬──────────────┘
                                                        │                             │
                                                        │ Top-K Chunks + Citations    │ LLM Synthesis
                                                        └──────────────┬──────────────┘
                                                                       │
                                                                       ▼
                                                       ┌───────────────────────────────┐
                                                       │  Synthesized Response Cards   │
                                                       │  • Direct Summary & Citations │
                                                       │  • 5 Indic Language Output    │
                                                       │  • Audio Read-Aloud (TTS)     │
                                                       └───────────────────────────────┘
```

---

## 📦 Ingested Indian Standards

The knowledge base in [`sample_data.py`](sample_data.py) comes pre-loaded with 22+ curated, clause-indexed Indian Standards spanning major engineering, construction, consumer, and safety domains:

| Standard Number | Category | Scope / Key Focus | Key Clauses Covered |
| :--- | :--- | :--- | :--- |
| **IS 2720 (Part 1):1983** | Civil & Geotechnical | Soil sample preparation and testing | Cl 2.0 (Apparatus: Mallet, Pulverizer, Sieves), Cl 3.0 (Drying limit <60°C for organic soils) |
| **IS 10262:2019** | Civil & Structural | Concrete mix proportioning guidelines | Cl 4.2 (Target strength formula $f'_{ck} = f_{ck} + 1.65S$), Table 4 (Water content), SCC slump flow (SF1–SF3) |
| **IS 456:2000** | Civil & Structural | Plain and reinforced concrete code | Cl 5.0 (Water permissible limits: pH >= 6.0), Table 5 (Durability, min cement), Formwork stripping times |
| **IS 1417:2016** | Precious Metals | Gold and gold alloys hallmarking | Table 1 (Purity grades: 24K/999, 22K/916, 18K/750), Cl 4.1.1 (Cadmium <= 0.02%), Mandatory symbols |
| **IS 1239 (Part 1):2004** | Mechanical & Piping | Steel tubes and wrought fittings | Cl 6.0 (ERW/HFS, Carbon <= 0.20%), Cl 13.0 (5 MPa hydrostatic pressure test, bend tests) |
| **IS 2062:2011** | Metallurgical & Steel | Hot rolled medium and high tensile steel | Tables 1 & 2 (Grades E250 to E650, Qualities A, BR, B0, C), Cl 12.0 (Charpy impact >= 27J at 0°C/-20°C) |
| **IS 10500:2012** | Chemical & Water | Drinking water quality specification | Table 1 (pH 6.5–8.5, TDS <= 500 mg/L), Table 3 (Lead <= 0.01 mg/L, Arsenic <= 0.01 mg/L), 0 CFU E. coli |
| **IS 1786:2008** | Structural Reinforcement | High strength deformed steel bars (TMT) | Table 3 (Fe 415, Fe 500, Fe 500D ductile seismic grade, Fe 550D, Yield stress, Elongation criteria) |
| **IS 1293:2019** | Electrotechnical | Plugs and socket-outlets up to 250V / 16A | Cl 13.1 (Mandatory child safety shutters on live/neutral pins, temperature rise <= 45 K) |
| **IS 732:2019** | Electrotechnical | Electrical wiring installations code | Cl 5.2 (Voltage drop limits: 3% lighting / 5% power, Continuous earthing per IS 3043) |
| **IS 15820:2009** | Consumer Protection | Assaying and hallmarking centre rules | Cl 5.1 (3 Mandatory marks: BIS logo, Purity 22K916, 6-digit alphanumeric HUID code) |
| **IS 2189:2008** | Fire & Life Safety | Automatic fire detection and alarm system | Cl 6.2 (Smoke detector 50 m², Heat detector 30 m², Manual Call Points at 1.4 m height) |
| **IS 16046:2018** | Electronics & Batteries | Secondary lithium cells and batteries | Cl 8.3 (Thermal abuse at 130°C, External short-circuit at 55°C, MeitY CRS R-Number mandate) |
| **IS 3589:2001** | Mechanical & Piping | Steel pipes for water & sewage (168–2540mm) | Cl 4 & 5 (Tensile strength, elongation, mandatory QCO for public water/sewage pipelines) |
| **IS 14543:2004** | Food & Water Safety | Packaged drinking water specification | Cl 3 & 4 (Mandatory ISI certification, microbiological limits, TDS <= 500 mg/L) |
| **IS 13630:2019** | Civil & Ceramic Tiles | Ceramic tiles sampling and test methods | Water absorption, modulus of rupture, chemical resistance, abrasion limits |
| **BIS Act 2016 & Schemes** | Conformity Assessment | BIS Schemes, ISI Mark, CRS & MSME Rules | 7-Step Roadmap, Scheme-I (ISI), Scheme-II (CRS), 80% Micro MSME subsidy, 50% Small MSME subsidy |

---

## ⚡ Getting Started

### Prerequisites
* **Python**: `3.10`, `3.11`, `3.12`, or `3.14`
* **Git**
* **Google Gemini API Key** or **Groq API Key** *(Optional; robust offline retrieval mode activates automatically if no API key is set)*

### 1. Clone the Repository
```bash
git clone https://github.com/shivam-1919/Standards-saathi.git
cd Standards-saathi
```

### 2. Set Up Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```
Edit `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=gsk_your_groq_api_key_here
ADMIN_PASSWORD=admin123
```

---

## 🖥️ Running the Application

### Option A: Modern Web Application (Recommended)
Launches the asynchronous FastAPI backend serving the rich, multilingual Stitch-inspired web UI:
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

### Option B: Streamlit Dashboard
Launches the standalone multi-tab Python analytics dashboard:
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

### Option C: Run Automated Test Suite
Executes the comprehensive 5-module validation test suite:
```bash
python test_features.py
```

---

## 📡 API Reference

### 1. `POST /api/chat`
RAG semantic search and multilingual synthesis.
```json
{
  "query": "What are the permissible limits for Lead in drinking water under IS 10500?",
  "language": "English",
  "top_k": 3,
  "msme_mode": false,
  "saral_mode": false
}
```

### 2. `POST /api/tools/checklist`
Generates a complete compliance checklist for any product or standard.
```json
{
  "product": "Packaged Drinking Water",
  "language": "Hindi",
  "is_msme": true
}
```

### 3. `POST /api/tools/tender-analyzer`
Analyzes tender clauses and procurement scopes for IS code alignment.
```json
{
  "tender_text": "Supply of ERW carbon steel tubes with hydrostatic testing at 5 MPa.",
  "language": "English"
}
```

### 4. `POST /api/tools/explain-clause`
Translates technical standard clauses into plain language with real-world examples.
```json
{
  "clause_text": "Clause 13.1: Every tube shall be subjected to hydrostatic test at 5.0 MPa for 3 seconds.",
  "language": "Hindi"
}
```

### 5. `POST /api/tools/onboarding-roadmap`
Evaluates a 4-question onboarding wizard to generate a tailored BIS certification roadmap.
```json
{
  "answers": {
    "product_type": "LED Bulbs",
    "material": "Drivers and plastic casing",
    "market": "Micro Enterprise Domestic",
    "current_certifications": "No prior BIS license"
  },
  "language": "English"
}
```

### 6. `POST /api/admin/security-logs`
Returns the protected audit trail of blocked prompt injection attempts.
```json
{
  "password": "admin123"
}
```

### 7. `POST /api/admin/config`
Updates API keys and system settings securely.
```json
{
  "admin_password": "admin123",
  "gemini_api_key": "AIza...",
  "groq_api_key": "gsk_..."
}
```

---

## 🛡️ Prompt Injection & Security Guardrails

Standards Saathi implements a defense-in-depth security architecture:

1. **Direct Instruction Overrides**: Prevents `Ignore all previous instructions`, `DAN Mode`, `Developer Mode`, and their Indic equivalents in Hindi, Tamil, Bengali, and Marathi.
2. **Exfiltration Defense**: Blocks queries seeking system prompts, base context, or API keys (`reveal your initial prompt`, `सिस्टम प्रॉम्प्ट दिखाओ`).
3. **Delimiter Sanitization**: Strips adversarial tokens (`<|system|>`, `[INST]`, ````system````).
4. **Indirect Injection Cleaning**: Purges zero-width unicode characters (`\u200B`–`\u200D`, `\uFEFF`) from external tender text and user documents.
5. **Admin Audit Logging**: Automatically records blocked attacks into an administrative audit log for security monitoring.

---

## 💬 Example Queries to Try

| Domain | English Query | Hindi Query (हिंदी) | Indic Multilingual (Tamil / Bengali / Marathi) |
| :--- | :--- | :--- | :--- |
| **Water Quality** | "What are the acceptable limits for Lead and TDS under IS 10500?" | "IS 10500 के अनुसार पीने के पानी में TDS और लेड की अधिकतम सीमा क्या है?" | "குடிநீரில் அனுமதிக்கப்பட்ட TDS மற்றும் ஈயத்தின் அளவு என்ன?" (Tamil) |
| **Steel Pipes** | "What standard applies to steel pipes for water and sewage?" | "पानी और सीवेज पाइप के लिए कौन सा भारतीय मानक लागू है?" | "ইস্পাত পাইপের জন্য প্রযোজ্য IS মানক কোনটি?" (Bengali) |
| **Structural Steel** | "What are the impact toughness requirements in IS 2062 for E250 Grade C?" | "IS 2062 में स्ट्रक्चरल स्टील के लिए -20°C पर Charpy Impact Test नियम क्या हैं?" | "IS 2062 नुसार स्ट्रक्चरल स्टीलचे इम्पॅक्ट नियम काय आहेत?" (Marathi) |
| **Gold Jewellery** | "What are the 3 mandatory marks on hallmarked gold jewellery?" | "सोने के गहनों पर 3 अनिवार्य हॉलमार्क और 6-अंकीय HUID कोड नियम क्या हैं?" | "தங்க நகைகளில் உள்ள 3 கட்டாய முத்திரைகள் எவை?" (Tamil) |
| **MSME Subsidies** | "How does a micro enterprise claim an 80% fee concession on BIS certification?" | "सूक्ष्म उद्यमों (Micro MSMEs) को BIS आवेदन और लाइसेंस शुल्क में 80% छूट कैसे मिलती है?" | "सूक्ष्म उद्योगांना BIS प्रमाणपत्रात ८०% सवलत कशी मिळते?" (Marathi) |

---

## 📂 Project Structure

```
Standards-saathi/
├── static/
│   ├── index.html            # Single-Page Web App (Stitch UI, WebSpeech STT/TTS, Proactive Tools, Security Logs)
│   └── logo.svg              # Standards Saathi Official SVG Emblem
├── app.py                    # Standalone Streamlit Multilingual Analytics Dashboard Application
├── server.py                 # FastAPI Asynchronous REST API Backend & Static File Server
├── rag_engine.py             # Core RAG Pipeline (FAISS, SentenceTransformers, Gemini/Groq, Prompt Injection Defense)
├── sample_data.py            # Pre-loaded Knowledge Base (22+ Curated Indian Standards, Clauses & QCO Metadata)
├── test_features.py          # End-to-End Automated Verification Test Suite (All 5 Modules)
├── requirements.txt          # Python Dependencies (FastAPI, Streamlit, FAISS, Sentence-Transformers, Groq)
├── packages.txt              # Linux / Cloud System Packages (libgomp1)
├── .env.example              # Environment Configuration Template
├── .gitignore                # Git Exclusions (.env, .venv, __pycache__)
└── README.md                 # Complete Project Documentation
```

---

## 🛡️ License & Disclaimer

* **License**: Distributed under the [MIT License](LICENSE).
* **Regulatory Disclaimer**: *Standards Saathi (मानक साथी) is an AI technical advisory tool designed to facilitate rapid reference, navigation, and understanding of Indian Standards (IS Codes) and BIS guidelines. It does not issue legal or certification grants. For official regulatory enforcement and statutory license applications, always refer directly to the gazette notifications published by the [Bureau of Indian Standards (BIS)](https://www.bis.gov.in) and [e-BIS Manakonline](https://www.manakonline.in).*

---

<div align="center">
  <sub>Built with pride for Indian Standards, Quality Assurance, and Atmanirbhar Bharat 🇮🇳</sub>
</div>
