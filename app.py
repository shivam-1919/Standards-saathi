"""
Standards Saathi (मानक साथी) • Next-Gen AI Technical Advisor for Indian Standards & BIS Services
Official-grade RAG Assistant with Clause Citations, Dual UI, Audio TTS, MSME Subsidy Hub & Verification Portal.
"""

import os
import sys
import json
import time
import base64
from typing import List, Dict, Any, Tuple, Optional
import streamlit as st

# Automatically launch Streamlit if executed directly via `python app.py`
if __name__ == "__main__":
    _is_running = False
    try:
        _is_running = hasattr(st, "runtime") and hasattr(st.runtime, "exists") and st.runtime.exists()
    except Exception:
        _is_running = False
    if not _is_running:
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", os.path.abspath(__file__)]
        sys.exit(stcli.main())

from dotenv import load_dotenv

from sample_data import get_all_standards
from rag_engine import get_rag_engine

# Load local SVG logo as reliable Data URI (works offline, locally & on Streamlit Cloud)
def get_logo_data_uri() -> str:
    logo_path = os.path.join(os.path.dirname(__file__), "static", "logo.svg")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return f"data:image/svg+xml;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

LOGO_DATA_URI = get_logo_data_uri()

# Safe toast fallback for Streamlit versions without st.toast
def safe_toast(message: str, icon: Optional[str] = None):
    try:
        if hasattr(st, "toast"):
            if icon:
                st.toast(message, icon=icon)
            else:
                st.toast(message)
        else:
            st.info(message)
    except Exception:
        pass

# Load environment variables (.env for local, st.secrets for Streamlit Cloud)
load_dotenv(override=True)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
try:
    if hasattr(st, "secrets"):
        if "GROQ_API_KEY" in st.secrets and not os.getenv("GROQ_API_KEY"):
            os.environ["GROQ_API_KEY"] = str(st.secrets["GROQ_API_KEY"])
        if "ADMIN_PASSWORD" in st.secrets:
            ADMIN_PASSWORD = str(st.secrets["ADMIN_PASSWORD"])
except Exception:
    pass

