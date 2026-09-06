<div align="center">

# 🇮🇳 Standards Saathi (मानक साथी)
### *Next-Gen AI Technical Advisor & Verification Hub for Indian Standards (IS Codes) and BIS Regulations*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-0467DF?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.1-f55036?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>Bilingual Conversational RAG • Dual Voice Assistant (STT + TTS) • License Verification • MSME 80% Subsidy Guide</b>
</p>

[Key Features](#-key-features) • [Tech Stack](#-tech-stack) • [Architecture](#-architecture) • [Getting Started](#-getting-started) • [API Reference](#-api-reference) • [Supported Standards](#-ingested-indian-standards)

---

</div>

## 📌 Overview

**Standards Saathi (मानक साथी)** is an official-grade, AI-powered Retrieval-Augmented Generation (RAG) assistant designed for engineers, architects, manufacturers, contractors, MSMEs, and Indian consumers. It provides instant, clause-level accurate answers on **Bureau of Indian Standards (BIS)** specifications, **Quality Control Orders (QCOs)**, **Gold Hallmarking (HUID)**, and **MSME fee concessions**.

Whether you need permissible TDS limits for drinking water (*IS 10500*), structural steel grades (*IS 2062*), concrete durability tables (*IS 456*), or verification of an ISI license number, Standards Saathi synthesizes authoritative responses with exact citations and purchase links in sub-seconds.

---

## 🚀 Key Features

### 1. 🌐 Full Bilingual Experience (English & हिंदी)
* **Instant One-Click Switch (`EN | हिं`)**: Real-time translation of all UI labels, capability cards, question chips, placeholders, and status badges.
* **Bilingual LLM Synthesis**: AI directly synthesizes technical answers in fluent English or natural Hindi (हिंदी / Hinglish) according to the selected mode.

### 2. 🎙️ Dual Voice Assistant (Speech-to-Text & Text-to-Speech)
* **Voice Input (STT)**: Powered by the Web Speech API with dynamic language switching (`hi-IN` and `en-IN`), visual pulsing feedback, and error handling.
* **Audio Read Aloud (TTS)**: Every AI response card includes a `🔊 Read Aloud` button using `window.speechSynthesis` to speak the answer aloud in Hindi or English.

### 3. 📄 Authoritative Source Citations & Purchase Links
* Every technical answer includes verified standard citations:
  > **Sources:** 📄 `IS_1239_2024.pdf`, Page 8, Section 3.2 | 🔗 Purchase: [BIS Manakonline](https://www.manakonline.in)
* Expandable accordion displaying retrieved clause contents, clause IDs, and vector similarity match percentages.

### 4. 📋 Comprehensive BIS Certification Guide
* **7-Step Process Roadmap**: Visual, interactive step-by-step path from standard selection (Step 1) to SIT laboratory setup, Manakonline application, factory audit, counter-sample testing, CM/L license grant, and renewal.
* **Cost Estimates & Timeline**: Realistic duration (30–60 days) and cost estimate (₹20,000–₹80,000) breakdown.
* **Interactive Tool Links**: Direct links to e-BIS Manakonline portal, BIS Laboratory Directory (LIMS), Fee Structure, QCO Tracker, and MSME Udyam.
* **Embedded FAQs & Chat Triggers**: Chatbot automatically surfaces certification roadmaps and navigation chips when users ask about getting certified.

### 5. 🛡️ BIS License & Hallmark Verification Portal
* **ISI License (CM/L)**: Validates 7 or 8-digit manufacturer license numbers against the BIS master registry.
* **Gold HUID Code**: Verifies 6-digit alphanumeric hallmark identifiers to ensure jewellery purity.
* **Electronics CRS (R-No)**: Checks Compulsory Registration Scheme registrations for electronics and batteries.

### 6. 🏢 MSME 80% Concession & Compliance Hub
* Clarifies statutory fee discounts under MSME schemes:
  * **80% Concession** on BIS Application and Annual License fees for Micro enterprises.
  * **50% Concession** on testing charges and fast-track 30-day audit approvals for Small enterprises/startups.

### 7. 🔐 Admin Portal & Dynamic Standard Ingestion
* Password-protected administrative controls.
* Add and index custom Indian Standards (*standard number, title, category, clauses*) directly into the live FAISS vector index at runtime.

---

## 🛠️ Tech Stack

```
                                  ┌────────────────────────────────┐
                                  │   Standards Saathi Frontend    │
                                  │  (Tailwind CSS + Web Speech)   │
                                  └───────────────┬────────────────┘
                                                  │ HTTP / JSON
                                                  ▼
                                  ┌────────────────────────────────┐
                                  │     FastAPI Backend Server     │
                                  │  (/api/chat, /api/standards)   │
                                  └───────────────┬────────────────┘
                                                  │
                         ┌────────────────────────┴────────────────────────┐
                         ▼                                                 ▼
          ┌─────────────────────────────┐                   ┌─────────────────────────────┐
          │      FAISS Vector Store     │                   │     Groq Inference API      │
          │ (SentenceTransformers 384d) │                   │     (Llama 3.1 8B Instant)  │
          └─────────────────────────────┘                   └─────────────────────────────┘
```

* **Frontend**: HTML5, Vanilla JavaScript (ES6+), Tailwind CSS, Marked.js, Material Symbols, Web Speech API (STT/TTS).
* **Secondary UI**: Streamlit 1.40+ (`app.py`) for rapid analytics and prototyping.
* **Backend Framework**: FastAPI & Uvicorn asynchronous REST API.
* **Vector Database**: FAISS (`faiss-cpu`) with normalized inner-product distance for millisecond retrieval.
* **Embedding Model**: `sentence-transformers` (`all-MiniLM-L6-v2`) generating 384-dimensional dense vectors.
* **LLM Acceleration**: Groq Cloud API running `llama-3.1-8b-instant` and `groq/compound-mini`.
* **Resilience**: Integrated offline fallback retriever that formats matched clauses when running without external APIs.

---

## 📦 Ingested Indian Standards

| Standard Number | Title / Subject | Key Clauses Covered |
| :--- | :--- | :--- |
| **IS 2720 (Part 1):1983** | Methods of Test for Soils — Preparation of Dry Soil Samples | Apparatus (mallet, pulverizer, sieves), Drying limits (<60°C for organic/calcareous soils), Sample quantities for Water content, LL/PL, CBR, Compaction |
| **IS 10262:2019** | Concrete Mix Proportioning — Guidelines (Second Revision) | Target mean strength formula ($f'_{ck} = f_{ck} + 1.65S$ or $f_{ck} + X$), Water content Table 4, Coarse aggregate Table 5, High strength M65–M100 (Table 8/9), SCC slump flow (SF1–SF3, L-box, V-funnel), Mass concrete (40/80/150 mm) |
| **IS 456:2000** *(Amend. 1–5)* | Plain and Reinforced Concrete — Code of Practice | Concrete grades (M10–M100), Exposure durability Table 5, Formwork stripping times (Table 11.3.1), Water limits (Table 1), Reinforcement detailing & cover (Table 16), Limit state design |
| **IS 10500:2012** | Drinking Water — Specification | Organoleptic (pH 6.5–8.5, TDS <= 500 mg/L, Turbidity), Heavy Metals (Pb, As, Hg, Cd), Bacteriological E. coli criteria |
| **IS 2062:2011** | Hot Rolled Medium & High Tensile Structural Steel | Steel grades (E250, E350, E410, E450), Yield strength, Charpy V-notch sub-zero impact toughness (27 Joules), QCO mandate |
| **IS 1239:2024** | Mild Steel Tubes, Tubulars and Steel Fittings | Heavy/Medium/Light series steel pipes, 50 bar hydrostatic pressure tests, Galvanizing, ISI Mark marking |
| **IS 15820:2009** | Gold & Silver Hallmarking — General Requirements | 3 Mandatory marks, 6-Digit Alphanumeric HUID verification, Purity grades (24K, 22K, 18K, 14K), BIS emblem |
| **IS 1786:2008** | High Strength Deformed Steel Bars (TMT Rebars) | Fe 415, Fe 500, Fe 500D (seismic), Fe 550D, Fe 600, Yield stress, Tensile strength/ratio, Elongation |
| **IS 1293:2019** | Plugs and Socket-Outlets up to 250V / 16A | Child safety shutters, 6A/16A pin dimensions, 45 K temperature rise limits, 750°C glow wire test, ISI Mark |
| **IS 732:2019** | Code of Practice for Electrical Wiring | Voltage drop limits (3% lighting / 5% power), Protective earthing, 30mA RCD / RCCB shock protection |
| **IS 2189:2008** | Automatic Fire Detection & Alarm Systems | Smoke detector coverage (50 m², 7.5 m spacing), Heat detectors, Manual Call Points (1.4 m height), 65–75 dBA sounders |
| **IS 16046:2018** | Secondary Cells & Batteries Containing Alkaline/Lithium | Thermal abuse (130°C), External short circuit, Overcharge tests, Forced internal indent test, CRS R-number |
| **BIS Services** | BIS Schemes, QCOs, MSME Concessions & Apps | Scheme-I (Product certification), Scheme-II (CRS), FMCS, BIS Care App, 80% MSME fee concession |


---

## ⚡ Getting Started

### Prerequisites
* Python 3.10, 3.11, or 3.12
* Git
* A free [Groq API Key](https://console.groq.com) (Optional, offline mode available)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/standards-saathi.git
cd standards-saathi
```

### 2. Create and Activate a Virtual Environment
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
Create a `.env` file in the root directory (or copy from `.env.example`):
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
ADMIN_PASSWORD=admin123
```

---

## 🖥️ Running the Application

### Option A: Modern Web App (Recommended)
Launches the full FastAPI server hosting the mobile-first UI with real-time RAG, voice assistant, and verification hub:
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

### Option B: Streamlit Dashboard UI
Launches the multi-tab Python dashboard with sidebar statistics, question chips, and answer downloads:
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 📡 API Reference

### `POST /api/chat`
Executes hybrid FAISS vector retrieval and Groq LLM synthesis.
* **Request Body**:
  ```json
  {
    "query": "What are the permissible limits for TDS and pH in drinking water under IS 10500?",
    "top_k": 3,
    "language": "English",
    "temperature": 0.2
  }
  ```
* **Response**:
  ```json
  {
    "answer": "**Direct Answer**\nUnder IS 10500:2012, the acceptable pH limit is 6.5–8.5...",
    "citations": [
      {
        "standard_number": "IS 10500:2012",
        "title": "Drinking Water — Specification",
        "clause_id": "Clause 4.1.4 & 4.1.6",
        "similarity_score": 0.89,
        "full_content": "..."
      }
    ],
    "sources_text": "📄 IS_10500_2012.pdf, Page 2, Section 4.1 | 🔗 Purchase: https://www.manakonline.in",
    "model": "llama-3.1-8b-instant"
  }
  ```

### `GET /api/standards`
Returns all indexed standards and clauses currently loaded in the system.

### `POST /api/standards`
Dynamically adds and indexes a new custom Indian Standard into the FAISS vector store.

### `POST /api/admin/auth`
Validates administrator credentials to unlock settings and ingestion controls.

---

## 💬 Example Queries to Try

| Category | English Query | Hindi Query (हिंदी) |
| :--- | :--- | :--- |
| **Water Quality** | "What are the critical parameters for drinking water under IS 10500?" | "IS 10500 के तहत पीने के पानी में TDS और pH की सीमा क्या है?" |
| **Civil & Concrete** | "What is the minimum grade of concrete for RCC works under IS 456?" | "RCC कंक्रीट के लिए IS 456 में न्यूनतम ग्रेड और कवर क्या है?" |
| **Structural Steel** | "What are the mandatory grades and QCO rules in IS 2062?" | "स्ट्रक्चरल स्टील के लिए IS 2062 के ग्रेड और QCO नियम क्या हैं?" |
| **Gold Jewellery** | "What are the 3 mandatory marks on hallmarked gold jewellery?" | "सोने के आभूषणों पर 3 अनिवार्य निशान और 6-अंकीय HUID का क्या नियम है?" |
| **MSME Benefits** | "What fee concessions do MSME units get for BIS certification?" | "MSME इकाइयों के लिए BIS लाइसेंस में 80% छूट कैसे मिलती है?" |

---

## 📂 Project Directory Structure

```
standards-saathi/
├── static/
│   └── index.html          # Modern Web App UI (Tailwind CSS, STT/TTS, Verification)
├── app.py                  # Streamlit Multi-Tab Dashboard Application
├── server.py               # FastAPI Asynchronous Backend & Static Server
├── rag_engine.py           # Core RAG Engine (FAISS, Embeddings, Groq LLM)
├── sample_data.py          # Curated Indian Standards Knowledge Base (IS Codes)
├── requirements.txt        # Project Dependencies
├── .env.example            # Environment Variable Template
├── .env                    # Local Secrets (ignored by git)
└── README.md               # Project Documentation
```

---

## 🛡️ License & Disclaimer

* **License**: Distributed under the [MIT License](LICENSE).
* **Disclaimer**: *Standards Saathi is an independent AI assistant designed to facilitate quick reference and navigation of Indian Standards. For official regulatory enforcement and legal compliance, always refer to the official gazette notifications published by the [Bureau of Indian Standards (BIS)](https://www.bis.gov.in).*

---

<div align="center">
  <sub>Built with ❤️ for Indian Standards, Quality Assurance, and Atmanirbhar Bharat 🇮🇳</sub>
</div>
