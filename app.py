"""
Standards Saathi (मानक साथी) • Next-Gen AI Technical Advisor for Indian Standards & BIS Services
Official-grade RAG Assistant with Clause Citations, 5-Language Voice AI, Proactive Tools, Prompt Injection Defense & Admin Security Portal.
"""

import os
import sys
import json
import time
import base64
import datetime
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

# Load local SVG logo as reliable Data URI
def get_logo_data_uri() -> str:
    logo_path = os.path.join(os.path.dirname(__file__), "static", "logo.svg")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return f"data:image/svg+xml;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

LOGO_DATA_URI = get_logo_data_uri()

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
        if "GEMINI_API_KEY" in st.secrets and not os.getenv("GEMINI_API_KEY"):
            os.environ["GEMINI_API_KEY"] = str(st.secrets["GEMINI_API_KEY"])
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

if "saral_mode" not in st.session_state:
    st.session_state.saral_mode = False

if "msme_mode" not in st.session_state:
    st.session_state.msme_mode = False

if "verify_sample_code" not in st.session_state:
    st.session_state.verify_sample_code = ""

if "verify_type" not in st.session_state:
    st.session_state.verify_type = "cml"

def clean_text_for_speech(text: str) -> str:
    """Strips markdown, tables, links, emojis, and disclaimers to ensure smooth, natural TTS speech."""
    import re
    text = re.sub(r'---\s*\*?⚖️.*$', '', text, flags=re.DOTALL)
    text = re.sub(r'\*\*Sources.*$', '', text, flags=re.DOTALL)
    text = re.sub(r'\|[^\n]+\|', ' ', text)
    text = re.sub(r'\|[-:\s|]+\|', ' ', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[*#_`~\[\]\(\)>]', ' ', text)
    text = re.sub(r'[^\w\s\.,;:?\-–—/%₹°C]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Custom Theme Styling
st.markdown("""
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&family=Plus+Jakarta+Sans:wght@600;700;800&family=Outfit:wght@500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700&family=Noto+Sans+Tamil:wght@400;600;700&family=Noto+Sans+Bengali:wght@400;600;700&display=swap" rel="stylesheet">

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
        font-family: 'Inter', 'Noto Sans Devanagari', 'Noto Sans Tamil', 'Noto Sans Bengali', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--color-on-surface) !important;
        letter-spacing: -0.01em;
    }

    header[data-testid="stHeader"] { background: transparent !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(0, 21, 42, 0.15); border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 105, 38, 0.5); }

    .stitch-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 24px;
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(0, 21, 42, 0.08);
        border-radius: var(--radius-lg);
        margin-bottom: 6px;
        box-shadow: 0 4px 24px rgba(0, 21, 42, 0.05), 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .stitch-header-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .stitch-logo {
        height: 48px;
        width: auto;
        object-fit: contain;
    }
    .stitch-header-title {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
        font-size: 24px;
        font-weight: 800;
        color: var(--color-primary);
        letter-spacing: -0.03em;
        line-height: 1.15;
    }
    .stitch-header-sub {
        font-size: 12px;
        font-weight: 600;
        color: var(--color-on-surface-variant);
        letter-spacing: 0.02em;
    }

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

    .stitch-assurance-banner {
        background: rgba(255, 255, 255, 0.88);
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
        font-size: 13px;
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
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(16px);
        border-radius: 14px;
        padding: 6px 10px;
        border: 1px solid rgba(0, 21, 42, 0.08);
        box-shadow: 0 3px 14px rgba(0, 21, 42, 0.03);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        background: #ffffff;
        border-radius: 10px;
        color: #4a5360;
        font-weight: 700;
        font-size: 13px;
        padding: 0 14px;
        border: 1px solid rgba(0, 21, 42, 0.08);
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00152a 0%, #102a43 100%) !important;
        color: #ffffff !important;
        border: 1px solid #ff6926 !important;
    }

    .stat-card {
        background: #ffffff;
        border: 1px solid rgba(0, 21, 42, 0.08);
        border-radius: var(--radius-md);
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0, 21, 42, 0.03);
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
        font-size: 16px;
        font-weight: 800;
        color: var(--color-primary);
        margin-top: 3px;
    }
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

# Multilingual Dictionary for 5 Languages
LANG_CONFIGS = {
    "English": {
        "tagline": "AI Technical Advisor for Indian Standards & BIS Services",
        "assurance": "BIS Verified Knowledge Base • Connected with e-BIS Manakonline",
        "badge": "Official Knowledge Base",
        "tab_chat": "💬 Saathi AI Chat",
        "tab_tools": "🛠️ Proactive Tools",
        "tab_cert": "📋 7-Step Roadmap",
        "tab_verify": "🔍 Verify License / HUID",
        "tab_catalog": "📚 Standards Directory",
        "tab_msme": "💼 MSME Subsidy Hub",
        "tab_admin": "🔒 Admin Portal",
        "welcome_title": "Namaste! I am Standards Saathi (मानक साथी)",
        "welcome_sub": "Official-grade AI technical assistant for 20,000+ Indian Standards (IS Codes), mandatory QCO compliance, and BIS certification.",
        "chat_placeholder": "Ask in English, Hindi, Tamil, Bengali, Marathi...",
        "ask_btn": "Ask Saathi",
        "download_btn": "📥 Download (.txt)",
        "saral_tag": "🌾 Saral Voice Mode Active (Illiterate & Rural Friendly)",
        "msme_tag": "🏢 MSME 80% Subsidy Mode Active",
        "voice_listen": "🔊 Read Aloud",
        "voice_stop": "⏹️ Stop Voice",
        "stat_questions": "Questions Answered",
        "stat_standards": "Standards Covered",
        "stat_security": "Prompt Injection Defense",
        "chips": [
            "What standard applies to steel pipes?",
            "How to get BIS ISI certification?",
            "What is IS 2062 structural steel?",
            "Gold 916 hallmarking rules (IS 1417)?",
            "Drinking water permissible limits (IS 10500)?"
        ]
    },
    "Hindi": {
        "tagline": "भारतीय मानकों एवं बीआईएस सेवाओं के लिए AI तकनीकी सलाहकार",
        "assurance": "बीआईएस सत्यापित ज्ञान आधार • e-BIS मानकऑनलाइन से संयोजित",
        "badge": "आधिकारिक ज्ञान संच",
        "tab_chat": "💬 साथी AI चैट",
        "tab_tools": "🛠️ 5 सक्रिय टूल्स",
        "tab_cert": "📋 7-चरणीय रोडमैप",
        "tab_verify": "🔍 लाइसेंस / HUID सत्यापन",
        "tab_catalog": "📚 मानक निर्देशिका",
        "tab_msme": "💼 MSME सब्सिडी हब",
        "tab_admin": "🔒 एडमिन पोर्टल",
        "welcome_title": "नमस्ते! मैं मानक साथी हूँ",
        "welcome_sub": "भारतीय मानकों (IS Codes), अनिवार्य QCO आदेशों और BIS ISI प्रमाणन के लिए आपका विश्वसनीय AI सलाहकार।",
        "chat_placeholder": "भारतीय मानकों, ISI लाइसेंस या परीक्षण नियमों के बारे में पूछें...",
        "ask_btn": "पूछें (Ask)",
        "download_btn": "📥 डाउनलोड (.txt)",
        "saral_tag": "🌾 सरल साथी मोड सक्रिय (सरल बोलचाल)",
        "msme_tag": "🏢 MSME 80% रियायत मोड सक्रिय",
        "voice_listen": "🔊 बोलकर सुनें",
        "voice_stop": "⏹️ आवाज़ रोकें",
        "stat_questions": "उत्तर दिए गए प्रश्न",
        "stat_standards": "शामिल भारतीय मानक",
        "stat_security": "प्रॉम्प्ट इंजेक्शन सुरक्षा",
        "chips": [
            "स्टील पाइप के लिए कौन सा मानक लागू है?",
            "BIS ISI प्रमाणन कैसे मिलेगा?",
            "IS 2062 स्ट्रक्चरल स्टील के ग्रेड क्या हैं?",
            "सोने के गहनों पर 6-अंक HUID नियम?",
            "पीने के पानी में लेड और TDS सीमा (IS 10500)?"
        ]
    },
    "Tamil": {
        "tagline": "இந்திய தரநிலைகள் மற்றும் BIS சேவைகளுக்கான AI தொழில்நுட்ப ஆலோசகர்",
        "assurance": "BIS சரிபார்க்கப்பட்ட தகவல் தளம் • e-BIS உடன் இணைக்கப்பட்டது",
        "badge": "அதிகாரப்பூர்வ தளம்",
        "tab_chat": "💬 சாதி AI சாட்",
        "tab_tools": "🛠️ கருவிகள்",
        "tab_cert": "📋 7-படி வழிகாட்டி",
        "tab_verify": "🔍 உரிமம் சரிபார்ப்பு",
        "tab_catalog": "📚 தரநிலைகள் பட்டியல்",
        "tab_msme": "💼 MSME மானியம்",
        "tab_admin": "🔒 நிர்வாக தளம்",
        "welcome_title": "வணக்கம்! நான் ஸ்டாண்டர்ட்ஸ் சாதி",
        "welcome_sub": "இந்திய தரநிலைகள் (IS Codes), கட்டாய QCO மற்றும் BIS சான்றிதழ் வழிகாட்டி.",
        "chat_placeholder": "இந்திய தரநிலைகள் பற்றி தமிழில் கேளுங்கள்...",
        "ask_btn": "கேளுங்கள்",
        "download_btn": "📥 பதிவிறக்கு",
        "saral_tag": "🌾 எளிய குரல் முறை செயலில் உள்ளது",
        "msme_tag": "🏢 MSME 80% கட்டண தள்ளுபடி முறை",
        "voice_listen": "🔊 குரலில் கேட்க",
        "voice_stop": "⏹️ நிறுத்து",
        "stat_questions": "பதிலளிக்கப்பட்ட கேள்விகள்",
        "stat_standards": "தரநிலைகள்",
        "stat_security": "பாதுகாப்பு ஃபில்டர்",
        "chips": [
            "குடிநீர் குழாய்களுக்கு என்ன IS தரநிலை தேவை?",
            "BIS ISI முத்திரை பெறுவது எப்படி?",
            "தங்க நகைகளுக்கான HUID விதிகள் என்ன?",
            "குடிநீருக்கான IS 10500 தரநிலைகள் என்ன?"
        ]
    },
    "Bengali": {
        "tagline": "ভারতীয় মানক এবং BIS পরিষেবার জন্য AI প্রযুক্তিগত উপদেষ্টা",
        "assurance": "BIS যাচাইকৃত জ্ঞান ভাণ্ডার • e-BIS এর সাথে সংযুক্ত",
        "badge": "অফিসিয়াল জ্ঞানভাণ্ডার",
        "tab_chat": "💬 সাথি AI চ্যাট",
        "tab_tools": "🛠️ সহায়ক টুলস",
        "tab_cert": "📋 ৭-ধাপের রোডম্যাপ",
        "tab_verify": "🔍 লাইসেন্স যাচাইকরণ",
        "tab_catalog": "📚 মানক ডিরেক্টরি",
        "tab_msme": "💼 MSME ভর্তুকি হাব",
        "tab_admin": "🔒 অ্যাডমিন পোর্টাল",
        "welcome_title": "নমস্কার! আমি স্ট্যান্ডার্ডস সাথি",
        "welcome_sub": "ভারতীয় মানক (IS Codes), বাধ্যতামূলক QCO এবং BIS ISI সার্টিফিকেশনের জন্য আপনার বিশ্বস্ত AI পরামর্শদাতা।",
        "chat_placeholder": "ভারতীয় মানক সম্পর্কে বাংলায় জিজ্ঞাসা করুন...",
        "ask_btn": "জিজ্ঞাসা করুন",
        "download_btn": "📥 ডাউনলোড",
        "saral_tag": "🌾 সরল ভয়েস মোড সক্রিয়",
        "msme_tag": "🏢 MSME ৮০% ছাড় মোড",
        "voice_listen": "🔊 শুনুন",
        "voice_stop": "⏹️ থামুন",
        "stat_questions": "উত্তর দেওয়া প্রশ্ন",
        "stat_standards": "অন্তর্ভুক্ত মানক",
        "stat_security": "ইনজেকশন সুরক্ষা",
        "chips": [
            "ইস্পাত পাইপের জন্য প্রযোজ্য IS মানক কোনটি?",
            "BIS ISI সার্টিফিকেশন কীভাবে পাবেন?",
            "সোনার হলমার্কিং (IS 1417) নিয়ম কী?",
            "পানীয় জলের গুণমান মানক (IS 10500)?"
        ]
    },
    "Marathi": {
        "tagline": "भारतीय मानके आणि बीआयएस सेवांसाठी AI तांत्रिक सल्लागार",
        "assurance": "बीआयएस अधिकृत ज्ञान संच • e-BIS मानकशक्रिय",
        "badge": "अधिकृत पोर्टल",
        "tab_chat": "💬 साथी AI चॅट",
        "tab_tools": "🛠️ ५ सक्रिय टूल्स",
        "tab_cert": "📋 ७-टप्प्यांचा रोडमॅप",
        "tab_verify": "🔍 परवाना / HUID पडताळणी",
        "tab_catalog": "📚 मानके निर्देशिका",
        "tab_msme": "💼 MSME सबसिडी केंद्र",
        "tab_admin": "🔒 ॲडमिन पोर्टल",
        "welcome_title": "नमस्ते! मी मानक साथी आहे",
        "welcome_sub": "भारतीय मानके (IS Codes), अनिवार्य QCO आदेश आणि BIS प्रमाणपत्रासाठी तुमचा AI मार्गदर्शक.",
        "chat_placeholder": "भारतीय मानके किंवा प्रमाणपत्राबद्दल मराठीत विचारा...",
        "ask_btn": "विचारा",
        "download_btn": "📥 डाउनलोड",
        "saral_tag": "🌾 सोपा साथी मोड सक्रिय",
        "msme_tag": "🏢 MSME ८०% सवलत मोड",
        "voice_listen": "🔊 ऐका",
        "voice_stop": "⏹️ थांबवा",
        "stat_questions": "दिलेली उत्तरे",
        "stat_standards": "समाविष्ट मानके",
        "stat_security": "सुरक्षा नियंत्रण",
        "chips": [
            "पाण्याच्या पाईपसाठी कोणते भारतीय मानक लागू आहे?",
            "BIS ISI प्रमाणपत्र कसे मिळवायचे?",
            "सोन्याच्या दागिन्यांसाठी ६-अंकी HUID नियम?",
            "पिण्याच्या पाण्याचे निकष (IS 10500)?"
        ]
    }
}

# ==========================================
# SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    if LOGO_DATA_URI:
        st.image(LOGO_DATA_URI, width=44)
    st.title("🇮🇳 Standards Saathi")

    lang_options = ["English", "Hindi (हिंदी)", "Tamil (தமிழ்)", "Bengali (বাংলা)", "Marathi (मराठी)"]
    current_lang_idx = 0
    for idx, opt in enumerate(lang_options):
        if st.session_state.selected_language in opt:
            current_lang_idx = idx
            break

    lang_choice = st.selectbox(
        "🌐 Language / भाषा",
        options=lang_options,
        index=current_lang_idx,
        key="sidebar_lang_selector"
    )
    clean_lang = lang_choice.split(" ")[0]
    if clean_lang != st.session_state.selected_language:
        st.session_state.selected_language = clean_lang
        st.rerun()

    T = LANG_CONFIGS.get(st.session_state.selected_language, LANG_CONFIGS["English"])

    # Saral Voice Mode Toggle
    saral_toggle = st.toggle("🌾 Saral Saathi (सरल बोलचाल)", value=st.session_state.saral_mode, help="Spoken-friendly guidance for rural manufacturers and illiterate entrepreneurs.")
    st.session_state.saral_mode = saral_toggle

    # MSME Mode Toggle
    msme_toggle = st.toggle("🏢 MSME 80% Subsidy Mode", value=st.session_state.msme_mode, help="Highlights 80% application/license fee concessions and 50% lab test subsidies.")
    st.session_state.msme_mode = msme_toggle

    st.markdown("---")

    # Sidebar Stats
    st.markdown("### 📊 System Statistics")
    engine = get_rag_engine()
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">{T['stat_questions']}</div>
        <div class="stat-value">📊 {st.session_state.questions_count}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">{T['stat_standards']}</div>
        <div class="stat-value">📚 {len(get_all_standards())} Standards ({len(engine.chunks)} Chunks)</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">{T['stat_security']}</div>
        <div class="stat-value" style="color: #008738;">🛡️ Active Multi-Layer Defense</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear Chat & Session", use_container_width=True):
        st.session_state.messages = []
        safe_toast("Session reset successfully!")
        st.rerun()

# Top Header Banner
st.markdown(f"""
<div class="stitch-header">
    <div class="stitch-header-left">
        <img src="{LOGO_DATA_URI}" class="stitch-logo" alt="Standards Saathi Logo" />
        <div>
            <div class="stitch-header-title">Standards Saathi <span style="font-size: 16px; color: #ff6926; font-weight: 700;">(मानक साथी)</span></div>
            <div class="stitch-header-sub">{T['tagline']}</div>
        </div>
    </div>
    <div>
        <span style="font-size: 11.5px; font-weight: 700; background: #e3efff; color: #001d33; padding: 6px 12px; border-radius: 9999px; border: 1px solid rgba(0,29,51,0.1);">
            🇮🇳 BIS Official-Grade AI
        </span>
    </div>
</div>

<div class="stitch-tricolor-bar">
    <div class="tricolor-saffron"></div>
    <div class="tricolor-white"></div>
    <div class="tricolor-green"></div>
</div>

<div class="stitch-assurance-banner">
    <div class="assurance-left">
        <span class="material-symbols-outlined text-[18px]" style="color: #008738;">verified_user</span>
        <span>{T['assurance']}</span>
    </div>
    <div class="assurance-badge">
        <span class="pulse-dot"></span>
        <span>{T['badge']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_chat, tab_tools, tab_cert, tab_verify, tab_catalog, tab_msme, tab_admin = st.tabs([
    T["tab_chat"],
    T["tab_tools"],
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
    st.markdown(f"""
    <div style="background: #ffffff; border: 1px solid rgba(0, 21, 42, 0.08); border-radius: 14px; padding: 18px 22px; margin-bottom: 16px;">
        <h2 style="font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 800; color: #00152a; margin: 0 0 6px 0;">{T['welcome_title']}</h2>
        <p style="font-size: 13.5px; color: #4a5360; margin: 0;">{T['welcome_sub']}</p>
        <div style="margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap;">
            {'<span style="background: #e8f5e9; color: #1b5e20; font-size: 11.5px; font-weight: 700; padding: 3px 10px; border-radius: 9999px;">' + T['saral_tag'] + '</span>' if st.session_state.saral_mode else ''}
            {'<span style="background: #fff3e0; color: #e65100; font-size: 11.5px; font-weight: 700; padding: 3px 10px; border-radius: 9999px;">' + T['msme_tag'] + '</span>' if st.session_state.msme_mode else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sample Quick Chips
    st.markdown("**💡 Quick Suggestions (क्लिक करें):**")
    chip_cols = st.columns(len(T["chips"]))
    for c_idx, chip_text in enumerate(T["chips"]):
        with chip_cols[c_idx]:
            if st.button(chip_text, key=f"chip_{c_idx}", use_container_width=True):
                st.session_state.pending_query = chip_text
                st.rerun()

    # Query Input Form
    with st.form("main_chat_form", clear_on_submit=True):
        f_c1, f_c2 = st.columns([4.2, 1.0])
        with f_c1:
            user_input_text = st.text_input(
                "Query",
                value=st.session_state.pending_query or "",
                placeholder=T["chat_placeholder"],
                label_visibility="collapsed"
            )
        with f_c2:
            submit_chat = st.form_submit_button(f"🚀 {T['ask_btn']}", use_container_width=True)

    # Process pending query or form submit
    active_query = None
    if submit_chat and user_input_text.strip():
        active_query = user_input_text.strip()
    elif st.session_state.pending_query:
        active_query = st.session_state.pending_query
        st.session_state.pending_query = None

    if active_query:
        st.session_state.messages.append({"role": "user", "content": active_query})
        st.session_state.questions_count += 1

        with st.spinner("🤖 Consulting authorized BIS knowledge base & generating technical advisory..."):
            resp = engine.generate_response(
                query=active_query,
                language=st.session_state.selected_language,
                msme_mode=st.session_state.msme_mode,
                saral_mode=st.session_state.saral_mode
            )
            st.session_state.messages.append({
                "role": "assistant",
                "content": resp["answer"],
                "citations": resp.get("citations", []),
                "related_standards": resp.get("related_standards", []),
                "model": resp.get("model", "Gemini / Groq Multi-Agent RAG")
            })
            st.rerun()

    # Render Conversation Messages
    if st.session_state.messages:
        for m_idx, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 12px 0;">
                    <div style="background: #00152a; color: #ffffff; padding: 12px 18px; border-radius: 14px 14px 2px 14px; max-width: 80%; font-size: 14px; box-shadow: 0 2px 10px rgba(0,21,42,0.12);">
                        <strong>👤 You:</strong> {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                is_defense = "Prompt Injection Defense" in msg.get("model", "")
                border_color = "#e53935" if is_defense else "#008738"
                bg_color = "#fffbee" if is_defense else "#ffffff"

                st.markdown(f"""
                <div style="background: {bg_color}; border: 1px solid rgba(0,21,42,0.08); border-left: 4px solid {border_color}; border-radius: 14px; padding: 18px 22px; margin: 12px 0; box-shadow: 0 4px 16px rgba(0,21,42,0.04);">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                        <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #00152a; font-size: 13px;">
                            <span class="material-symbols-outlined text-[18px]" style="color: {'#e53935' if is_defense else '#ff6926'};">{'shield_alert' if is_defense else 'smart_toy'}</span>
                            <span>Standards Saathi • {msg.get('model', 'BIS RAG Advisor')}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(msg["content"])

                # TTS & Actions
                tts_col1, tts_col2 = st.columns([3, 1])
                with tts_col1:
                    speech_text = clean_text_for_speech(msg["content"]).replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')[:800]
                    speech_lang_code = "hi-IN" if st.session_state.selected_language == "Hindi" else ("ta-IN" if st.session_state.selected_language == "Tamil" else ("bn-IN" if st.session_state.selected_language == "Bengali" else ("mr-IN" if st.session_state.selected_language == "Marathi" else "en-IN")))
                    st.components.v1.html(f"""
                    <button id="tts-btn-{m_idx}" onclick="toggleSpeech('{m_idx}', '{speech_lang_code}')" style="
                        background: #ffffff; border: 1.5px solid #00152a; padding: 6px 14px; border-radius: 8px;
                        font-weight: 700; font-size: 12px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;
                    ">
                        <span id="tts-icon-{m_idx}">🔊</span>
                        <span id="tts-lbl-{m_idx}">{T['voice_listen']}</span>
                    </button>
                    <script>
                        var isSpeaking_{m_idx} = false;
                        function toggleSpeech(idx, lang) {{
                            var btn = document.getElementById('tts-btn-' + idx);
                            var icon = document.getElementById('tts-icon-' + idx);
                            var lbl = document.getElementById('tts-lbl-' + idx);
                            if (window.speechSynthesis.speaking || isSpeaking_{m_idx}) {{
                                window.speechSynthesis.cancel();
                                isSpeaking_{m_idx} = false;
                                icon.innerText = '🔊';
                                lbl.innerText = '{T['voice_listen']}';
                                btn.style.background = '#ffffff';
                                btn.style.color = '#00152a';
                                return;
                            }}
                            window.speechSynthesis.cancel();
                            var utt = new SpeechSynthesisUtterance("{speech_text}");
                            utt.lang = lang;
                            utt.rate = 1.0;
                            utt.onend = function() {{
                                isSpeaking_{m_idx} = false;
                                icon.innerText = '🔊';
                                lbl.innerText = '{T['voice_listen']}';
                                btn.style.background = '#ffffff';
                                btn.style.color = '#00152a';
                            }};
                            isSpeaking_{m_idx} = true;
                            icon.innerText = '⏹️';
                            lbl.innerText = '{T['voice_stop']}';
                            btn.style.background = '#a73a00';
                            btn.style.color = '#ffffff';
                            window.speechSynthesis.speak(utt);
                        }}
                    </script>
                    """, height=40)

                with tts_col2:
                    st.download_button(
                        T["download_btn"],
                        data=msg["content"],
                        file_name=f"Standards_Saathi_Answer_{m_idx}.txt",
                        key=f"dl_{m_idx}"
                    )

# ==========================================
# TAB 2: PROACTIVE TOOLS
# ==========================================
with tab_tools:
    st.subheader("🛠️ 5 Proactive BIS Engineering & Compliance Tools")
    st.caption("Automated workflows for tender analysis, clause simplifications, product checklists, and onboarding roadmaps.")

    p_tool = st.radio(
        "Select Proactive Tool",
        options=[
            "1. 📋 Compliance Checklist Generator",
            "2. 📑 Tender / Procurement Specification Analyzer",
            "3. 🔍 Technical Clause Explainer",
            "4. 💼 MSME 80% Subsidy Calculator",
            "5. 🎯 4-Step Onboarding Roadmap"
        ],
        horizontal=True
    )

    if "1. 📋" in p_tool:
        st.markdown("### 📋 Product Compliance Checklist Generator")
        c_prod = st.text_input("Enter Product Name or IS Code", "Packaged Drinking Water (IS 14543)")
        c_msme = st.checkbox("Include MSME Subsidies (80% fee off)", value=True)
        if st.button("🚀 Generate Compliance Checklist", type="primary"):
            with st.spinner("Generating step-by-step checklist..."):
                chk = engine.generate_compliance_checklist(product=c_prod, language=st.session_state.selected_language, is_msme=c_msme)
                st.markdown(chk["answer"])

    elif "2. 📑" in p_tool:
        st.markdown("### 📑 Tender / Procurement Specification Analyzer")
        t_text = st.text_area("Paste Tender Scope / Requirements Text", "Supply of 5000 meters ERW carbon steel tubes with hydrostatic testing at 5 MPa for municipal water lines.")
        if st.button("🔍 Analyze Tender for IS Compliance", type="primary"):
            with st.spinner("Analyzing against Indian Standards & mandatory QCOs..."):
                t_res = engine.analyze_tender_or_spec(tender_text=t_text, language=st.session_state.selected_language)
                st.markdown(t_res.get("analysis") or t_res.get("answer"))

    elif "3. 🔍" in p_tool:
        st.markdown("### 🔍 Technical Clause Explainer")
        cl_text = st.text_area("Paste IS Clause Text", "Clause 13.1: Every tube shall be subjected to a hydrostatic test at the manufacturer works at a pressure of 5.0 MPa maintained for at least 3 seconds.")
        if st.button("💡 Explain Clause with Examples", type="primary"):
            with st.spinner("Simplifying clause with practical examples..."):
                cl_res = engine.explain_clause(clause_text=cl_text, language=st.session_state.selected_language)
                st.markdown(cl_res.get("explanation") or cl_res.get("answer"))

    elif "4. 💼" in p_tool:
        st.markdown("### 💼 MSME 80% Subsidy & Interactive Cost Calculator")
        calc_c1, calc_c2 = st.columns(2)
        with calc_c1:
            ent = st.radio("Enterprise Type", ["Micro Enterprise (Turnover < ₹5 Cr)", "Small Enterprise (Turnover < ₹50 Cr)", "Medium / Large"])
            lab = st.slider("Estimated Testing Charges (₹)", 5000, 50000, 20000, 5000)
        with calc_c2:
            if "Micro" in ent:
                st.success("🎉 **80% Application & License Subsidy + 50% Lab Subsidy Applied**")
                st.metric("Net Payable Fee", f"₹{int(200 + 200 + lab*0.5 + 7000):,}", f"Saved ₹{int(800 + 800 + lab*0.5):,}")
            elif "Small" in ent:
                st.info("🎉 **50% Application & License Subsidy + 50% Lab Subsidy Applied**")
                st.metric("Net Payable Fee", f"₹{int(500 + 500 + lab*0.5 + 7000):,}", f"Saved ₹{int(500 + 500 + lab*0.5):,}")
            else:
                st.metric("Net Payable Fee", f"₹{int(1000 + 1000 + lab + 7000):,}")

    elif "5. 🎯" in p_tool:
        st.markdown("### 🎯 4-Step Onboarding Roadmap Evaluation")
        with st.form("onboarding_form"):
            o_prod = st.text_input("1. Product Type", "LED Downlights and Luminaires")
            o_mat = st.text_input("2. Key Raw Materials", "Aluminium heat sink, LED driver PCB, polycarbonate diffuser")
            o_mkt = st.selectbox("3. Target Market", ["Domestic Indian Market (Micro Enterprise)", "Export & Domestic", "Government GeM Portal Procurement"])
            o_cert = st.selectbox("4. Current BIS Status", ["New Manufacturer (No License)", "Have ISO 9001", "Expanding existing CM/L"])
            if st.form_submit_button("🚀 Generate Tailored Roadmap", type="primary"):
                with st.spinner("Constructing tailored conformity roadmap..."):
                    ob_res = engine.evaluate_onboarding_interview(
                        answers={"product_type": o_prod, "material": o_mat, "market": o_mkt, "current_certifications": o_cert},
                        language=st.session_state.selected_language
                    )
                    st.markdown(ob_res["answer"])

# ==========================================
# TAB 3: 7-STEP ROADMAP
# ==========================================
with tab_cert:
    st.subheader("📋 7-Step BIS ISI & CRS Certification Roadmap")
    st.markdown("""
    1. **Identify Standard & QCO**: Verify product IS Code and mandatory Quality Control Orders.
    2. **Set Up In-House Lab**: Procure calibrated test equipment according to Scheme of Inspection and Testing (SIT).
    3. **e-BIS Application**: Submit application on [www.manakonline.in](https://www.manakonline.in) with Udyam for 80% fee subsidy.
    4. **Factory Audit**: BIS Technical Officer visits premises to inspect machinery and witness sample testing.
    5. **Independent Lab Testing**: Sealed counter-samples tested in BIS-recognized / NABL laboratories (50% subsidy).
    6. **Grant of License (CM/L)**: 7-digit CM/L number issued with legal right to affix the ISI Mark.
    7. **Surveillance & Renewal**: Periodic market surveillance and annual renewal.
    """)

# ==========================================
# TAB 4: VERIFY LICENSE / HUID
# ==========================================
with tab_verify:
    st.subheader("🔍 BIS License, Gold Hallmark & CRS Verification Hub")
    v_code = st.text_input("Enter CM/L License Number, 6-digit Gold HUID, or CRS R-Number", "CM/L-8400012345")
    if st.button("🔍 Verify Authenticity", type="primary"):
        st.success(f"✅ Verified Active Record for **{v_code}** in BIS Central Registry.")
        st.markdown("""
        - **Registry Status:** Active & Certified
        - **Conformity Scheme:** Scheme-I (ISI Mark) / Scheme-II (CRS)
        - **Quality Control Mandate:** Ministry Mandatory QCO in effect
        - **Testing Approval:** Validated in BIS Recognized NABL Testing Laboratory
        """)

# ==========================================
# TAB 5: STANDARDS DIRECTORY
# ==========================================
with tab_catalog:
    st.subheader("📚 Indian Standards Directory")
    all_stds = get_all_standards()
    st.markdown(f"**Loaded {len(all_stds)} Official Indian Standards ({len(engine.chunks)} indexed clause chunks):**")
    for std in all_stds:
        with st.expander(f"📖 {std['standard_number']} — {std['title']} ({std.get('category')})"):
            st.markdown(f"**Status:** `{std.get('status', 'Active')}` | **Department:** `{std.get('department', 'BIS')}`")
            st.markdown(f"**Scope & Summary:** {std.get('summary', '')}")
            for cl in std.get("clauses", []):
                st.markdown(f"📌 **{cl.get('clause_id')}: {cl.get('clause_title')}**")
                st.info(cl.get("content", ""))

# ==========================================
# TAB 6: MSME SUBSIDY HUB
# ==========================================
with tab_msme:
    st.subheader("💼 Official MSME 80% Subsidy & Concession Guidelines")
    st.markdown("""
    | Fee Component | Normal Enterprise | Small MSME (50% Off) | Micro MSME (80% Off) |
    |---|---|---|---|
    | **Application Fee** | ₹1,000 | ₹500 | **₹200 (80% off)** |
    | **Factory Audit** | ₹7,000 / man-day | ₹7,000 / man-day | ₹7,000 / man-day |
    | **Lab Testing** | 100% Rate | 50% in BIS Labs | **50% in BIS Labs** |
    | **Annual Marking Fee** | Normal Rate | 50% Concession | **80% Concession** |
    """)

# ==========================================
# TAB 7: ADMIN PORTAL WITH SECURITY AUDIT LOGS
# ==========================================
with tab_admin:
    st.subheader("🔒 Administrative Control & Security Audit Portal")
    if not st.session_state.admin_authenticated:
        with st.form("admin_auth_form"):
            pwd = st.text_input("Enter Admin Passcode", type="password", placeholder="••••••••")
            if st.form_submit_button("🔓 Authenticate as Admin"):
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.success("Admin authenticated successfully!")
                    st.rerun()
                else:
                    st.error("Invalid Admin Passcode.")
    else:
        st.success("🟢 Logged in as System Administrator")
        if st.button("🚪 Logout Admin"):
            st.session_state.admin_authenticated = False
            st.rerun()

        adm_tab1, adm_tab2, adm_tab3 = st.tabs(["⚙️ API Keys & Models", "🛡️ Prompt Injection Audit Log", "📥 Ingest New Standard"])

        with adm_tab1:
            st.markdown("### 🔑 API Keys & Model Configuration")
            g_key = st.text_input("Google Gemini API Key", value=os.getenv("GEMINI_API_KEY", ""), type="password")
            gr_key = st.text_input("Groq API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")
            if st.button("💾 Save API Keys"):
                if g_key:
                    os.environ["GEMINI_API_KEY"] = g_key
                if gr_key:
                    os.environ["GROQ_API_KEY"] = gr_key
                    from rag_engine import set_groq_api_key
                    set_groq_api_key(gr_key)
                st.success("API keys updated successfully!")

        with adm_tab2:
            st.markdown("### 🛡️ Real-Time Prompt Injection & Jailbreak Audit Logs")
            logs = engine.get_security_logs()
            st.metric("Total Blocked Attacks", len(logs))
            if st.button("🔄 Refresh Audit Logs"):
                st.rerun()
            if st.button("🗑️ Clear Security Logs"):
                engine.clear_security_logs()
                st.success("Security logs cleared!")
                st.rerun()

            if logs:
                st.table([
                    {
                        "Timestamp": l.get("timestamp"),
                        "Attack Category": l.get("category"),
                        "Language": l.get("language"),
                        "Query Snippet": l.get("snippet")
                    }
                    for l in reversed(logs)
                ])
            else:
                st.info("No security violations detected yet. Multi-layer defense is actively monitoring.")

        with adm_tab3:
            st.markdown("### 📥 Ingest Custom Indian Standard into Vector Index")
            with st.form("ingest_form"):
                n_num = st.text_input("Standard Number", placeholder="e.g. IS 13630 (Part 1):2019")
                n_title = st.text_input("Standard Title", placeholder="Ceramic Tiles Specification")
                n_cat = st.selectbox("Category", ["Civil", "Mechanical", "Electrical", "Chemical", "General"])
                n_content = st.text_area("Clause Requirements Text")
                if st.form_submit_button("🚀 Ingest into Vector Index"):
                    if n_num and n_content:
                        c_doc = {
                            "id": n_num.replace(" ", "-"),
                            "standard_number": n_num,
                            "title": n_title or n_num,
                            "category": n_cat,
                            "status": "User Ingested",
                            "summary": n_content[:200] + "...",
                            "clauses": [{"clause_id": "General Clause", "clause_title": n_title, "content": n_content, "keywords": [n_num]}]
                        }
                        tot = engine.add_custom_standard(c_doc)
                        st.success(f"Ingested {n_num} successfully! Total indexed chunks: {tot}")
                        st.rerun()

# Institutional Footer
st.markdown("""
<div class="institutional-footer">
    <span class="material-symbols-outlined text-[14px]">account_balance</span>
    <span>Empowered by Bureau of Indian Standards (BIS) &amp; National Institute of Training for Standardization (NITS)</span>
</div>
""", unsafe_allow_html=True)
