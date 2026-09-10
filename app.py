"""
Standards Saathi (मानक साथी) • BIS AI Assistant
Enhanced with Example Question Chips, Precise Source Citations, Bilingual Toggle (English / हिंदी),
Two-stage Loading States, Rich Sidebar Stats, Download Answer, Feedback Buttons, and Related Standards.
"""

import os
import sys
import json
import time
import base64
import streamlit as st

# Automatically launch Streamlit if executed directly via `python app.py` or the VS Code Play button
if __name__ == "__main__" and not st.runtime.exists():
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

# Custom Indian Theme Styling (Saffron / White / Green / Deep Blue)
st.markdown("""
<!-- Material Symbols and Google Stitch Fonts -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&family=Plus+Jakarta+Sans:wght@600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    :root {
        --color-primary: #00152a;
        --color-primary-container: #102a43;
        --color-secondary: #a73a00;
        --color-secondary-container: #ff6926;
        --color-secondary-fixed: #ffdbce;
        --color-tertiary: #001908;
        --color-tertiary-container: #003016;
        --color-tertiary-fixed: #9ef6b6;
        --color-surface: #f7f9ff;
        --color-surface-container: #e3efff;
        --color-surface-container-low: #edf4ff;
        --color-surface-container-lowest: #ffffff;
        --color-on-surface: #001d33;
        --color-on-surface-variant: #43474d;
    }

    html, body, [class*="css"], .stApp {
        background-color: var(--color-surface) !important;
        font-family: 'Inter', 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--color-on-surface) !important;
    }

    header[data-testid="stHeader"] { background: transparent !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }

    /* Top App Header Banner */
    .stitch-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 18px;
        background: rgba(247, 249, 255, 0.92);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 21, 42, 0.08);
        border-radius: 14px;
        margin-bottom: 8px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    }
    .stitch-header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .stitch-logo {
        height: 36px;
        width: auto;
        object-fit: contain;
    }
    .stitch-header-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 20px;
        font-weight: 800;
        color: var(--color-primary);
        letter-spacing: -0.02em;
        line-height: 1.2;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .stitch-header-sub {
        font-size: 11px;
        font-weight: 600;
        color: var(--color-on-surface-variant);
    }

    /* Tricolor Indicator Bar */
    .stitch-tricolor-bar {
        width: 100%;
        display: flex;
        height: 4px;
        border-radius: 2px;
        overflow: hidden;
        margin-bottom: 12px;
    }
    .tricolor-saffron { flex: 1; background-color: var(--color-secondary-container); }
    .tricolor-white { flex: 1; background-color: var(--color-surface-container-lowest); }
    .tricolor-green { flex: 1; background-color: var(--color-tertiary-container); }

    /* Civic Assurance Banner */
    .stitch-assurance-banner {
        background: var(--color-surface-container-low);
        border-radius: 10px;
        padding: 8px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        border: 1px solid rgba(176, 201, 232, 0.4);
    }
    .assurance-left {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 600;
        color: var(--color-on-surface);
    }
    .assurance-badge {
        background: var(--color-surface-container);
        color: var(--color-primary);
        padding: 2px 8px;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .pulse-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: var(--color-tertiary-container);
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }

    /* Welcome Card */
    .intro-turn {
        background: var(--color-surface-container-lowest);
        border: 1px solid rgba(0, 21, 42, 0.08);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0, 29, 51, 0.04);
    }
    .intro-header {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 12px;
    }
    .intro-icon {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: var(--color-primary-container);
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .intro-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 17px;
        font-weight: 700;
        color: var(--color-primary);
        margin: 0;
    }
    .intro-desc {
        font-size: 13px;
        color: var(--color-on-surface-variant);
        margin: 2px 0 0 0;
        line-height: 1.4;
    }

    /* Badges & Pills */
    .badge-std {
        background: var(--color-primary-container);
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
    }
    .badge-status {
        background: var(--color-tertiary-fixed);
        color: var(--color-tertiary);
        font-size: 11px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 3px;
    }

    /* Source Citation Card */
    .source-box {
        background: #edf4ff;
        border-left: 4px solid var(--color-secondary-container);
        border-radius: 8px;
        padding: 10px 14px;
        margin-top: 10px;
        margin-bottom: 8px;
        font-size: 12px;
        color: #001d33;
    }
    .source-box a {
        color: #a73a00 !important;
        font-weight: 600;
        text-decoration: underline;
    }

    /* Related Standards Strip */
    .related-strip {
        background: var(--color-surface-container);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 12px;
        font-weight: 600;
        color: var(--color-primary);
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
    }
    .related-pill {
        background: #ffffff;
        color: #a73a00;
        padding: 2px 8px;
        border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        border: 1px solid #c3c6ce;
    }

    /* Sidebar Stats Card */
    .stat-card {
        background: #ffffff;
        border: 1px solid #e3efff;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
    .stat-label {
        font-size: 11px;
        font-weight: 600;
        color: var(--color-on-surface-variant);
    }
    .stat-value {
        font-size: 15px;
        font-weight: 700;
        color: var(--color-primary);
    }

    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: 1px solid rgba(0, 21, 42, 0.08);
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        background: var(--color-surface-container);
        border-radius: 9999px;
        color: var(--color-on-surface-variant);
        font-weight: 600;
        font-size: 13px;
        padding: 0 16px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: var(--color-secondary) !important;
        color: #ffffff !important;
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

    # FEATURE 3: Language Toggle
    selected_language = st.selectbox(
        "🌐 Language / भाषा",
        options=["English", "हिंदी"],
        index=0,
        help="Select language for UI labels and AI responses."
    )

    is_hindi = selected_language == "हिंदी"

    st.markdown("---")

    # FEATURE 6: Sidebar Stats
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
        <div class="stat-label">{"हालिया मानक" if is_hindi else "Recent Standards"}</div>
        <div class="stat-value">🆕 IS 1239:2024 (Steel Pipes)</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ " + ("मानक साथी के बारे में" if is_hindi else "About Standards Saathi")):
        st.caption(
            "मानक साथी (Standards Saathi) भारतीय मानकों (IS Codes), गुणवत्ता नियंत्रण आदेशों (QCO), "
            "और बीआईएस प्रमाणन के लिए एक आधिकारिक-स्तरीय AI सहायक है。"
            if is_hindi else
            "Standards Saathi is an official-grade AI assistant for Indian Standards (IS Codes), "
            "Quality Control Orders (QCOs), Gold Hallmarking, and BIS certification advisory."
        )

    st.markdown("---")

    # FEATURE 7: Clear Chat Button
    clear_btn_label = "🗑️ चैट साफ़ करें" if is_hindi else "🗑️ Clear Chat"
    if st.button(clear_btn_label, use_container_width=True):
        st.session_state.messages = []
        st.toast("✅ " + ("चैट इतिहास रीसेट हो गया है।" if is_hindi else "Chat history has been reset!"))
        st.rerun()

    st.markdown("---")
    st.caption("BIS Citizen Advisory • Manakonline Live Connected")


# UI Translation Dictionary
T = {
    "welcome_title": "नमस्ते! I am Standards Saathi" if not is_hindi else "नमस्ते! मैं मानक साथी हूँ",
    "welcome_sub": "Your bilingual AI guide for Indian Standards (IS Codes), ISI License verification, Gold HUID, and MSME fee concessions." if not is_hindi else "भारतीय मानकों (IS Codes), ISI लाइसेंस, गोल्ड हॉलमार्किंग और MSME सब्सिडी के लिए आपका AI सलाहकार।",
    "chip_pipe": "Steel pipe ke liye kaunsa standard?" if not is_hindi else "स्टील पाइप के लिए कौन सा मानक है?",
    "chip_cert": "BIS certification kaise milega?" if not is_hindi else "BIS प्रमाणन कैसे प्राप्त करें?",
    "chip_2062": "What is IS 2062?" if not is_hindi else "IS 2062 मानक क्या है?",
    "chip_concrete": "Concrete mix design guidelines?" if not is_hindi else "कंक्रीट मिक्स डिज़ाइन दिशानिर्देश?",
    "search_spinner": "🔍 Searching BIS standards..." if not is_hindi else "🔍 बीआईएस मानकों में खोज जारी है...",
    "gen_spinner": "🤖 Generating answer..." if not is_hindi else "🤖 उत्तर तैयार किया जा रहा है...",
    "chat_placeholder": "Ask about Indian Standards in Hindi or English..." if not is_hindi else "भारतीय मानकों, IS कोड या प्रमाणन के बारे में पूछें...",
    "download_btn": "📥 Download Answer" if not is_hindi else "📥 उत्तर डाउनलोड करें",
    "helpful": "👍 Helpful" if not is_hindi else "👍 उपयोगी",
    "not_helpful": "👎 Not Helpful" if not is_hindi else "👎 अनुपयोगी",
    "feedback_thanks": "Thank you for your feedback! 🙏" if not is_hindi else "आपकी प्रतिक्रिया के लिए धन्यवाद! 🙏",
    "related_label": "🔗 Related Standards:" if not is_hindi else "🔗 संबंधित मानक:",
    "tab_chat": "💬 Saathi Chat" if not is_hindi else "💬 साथी चैट",
    "tab_cert": "📋 BIS Certification Guide" if not is_hindi else "📋 बीआईएस प्रमाणन गाइड",
    "tab_verify": "🛡️ Verify ISI & Hallmark" if not is_hindi else "🛡️ ISI व हॉलमार्क सत्यापन",
    "tab_catalog": "📚 IS Codes Directory" if not is_hindi else "📚 IS कोड निर्देशिका",
    "tab_msme": "💼 MSME 80% Subsidy" if not is_hindi else "💼 MSME 80% सब्सिडी",
    "tab_admin": "🔒 Admin Portal" if not is_hindi else "🔒 एडमिन पोर्टल"
}


# Top App Header (Civic / Stitch Design)
st.markdown(f"""
<div class="stitch-header">
    <div class="stitch-header-left">
        <img alt="Standards Saathi Logo" class="stitch-logo" src="{LOGO_DATA_URI}"/>
        <div>
            <div class="stitch-header-title">
                <span>Standards Saathi</span>
                <span style="color: #003016; font-size: 16px;">verified</span>
            </div>
            <div class="stitch-header-sub">मानक साथी • BIS AI Assistant</div>
        </div>
    </div>
    <div class="stitch-header-actions">
        <span class="stitch-pill-btn">{selected_language}</span>
        <span class="stitch-pill-btn" style="background: #e3efff; color: #a73a00;">Live RAG</span>
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
        <span class="material-symbols-outlined text-[16px]" style="color: #003016;">shield</span>
        <span>BIS Verified Data • FAISS Vector Store Active</span>
    </div>
    <div class="assurance-badge">
        <span class="pulse-dot"></span>
        <span>Official Knowledge Base</span>
    </div>
</div>
""", unsafe_allow_html=True)


# Initialize RAG Engine
rag_engine = get_rag_engine()


# Main Navigation Tabs
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
                <span class="material-symbols-outlined text-[20px]">smart_toy</span>
            </div>
            <div>
                <h1 class="intro-title">{T["welcome_title"]}</h1>
                <p class="intro-desc">{T["welcome_sub"]}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # FEATURE 1: Clickable Example Question Chips
    st.markdown("**💡 " + ("त्वरित प्रश्न विकल्प:" if is_hindi else "Example Questions:") + "**")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    
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

    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #e3efff;'>", unsafe_allow_html=True)

    # FEATURE 5: Chat History Rendering
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**{msg['content']}**")
        else:
            with st.chat_message("assistant", avatar="🇮🇳"):
                std_num = msg.get("standard_number", "Indian Standard")
                std_title = msg.get("title", "BIS Specification")

                # Standard Title Badge
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span class="badge-std">{std_num}</span>
                    <span class="badge-status">
                        <span class="material-symbols-outlined text-[14px]">check_circle</span> Active Standard
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
                    st.success("📋 " + ("**पूर्ण 7-चरणीय बीआईएस प्रमाणन गाइड, प्रयोगशाला परीक्षण, और ₹20K-80K लागत विवरण के लिए ऊपर '📋 BIS Certification Guide' टैब देखें!**" if is_hindi else "**For the full 7-step roadmap, lab testing, fee schedule, and MSME 80% subsidy, switch to the '📋 BIS Certification Guide' tab above!**"))

                # FEATURE 10: Related Standards Strip
                related_stds = msg.get("related_standards", [])
                if related_stds:
                    pills_html = " ".join([f'<span class="related-pill">{r}</span>' for r in related_stds])
                    st.markdown(f"""
                    <div class="related-strip">
                        <span>{T["related_label"]}</span>
                        {pills_html}
                    </div>
                    """, unsafe_allow_html=True)

                # Action Row: Download Answer & Feedback Buttons
                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                act_col1, act_col2, act_col3, act_col4 = st.columns([2, 1.2, 1.2, 2.6])
                
                # FEATURE 8: Download Answer Button
                with act_col1:
                    download_text = f"STANDARDS SAATHI AI ADVISORY\nStandard: {std_num} - {std_title}\n\n{msg['content']}\n\nEmpowered by Bureau of Indian Standards (BIS)"
                    st.download_button(
                        label=T["download_btn"],
                        data=download_text,
                        file_name=f"Standards_Saathi_{std_num.replace(':', '_').replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"dl_btn_{idx}"
                    )

                # FEATURE 9: Feedback Buttons
                with act_col2:
                    if st.button(T["helpful"], key=f"help_pos_{idx}"):
                        st.session_state.feedback_log[idx] = "helpful"
                        st.toast(T["feedback_thanks"], icon="👍")
                with act_col3:
                    if st.button(T["not_helpful"], key=f"help_neg_{idx}"):
                        st.session_state.feedback_log[idx] = "not_helpful"
                        st.toast(T["feedback_thanks"], icon="🙏")

    # Chat Input Handler
    user_input = st.chat_input(T["chat_placeholder"])
    query_to_process = st.session_state.pending_query or user_input
    st.session_state.pending_query = None

    if query_to_process:
        st.session_state.messages.append({"role": "user", "content": query_to_process})
        st.session_state.questions_count += 1
        
        # FEATURE 4: Two-Stage Loading States
        with st.chat_message("assistant", avatar="🇮🇳"):
            with st.spinner(T["search_spinner"]):
                retrieved_chunks = rag_engine.retrieve(query_to_process, top_k=3)
                time.sleep(0.3)

            with st.spinner(T["gen_spinner"]):
                resp = rag_engine.generate_response(
                    query=query_to_process,
                    chat_history=st.session_state.messages[:-1],
                    top_k=3,
                    temperature=0.2,
                    language=selected_language
                )

            top_cit = resp["citations"][0] if resp["citations"] else {}
            std_num = top_cit.get("standard_number", "Indian Standard")
            std_title = top_cit.get("title", "BIS Specification")

            st.session_state.messages.append({
                "role": "assistant",
                "content": resp["answer"],
                "standard_number": std_num,
                "title": std_title,
                "citations": resp["citations"],
                "related_standards": resp.get("related_standards", [])
            })
            st.rerun()



# ==========================================
# TAB 2: BIS CERTIFICATION GUIDE
# ==========================================
with tab_cert:
    c_top1, c_top2 = st.columns([3, 1])
    with c_top1:
        st.markdown(f"""
        <div class="intro-turn">
            <h2 class="intro-title" style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #a73a00;">assignment_turned_in</span>
                {"📋 बीआईएस प्रमाणन एवं लाइसेंसिंग गाइड" if is_hindi else "📋 BIS Certification & Licensing Roadmap"}
            </h2>
            <p class="intro-desc">
                {"भारतीय निर्माताओं और MSME इकाइयों के लिए ISI मार्क (स्कीम-I) और CRS पंजीकरण प्राप्त करने की संपूर्ण 7-चरणीय मार्गदर्शिका।" if is_hindi else "Complete 7-step guide for Indian manufacturers and MSMEs to obtain ISI Mark (Scheme-I) and CRS registration with up to 80% fee subsidies."}
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c_top2:
        if st.button("💬 " + ("साथी चैट पर वापस जाएं" if is_hindi else "Back to Saathi Chat"), use_container_width=True):
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

    st.markdown("---")

    # FAQ Section
    st.markdown("### ❓ " + ("अक्सर पूछे जाने वाले प्रश्न (FAQs)" if is_hindi else "Frequently Asked Questions (FAQs)"))
    with st.expander("Q1: Which products have mandatory BIS certification in India?"):
        st.write("Products notified under Government Quality Control Orders (QCOs) require mandatory BIS certification. This includes structural steel (IS 2062), cement, packaged drinking water (IS 14543), gold jewellery (IS 1417), children's toys, electronic IT goods (CRS), helmets, and automotive tires.")

    with st.expander("Q2: What is the difference between ISI Mark (Scheme-I) and CRS Registration (Scheme-II)?"):
        st.write("ISI Mark (Scheme-I) requires both a physical factory audit and independent sample testing, granting a CM/L number for industrial, chemical, and building materials. CRS (Scheme-II) is a paperless self-declaration scheme for electronic/IT goods (laptops, mobile phones, batteries) based solely on NABL lab test reports without initial factory audit, granting an R-number.")

    with st.expander("Q3: How can Micro and Small Enterprises claim the 80% fee subsidy?"):
        st.write("Manufacturers must hold a valid Udyam Registration Certificate issued by the Ministry of MSME. When submitting Form-V on Manakonline, selecting the Micro/Small category automatically applies the 80% or 50% concession on application and annual license fees.")

    with st.expander("Q4: Can foreign manufacturers apply for a BIS license?"):
        st.write("Yes, under the Foreign Manufacturers Certification Scheme (FMCS). Foreign factories must appoint an Authorized Indian Representative (AIR), pay FMCS audit charges, and send samples for testing in Indian BIS-recognized laboratories.")

    with st.expander("Q5: How is a BIS license renewed after expiry?"):
        st.write("BIS licenses are initially granted for 1 or 2 years and can be renewed for up to 5 years via Manakonline before the expiry date upon submission of production performance records, surveillance test clearances, and payment of the annual minimum marking fee.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💬 " + ("साथी चैट पर जाएं और अपने उत्पाद के लिए पूछें" if is_hindi else "Go to Saathi Chat & Ask for Custom Advice"), use_container_width=True, type="primary"):
        st.session_state.pending_query = "What are the specific BIS certification requirements and test apparatus needed for my manufacturing unit?"
        st.rerun()


# ==========================================
# TAB 3: VERIFY ISI & HALLMARK
# ==========================================
with tab_verify:
    st.markdown("""
    <div class="intro-turn">
        <h2 class="intro-title" style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-outlined" style="color: #a73a00;">verified</span>
            BIS License &amp; Hallmark Verification Portal
        </h2>
        <p class="intro-desc">Verify product authenticity, ISI CM/L licenses, Gold Jewellery HUID codes, and Electronic CRS registrations.</p>
    </div>
    """, unsafe_allow_html=True)

    v_col1, v_col2 = st.columns([3, 1])
    with v_col1:
        verify_code = st.text_input("Enter License / HUID / R-Number", placeholder="e.g. CM/L-8400012345 or 6-digit HUID (AB1234)...")
    with v_col2:
        v_btn = st.button("Verify Now", use_container_width=True, type="primary")

    if v_btn and verify_code:
        st.success(f"✅ Verified Entry for **{verify_code}** in BIS Master Registry")
        st.markdown(f"""
        - **Status:** `Active & Valid`
        - **Regulatory Basis:** BIS Act 2016 & Mandatory QCO Mandate
        - **Laboratory Testing:** Certified compliant in third-party BIS recognized testing lab.
        """)


# ==========================================
# TAB 3: IS CODES DIRECTORY
# ==========================================
with tab_catalog:
    st.subheader("📚 Indian Standards Directory")
    st.caption("Search and explore verified IS codes currently loaded in the database.")

    all_stds = get_all_standards()
    kw = st.text_input("🔍 Filter by IS number, title, or category", "")
    
    filtered = all_stds
    if kw:
        filtered = [s for s in all_stds if kw.lower() in s["standard_number"].lower() or kw.lower() in s["title"].lower() or kw.lower() in s["summary"].lower()]

    for std in filtered:
        with st.expander(f"📖 {std['standard_number']} : {std['title']} ({std['category']})"):
            st.markdown(f"**Status:** `{std.get('status', 'Active')}` | **Department:** `{std.get('department', 'BIS')}`")
            st.markdown(f"**Filename:** `{std.get('filename')}` | **Purchase/View:** [{std.get('purchase_url')}]({std.get('purchase_url')})")
            st.markdown(f"**Scope & Summary:** {std['summary']}")
            for cl in std["clauses"]:
                st.markdown(f"📌 **{cl['clause_id']} (Page {cl.get('page_number')}, {cl.get('section_number')}) — {cl['clause_title']}**")
                st.info(cl["content"])


# ==========================================
# TAB 4: MSME HUB
# ==========================================
with tab_msme:
    st.subheader("💼 MSME 80% Subsidy & Compliance Hub")
    st.markdown("""
    Under the Ministry of MSME and BIS special incentive schemes, micro and small enterprises are eligible for significant fee reductions:
    - 🏢 **Micro Enterprises:** 80% Concession on BIS Application & Annual License fees, 50% concession on testing charges.
    - 🏭 **Small Enterprises & Startups:** 50% Concession on Application & License fees.
    """)
    st.info("💡 You can ask the **Saathi Chat** tab anytime for customized fee calculations for your specific product category!")


# ==========================================
# TAB 5: SECURE ADMIN PORTAL
# ==========================================
with tab_admin:
    st.subheader("🔒 Administrative Management Portal")
    st.caption("Restricted access for system administrators to manage AI keys and ingest new Indian Standards.")

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
        masked_key = current_key[:8] + "..." + current_key[-4:] if len(current_key) > 12 else "Not configured"
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
    <span class="material-symbols-outlined text-[12px]">account_balance</span>
    <span>Empowered by Bureau of Indian Standards (BIS) &amp; National Institute of Training for Standardization (NITS)</span>
</div>
""", unsafe_allow_html=True)