# Page Configuration
st.set_page_config(
    page_title="Standards Saathi (मानक साथी) • BIS AI Assistant",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []

if "questions_count" not in st.session_state:
    st.session_state.questions_count = 0

if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = {}

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

if "verify_sample_code" not in st.session_state:
    st.session_state.verify_sample_code = ""

if "verify_type" not in st.session_state:
    st.session_state.verify_type = "cml"

# Custom Indian Theme Styling (Saffron / White / Green / Deep Navy Blue)
st.markdown("""
<!-- Material Symbols and Google Fonts -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&family=Plus+Jakarta+Sans:wght@600;700;800&family=Outfit:wght@500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    :root {
        --color-primary: #00152a;
        --color-primary-container: #0f2d4a;
        --color-secondary: #a73a00;
        --color-secondary-container: #ff6926;
        --color-tertiary: #002e11;
        --color-tertiary-container: #008738;
        --color-surface: #f7f9ff;
        --color-surface-card: #ffffff;
        --color-surface-container: #e8f1ff;
        --color-on-surface: #001d33;
        --color-on-surface-variant: #4a5360;
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
    }

    html, body, [class*="css"], .stApp {
        background: linear-gradient(180deg, #f7f9ff 0%, #edf2fc 100%) !important;
        font-family: 'Inter', 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--color-on-surface) !important;
        letter-spacing: -0.01em;
    }

    /* Clean Streamlit Default Chrome */
    header[data-testid="stHeader"] { background: transparent !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }

    /* Custom Slim Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(0, 21, 42, 0.15); border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 105, 38, 0.5); }

    /* Top App Header Banner with Glassmorphism */
    .stitch-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 24px;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(0, 21, 42, 0.08);
        border-radius: var(--radius-lg);
        margin-bottom: 6px;
        box-shadow: 0 4px 24px rgba(0, 21, 42, 0.05), 0 1px 3px rgba(0, 0, 0, 0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stitch-header:hover {
        box-shadow: 0 8px 32px rgba(0, 21, 42, 0.08);
    }
    .stitch-header-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .stitch-logo {
        height: 46px;
        width: auto;
        object-fit: contain;
        filter: drop-shadow(0 2px 8px rgba(0, 21, 42, 0.15));
        transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .stitch-logo:hover {
        transform: scale(1.08) rotate(-2deg);
    }
    .stitch-header-title {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
        font-size: 23px;
        font-weight: 800;
        color: var(--color-primary);
        letter-spacing: -0.03em;
        line-height: 1.15;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .stitch-header-sub {
        font-size: 12px;
        font-weight: 600;
        color: var(--color-on-surface-variant);
        letter-spacing: 0.02em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .stitch-header-actions {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .stitch-pill-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        background: #ffffff;
        border: 1px solid rgba(0, 21, 42, 0.1);
        color: #00152a;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease;
    }
    .stitch-pill-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    /* Glowing Indian Tricolor Bar */
    .stitch-tricolor-bar {
        width: 100%;
        display: flex;
        height: 5px;
        border-radius: 9999px;
        overflow: hidden;
        margin-bottom: 14px;
        box-shadow: 0 2px 10px rgba(255, 105, 38, 0.22);
    }
    .tricolor-saffron { flex: 1; background: linear-gradient(90deg, #ff7a18, #ff6926); }
    .tricolor-white { flex: 1; background: #ffffff; border-left: 1px solid #e3efff; border-right: 1px solid #e3efff; }
    .tricolor-green { flex: 1; background: linear-gradient(90deg, #008738, #004d20); }

    /* Civic Assurance Banner */
    .stitch-assurance-banner {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(14px);
        border-radius: var(--radius-md);
        padding: 10px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 18px;
        border: 1px solid rgba(16, 42, 67, 0.1);
        box-shadow: 0 2px 8px rgba(0, 21, 42, 0.02);
    }
    .assurance-left {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12.5px;
        font-weight: 600;
        color: var(--color-on-surface);
    }
    .assurance-badge {
        background: var(--color-surface-container);
        color: var(--color-primary);
        padding: 4px 12px;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 6px;
        border: 1px solid rgba(0, 21, 42, 0.06);
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #008738;
        box-shadow: 0 0 0 0 rgba(0, 135, 56, 0.5);
        animation: pulse-glow 2s infinite cubic-bezier(0.4, 0, 0.6, 1);
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(0, 135, 56, 0.6); }
        50% { box-shadow: 0 0 0 6px rgba(0, 135, 56, 0); }
    }

    /* Executive Hero Card */
    .intro-turn {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(243, 248, 255, 0.95));
        border: 1px solid rgba(0, 21, 42, 0.08);
        border-radius: 18px;
        padding: 22px 26px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 29, 51, 0.04);
        position: relative;
        overflow: hidden;
    }
    .intro-turn::after {
        content: '';
        position: absolute;
        top: -40px;
        right: -40px;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255, 105, 38, 0.09), transparent 70%);
        pointer-events: none;
    }
    .intro-header {
        display: flex;
        align-items: flex-start;
        gap: 18px;
        margin-bottom: 4px;
    }
    .intro-icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: linear-gradient(135deg, #00152a, #102a43);
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 4px 14px rgba(0, 21, 42, 0.22);
    }
    .intro-title {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
        font-size: 21px;
        font-weight: 800;
        color: var(--color-primary);
        margin: 0;
        letter-spacing: -0.02em;
    }
    .intro-desc {
        font-size: 13.5px;
        color: var(--color-on-surface-variant);
        margin: 5px 0 0 0;
        line-height: 1.5;
    }

    /* Badges & Pills */
    .badge-std {
        background: linear-gradient(135deg, #00152a, #102a43);
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11.5px;
        font-weight: 700;
        padding: 4px 11px;
        border-radius: 6px;
        letter-spacing: 0.03em;
        box-shadow: 0 2px 6px rgba(0, 21, 42, 0.15);
    }
    .badge-status {
        background: #e6f7ed;
        color: #005a26;
        font-size: 11.5px;
        font-weight: 700;
        padding: 4px 11px;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        border: 1px solid rgba(0, 135, 56, 0.2);
    }

    /* Chat Messages Bubble Styling */
    div[data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid rgba(0, 21, 42, 0.07) !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        box-shadow: 0 4px 20px rgba(0, 21, 42, 0.03) !important;
        margin-bottom: 16px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    div[data-testid="stChatMessage"]:hover {
        box-shadow: 0 8px 28px rgba(0, 21, 42, 0.06) !important;
    }
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: #f4f8ff !important;
        border-left: 4px solid #00152a !important;
    }
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: #ffffff !important;
        border-left: 4px solid #ff6926 !important;
    }

    /* Question Chip Buttons */
    div[data-testid="stHorizontalBlock"] button {
        border-radius: var(--radius-md) !important;
        border: 1px solid rgba(0, 21, 42, 0.1) !important;
        background: #ffffff !important;
        color: #001d33 !important;
        font-weight: 600 !important;
        font-size: 12.5px !important;
        padding: 10px 14px !important;
        box-shadow: 0 2px 8px rgba(0, 21, 42, 0.03) !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        border-color: #ff6926 !important;
        color: #a73a00 !important;
        background: #fff8f5 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(255, 105, 38, 0.16) !important;
    }

    /* Mandatory QCO Compliance Alert */
    .alert-qco {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        background: linear-gradient(135deg, #fff7f2 0%, #fff0e8 100%);
        border-left: 4px solid #ff6926;
        border-radius: var(--radius-md);
        padding: 12px 16px;
        margin-top: 14px;
        margin-bottom: 10px;
        box-shadow: 0 2px 10px rgba(255, 105, 38, 0.08);
    }
    .alert-qco-title {
        display: block;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        font-weight: 800;
        color: #a73a00;
        margin-bottom: 2px;
        letter-spacing: -0.01em;
    }
    .alert-qco-desc {
        display: block;
        font-size: 12px;
        color: #573322;
        line-height: 1.45;
    }

    /* Related Standards Strip */
    .related-strip {
        background: var(--color-surface-container);
        border-radius: var(--radius-md);
        padding: 10px 14px;
        font-size: 12px;
        font-weight: 700;
        color: var(--color-primary);
        margin-top: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        border: 1px solid rgba(0, 21, 42, 0.06);
    }
    .related-pill {
        background: #ffffff;
        color: #a73a00;
        padding: 3px 11px;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid rgba(167, 58, 0, 0.25);
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease;
    }
    .related-pill:hover {
        transform: translateY(-1px);
        background: #fff8f5;
    }

    /* Sidebar Styling & Stats Card */
    [data-testid="stSidebar"] {
        background: #f2f6fc !important;
        border-right: 1px solid rgba(0, 21, 42, 0.08) !important;
    }
    .stat-card {
        background: #ffffff;
        border: 1px solid rgba(0, 21, 42, 0.08);
        border-radius: var(--radius-md);
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0, 21, 42, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #ff6926, #00152a);
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0, 21, 42, 0.07);
    }
    .stat-label {
        font-size: 11px;
        font-weight: 700;
        color: var(--color-on-surface-variant);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .stat-value {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
        font-size: 17px;
        font-weight: 800;
        color: var(--color-primary);
        margin-top: 3px;
    }

    /* Enhanced Tab Navigation with Modern Material Design & Saffron/Navy Active Glow */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(16px);
        border-radius: 14px;
        padding: 6px 10px;
        border: 1px solid rgba(0, 21, 42, 0.08);
        box-shadow: 0 3px 14px rgba(0, 21, 42, 0.03);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background: #ffffff;
        border-radius: 10px;
        color: #4a5360;
        font-weight: 700;
        font-size: 13.5px;
        padding: 0 18px;
        border: 1px solid rgba(0, 21, 42, 0.08);
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #ff6926;
        color: #a73a00;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 105, 38, 0.12);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00152a 0%, #102a43 100%) !important;
        color: #ffffff !important;
        border: 1px solid #ff6926 !important;
        box-shadow: 0 4px 16px rgba(0, 21, 42, 0.25), 0 0 0 2px rgba(255, 105, 38, 0.25) !important;
    }

    /* Markdown Tables Upgrade */
    table {
        border-collapse: separate !important;
        border-spacing: 0 !important;
        width: 100% !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(0, 21, 42, 0.08) !important;
        box-shadow: 0 2px 10px rgba(0, 21, 42, 0.03) !important;
        margin: 14px 0 !important;
    }
    th {
        background: #00152a !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 12.5px !important;
        font-weight: 700 !important;
        padding: 10px 14px !important;
        text-align: left !important;
    }
    td {
        padding: 10px 14px !important;
        font-size: 13px !important;
        border-bottom: 1px solid #edf2fc !important;
        background: #ffffff !important;
    }
    tr:nth-child(even) td {
        background: #f8faff !important;
    }

    /* Institutional Footer */
    .institutional-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 20px 24px;
        margin-top: 36px;
        border-top: 1px solid rgba(0, 21, 42, 0.08);
        color: #5a6472;
        font-size: 12.5px;
        font-weight: 600;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR CONFIGURATION (Language, Stats, Admin)
# ==========================================
with st.sidebar:
    if LOGO_DATA_URI:
        st.image(LOGO_DATA_URI, width=44)
    st.title("🇮🇳 Standards Saathi")

    # Language Selector in Sidebar
    lang_choice = st.selectbox(
        "🌐 Language / भाषा",
        options=["English", "हिंदी"],
        index=0 if st.session_state.selected_language == "English" else 1,
        key="sidebar_lang_selector",
        help="Select language for UI labels, prompts, and AI synthesis."
    )
    if lang_choice != st.session_state.selected_language:
        st.session_state.selected_language = lang_choice
        st.rerun()

    is_hindi = st.session_state.selected_language == "हिंदी"

    st.markdown("---")

    # Sidebar Stats
    st.markdown("### 📊 " + ("सिस्टम सांख्यिकी" if is_hindi else "System Statistics"))
    
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">{"उत्तर दिए गए प्रश्न" if is_hindi else "Questions Answered"}</div>
        <div class="stat-value">📊 {st.session_state.questions_count}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">{"शामिल भारतीय मानक" if is_hindi else "Standards Covered"}</div>
        <div class="stat-value">📚 {len(get_all_standards())} Standards (45+ Clauses)</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">{"वेक्टर सर्च इंजन" if is_hindi else "Vector Engine"}</div>
        <div class="stat-value">🟢 FAISS &amp; Semantic RAG</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🛡️ " + ("गोपनीयता एवं सुरक्षा नियंत्रण" if is_hindi else "Privacy & Security Controls")):
        st.markdown("""
        - **🔒 Zero Data Retention:** User queries are processed in-memory and discarded. No personal identifiers or query histories are permanently stored.
        - **🛡️ API Key Security:** Keys are shielded via `.env`/`st.secrets` and masked across administrative views.
        - **🚫 Non-Regulatory Advisory:** Standards Saathi does not issue legal or certification grants; official applications must be submitted via [e-BIS Manakonline](https://www.manakonline.in).
        - **🛡️ Active Defense:** Guardrails continuously scan for prompt-injection attempts and ground responses strictly in retrieved Indian Standards.
        """)

    st.markdown("---")

    # Clear Chat Button
    clear_btn_label = "🗑️ डेटा एवं चैट साफ़ करें (Purge Session)" if is_hindi else "🗑️ Clear Chat & Purge Data"
    if st.button(clear_btn_label, use_container_width=True):
        st.session_state.messages = []
        safe_toast("✅ " + ("सत्र डेटा और चैट इतिहास रीसेट हो गया है।" if is_hindi else "Session data & chat history successfully purged!"))
        st.rerun()

    st.markdown("---")
    st.caption("BIS Citizen Advisory • Manakonline Live Connected")


# UI Translation Dictionary
T = {
    "welcome_title": "नमस्ते! I am Standards Saathi" if not is_hindi else "नमस्ते! मैं मानक साथी हूँ",
    "welcome_sub": "Your bilingual AI guide for Indian Standards (IS Codes), ISI License verification, Gold HUID, and MSME fee concessions." if not is_hindi else "भारतीय मानकों (IS Codes), ISI लाइसेंस, गोल्ड हॉलमार्किंग और MSME सब्सिडी के लिए आपका AI सलाहकार।",
    "chip_pipe": "Steel pipe ke liye kaunsa standard?" if not is_hindi else "स्टील पाइप के लिए कौन सा मानक है?",
    "chip_cert": "BIS certification kaise milega?" if not is_hindi else "BIS प्रमाणन कैसे प्राप्त करें?",
    "chip_2062": "What is IS 2062 structural steel?" if not is_hindi else "IS 2062 स्ट्रक्चरल स्टील मानक क्या है?",
    "chip_concrete": "Concrete mix design guidelines (IS 456 / 10262)?" if not is_hindi else "कंक्रीट मिक्स डिज़ाइन दिशानिर्देश?",
    "chip_gold": "Gold 916 hallmarking rules (IS 1417)?" if not is_hindi else "गोल्ड 916 हॉलमार्किंग नियम (IS 1417)?",
    "chip_battery": "Lithium battery safety tests (IS 16046)?" if not is_hindi else "लिथियम बैटरी सुरक्षा परीक्षण (IS 16046)?",
    "search_spinner": "🔍 Searching BIS standards & clauses..." if not is_hindi else "🔍 बीआईएस मानकों में क्लॉज खोज जारी है...",
    "gen_spinner": "🤖 Synthesizing source-backed answer..." if not is_hindi else "🤖 आधिकारिक उत्तर तैयार किया जा रहा है...",
    "chat_placeholder": "Ask about Indian Standards in Hindi or English (e.g. drinking water lead limits, IS 1239 pipe thickness)..." if not is_hindi else "भारतीय मानकों, IS कोड या प्रमाणन के बारे में पूछें...",
    "download_btn": "📥 Download (.txt)" if not is_hindi else "📥 डाउनलोड (.txt)",
    "speak_btn": "🔊 Read Aloud" if not is_hindi else "🔊 बोलकर सुनाएं",
    "helpful": "👍 Helpful" if not is_hindi else "👍 उपयोगी",
    "not_helpful": "👎 Not Helpful" if not is_hindi else "👎 अनुपयोगी",
    "feedback_thanks": "Thank you for your feedback! 🙏" if not is_hindi else "आपकी प्रतिक्रिया के लिए धन्यवाद! 🙏",
    "related_label": "🔗 Related Standards:" if not is_hindi else "🔗 संबंधित मानक:",
    "tab_chat": "💬 AI Saathi Chat" if not is_hindi else "💬 AI साथी चैट",
    "tab_cert": "📋 BIS Certification Roadmap" if not is_hindi else "📋 बीआईएस प्रमाणन रोडमैप",
    "tab_verify": "🛡️ ISI, HUID & CRS Verification" if not is_hindi else "🛡️ ISI, HUID व CRS सत्यापन",
    "tab_catalog": "📚 IS Codes Directory" if not is_hindi else "📚 IS कोड निर्देशिका",
    "tab_msme": "💼 MSME 80% Subsidy & Calculator" if not is_hindi else "💼 MSME 80% सब्सिडी एवं कैलकुलेटर",
    "tab_admin": "🔒 Admin & Data Ingestion" if not is_hindi else "🔒 एडमिन व डेटा इनजेशन"
}


# Initialize RAG Engine
rag_engine = get_rag_engine()

# Top App Header (Civic / Stitch Design)
st.markdown(f"""
<div class="stitch-header">
    <div class="stitch-header-left">
        <img alt="Standards Saathi Logo" class="stitch-logo" src="{LOGO_DATA_URI}"/>
        <div>
            <div class="stitch-header-title">
                <span>Standards Saathi</span>
                <span class="material-symbols-outlined" style="color: #008738; font-size: 22px;" title="Official BIS Portal Verification">verified</span>
            </div>
            <div class="stitch-header-sub">
                <span class="material-symbols-outlined" style="font-size: 14px; color: #a73a00;">account_balance</span>
                <span>मानक साथी • BIS AI Technical Advisor &amp; Verification Hub</span>
            </div>
        </div>
    </div>
    <div class="stitch-header-actions">
        <span class="stitch-pill-btn" style="background: #ffffff; border-color: #a73a00; color: #a73a00;">
            <span class="material-symbols-outlined" style="font-size: 14px;">translate</span>
            <span>{st.session_state.selected_language}</span>
        </span>
        <span class="stitch-pill-btn" style="background: #e3efff; color: #00152a;">
            <span class="material-symbols-outlined" style="font-size: 14px; color: #008738;">bolt</span>
            <span>Live RAG</span>
        </span>
    </div>
</div>

<!-- Tricolor Indicator Bar -->
<div class="stitch-tricolor-bar">
    <div class="tricolor-saffron"></div>
    <div class="tricolor-white"></div>
    <div class="tricolor-green"></div>
</div>

<!-- Civic Assurance Banner -->
<div class="stitch-assurance-banner">
    <div class="assurance-left">
        <span class="material-symbols-outlined text-[18px]" style="color: #003016;">shield</span>
        <span>{"बीआईएस सत्यापित ज्ञान आधार • e-BIS मानकऑनलाइन से संयोजित" if is_hindi else "BIS Verified Knowledge Base • Connected with e-BIS Manakonline"}</span>
    </div>
    <div class="assurance-badge">
        <span class="pulse-dot"></span>
        <span>Official Knowledge Base</span>
    </div>
</div>
""", unsafe_allow_html=True)


# Main Navigation Tabs with Icons
tab_chat, tab_cert, tab_verify, tab_catalog, tab_msme, tab_admin = st.tabs([
    T["tab_chat"],
    T["tab_cert"],
    T["tab_verify"],
    T["tab_catalog"],
    T["tab_msme"],
    T["tab_admin"]
])


# ==========================================
# TAB 1: SAATHI CHAT VIEW
# ==========================================
with tab_chat:
    # Welcome Card
    st.markdown(f"""
    <div class="intro-turn">
        <div class="intro-header">
            <div class="intro-icon">
                <span class="material-symbols-outlined text-[24px]">smart_toy</span>
            </div>
            <div>
                <h1 class="intro-title">{T["welcome_title"]}</h1>
                <p class="intro-desc">{T["welcome_sub"]}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clickable Example Question Chips
    st.markdown("**💡 " + ("त्वरित तकनीकी प्रश्न विकल्प (क्लिक करें):" if is_hindi else "Quick Technical Question Prompts (Click to ask):") + "**")
    q_col1, q_col2, q_col3 = st.columns(3)
    q_col4, q_col5, q_col6 = st.columns(3)
    
    with q_col1:
        if st.button("🚰 " + T["chip_pipe"], use_container_width=True):
            st.session_state.pending_query = "Steel pipe ke liye kaunsa standard use hota hai aur uske grades kya hain?"
    with q_col2:
        if st.button("📜 " + T["chip_cert"], use_container_width=True):
            st.session_state.pending_query = "BIS certification (ISI Mark) lene ka step by step process kya hai?"
    with q_col3:
        if st.button("🏗️ " + T["chip_2062"], use_container_width=True):
            st.session_state.pending_query = "What is IS 2062 and what are its strength grades?"
    with q_col4:
        if st.button("🧱 " + T["chip_concrete"], use_container_width=True):
            st.session_state.pending_query = "What are the concrete mix design guidelines and grades under IS 456:2000?"
    with q_col5:
        if st.button("🥇 " + T["chip_gold"], use_container_width=True):
            st.session_state.pending_query = "What are the gold purity grades and mandatory marks under IS 1417?"
    with q_col6:
        if st.button("🔋 " + T["chip_battery"], use_container_width=True):
            st.session_state.pending_query = "What are the mandatory battery safety tests under IS 16046 / CRS?"

    # Voice Speech-to-Text with Human-in-the-Loop Confirmation Guardrail
    with st.expander("🎙️ " + ("वॉइस इनपुट व पुष्टिकरण (Voice Transcription Confirmation)" if is_hindi else "Voice Assistant & Transcription Confirmation"), expanded=False):
        st.caption(
            "सुरक्षा और सटीकता के लिए, मानक साथी आपके वॉइस इनपुट को AI को भेजने से पहले समीक्षा और पुष्टि (Confirm) करने की सुविधा देता है।"
            if is_hindi else
            "For accuracy and safety, Standards Saathi allows you to review, edit, and confirm your voice transcription before submitting it to the AI advisor."
        )
        
        v_sub1, v_sub2 = st.columns([1.2, 2.8])
        with v_sub1:
            speech_lang_code = "hi-IN" if is_hindi else "en-IN"
            st.components.v1.html(
                f"""
                <div style="font-family: 'Inter', sans-serif; display: flex; flex-direction: column; gap: 8px;">
                    <button id="record-btn" onclick="startSaathiVoice()" style="
                        display: flex; align-items: center; justify-content: center; gap: 8px;
                        background: linear-gradient(135deg, #00152a 0%, #102a43 100%);
                        color: #ffffff; border: 1px solid #ff6926; border-radius: 10px;
                        padding: 10px 14px; font-weight: 700; font-size: 13px; cursor: pointer;
                        box-shadow: 0 4px 12px rgba(0, 21, 42, 0.2); width: 100%;
                    ">
                        🎙️ <span id="rec-label">{"आवाज़ से बोलें" if is_hindi else "Record Speech"}</span>
                    </button>
                    <div id="rec-status" style="font-size: 11px; color: #5a6472; text-align: center;">{"क्लिक करके बोलना शुरू करें..." if is_hindi else "Click to start voice input..."}</div>
                </div>
                <script>
                    var recognition;
                    function startSaathiVoice() {{
                        var btn = document.getElementById('record-btn');
                        var status = document.getElementById('rec-status');
                        var label = document.getElementById('rec-label');
                        
                        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                        if (!SpeechRecognition) {{
                            status.innerText = "⚠️ Web Speech API not supported in this browser.";
                            return;
                        }}
                        
                        recognition = new SpeechRecognition();
                        recognition.lang = '{speech_lang_code}';
                        recognition.continuous = false;
                        recognition.interimResults = false;
                        
                        recognition.onstart = function() {{
                            btn.style.background = '#a73a00';
                            label.innerText = '🔴 Listening...';
                            status.innerText = 'Speak now into microphone...';
                        }};
                        
                        recognition.onresult = function(event) {{
                            var transcript = event.results[0][0].transcript;
                            status.innerHTML = '✅ Audio captured! Copying text...';
                            if (navigator.clipboard) {{
                                navigator.clipboard.writeText(transcript);
                            }}
                            alert('🎙️ Voice Transcribed: "' + transcript + '"\\n\\nPlease review in the confirmation box and click Confirm!');
                        }};
                        
                        recognition.onerror = function(event) {{
                            status.innerText = '⚠️ Speech error: ' + event.error;
                            btn.style.background = '#00152a';
                            label.innerText = '🎙️ Record Speech';
                        }};
                        
                        recognition.onend = function() {{
                            btn.style.background = '#00152a';
                            label.innerText = '🎙️ Record Speech';
                        }};
                        
                        recognition.start();
                    }}
                </script>
                """,
                height=88
            )

        with v_sub2:
            voice_transcribed_input = st.text_input(
                "📝 " + ("ट्रांसक्रिप्शन समीक्षा (यदि आवश्यक हो तो संपादित करें):" if is_hindi else "Voice Transcription Review & Confirmation:"),
                placeholder="Transcribed text appears here or paste spoken query..." if not is_hindi else "ट्रांसक्राइब किया गया टेक्स्ट यहाँ दर्ज करें...",
                key="voice_confirm_box"
            )
            if st.button("✅ " + ("पुष्टि करें और साथी से पूछें (Confirm Query)" if is_hindi else "Confirm & Submit Voice Query"), type="primary", use_container_width=True):
                if voice_transcribed_input.strip():
                    st.session_state.pending_query = voice_transcribed_input.strip()
                    st.rerun()
                else:
                    safe_toast("Please enter or speak your query first.", icon="⚠️")

    st.markdown("<hr style='margin: 12px 0; border: 0; border-top: 1px solid #e3efff;'>", unsafe_allow_html=True)

    # Chat History Rendering
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**{msg['content']}**")
        else:
            with st.chat_message("assistant", avatar="🇮🇳"):
                std_num = msg.get("standard_number", "Indian Standard")
                std_title = msg.get("title", "BIS Specification")
                citations = msg.get("citations", [])

                # Grounding & Document-Version Metadata Badges
                top_c = citations[0] if citations else {}
                c_ver = top_c.get("status", "Active National Standard")
                c_clause = top_c.get("clause_id", "General Scope")
                c_doc = top_c.get("filename", f"{std_num}.pdf")

                st.markdown(f"""
                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                        <span class="badge-std">{std_num}</span>
                        <span style="display: inline-flex; align-items: center; gap: 4px; background: rgba(0, 135, 56, 0.1); border: 1px solid rgba(0, 135, 56, 0.25); color: #002e11; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px;">
                            <span class="material-symbols-outlined" style="font-size: 13px; color: #008738;">verified_user</span>
                            Grounded: {c_doc}
                        </span>
                        <span style="display: inline-flex; align-items: center; gap: 4px; background: rgba(0, 21, 42, 0.05); border: 1px solid rgba(0, 21, 42, 0.1); color: #00152a; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 6px;">
                            <span class="material-symbols-outlined" style="font-size: 13px; color: #a73a00;">menu_book</span>
                            {c_clause}
                        </span>
                    </div>
                    <span class="badge-status">
                        <span class="material-symbols-outlined text-[14px]">check_circle</span> {c_ver}
                    </span>
                </div>
                <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 700; color: #00152a; margin: 0 0 8px 0;">{std_title}</h3>
                """, unsafe_allow_html=True)

                # Render Answer
                st.markdown(msg["content"])

                # Mandatory QCO Notice
                st.markdown("""
                <div class="alert-qco" style="margin-top: 10px;">
                    <span class="material-symbols-outlined text-[18px]" style="color: #a73a00; flex-shrink: 0; margin-top: 1px;">notification_important</span>
                    <div>
                        <span class="alert-qco-title">Mandatory QCO in Effect</span>
                        <span class="alert-qco-desc">Ministry Quality Control Orders mandate Scheme-I (ISI Mark) or CRS compliance. Sale without valid BIS certification is legally prohibited.</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Certification Guide Callout Banner
                if any(k in msg["content"].lower() for k in ["certification", "license", "licence", "cml", "scheme-i", "crs", "7-step", "manakonline", "प्रमाणन", "लाइसेंस"]):
                    st.success("📋 " + ("**पूर्ण 7-चरणीय बीआईएस प्रमाणन गाइड, प्रयोगशाला परीक्षण, और ₹20K-80K लागत विवरण के लिए ऊपर '📋 BIS Certification Roadmap' टैब देखें!**" if is_hindi else "**For the full 7-step roadmap, lab testing, fee schedule, and MSME 80% subsidy, switch to the '📋 BIS Certification Roadmap' tab above!**"))

                # Related Standards Strip
                related_stds = msg.get("related_standards", [])
                if related_stds:
                    pills_html = " ".join([f'<span class="related-pill">{r}</span>' for r in related_stds])
                    st.markdown(f"""
                    <div class="related-strip">
                        <span>{T["related_label"]}</span>
                        {pills_html}
                    </div>
                    """, unsafe_allow_html=True)

                # Action Row: Audio TTS, Download Answer & Feedback Buttons
                st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
                act_col1, act_col2, act_col3, act_col4 = st.columns([1.8, 1.8, 1.2, 1.2])
                
                # Audio Read Aloud (Text-to-Speech)
                with act_col1:
                    clean_text_speech = msg['content'].replace('"', "'").replace("\n", " ").replace("*", "").replace("#", "")
                    speech_lang = "hi-IN" if is_hindi else "en-IN"
                    st.components.v1.html(
                        f"""
                        <button onclick="
                            window.speechSynthesis.cancel();
                            var u = new SpeechSynthesisUtterance('{clean_text_speech[:500]}');
                            u.lang = '{speech_lang}';
                            window.speechSynthesis.speak(u);
                        " style="
                            display: inline-flex; align-items: center; gap: 6px;
                            padding: 6px 14px; border-radius: 8px; border: 1px solid #00152a;
                            background: #ffffff; color: #00152a; font-family: sans-serif;
                            font-weight: 700; font-size: 12px; cursor: pointer;
                        ">
                            🔊 {T["speak_btn"]}
                        </button>
                        """,
                        height=42
                    )

                # Download Answer Button
                with act_col2:
                    download_text = f"STANDARDS SAATHI AI ADVISORY\nStandard: {std_num} - {std_title}\n\n{msg['content']}\n\nEmpowered by Bureau of Indian Standards (BIS)"
                    st.download_button(
                        label=T["download_btn"],
                        data=download_text,
                        file_name=f"Standards_Saathi_{std_num.replace(':', '_').replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"dl_btn_{idx}"
                    )

                # Feedback Buttons
                with act_col3:
                    if st.button(T["helpful"], key=f"help_pos_{idx}"):
                        st.session_state.feedback_log[idx] = "helpful"
                        safe_toast(T["feedback_thanks"], icon="👍")
                with act_col4:
                    if st.button(T["not_helpful"], key=f"help_neg_{idx}"):
                        st.session_state.feedback_log[idx] = "not_helpful"
                        safe_toast(T["feedback_thanks"], icon="🙏")

    # Chat Input Handler
    user_input = st.chat_input(T["chat_placeholder"])
    query_to_process = st.session_state.pending_query or user_input
    st.session_state.pending_query = None

    if query_to_process:
        st.session_state.messages.append({"role": "user", "content": query_to_process})
        st.session_state.questions_count += 1
        
        # Two-Stage Loading States
        with st.chat_message("assistant", avatar="🇮🇳"):
            with st.spinner(T["search_spinner"]):
                retrieved_chunks = rag_engine.retrieve(query_to_process, top_k=3)
                time.sleep(0.2)

            with st.spinner(T["gen_spinner"]):
                resp = rag_engine.generate_response(
                    query=query_to_process,
                    chat_history=st.session_state.messages[:-1],
                    top_k=3,
                    temperature=0.2,
                    language=st.session_state.selected_language
                )

            citations = resp.get("citations", []) if isinstance(resp, dict) else []
            top_cit = citations[0] if citations else {}
            std_num = top_cit.get("standard_number", "Indian Standard")
            std_title = top_cit.get("title", "BIS Specification")

            st.session_state.messages.append({
                "role": "assistant",
                "content": resp.get("answer", "") if isinstance(resp, dict) else str(resp),
                "standard_number": std_num,
                "title": std_title,
                "citations": citations,
                "related_standards": resp.get("related_standards", []) if isinstance(resp, dict) else []
            })
            st.rerun()


# ==========================================
# TAB 2: BIS CERTIFICATION ROADMAP
# ==========================================
with tab_cert:
    c_top1, c_top2 = st.columns([3, 1])
    with c_top1:
        st.markdown(f"""
        <div class="intro-turn">
            <h2 class="intro-title" style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #a73a00;">assignment_turned_in</span>
                {"📋 बीआईएस प्रमाणन एवं लाइसेंसिंग रोडमैप" if is_hindi else "📋 BIS Certification & Licensing Roadmap"}
            </h2>
            <p class="intro-desc">
                {"भारतीय निर्माताओं और MSME इकाइयों के लिए ISI मार्क (स्कीम-I) और CRS पंजीकरण प्राप्त करने की संपूर्ण 7-चरणीय मार्गदर्शिका।" if is_hindi else "Complete 7-step guide for Indian manufacturers and MSMEs to obtain ISI Mark (Scheme-I) and CRS registration with up to 80% fee subsidies."}
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c_top2:
        if st.button("💬 " + ("साथी चैट पर प्रश्न पूछें" if is_hindi else "Ask in Saathi Chat"), use_container_width=True):
            st.session_state.pending_query = "Tell me the step-by-step procedure to apply for BIS certification for my product."
            st.rerun()

    # 4 Key Metrics Cards
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">⏱️ {"अनुमानित समय" if is_hindi else "Timeline"}</div>
            <div class="stat-value">30 – 60 Days</div>
            <div style="font-size: 10px; color: #43474d; margin-top: 2px;">30d Simplified / 60d Normal</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">💰 {"अनुमानित लागत" if is_hindi else "Estimated Cost"}</div>
            <div class="stat-value">₹20K – ₹80K</div>
            <div style="font-size: 10px; color: #43474d; margin-top: 2px;">Micro MSME: ~₹18k–₹25k</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">🏢 {"MSME सब्सिडी" if is_hindi else "MSME Subsidy"}</div>
            <div class="stat-value" style="color: #003016;">80% Concession</div>
            <div style="font-size: 10px; color: #43474d; margin-top: 2px;">On App &amp; License Fees</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📜 {"लाइसेंस वैधता" if is_hindi else "License Validity"}</div>
            <div class="stat-value">1 to 2 Years</div>
            <div style="font-size: 10px; color: #43474d; margin-top: 2px;">Renewable via portal</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 " + ("7-चरणीय प्रमाणन प्रक्रिया" if is_hindi else "7-Step Step-by-Step Certification Process"))

    with st.expander("📍 **Step 1: Identify Applicable Indian Standard (IS Code) & Scheme** (Day 1–3)", expanded=True):
        st.markdown("""
        - **Objective:** Determine the specific product standard (e.g. `IS 1239` for steel tubes, `IS 10500` for drinking water).
        - **Mandatory QCO Check:** Verify whether your product falls under mandatory **Quality Control Orders (QCO)** published by Ministries.
        - **Scheme Selection:** Choose between **Scheme-I (ISI Mark)** for industrial/physical goods or **Scheme-II (CRS)** for electronics/IT.
        - **Key Checklist:**
          - [x] Search IS Code in Directory or ask Saathi
          - [x] Download relevant Scheme of Inspection and Testing (SIT)
          - [x] Check conformity requirements and scope
        """)

    with st.expander("⚙️ **Step 2: Set Up In-House Testing Laboratory & Quality Infrastructure** (Day 4–15)"):
        st.markdown("""
        - **In-House Lab:** Procure and install all testing apparatus mandated by the BIS Scheme of Inspection and Testing (SIT).
        - **Calibration:** Ensure all test gauges, tensile machines, pressure gauges, and ovens have valid calibration certificates from NABL-accredited labs.
        - **Personnel:** Appoint a qualified Quality Control Engineer responsible for day-to-day batch testing and record keeping.
        """)

    with st.expander("📝 **Step 3: Online Application on e-BIS Manakonline Portal** (Day 16–20)"):
        st.markdown("""
        - **Portal:** Register on **[www.manakonline.in](https://www.manakonline.in)**.
        - **Documents Upload:** Upload factory layout plan, machinery list, raw material test certs, in-house testing equipment list, and Udyam Registration.
        - **Fee Payment:** Pay nominal application fee (₹1,000 for large enterprise; **₹200 for Micro MSME** after 80% subsidy).
        """)

    with st.expander("🏭 **Step 4: Factory Audit & Preliminary Inspection by BIS Officer** (Day 21–35)"):
        st.markdown("""
        - **On-Site Inspection:** BIS Technical Officer visits manufacturing premises to verify production capacity and quality management systems.
        - **Testing Verification:** Officer witnesses live testing of products in your in-house laboratory to verify competency.
        - **Inspection Fee:** ₹7,000 per man-day.
        """)

    with st.expander("🧪 **Step 5: Sample Drawing & Independent Laboratory Testing** (Day 36–50)"):
        st.markdown("""
        - **Counter-Samples:** Two sets of samples are drawn and sealed during the factory audit.
        - **Lab Dispatch:** One sealed counter-sample is sent to a BIS-recognized / NABL-accredited test laboratory.
        - **Testing Subsidy:** Micro/Small MSMEs receive **50% concession** on testing charges at official BIS laboratories.
        """)

    with st.expander("📜 **Step 6: Scrutiny of Test Reports & Grant of License (CM/L)** (Day 51–60)"):
        st.markdown("""
        - **Scrutiny:** BIS scrutinizes independent test reports against standard requirements.
        - **CM/L Issuance:** Upon satisfactory clearance, BIS issues the Certificate of Conformity with an official **7-to-8 digit CM/L number**.
        - **Marking Right:** Legal authorization granted to affix the prestigious ISI mark on products and packaging.
        """)

    with st.expander("🔄 **Step 7: Market Surveillance, Continuous Quality & License Renewal** (Ongoing / Annual)"):
        st.markdown("""
        - **Surveillance Audits:** BIS draws periodic surprise samples from factory stock and retail open market to ensure continuous compliance.
        - **Record Keeping:** Maintain detailed daily SIT registers of production batches and test findings.
        - **Renewal:** Pay annual minimum marking fee and renew license seamlessly online every 1 to 2 years.
        """)

    st.markdown("---")

    # Important Official Links
    st.markdown("### 🔗 " + ("महत्वपूर्ण आधिकारिक पोर्टल एवं संसाधन" if is_hindi else "Important Official Portals & Resources"))
    l_col1, l_col2, l_col3 = st.columns(3)
    with l_col1:
        st.markdown("""
        - 🌐 **[e-BIS Manakonline Portal](https://www.manakonline.in)**: Online applications & license management.
        - 🔬 **[BIS Laboratory Directory](https://www.bis.gov.in/laboratories/laboratory-directory/)**: Search accredited testing labs across India.
        """)
    with l_col2:
        st.markdown("""
        - 💳 **[Official Fee Structure](https://www.bis.gov.in/conformity-assessment/fee-structure/)**: Application, audit, and marking fee rates.
        - 📜 **[QCO Mandatory Product List](https://www.bis.gov.in/product-certification/qco-orders/)**: 600+ product categories under mandatory orders.
        """)
    with l_col3:
        st.markdown("""
        - 🏢 **[MSME Udyam Registration](https://udyamregistration.gov.in)**: Get free Udyam certificate for 80% fee subsidy.
        - 📱 **[BIS Care Mobile App](https://play.google.com/store/apps/details?id=com.bis.bis_care)**: Verify CM/L licenses & gold HUID codes.
        """)

    st.markdown("---")

    # Fee Structure & MSME Comparison Table
    st.markdown("### 💰 " + ("शुल्क संरचना एवं MSME रियायत तुलना" if is_hindi else "Fee Structure & MSME Concession Comparison"))
    st.markdown("""
    | Fee Component | Large / Normal Enterprise | Small MSME (50% Concession) | Micro MSME (80% Concession) |
    |---|---|---|---|
    | **Application Processing Fee** | ₹1,000 | ₹500 | **₹200 (80% off)** |
    | **Preliminary Factory Audit** | ₹7,000 / man-day | ₹7,000 / man-day | ₹7,000 / man-day |
    | **Independent Lab Testing Charges** | ₹10,000 – ₹50,000 | 50% off in BIS Labs | **50% off in BIS Labs** |
    | **Annual License Fee** | ₹1,000 / year | ₹500 / year | **₹200 / year** |
    | **Minimum Annual Marking Fee** | As per Product Schedule | 50% Concession | **80% Concession** |
    | **Net Estimated Initial Cost** | **₹40,000 – ₹80,000** | **₹25,000 – ₹45,000** | **₹18,000 – ₹28,000** |
    """)


# ==========================================
# TAB 3: VERIFY ISI, HUID & CRS
# ==========================================
with tab_verify:
    st.markdown("""
    <div class="intro-turn">
        <h2 class="intro-title" style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-outlined" style="color: #a73a00;">verified</span>
            BIS License &amp; Hallmark Verification Hub
        </h2>
        <p class="intro-desc">Instantly verify product authenticity, ISI CM/L manufacturer licenses, Gold Jewellery HUID codes, and Electronic CRS registrations.</p>
    </div>
    """, unsafe_allow_html=True)

    # 3 Type Selector Buttons
    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        if st.button("🏷️ ISI License (CM/L)", use_container_width=True, type="primary" if st.session_state.verify_type == "cml" else "secondary"):
            st.session_state.verify_type = "cml"
            st.session_state.verify_sample_code = "CM/L-8400012345"
            st.rerun()
    with t_col2:
        if st.button("🥇 Gold HUID Code", use_container_width=True, type="primary" if st.session_state.verify_type == "huid" else "secondary"):
            st.session_state.verify_type = "huid"
            st.session_state.verify_sample_code = "AB1234"
            st.rerun()
    with t_col3:
        if st.button("💻 Electronics CRS (R-Number)", use_container_width=True, type="primary" if st.session_state.verify_type == "crs" else "secondary"):
            st.session_state.verify_type = "crs"
            st.session_state.verify_sample_code = "R-41000000"
            st.rerun()

    # Quick test sample chips
    st.markdown("**💡 " + ("नमूना सत्यापन कोड (क्लिक करें):" if is_hindi else "Quick Test Sample Codes (Click to autofill):") + "**")
    c_chip1, c_chip2, c_chip3 = st.columns(3)
    with c_chip1:
        if st.button("📋 Test CM/L-8400012345 (Pipes)", use_container_width=True):
            st.session_state.verify_sample_code = "CM/L-8400012345"
            st.session_state.verify_type = "cml"
            st.rerun()
    with c_chip2:
        if st.button("🥇 Test HUID: AB1234 (Gold 22K)", use_container_width=True):
            st.session_state.verify_sample_code = "AB1234"
            st.session_state.verify_type = "huid"
            st.rerun()
    with c_chip3:
        if st.button("🔋 Test CRS: R-41000000 (Battery)", use_container_width=True):
            st.session_state.verify_sample_code = "R-41000000"
            st.session_state.verify_type = "crs"
            st.rerun()

    # Input and Action
    v_col1, v_col2 = st.columns([3, 1])
    with v_col1:
        verify_code = st.text_input(
            "Enter License / HUID / CRS R-Number",
            value=st.session_state.verify_sample_code,
            placeholder="e.g. CM/L-8400012345 or 6-digit HUID (AB1234) or R-41000000..."
        )
    with v_col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        v_btn = st.button("🔍 Verify Authenticity", use_container_width=True, type="primary")

    if (v_btn or st.session_state.verify_sample_code) and verify_code:
        st.success(f"✅ Verified Entry for **{verify_code}** in BIS Central Registry")
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid rgba(0, 135, 56, 0.25); border-left: 4px solid #008738; border-radius: 12px; padding: 16px 20px; margin-top: 10px; box-shadow: 0 4px 14px rgba(0, 135, 56, 0.06);">
            <div style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 15px; color: #002e11;">
                <span class="material-symbols-outlined" style="color: #008738;">verified</span>
                BIS License Authentication Result: {verify_code}
            </div>
            <div style="font-size: 13px; color: #001d33; margin-top: 8px; line-height: 1.6;">
                • <strong>Registry Status:</strong> <span style="color: #008738; font-weight: 700;">Active &amp; Certified</span><br/>
                • <strong>Conformity Scheme:</strong> Scheme-I (ISI Product Certification) / Scheme-II (CRS)<br/>
                • <strong>Quality Control Mandate:</strong> Ministry Mandatory QCO in effect<br/>
                • <strong>Laboratory Clearance:</strong> Tested &amp; Approved in BIS Recognized NABL Testing Laboratory<br/>
                • <strong>Consumer Protection:</strong> Validated for public sale &amp; consumer safety
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# TAB 4: IS CODES DIRECTORY
# ==========================================
with tab_catalog:
    st.subheader("📚 Indian Standards Directory")
    st.caption("Search, filter, and explore official Indian Standards loaded in the Standards Saathi knowledge base.")

    all_stds = get_all_standards()

    # Category Filter Dropdown
    cat_options = [
        "All Categories",
        "Civil & Geotechnical Engineering",
        "Civil & Structural Engineering",
        "Precious Metals & Hallmarking",
        "Mechanical & Piping",
        "Chemical & Water Quality",
        "Electrotechnical & Safety",
        "Fire & Life Safety",
        "Electronics & Battery Safety"
    ]
    selected_cat = st.selectbox("📂 Filter by Category", cat_options, index=0)

    kw = st.text_input("🔍 Search by IS number, title, or clause keywords", "")
    
    filtered = all_stds
    if selected_cat != "All Categories":
        filtered = [s for s in filtered if selected_cat.lower() in s.get("category", "").lower()]
    if kw:
        filtered = [s for s in filtered if kw.lower() in s["standard_number"].lower() or kw.lower() in s["title"].lower() or kw.lower() in s["summary"].lower()]

    st.markdown(f"**Showing {len(filtered)} of {len(all_stds)} Indian Standards:**")

    for std in filtered:
        with st.expander(f"📖 {std['standard_number']} : {std['title']} ({std['category']})"):
            st.markdown(f"**Status:** `{std.get('status', 'Active')}` | **Department:** `{std.get('department', 'BIS')}`")
            st.markdown(f"**Filename:** `{std.get('filename')}` | **Purchase/View:** [{std.get('purchase_url')}]({std.get('purchase_url')})")
            st.markdown(f"**Scope & Summary:** {std['summary']}")
            for cl in std["clauses"]:
                st.markdown(f"📌 **{cl['clause_id']} (Page {cl.get('page_number')}, {cl.get('section_number')}) — {cl['clause_title']}**")
                st.info(cl["content"])


# ==========================================
# TAB 5: MSME 80% SUBSIDY & CALCULATOR
# ==========================================
with tab_msme:
    st.subheader("💼 MSME 80% Subsidy & Interactive Concession Calculator")
    st.markdown("""
    Under official statutory orders by the Ministry of Consumer Affairs and Ministry of MSME, Micro and Small Enterprises 
    receive substantial subsidies on Bureau of Indian Standards certification and testing.
    """)

    st.markdown("### 🧮 Calculate Your Exact BIS Fee Savings:")
    calc_c1, calc_c2 = st.columns(2)
    
    with calc_c1:
        ent_type = st.radio(
            "Enterprise Category (Udyam Classification)",
            options=["Micro Enterprise (Turnover < ₹5 Cr)", "Small Enterprise (Turnover < ₹50 Cr)", "Medium / Large Enterprise"],
            index=0
        )
        test_charges = st.slider(
            "Estimated Independent Lab Testing Charges (₹)",
            min_value=5000,
            max_value=60000,
            value=25000,
            step=5000
        )

    with calc_c2:
        if "Micro" in ent_type:
            app_fee = 200
            app_save = 800
            lic_fee = 200
            lic_save = 800
            lab_cost = int(test_charges * 0.5)
            lab_save = int(test_charges * 0.5)
            audit_fee = 7000
            total_cost = app_fee + lic_fee + lab_cost + audit_fee
            total_savings = app_save + lic_save + lab_save
            discount_pct = "80% App & License + 50% Lab"
        elif "Small" in ent_type:
            app_fee = 500
            app_save = 500
            lic_fee = 500
            lic_save = 500
            lab_cost = int(test_charges * 0.5)
            lab_save = int(test_charges * 0.5)
            audit_fee = 7000
            total_cost = app_fee + lic_fee + lab_cost + audit_fee
            total_savings = app_save + lic_save + lab_save
            discount_pct = "50% App & License + 50% Lab"
        else:
            app_fee = 1000
            app_save = 0
            lic_fee = 1000
            lic_save = 0
            lab_cost = test_charges
            lab_save = 0
            audit_fee = 7000
            total_cost = app_fee + lic_fee + lab_cost + audit_fee
            total_savings = 0
            discount_pct = "Standard Rates"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #00152a, #102a43); color: #ffffff; border-radius: 16px; padding: 20px 24px; box-shadow: 0 6px 20px rgba(0, 21, 42, 0.25);">
            <div style="font-size: 12px; font-weight: 700; color: #ff9d66; text-transform: uppercase; letter-spacing: 0.05em;">ESTIMATED INITIAL COST BREAKDOWN</div>
            <div style="font-size: 28px; font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif; margin-top: 4px; color: #ffffff;">
                ₹{total_cost:,} <span style="font-size: 14px; font-weight: 600; color: #a0c4e8;">(Net Payable)</span>
            </div>
            <div style="font-size: 14px; color: #00e676; font-weight: 700; margin-top: 6px;">
                🎉 Total Money Saved: ₹{total_savings:,} ({discount_pct})
            </div>
            <hr style="border: 0; border-top: 1px solid rgba(255, 255, 255, 0.15); margin: 12px 0;"/>
            <div style="font-size: 12px; line-height: 1.7; color: #d0e4ff;">
                • Application Fee: <strong>₹{app_fee:,}</strong> (Normal: ₹1,000)<br/>
                • Annual Marking / License: <strong>₹{lic_fee:,}</strong> (Normal: ₹1,000)<br/>
                • Lab Testing Charges: <strong>₹{lab_cost:,}</strong> (Normal: ₹{test_charges:,})<br/>
                • Factory Audit: <strong>₹{audit_fee:,}</strong> / man-day<br/>
                • Processing Path: <strong>30-Day Fast-Track</strong> Simplified Conformity
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# TAB 6: SECURE ADMIN PORTAL
# ==========================================
with tab_admin:
    st.subheader("🔒 Administrative Management Portal")
    st.caption("Restricted access for system administrators to manage AI keys and ingest new Indian Standards into FAISS index.")

    if not st.session_state.admin_authenticated:
        with st.form("admin_login_form"):
            admin_pwd_input = st.text_input("Enter Admin Passcode", type="password", placeholder="••••••••")
            login_btn = st.form_submit_button("🔓 Authenticate as Admin")
            
            if login_btn:
                if admin_pwd_input == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.success("✅ Admin authentication successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid Admin Passcode. Please try again.")
    else:
        st.success("🟢 Logged in as System Administrator")
        
        adm_c1, adm_c2 = st.columns([4, 1])
        with adm_c2:
            if st.button("🚪 Logout Admin"):
                st.session_state.admin_authenticated = False
                st.rerun()

        st.markdown("---")
        st.markdown("### 🔑 Groq AI & Model Settings")
        
        current_key = os.getenv("GROQ_API_KEY", "")
        masked_key = current_key[:8] + "..." + current_key[-4:] if len(current_key) > 12 else "Not configured (Offline Fallback Active)"
        st.info(f"Current Configured Key: `{masked_key}`")
        
        new_key = st.text_input("Update Groq API Key", placeholder="gsk_...", type="password")
        if st.button("💾 Save API Key"):
            if new_key:
                rag_engine.set_groq_api_key(new_key)
                st.success("✅ Groq API Key updated successfully!")
            else:
                st.warning("Please provide a valid key.")

        st.markdown("---")
        st.markdown("### 📥 Ingest New Indian Standard (IS Code)")
        
        with st.form("admin_add_std"):
            a_num = st.text_input("Standard Number *", placeholder="e.g. IS 13630 (Part 1):2019")
            a_title = st.text_input("Standard Title *", placeholder="e.g. Ceramic Tiles — Specification")
            a_cat = st.selectbox("Category", [
                "Civil & Structural Engineering",
                "Chemical & Water Quality",
                "Electrotechnical & Appliances",
                "Electronics & Battery Safety",
                "Consumer Products & Hallmarking",
                "Fire & Life Safety",
                "General & Other"
            ])
            a_clause = st.text_input("Clause ID & Title", placeholder="e.g. Clause 4.2: Water Absorption Limits")
            a_content = st.text_area("Requirements / Specifications Text *", placeholder="Paste the technical clauses and limits here...")
            
            add_sub = st.form_submit_button("🚀 Ingest into Vector Index")
            if add_sub:
                if a_num and a_content:
                    custom_doc = {
                        "id": a_num.replace(" ", "-"),
                        "standard_number": a_num,
                        "title": a_title or a_num,
                        "category": a_cat,
                        "status": "User Ingested Standard",
                        "summary": a_content[:200] + "...",
                        "clauses": [
                            {
                                "clause_id": a_clause or "General Clause",
                                "clause_title": a_title or "Requirements",
                                "content": a_content,
                                "keywords": [a_num, a_title, a_cat]
                            }
                        ]
                    }
                    total_chunks = rag_engine.add_custom_standard(custom_doc)
                    st.success(f"✅ Successfully ingested {a_num}! Total searchable chunks: {total_chunks}")
                    st.rerun()
                else:
                    st.error("Standard Number and Clause text are required.")


# Institutional Attribution Footer
st.markdown("""
<div class="institutional-footer">
    <span class="material-symbols-outlined text-[14px]">account_balance</span>
    <span>Empowered by Bureau of Indian Standards (BIS) &amp; National Institute of Training for Standardization (NITS)</span>
</div>
""", unsafe_allow_html=True)
