<div align="center">

# 🇮🇳 Standards Saathi (मानक साथी)
### *Enterprise AI Technical Advisor, Multilingual Voice Assistant & Prompt-Injection Guardrail for Indian Standards (IS Codes) & BIS Regulations*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash%20%7C%20Pro-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%20%7C%203.1-f55036?style=for-the-badge)](https://groq.com)
[![Bhashini AI](https://img.shields.io/badge/Bhashini%20AI-NLTM%20%7C%20MeitY-FF9933?style=for-the-badge)](https://bhashini.gov.in)
[![Memory Optimized](https://img.shields.io/badge/Memory%20Footprint-~45MB%20Ultra--Light-138808?style=for-the-badge)](#-ultra-lightweight-semantic-engine--cloud-optimizations)
[![Uptime Monitoring](https://img.shields.io/badge/Monitoring-UptimeRobot%20Ready-00B0FF?style=for-the-badge)](#-health-monitoring--cloud-deployment)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>5 Indic Languages (EN, HI, TA, BN, MR) • Bhashini IndicTTS & IndicTrans2 • Saral Voice Assistant (Rural/Low-Literacy Mode) • Clause-Level Citations • ISI / HUID / CRS Verification • 5 Proactive Tools • MSME 80% Subsidy Hub • Multi-Layer Prompt Injection Defense • Admin Security Audit Portal</b>
</p>

[Key Features](#-key-features) • [Bhashini & Voice AI](#-bhashini-nltm--voice-ai-architecture) • [Tech Stack](#-tech-stack) • [System Architecture](#-system-architecture) • [Ingested Indian Standards](#-ingested-indian-standards) • [Getting Started](#-getting-started) • [Running the Application](#-running-the-application) • [API Reference](#-api-reference) • [Prompt Injection Defense](#-prompt-injection--security-guardrails) • [Example Queries](#-example-queries-to-try) • [Project Structure](#-project-structure)

---

</div>

## 📌 Overview

**Standards Saathi (मानक साथी)** is an enterprise-grade, highly accessible Retrieval-Augmented Generation (RAG) platform engineered for civil/mechanical/electrical engineers, architects, MSME entrepreneurs, rural manufacturers, quality control (QC) managers, and Indian citizens. It delivers clause-level, citation-backed technical guidance on **Bureau of Indian Standards (BIS)** codes, mandatory **Quality Control Orders (QCOs)**, **ISI Certification Schemes**, **Gold Hallmarking (HUID)**, and statutory **MSME concessions (80% fee subsidies)**.

Standards Saathi supports **5 Indian Languages** (English, Hindi, Tamil, Bengali, Marathi), integrates official **Bhashini AI models (NLTM / MeitY)** alongside **Saral Voice Mode (सरल साथी)** for low-literacy users, interactive **5 Proactive Engineering Tools**, a **Multi-Layer Prompt Injection Defense Guardrail**, and an **Admin Security Audit Portal**.

---

## 🚀 Key Features

### 1. 🌐 5 Indian Languages & Native Localization
* **Full Multilingual Interface & Generation**: Native prompt understanding, translation, and structured synthesis across:
  - 🇬🇧 **English**
  - 🇮🇳 **Hindi (हिंदी)**
  - 🇮🇳 **Tamil (தமிழ்)**
  - 🇮🇳 **Bengali (বাংলা)**
  - 🇮🇳 **Marathi (मराठी)**
* **Cross-Lingual RAG Retrieval**: Indic domain queries automatically expand into technical English terms for high-recall vector matching, followed by structured, localized synthesis in the user's selected language.
* **Auto Language Detection & Root-Stem Matching**: Automatically recognizes user intent and language script, preserving consistency across conversational turns.

### 2. 🎙️ Accessible Voice Assistant & Saral Saathi (सरल साथी)
* **Bhashini AI Integration (NLTM / MeitY)**: Connects to India's National Language Translation Mission models (`IndicTTS` & `IndicTrans2`) for natural, human-sounding Indic speech synthesis and neural translation.
* **Dual Voice Pipeline**: Combines server-side high-fidelity Bhashini TTS (`/api/tts`) with universal browser-native **Web Speech API** (`webkitSpeechRecognition` & `SpeechSynthesis`) for zero-barrier voice accessibility across desktop and mobile browsers.
* **Responsive Voice Controls**: Dedicated **Play / Stop** audio controls on every response card, with automatic audio silencing upon submitting a new query.
* **Saral Voice Mode (सरल साथी)**: Conversational mode tailored for rural artisans, micro-manufacturers, and low-literacy users, explaining complex compliance rules in spoken-friendly everyday terms without dense jargon.

### 3. ⚡ Ultra-Lightweight Semantic Engine & Cloud Optimizations
* **~45MB Memory Footprint**: Optimized vector search engine designed specifically to thrive within free-tier cloud environments (e.g., Render 512MB RAM constraints) without Out-Of-Memory crashes.
* **10-Second Render Cloud Builds**: Streamlined dependencies (`requirements.txt`) ensure ultra-fast deployment cycles.
* **Collapsible Source Citations**: Interactive source cards with clause-level references, confidence meters, and highlighted clickable links.

### 4. 🛡️ Multi-Layer Prompt Injection & Jailbreak Defense
* **Multilingual Direct Override Interception**: Detects and blocks instruction overrides, DAN modes, role-play bypasses, and rule disregard across English, Hindi, Tamil, Bengali, and Marathi.
* **System Prompt & API Key Exfiltration Shield**: Prevents leaking of developer prompts, internal system directives, or API credentials (`GEMINI_API_KEY`, `GROQ_API_KEY`, `BHASHINI_*`).
* **Control Token & Delimiter Sanitization**: Filters adversarial delimiters (`<|system|>`, `[INST]`, ````system````, etc.).
* **Indirect Prompt Injection Sanitization**: Cleans zero-width unicode characters (`\u200B`–`\u200D`, `\uFEFF`) and hidden payloads inside user-submitted tender texts or clause snippets.
* **Statutory Fraud Guardrail**: Blocks requests attempting to forge fake ISI marks, fake licenses, or circumvent mandatory QCOs.
* **Zero False Positives**: Verified against authentic technical standard inquiries.

### 5. 🛠️ 5 Proactive BIS Engineering Tools
1. **📋 Compliance Checklist Generator** (`/api/tools/checklist`): Generates step-by-step checklists for any product or IS code covering QCO mandates, in-house lab equipment, required documents, and 80% MSME fee subsidies.
2. **📑 Tender & Specification Analyzer** (`/api/tools/tender-analyzer`): Ingests tender text or procurement scopes, sanitizes indirect inputs, identifies cited IS codes, flags missing mandatory standards, and outputs compliance recommendations.
3. **🔍 Technical Clause Explainer** (`/api/tools/explain-clause`): Translates dense standard clauses into plain language with 1–2 practical real-world application examples.
4. **💼 MSME 80% Subsidy Hub & Live Calculator**: Calculates net fee savings (80% on application & license fees, 50% on lab testing) based on enterprise Udyam classification.
5. **🎯 4-Step Onboarding Roadmap** (`/api/tools/onboarding-roadmap`): Interactive questionnaire evaluating product type, materials, market scale, and current certifications to generate a customized BIS roadmap.

### 6. 🔍 BIS License, Hallmark & CRS Verification Hub
* **ISI License (CM/L)**: Verifies 7-to-8 digit manufacturer license numbers against BIS standard schemas.
* **Gold HUID Code**: Validates 6-digit alphanumeric laser-engraved hallmark identifiers.
* **Electronics CRS (R-Number)**: Checks 8-digit Compulsory Registration Scheme numbers for lithium batteries, electronics, adapters, and smart devices.

### 7. 🔒 Admin Security Audit Log Portal & Key Management
* **Zero User-Facing API Key Exposure**: All sensitive configurations are shielded behind admin password authentication.
* **Real-Time Security Audit Logs**: Live table logging every intercepted injection attempt with timestamp, category, query snippet, and detected language, with refresh and clear controls.
* **Runtime Vector Ingestion**: Administrators can dynamically ingest new custom Indian Standards into the index with instant re-indexing.

---

## 🎙️ Bhashini (NLTM) & Voice AI Architecture

Standards Saathi implements a dual-layer speech and translation pipeline designed for universal accessibility across India:

```
                               ┌────────────────────────────────────────────────────────┐
                               │                    USER VOICE INPUT                    │
                               │           (Microphone / Speech Recognition)            │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                                                           ▼
                               ┌────────────────────────────────────────────────────────┐
                               │             BROWSER WEB SPEECH API (STT)               │
                               │       en-IN  |  hi-IN  |  ta-IN  |  bn-IN  |  mr-IN    │
                               └───────────────────────────┬────────────────────────────┘
                                                           │ Transcribed Text
                                                           ▼
                               ┌────────────────────────────────────────────────────────┐
                               │                 STANDARDS SAATHI RAG                   │
                               │          Semantic Retrieval & LLM Synthesis            │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                                            ┌──────────────┴──────────────┐
                                            ▼                             ▼
                             ┌─────────────────────────────┐┌───────────────────────────┐
                             │    BHASHINI AI (MeitY)      ││   BROWSER WEB SPEECH      │
                             │ • IndicTTS (Neural Voice)   ││   • Client-side TTS       │
                             │ • IndicTrans2 (Translation) ││   • Instant Fallback      │
                             └──────────────┬──────────────┘└─────────────┬─────────────┘
                                            │ Raw Audio                   │ SpeechSynthesis
                                            ▼                             ▼
                             ┌──────────────────────────────────────────────────────────┐
                             │               RESPONSIVE AUDIO CONTROLS                  │
                             │  • Play / Stop Voice Toggle • Auto-Silence on New Query  │
                             └──────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **LLM Inference** | **Google Gemini AI & Groq Cloud** | Multi-agent reasoning via Gemini 2.5 Flash/Pro and Groq LLaMA 3.3/3.1 models |
| **National AI Translation** | **Bhashini (NLTM / MeitY)** | IndicTrans2 (Machine Translation) & IndicTTS (Speech Synthesis) across Indian languages |
| **Vector Engine** | **Lightweight Semantic Vector Engine** | Cosine similarity & dense indexing optimized to ~45MB memory footprint |
| **Backend Server** | **FastAPI & Uvicorn** | Asynchronous high-performance REST API backend with Pydantic validation |
| **Primary Web Interface** | **Single-Page App (HTML5/JS/Tailwind)** | Stitch-inspired civic design, Glassmorphism, 24-spoke Indian Ashoka Chakra SVG, Web Speech API |
| **Analytics Dashboard** | **Streamlit** | Standalone multi-tab Python dashboard with live telemetry and vector diagnostics |
| **Voice Processing** | **Bhashini IndicTTS + Web Speech API** | Universal server + client speech transcription and synthesis with Play/Stop toggle |
| **Security Guardrails** | **Custom Multi-Layer Defense Engine** | Multilingual regex filters, indirect delimiter sanitization, and audit log telemetry |
| **Uptime & Health** | **UptimeRobot & Render Endpoints** | Dedicated `/health`, `/healthz`, and `/api/health` monitoring endpoints |

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
                                  │   • POST /api/chat           • GET  /health, /healthz    │
                                  │   • POST /api/tts            • POST /api/translate       │
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
                                  │   • Indirect Injection Sanitization • Fraud Guardrail    │
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
      │  Semantic Vector Engine     │        │ Ingested IS Dataset │   │ Google Gemini / Groq Cloud  │
      │  (~45MB Memory Footprint)   │───────▶│ (22+ Standards,     │   │ (Multilingual Synthesis     │
      │  Dense Semantic Similarity  │        │  Clauses, & QCOs)   │   │  & Saral Voice Mode)        │
      └─────────────────────────────┘        └──────────┬──────────┘   └──────────────┬──────────────┘
                                                        │                             │
                                                        │ Top-K Chunks + Citations    │ LLM Synthesis
                                                        └──────────────┬──────────────┘
                                                                       │
                                                                       ▼
                                                       ┌───────────────────────────────┐
                                                       │  Synthesized Response Cards   │
                                                       │  • Collapsible Source Badges  │
                                                       │  • 5 Indic Language Output    │
                                                       │  • Bhashini / WebSpeech Voice │
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
* **Google Gemini API Key** or **Groq API Key** *(Optional; offline semantic retrieval mode activates automatically if no API key is configured)*
* **Bhashini API Credentials** *(Optional; browser Web Speech API activates automatically as fallback)*

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
BHASHINI_USER_ID=your_bhashini_user_id
BHASHINI_API_KEY=your_bhashini_api_key
BHASHINI_INFERENCE_KEY=your_bhashini_inference_key
ADMIN_PASSWORD=admin123
PORT=8000
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

### Option C: Run Automated Test Suites
Executes the comprehensive validation test suite and Bhashini AI checks:
```bash
# Test full feature suite (RAG, 5 Languages, 5 Tools, Security)
python test_features.py

# Test Bhashini translation & TTS pipeline
python test_bhashini.py
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

### 2. `POST /api/tts`
Synthesizes high-fidelity Indian speech audio using Bhashini IndicTTS.
```json
{
  "text": "भारतीय मानक ब्यूरो उत्पाद की गुणवत्ता सुनिश्चित करता है।",
  "language": "hi",
  "gender": "female"
}
```

### 3. `POST /api/translate`
Translates text across Indian languages using Bhashini IndicTrans2.
```json
{
  "text": "Bureau of Indian Standards ensures product quality and consumer safety.",
  "source_language": "en",
  "target_language": "ta"
}
```

### 4. `POST /api/tools/checklist`
Generates a complete compliance checklist for any product or standard.
```json
{
  "product": "Packaged Drinking Water",
  "language": "Hindi",
  "is_msme": true
}
```

### 5. `POST /api/tools/tender-analyzer`
Analyzes tender clauses and procurement scopes for IS code alignment.
```json
{
  "tender_text": "Supply of ERW carbon steel tubes with hydrostatic testing at 5 MPa.",
  "language": "English"
}
```

### 6. `POST /api/tools/explain-clause`
Translates technical standard clauses into plain language with real-world examples.
```json
{
  "clause_text": "Clause 13.1: Every tube shall be subjected to hydrostatic test at 5.0 MPa for 3 seconds.",
  "language": "Hindi"
}
```

### 7. `POST /api/tools/onboarding-roadmap`
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

### 8. `GET /health` & `GET /healthz`
Lightweight monitoring endpoint for UptimeRobot, Render, and cloud infrastructure.
```json
{
  "status": "healthy",
  "service": "Standards Saathi AI",
  "version": "2.0.0",
  "uptime": "active"
}
```

### 9. `POST /api/admin/security-logs`
Returns the protected audit trail of blocked prompt injection attempts.
```json
{
  "password": "admin123"
}
```

### 10. `POST /api/admin/config`
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
4. **Indirect Injection Cleaning**: Purges zero-width unicode characters (`\u200B`–`\u200D`, `\uFEFF`) and adversarial scripts from external tender text and user documents.
5. **Statutory Fraud Guardrail**: Identifies and blocks fraudulent attempts to generate counterfeit ISI marks, fake HUID codes, or bypass mandatory QCOs.
6. **Admin Audit Logging**: Automatically records blocked attacks into an administrative audit log with timestamps, categories, and input snippets.

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
│   ├── index.html            # Single-Page Web App (Stitch UI, Bhashini & WebSpeech Voice, Proactive Tools, Security Logs)
│   └── logo.svg              # Standards Saathi Official SVG Emblem with 24-Spoke Ashoka Chakra
├── app.py                    # Standalone Streamlit Multilingual Analytics Dashboard Application
├── bhashini_client.py        # Bhashini Udyat/ULCA Client (IndicTrans2 NMT & IndicTTS Speech Models)
├── server.py                 # FastAPI Asynchronous REST API Backend & Uptime Monitoring Endpoints
├── rag_engine.py             # Core RAG Pipeline (Lightweight Semantic Vector Engine, Gemini/Groq, Security Guardrails)
├── sample_data.py            # Pre-loaded Knowledge Base (22+ Curated Indian Standards, Clauses & QCO Metadata)
├── test_features.py          # End-to-End Automated Verification Test Suite (All 5 Modules)
├── test_bhashini.py          # Bhashini Translation & IndicTTS Verification Script
├── render.yaml               # Optimized Render Cloud Deployment Configuration
├── Procfile                  # Production Process File
├── requirements.txt          # Lightweight Python Dependencies (FastAPI, Uvicorn, Groq, Google-GenAI)
├── packages.txt              # Linux / Cloud System Packages
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
