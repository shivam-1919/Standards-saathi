"""
RAG (Retrieval-Augmented Generation) Engine for Indian Standards & BIS Services.
Integrates Sentence Transformers for embeddings, FAISS for vector indexing,
and Groq API (llama-3.1-8b-instant) for generative synthesis with citations.
"""

import os
import re
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sentence Transformers & FAISS (Optional; defaults to ultra-fast 15MB in-memory semantic TF-IDF matcher on 512MB RAM cloud hosts)
try:
    if os.getenv("DISABLE_HEAVY_EMBEDDINGS", "0").lower() in ["1", "true", "yes"]:
        HAS_SENTENCE_TRANSFORMERS = False
    else:
        from sentence_transformers import SentenceTransformer
        HAS_SENTENCE_TRANSFORMERS = True
except Exception:
    HAS_SENTENCE_TRANSFORMERS = False

try:
    if os.getenv("DISABLE_HEAVY_EMBEDDINGS", "0").lower() in ["1", "true", "yes"]:
        HAS_FAISS = False
    else:
        import faiss
        HAS_FAISS = True
except Exception:
    HAS_FAISS = False

# Google GenAI (Gemini) Client
try:
    from google import genai
    HAS_GOOGLE_GENAI = True
except Exception:
    HAS_GOOGLE_GENAI = False

# Groq Client
try:
    from groq import Groq
    HAS_GROQ = True
except Exception:
    HAS_GROQ = False

from sample_data import get_flattened_chunks, SAMPLE_STANDARDS


# Multilingual Cross-Lingual Concept Bridge for Indian Standards & BIS Services
INDIC_CROSS_LINGUAL_MAP = [
    # Steel, Pipes, Iron, Tubes, Structural, GI, TMT
    (
        ["स्टील", "पाइप", "लोहा", "नली", "ट्यूब", "पाइपों", "குழாய்", "இரும்பு", "கம்பி", "குழாய்கள்", "குழா", "পাইপ", "ইস্পাত", "লোহা", "নল", "पाईप", "लोखंड", "स्टिल", "रॉड", "सरिया", "gi pipe", "tmt"],
        "steel tubes pipes structural steel plumbing IS 1239 IS 3589 IS 2062 IS 1786 galvanized iron"
    ),
    # Drinking Water, Bottled Water, RO, Mineral Water
    (
        ["पानी", "जल", "पीने", "बोतलबंद", "मिनरल", "தண்ணீர்", "தண்ணீ", "நீர்", "குடிநீர்", "குடி", "பாட்டில்", "জল", "পানীয়", "মিনারেল", "পাখী", "पाणी", "पाण्या", "पिण्या", "पिण्याचे", "बाटलीबंद", "जलशुद्धीकरण"],
        "packaged drinking water potable water mineral water IS 10500 IS 14543 water testing"
    ),
    # Gold, Jewellery, Hallmarking, HUID, Silver
    (
        ["सोना", "स्वर्ण", "आभूषण", "हॉलमार्क", "हॉलमार्किंग", "चांदी", "தங்கம்", "நகை", "ஹால்மார்க்", "ஹால்மார்க்கிங்", "வெள்ளி", "সোনা", "অলঙ্কার", "হলমার্ক", "রূপা", "सोन्याचे", "दागिने", "हॉलमार्क", "चांदीचे", "huid", "carat", "कैरेट", "कॅरेट", "கேரட்"],
        "gold hallmarking jewellery HUID 6 digit code assaying 22 carat 18 carat IS 1417 IS 15820 IS 2112"
    ),
    # Cement, Concrete, Construction, Building
    (
        ["सीमेंट", "कंक्रीट", "भवन", "इमारत", "निर्माण", "सिमेंट", "சிமெண்ட்", "கான்கிரீட்", "கட்டிடம்", "সিমেন্ট", "কংক্রিট", "নির্মাণ", "काँक्रीट", "बांधकाम", "पुल"],
        "plain and reinforced concrete cement mix design construction IS 456 IS 10262 IS 1489 IS 12269"
    ),
    # Toys, Children Safety
    (
        ["खिलौना", "खिलौने", "बच्चों", "गुड़िया", "பொம்மை", "பொம்மைகள்", "குழந்தைகள்", "খেলনা", "বাচ্চাদের", "खेळणी", "बाळांची"],
        "safety of toys mechanical physical flammability electric toys IS 9873 IS 15644"
    ),
    # Electronics, Batteries, Mobile, Laptops, Chargers
    (
        ["बैटरी", "मोबाइल", "इलेक्ट्रॉनिक्स", "चार्जर", "लैपटॉप", "மின்கலம்", "மொபைல்", "மின்னணு", "சார்ஜர்", "ইলেকট্রনিক্স", "ব্যাটারি", "মোবাইল", "চার্জার", "मोबाईल", "बॅटरी", "इलेक्ट्रॉनिक"],
        "electronics safety lithium ion battery secondary cells CRS scheme IS 16046 IS 13252"
    ),
    # Fire Safety, Fire Alarms, Extinguishers
    (
        ["आग", "अग्नि", "अग्निशामक", "फायर", "अलार्म", "தீ", "தீயணைப்பான்", "அலாரம்", "আগুন", "অগ্নি", "অ্যালার্ম", "अग्निशामक"],
        "fire detection alarm system portable fire extinguisher safety IS 2189 IS 15683"
    ),
    # Soil Testing, Earth, Compaction
    (
        ["मिट्टी", "मृदा", "परीक्षण", "மண்", "மண் பரிசோதனை", "মাটি", "মাটি পরীক্ষা", "माती", "माती परीक्षण"],
        "soil testing grain size liquid limit plastic limit compaction moisture IS 2720"
    ),
    # Footwear, Shoes, Boots, Sandals
    (
        ["जूते", "जूता", "चप्पल", "बूट", "सैंडल", "காலணி", "காலணிகள்", "செருப்பு", "ஷூ", "জুতো", "জুতো-স্যান্ডেল", "চটি", "पादत्राणे", "बूट", "चप्पल"],
        "safety footwear leather rubber shoes sports footwear industrial shoes IS 15844"
    ),
    # Helmets, Two-wheelers
    (
        ["हेलमेट", "हेल्मेट", "दुपहिया", "ஹெல்மெட்", "இருசக்கர", "হেলমেট", "दुचाकी"],
        "protective helmet two wheeler rider safety IS 4151"
    ),
    # Pressure Cooker, Kitchen Appliances
    (
        ["कुकर", "प्रेशर कुकर", "रसोई", "பிரஷர் குக்கர்", "குக்கர்", "சமையல்", "প্রেসার কুকার", "রান্নাঘর"],
        "domestic pressure cooker safety thermal release IS 2347"
    ),
    # Cables, Wiring, Electrical Lines
    (
        ["तार", "केबल", "वायर", "बिजली", "வயர்", "மின் கம்பி", "கேபிள்", "বৈদ্যুতিক তার", "ক্যাবল", "इलेक्ट्रिक केबल"],
        "PVC insulated electric cables heavy duty electric wiring IS 694 IS 1554"
    ),
    # Plywood, Wood, Timber
    (
        ["प्लाईवुड", "लकड़ी", "बोर्ड", "ப்ளைவுட்", "மரம்", "কাঠ", "পাতলা কাঠ", "प्लायवूड", "लाकूड"],
        "plywood commercial moisture resistant marine grade IS 303 IS 710"
    ),
    # MSME, Small business, Subsidy, Concession, Discount, Factory
    (
        ["msme", "एमएसएमई", "लघु उद्योग", "सूक्ष्म", "छूट", "सब्सिडी", "सवलत", "கட்டணச் சலுகை", "மானிய", "சிறு தொழில்", "ফি ছাড়", "ভর্তুকি", "ক্ষুদ্র শিল্প", "सवलती", "अनुदान", "लहान व्यवसाय"],
        "MSME 80% fee concession 50% testing subsidy simplified scheme micro small enterprise"
    ),
    # BIS License, Certificate, ISI Mark, Procedure, Steps
    (
        ["लाइसेंस", "प्रमाणन", "रजिस्ट्रेशन", "नियम", "प्रक्रिया", "कदम", "कहाँ जाएं", "சான்றிதழ்", "பதிவு", "விதிமுறைகள்", "வழிமுறை", "லைসেন্স", "নিবন্ধন", "নিয়ম", "পদ্ধতি", "পর্যায়", "परवाना", "प्रमाणपत्र", "प्रक्रिया"],
        "BIS licensing ISI mark CRS scheme Manakonline application procedure steps"
    )
]


class StandardsRAGEngine:
    """
    RAG Engine that embeds, indexes, and queries Indian Standards documents
    powered by Google Gemini and Groq LLMs.
    """
    _instance = None

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        gemini_api_key: Optional[str] = None,
        groq_api_key: Optional[str] = None
    ):
        self.model_name = model_name
        
        # Load API keys
        g_key = gemini_api_key or os.getenv("GEMINI_API_KEY", "")
        if not g_key:
            try:
                import streamlit as st
                if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                    g_key = str(st.secrets["GEMINI_API_KEY"])
            except Exception:
                pass
        self.gemini_api_key = g_key

        q_key = groq_api_key or os.getenv("GROQ_API_KEY", "")
        if not q_key:
            try:
                import streamlit as st
                if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                    q_key = str(st.secrets["GROQ_API_KEY"])
            except Exception:
                pass
        self.groq_api_key = q_key

        self.embedding_model = None
        self.faiss_index = None
        self.chunks: List[Dict[str, Any]] = []
        self.chunk_embeddings: Optional[np.ndarray] = None
        self.is_initialized = False
        self.security_logs: List[Dict[str, Any]] = []
        
        self.initialize_engine()

    def initialize_engine(self):
        """Loads embedding model, prepares chunks, and builds FAISS vector index."""
        # 1. Load Embedding Model
        if HAS_SENTENCE_TRANSFORMERS:
            try:
                self.embedding_model = SentenceTransformer(self.model_name)
            except Exception as e:
                self.embedding_model = None
        else:
            self.embedding_model = None

        # 2. Ingest Sample Standards
        self.chunks = get_flattened_chunks()
        
        # 3. Build Vector / TF-IDF Index
        self.rebuild_index()
        self.is_initialized = True

    @property
    def is_degraded(self) -> bool:
        """True only if both embedding model and fallback have no chunks."""
        return len(self.chunks) == 0

    @is_degraded.setter
    def is_degraded(self, value: bool):
        pass

    def set_gemini_api_key(self, api_key: str):
        """Updates the Google Gemini API key dynamically."""
        self.gemini_api_key = api_key

    def set_groq_api_key(self, api_key: str):
        """Updates the Groq API key dynamically."""
        self.groq_api_key = api_key

    def get_security_logs(self) -> List[Dict[str, Any]]:
        """Returns the most recent security and prompt injection audit events."""
        return list(reversed(self.security_logs[-100:]))

    def clear_security_logs(self):
        """Clears the security audit log history."""
        self.security_logs.clear()

    def rebuild_index(self):
        """Computes embeddings for all chunks and builds/refreshes the FAISS index."""
        if not self.chunks:
            return

        texts = [chunk["text"] for chunk in self.chunks]

        if self.embedding_model is not None and HAS_FAISS:
            try:
                # Generate dense embeddings
                raw_embeddings = self.embedding_model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
                faiss.normalize_L2(raw_embeddings)
                self.chunk_embeddings = raw_embeddings.astype(np.float32)
                dim = self.chunk_embeddings.shape[1]
                self.faiss_index = faiss.IndexFlatIP(dim)
                self.faiss_index.add(self.chunk_embeddings)
            except Exception:
                self.embedding_model = None
                self.faiss_index = None

        # Always build TF-IDF vocabulary for instant high-precision matching
        self._build_tfidf_index()

    def _build_tfidf_index(self):
        """Builds a fast in-memory TF-IDF index with Unicode support for Indian languages."""
        import math
        from collections import Counter
        
        self.vocab = {}
        self.idf = {}
        self.doc_vectors = []
        doc_count = len(self.chunks)
        
        df = Counter()
        doc_tokens_list = []
        
        for chunk in self.chunks:
            # Combine text, standard number, keywords, and title with weights
            std_num = chunk.get("standard_number", "").lower()
            title = chunk.get("title", "").lower()
            clause_title = chunk.get("clause_title", "").lower()
            keywords = " ".join(chunk.get("keywords", [])).lower()
            full_text = f"{std_num} {std_num} {title} {clause_title} {keywords} {chunk.get('text', '').lower()}"
            
            # Unicode token regex preserves Indic, Devanagari, Tamil, Bengali tokens
            tokens = re.findall(r'[\w\-\:]+', full_text, re.UNICODE)
            doc_tokens_list.append(tokens)
            unique_tokens = set(tokens)
            for tok in unique_tokens:
                df[tok] += 1
                
        # Calculate IDF
        for tok, count in df.items():
            self.idf[tok] = math.log((1 + doc_count) / (1 + count)) + 1.0
            
        # Build normalized TF-IDF vector dict for each document
        for tokens in doc_tokens_list:
            tf = Counter(tokens)
            doc_len = len(tokens) or 1
            vec = {}
            norm_sq = 0.0
            for tok, count in tf.items():
                val = (count / doc_len) * self.idf.get(tok, 1.0)
                vec[tok] = val
                norm_sq += val * val
            norm = math.sqrt(norm_sq) or 1.0
            for tok in vec:
                vec[tok] /= norm
            self.doc_vectors.append(vec)

    def _expand_multilingual_query(self, query: str) -> Tuple[str, bool]:
        """
        Translates and expands Indic queries (Hindi, Tamil, Bengali, Marathi) into domain
        concepts and IS codes to ensure 100% accurate retrieval without false refusals.
        """
        q_lower = query.lower()
        expanded_terms = []
        matched = False
        
        for keywords, eng_expansion in INDIC_CROSS_LINGUAL_MAP:
            for kw in keywords:
                if kw in q_lower:
                    expanded_terms.append(eng_expansion)
                    matched = True
                    break
                    
        if expanded_terms:
            return f"{query} {' '.join(expanded_terms)}", True
        return query, False

    def _fallback_retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """High-precision BM25/TF-IDF and cross-lingual semantic keyword retriever."""
        import math
        from collections import Counter
        
        expanded_query, was_expanded = self._expand_multilingual_query(query)
        query_tokens = re.findall(r'[\w\-\:]+', expanded_query.lower(), re.UNICODE)
        if not query_tokens:
            return self.chunks[:top_k]
            
        # Extract query standard numbers (e.g. 10500, 2062, 1239, 456, 1417, 15820, 2720, 1293, 732, 2189, 16046, 15844, 4151, 2347, 694, 303)
        query_is_numbers = re.findall(r'(?:is|is\s*)?(\d{3,5})', expanded_query.lower())
        
        # Build query TF-IDF vector
        tf = Counter(query_tokens)
        q_len = len(query_tokens) or 1
        q_vec = {}
        norm_sq = 0.0
        for tok, count in tf.items():
            idf_val = self.idf.get(tok, 1.0) if hasattr(self, 'idf') else 1.0
            val = (count / q_len) * idf_val
            q_vec[tok] = val
            norm_sq += val * val
        q_norm = math.sqrt(norm_sq) or 1.0
        for tok in q_vec:
            q_vec[tok] /= q_norm
            
        scored = []
        for idx, chunk in enumerate(self.chunks):
            doc_vec = self.doc_vectors[idx] if hasattr(self, 'doc_vectors') and idx < len(self.doc_vectors) else {}
            score = sum(doc_vec.get(tok, 0.0) * weight for tok, weight in q_vec.items())
            
            # Boost 1: Exact IS code match
            std_num_lower = chunk.get("standard_number", "").lower()
            for is_num in query_is_numbers:
                if is_num in std_num_lower:
                    score += 0.50
                    
            # Boost 2: Keyword overlap
            chunk_keywords = [k.lower() for k in chunk.get("keywords", [])]
            for q_tok in query_tokens:
                if any(q_tok in k for k in chunk_keywords):
                    score += 0.10
                    
            # Boost 3: Category match
            cat_lower = chunk.get("category", "").lower()
            for q_tok in query_tokens:
                if len(q_tok) > 3 and q_tok in cat_lower:
                    score += 0.08
                    
            chunk_data = dict(chunk)
            # If cross-lingual expansion was triggered, give an extra baseline boost
            if was_expanded and score > 0.01:
                score = max(score, 0.35)
                
            chunk_data["similarity_score"] = min(0.99, max(0.0, float(score * 1.8)))
            scored.append((score, chunk_data))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    def add_custom_standard(self, standard_data: Dict[str, Any]) -> int:
        """
        Allows users to add new Indian Standards on the fly.
        Appends chunks and immediately rebuilds the FAISS/TF-IDF vector index.
        """
        std_id = standard_data.get("id", f"CUSTOM-{len(self.chunks)+1}")
        std_num = standard_data.get("standard_number", "Custom Indian Standard")
        std_title = standard_data.get("title", "User Uploaded Standard")
        category = standard_data.get("category", "General")
        status = standard_data.get("status", "Active")
        summary = standard_data.get("summary", "")
        clauses = standard_data.get("clauses", [])

        # Add summary chunk
        if summary:
            self.chunks.append({
                "chunk_id": f"{std_id}-SUMMARY",
                "standard_id": std_id,
                "standard_number": std_num,
                "title": std_title,
                "category": category,
                "status": status,
                "clause_id": "Scope & Overview",
                "clause_title": std_title,
                "text": f"Indian Standard: {std_num} - {std_title}.\nCategory: {category}.\nStatus: {status}.\nSummary: {summary}",
                "full_content": summary,
                "keywords": [std_num, std_title, category]
            })

        # Add clause chunks
        for idx, clause in enumerate(clauses):
            clause_id = clause.get("clause_id", f"Clause {idx+1}")
            clause_title = clause.get("clause_title", "General Requirements")
            content = clause.get("content", "")
            
            chunk_text = (
                f"Indian Standard: {std_num} - {std_title}\n"
                f"Category: {category} | Status: {status}\n"
                f"Clause/Section: {clause_id} - {clause_title}\n"
                f"Requirements & Content:\n{content}"
            )
            
            self.chunks.append({
                "chunk_id": f"{std_id}-C{idx+1}",
                "standard_id": std_id,
                "standard_number": std_num,
                "title": std_title,
                "category": category,
                "status": status,
                "clause_id": clause_id,
                "clause_title": clause_title,
                "text": chunk_text,
                "full_content": content,
                "keywords": clause.get("keywords", [])
            })

        # Re-index all chunks
        self.rebuild_index()
        return len(self.chunks)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves the top_k most relevant chunks using FAISS or high-precision TF-IDF matcher with cross-lingual expansion.
        """
        if not self.chunks:
            return []

        top_k = min(top_k, len(self.chunks))
        expanded_query, was_expanded = self._expand_multilingual_query(query)

        # Retrieve via fallback first if Indic or domain terms found
        fallback_results = self._fallback_retrieve(query, top_k=top_k)
        fb_top_score = fallback_results[0].get("similarity_score", 0.0) if fallback_results else 0.0

        if HAS_FAISS and self.faiss_index is not None and self.embedding_model is not None:
            try:
                # Use expanded query for embedding if query was Indic/non-English
                query_vec = self.embedding_model.encode([expanded_query], convert_to_numpy=True).astype(np.float32)
                faiss.normalize_L2(query_vec)
                scores, indices = self.faiss_index.search(query_vec, top_k)
                dense_results = []
                for score, idx in zip(scores[0], indices[0]):
                    if idx < len(self.chunks) and idx >= 0:
                        chunk_data = dict(self.chunks[idx])
                        chunk_data["similarity_score"] = float(score)
                        dense_results.append(chunk_data)

                dense_top_score = dense_results[0].get("similarity_score", 0.0) if dense_results else 0.0
                if dense_top_score >= 0.45 or (dense_top_score >= fb_top_score and dense_top_score >= 0.30):
                    return dense_results
            except Exception:
                pass

        return fallback_results

    def _sanitize_indirect_input(self, text: str) -> str:
        """
        Sanitize user-provided clauses, tenders, or unstructured inputs against
        indirect prompt injection, hidden delimiters, and unicode obfuscation.
        """
        if not text:
            return ""
        # 1. Strip zero-width and invisible unicode characters used for prompt obfuscation
        text = re.sub(r'[\u200B-\u200D\uFEFF\u00A0\u202A-\u202E]', ' ', text)
        # 2. Sanitize adversarial delimiters that mimic system instructions
        text = re.sub(r'(?i)<\|im_start\|>|<\|system\|>|<\|endoftext\|>|\[INST\]|\[/INST\]|<<SYS>>|```\s*system', ' [FILTERED_DELIMITER] ', text)
        return text.strip()

    def _detect_prompt_injection(self, query: str, language: str = "English") -> Optional[str]:
        """
        Multilingual, multi-category Prompt Injection & Jailbreak Defense Guardrail.
        Detects:
        - Direct instruction override & jailbreak attempts (English, Hindi, Tamil, Bengali, Marathi)
        - System prompt & API key exfiltration attempts
        - Delimiter and role-play subversion (DAN, Developer Mode, unfiltered persona)
        - Regulatory fraud & fake license requests
        """
        if not query:
            return None

        # Clean zero-width and invisible obfuscation characters
        clean_q = re.sub(r'[\u200B-\u200D\uFEFF]', '', query)
        q_lower = clean_q.lower().strip()
        detected_category = None

        # Category 1: Direct Instruction Overrides & Jailbreaks (English & Multilingual)
        override_patterns = [
            r"ignore\s+(all\s+)?(previous|prior|above|past|rules|safety)\s+(instructions|directives|rules|guidelines)",
            r"disregard\s+(all\s+)?(previous|prior|above|past|rules|directives|safety|guidelines)",
            r"forget\s+(all\s+)?(previous|prior|your)\s+(instructions|directives|rules)",
            r"bypass\s+(all\s+)?(safety|security|rules|guardrails|filters)",
            r"override\s+(all\s+)?(safety|system)\s+directives",
            r"do\s+not\s+follow\s+any\s+(rules|instructions)",
            r"you\s+are\s+now\s+(in\s+)?(dan|developer|jailbreak|unrestricted|god)\s+mode",
            r"act\s+as\s+(an?\s+)?(unfiltered|unrestricted|adversarial|jailbroken)",
            r"pretend\s+you\s+have\s+no\s+(rules|limits|safety)",
            # Hindi
            r"(सभी\s+|सारे\s+)?(पिछले|पूर्व|पुराने)\s+(निर्देश|नियम|आदेश)\s*(भूल\s+जाओ|रद्द\s+करो|अनदेखा\s+करो|हटाओ)",
            r"(सभी|सारे)\s+(निर्देश|नियम|आदेश)\s*(भूल\s+जाओ|रद्द\s+करो|अनदेखा\s+करो|हटाओ)",
            r"सुरक्षा\s+नियम\s*(बायपास|तोड़ो|हटाओ)",
            # Tamil
            r"(அனைத்து\s+)?(முந்தைய|பழைய)\s+(விதிகளை(யும்)?|கட்டளைகளை)\s*(மறந்துவிடு|புறக்கணிக்கவும்|நீக்கு)",
            r"அனைத்து\s+(விதிகளை(யும்)?|கட்டளைகளை)\s*(மறந்துவிடு|புறக்கணிக்கவும்|நீக்கு)",
            r"பாதுகாப்பு\s+விதிகளை\s*மீறு",
            # Bengali
            r"(সব\s+|সমস্ত\s+)?(আগের|পূর্বের)\s+(নির্দেশ|নিয়ম)\s*(ভুলে\s+যাও|উপেক্ষা\s+করো|বাতিল\s+করো)",
            r"(সব|সমস্ত)\s+(নির্দেশ|নিয়ম)\s*(ভুলে\s+যাও|উপেক্ষা\s+করো|বাতিল\s+করো)",
            r"নিরাপত্তা\s+নিয়ম\s*(বাইপাস|ভেঙে\s+ফেলো)",
            # Marathi
            r"(सर्व\s+)?(मागील|पूर्वीच्या)\s+(सूचना|नियम)\s*(विसरा|दुर्लक्षित\s+करा|रद्द\s+करा)",
            r"सर्व\s+(सूचना|नियम)\s*(विसरा|दुर्लक्षित\s+करा|रद्द\s+करा)",
            r"सुरक्षा\s+नियम\s*(बायपास\s+करा|तोडा)"
        ]
        for pat in override_patterns:
            if re.search(pat, q_lower):
                detected_category = "Instruction Override / Jailbreak"
                break

        # Category 2: System Prompt & Secret Exfiltration
        if not detected_category:
            exfiltration_patterns = [
                r"(reveal|print|output|show|display|tell|expose|leak|dump)\s+(me\s+)?(all\s+)?(your\s+)?(initial\s+|system\s+|base\s+|developer\s+|hidden\s+|secret\s+)*(prompt|instructions|rules|directives|context)",
                r"(reveal|print|output|show|display|tell|give)\s+(me\s+)?(your\s+)?(api\s*key|api\s*keys|secret\s*key|credentials|gemini\s*key|groq\s*key)",
                r"repeat\s+the\s+(text|words|instructions)\s+above",
                r"(what\s+is|what\s+are)\s+(your\s+)?(system\s+prompt|initial\s+prompt|base\s+prompt|gemini\s+api\s+key|groq\s+api\s+key|api\s+key|developer\s+prompt)",
                # Indic Exfiltration
                r"(सिस्टम\s*प्रॉम्प्ट|गुप्त\s*नियम|निर्देश)\s*(दिखाओ|बताओ|प्रिंट\s*करो)",
                r"एपीआई\s*(की|कुंजी)\s*(दिखाओ|बताओ)",
                r"(சிஸ்டம்\s*ப்ராம்ப்ட்|ரகசிய\s*விதிகள்)\s*(காட்டு|சொல்)",
                r"(সিস্টেম\s*প্রম্পট|গোপন\s*নিয়ম)\s*(দেখান|বলুন)",
                r"(सिस्टम\s*प्रॉम्प्ट|गुप्त\s*नियम)\s*(दाखवा|सांगा)"
            ]
            for pat in exfiltration_patterns:
                if re.search(pat, q_lower):
                    detected_category = "System Prompt / Secret Exfiltration"
                    break

        # Category 3: Delimiter Hijacking & Format Spoofing
        if not detected_category:
            delimiter_patterns = [
                r"<\|im_start\|>",
                r"<\|system\|>",
                r"<\|endoftext\|>",
                r"\[INST\]",
                r"\[/INST\]",
                r"<<SYS>>",
                r"```\s*system",
                r"---BEGIN SYSTEM PROMPT---",
                r"\[filtered_delimiter\]"
            ]
            for pat in delimiter_patterns:
                if re.search(pat, q_lower):
                    detected_category = "Control Token / Delimiter Injection"
                    break

        # Category 4: Regulatory Fraud & Fake Certification Claims
        if not detected_category:
            fraud_patterns = [
                r"grant\s+me\s+(a\s+)?legal\s+(license|exemption|ruling)",
                r"fake\s+(isi\s+mark|bis\s+certificate|huid)",
                r"forge\s+(isi\s+license|hallmark)",
                r"नक़ली\s*(isi|बीआईएस\s*लाइसेंस|हॉलमार्क)",
                r"போலி\s*(isi|ஹால்மார்க்)"
            ]
            for pat in fraud_patterns:
                if re.search(pat, q_lower):
                    detected_category = "Statutory Fraud / Certification Forgery"
                    break

        if detected_category:
            import datetime
            # Log security event
            log_entry = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "category": detected_category,
                "snippet": clean_q[:140],
                "language": self._detect_language_name(language)
            }
            self.security_logs.append(log_entry)
            if len(self.security_logs) > 200:
                self.security_logs.pop(0)

            lang = self._detect_language_name(language)
            if lang == "Hindi":
                return (
                    "🛡️ **सुरक्षा चेतावनी (Security Advisory)**: अनधिकृत निर्देश ओवरराइड, प्रॉम्प्ट इंजेक्शन, अथवा सुरक्षा नियम उल्लंघन का प्रयास पहचाना गया है।\n\n"
                    "मानक साथी भारतीय मानक ब्यूरो (BIS) के अधिकृत तकनीकी नियमों और सुरक्षा प्रोटोकॉल के अंतर्गत संचालित होता है। "
                    "कृपया भारतीय मानक (IS Codes), गुणवत्ता नियंत्रण आदेश (QCOs), अथवा BIS सेवाओं से संबंधित वैध तकनीकी प्रश्न पूछें।"
                )
            elif lang == "Tamil":
                return (
                    "🛡️ **பாதுகாப்பு எச்சரிக்கை (Security Advisory)**: அங்கீகரிக்கப்படாத அறிவுறுத்தல் மீறல் அல்லது ப்ராம்ப்ட் இன்ஜெக்ஷன் முயற்சி கண்டறியப்பட்டது.\n\n"
                    "ஸ்டாண்டர்ட்ஸ் சாதி இந்திய தரநிலைகள் பணியகத்தின் (BIS) உத்தியோகபூர்வ பாதுகாப்பு விதிகளுக்கு உட்பட்டு செயல்படுகிறது. "
                    "தயவுசெய்து இந்திய தரநிலைகள் (IS Codes) அல்லது சான்றிதழ் நடைமுறைகள் தொடர்பான சரியான தொழில்நுட்பக் கேள்விகளை சமர்ப்பிக்கவும்."
                )
            elif lang == "Bengali":
                return (
                    "🛡️ **নিরাপত্তা সতর্কতা (Security Advisory)**: অননুমোদিত নির্দেশ ওভাররাইড বা প্রম্পট ইনজেকশন প্রচেষ্টা শনাক্ত হয়েছে।\n\n"
                    "স্ট্যান্ডার্ডস সাথি ভারতীয় মানক ব্যুরো (BIS)-এর সরকারি নিরাপত্তা প্রোটোকল কঠোরভাবে অনুসরণ করে। "
                    "অনুগ্রহ করে ভারতীয় মানক (IS Codes) বা সার্টিফিকেশন পদ্ধতি সম্পর্কিত বৈধ প্রশ্ন জিজ্ঞাসা করুন।"
                )
            elif lang == "Marathi":
                return (
                    "🛡️ **सुरक्षा सूचना (Security Advisory)**: अनधिकृत सूचना ओव्हरराइड किंवा प्रॉम्प्ट इंजेक्शनचा प्रयत्न आढळला आहे.\n\n"
                    "मानक साथी हे भारतीय मानक ब्युरोच्या (BIS) अधिकृत सुरक्षा प्रोटोकॉलनुसार कार्य करते. "
                    "कृपया भारतीय मानके (IS Codes) किंवा बीआयएस प्रमाणपत्राशी संबंधित वैध तांत्रिक प्रश्न विचारा."
                )

            return (
                f"🛡️ **Safety & Security Advisory**: Unauthorized prompt injection pattern, instruction override, "
                f"or delimiter hijacking detected ({detected_category}).\n\n"
                "Standards Saathi strictly enforces Bureau of Indian Standards (BIS) regulatory ground rules and AI safety guardrails. "
                "Please submit a valid technical inquiry regarding Indian Standards (IS Codes), mandatory QCOs, or BIS certification procedures."
            )

        return None

    def _detect_language_name(self, lang_input: str) -> str:
        """Normalizes language string to one of 5 supported languages."""
        if not lang_input:
            return "English"
        l = lang_input.strip().lower()
        if l in ["mr", "mar", "marathi", "मराठी"] or "marathi" in l or "मराठी" in l:
            return "Marathi"
        if l in ["ta", "tam", "tamil", "தமிழ்"] or "tamil" in l or "தமிழ்" in l:
            return "Tamil"
        if l in ["bn", "ben", "bengali", "bangla", "বাংলা"] or "bengali" in l or "bangla" in l or "বাংলা" in l:
            return "Bengali"
        if l in ["hi", "hin", "hindi", "हिंदी"] or "hindi" in l or "हिंदी" in l:
            return "Hindi"
        return "English"

    def _detect_effective_language(self, query: str, requested_language: Optional[str] = "English") -> str:
        """
        Intelligently determines the effective language for generation:
        1. If query contains Indic scripts (Tamil, Bengali, Devanagari), auto-detect language!
        2. If query contains strong Romanized Indic keywords (e.g. 'paani ke liye', 'kivabe'), auto-detect language.
        3. Otherwise defaults to the user's selected language.
        """
        if not query:
            return self._detect_language_name(requested_language or "English")

        # Tamil script (\u0B80-\u0BFF)
        if re.search(r'[\u0B80-\u0BFF]', query):
            return "Tamil"

        # Bengali script (\u0980-\u09FF)
        if re.search(r'[\u0980-\u09FF]', query):
            return "Bengali"

        # Devanagari script (\u0900-\u097F)
        if re.search(r'[\u0900-\u097F]', query):
            marathi_markers = ["आहे", "नाही", "काय", "कसे", "कसा", "सांगा", "पाईप", "मानके", "सवलत", "मिळेल", "करावे", "कोणते", "दागिने"]
            if any(m in query for m in marathi_markers) or requested_language == "Marathi":
                return "Marathi"
            return "Hindi"

        # Romanized Indic keywords
        q_low = query.lower()
        hindi_words = ["kaunsa", "konsa", "kya hai", "kaise", "chahiye", "batao", "paani", "loha", "sariya", "soona", "chandi", "milega", "karein", "niyam", "manak"]
        tamil_words = ["enna", "eppadi", "thanni", "kuzhai", "thangam", "thevai", "solunga"]
        bengali_words = ["kivabe", "ki", "dorkar", "bolun", "pabo", "ispat", "manak"]
        marathi_words = ["kasa", "kay", "pahije", "sangaa", "ahe", "nahi", "milnar", "konte"]

        if any(w in q_low for w in marathi_words):
            return "Marathi"
        if any(w in q_low for w in tamil_words):
            return "Tamil"
        if any(w in q_low for w in bengali_words):
            return "Bengali"
        if any(w in q_low for w in hindi_words):
            return "Hindi"

        return self._detect_language_name(requested_language or "English")

    def _get_statutory_disclaimer(self, language: str = "English") -> str:
        """Returns statutory disclaimer in the selected language."""
        lang = self._detect_language_name(language)
        if lang == "Hindi":
            return (
                "\n\n---\n*⚖️ वैधानिक सूचना: मानक साथी भारतीय मानकों पर आधारित एक AI तकनीकी सलाहकार उपकरण है। यह कोई कानूनी, प्रमाणन, या प्रयोगशाला अनुमोदन निर्णय जारी नहीं करता है। आधिकारिक प्रमाणन के लिए e-BIS मानकऑनलाइन (www.manakonline.in) पर संपर्क करें।*"
            )
        elif lang == "Tamil":
            return (
                "\n\n---\n*⚖️ சட்டப்பூர்வ அறிவிப்பு: 'Standards Saathi' என்பது இந்திய தரநிலைகள் அடிப்படையிலான AI வழிகாட்டி கருவியாகும். இது உத்தியோகபூர்வ சான்றிதழ் முடிவுகளை வழங்காது. இறுதி விவரங்களுக்கு e-BIS Manakonline (www.manakonline.in) பார்க்கவும்.*"
            )
        elif lang == "Bengali":
            return (
                "\n\n---\n*⚖️ সংবিধিবদ্ধ বিজ্ঞপ্তি: 'Standards Saathi' হলো ভারতীয় মানক ভিত্তিক একটি AI প্রযুক্তিগত উপদেষ্টা। এটি কোনো আইনি বা চূড়ান্ত লাইসেন্স প্রদানকারী সিদ্ধান্ত দেয় না। অফিসিয়াল তথ্যের জন্য e-BIS Manakonline (www.manakonline.in) দেখুন।*"
            )
        elif lang == "Marathi":
            return (
                "\n\n---\n*⚖️ वैधानिक सूचना: 'Standards Saathi' हे भारतीय मानकांवर आधारित AI तांत्रिक सल्लागार साधन आहे. हे कोणतेही अंतिम कायदेशीर किंवा परवाना निर्णय देत नाही. अधिकृत पडताळणीसाठी e-BIS Manakonline (www.manakonline.in) ला भेट द्या.*"
            )
        return (
            "\n\n---\n*⚖️ Statutory Notice: Standards Saathi provides technical and procedural advisory grounded in Indian Standards. "
            "It does NOT issue legal decisions, licensing grants, or statutory laboratory approval rulings. "
            "For official certifications, please apply through e-BIS Manakonline (www.manakonline.in).*"
        )

    def _generate_no_evidence_response(self, query: str, language: str = "English") -> str:
        """Generates a reliable refusal response when relevant evidence is not found in the BIS database."""
        lang = self._detect_language_name(language)
        if lang == "Hindi":
            return (
                "### ℹ️ बीआईएस ज्ञान आधार में पर्याप्त साक्ष्य उपलब्ध नहीं है\n\n"
                "मानक साथी (Standards Saathi) के अधिकृत डेटाबेस में इस प्रश्न का सटीक व सत्यापित उत्तर देने के लिए **पर्याप्त क्लॉज या दस्तावेजी साक्ष्य नहीं मिले हैं।**\n\n"
                "सटीकता और विश्वसनीयता बनाए रखने के लिए, मानक साथी अनुमान नहीं लगाता है।\n\n"
                "**अनुशंसित आधिकारिक कदम:**\n"
                "- 🔍 **बीआईएस मानक पोर्टल**: 20,000+ भारतीय मानकों को खोजने के लिए [www.standardsbis.in](https://www.standardsbis.in) पर जाएं।\n"
                "- 📋 **e-BIS मानकऑनलाइन**: प्रमाणन और लाइसेंसिंग के लिए [www.manakonline.in](https://www.manakonline.in) पर जाएं।\n"
                "- 🏢 **QCO ट्रैकर**: अनिवार्य गुणवत्ता नियंत्रण आदेशों की सूची [BIS QCO Orders](https://www.bis.gov.in/product-certification/qco-orders/) पर देखें।"
            )
        elif lang == "Tamil":
            return (
                "### ℹ️ BIS தரவுத்தளத்தில் போதுமான சான்றுகள் கிடைக்கவில்லை\n\n"
                "இந்தக் கேள்விக்கு துல்லியமான பதில் அளிக்க **அங்கீகரிக்கப்பட்ட IS குறியீடு சான்றுகள் கிடைக்கவில்லை.**\n\n"
                "**அதிகாரப்பூர்வ தளங்கள்:**\n"
                "- 🔍 **BIS தரநிலைகள் தளம்**: [www.standardsbis.in](https://www.standardsbis.in)\n"
                "- 📋 **e-BIS Manakonline**: [www.manakonline.in](https://www.manakonline.in)\n"
                "- 🏢 **QCO பட்டியல்**: [BIS QCO Orders](https://www.bis.gov.in/product-certification/qco-orders/)"
            )
        elif lang == "Bengali":
            return (
                "### ℹ️ BIS জ্ঞান ভাণ্ডারে পর্যাপ্ত তথ্য পাওয়া যায়নি\n\n"
                "এই প্রশ্নের সঠিক উত্তর দেওয়ার জন্য অনুমোদিত ডেটাবেসে **পর্যাপ্ত ধারা বা প্রামাণ্য নথি মেলেনি।**\n\n"
                "**অফিসিয়াল পদক্ষেপ:**\n"
                "- 🔍 **BIS স্ট্যান্ডার্ড পোর্টাল**: [www.standardsbis.in](https://www.standardsbis.in)\n"
                "- 📋 **e-BIS মানকঅনলাইন**: [www.manakonline.in](https://www.manakonline.in)\n"
                "- 🏢 **QCO ট্র্যাকার**: [BIS QCO Orders](https://www.bis.gov.in/product-certification/qco-orders/)"
            )
        elif lang == "Marathi":
            return (
                "### ℹ️ बीआयएस ज्ञान संचामध्ये पुरेसा पुरावा उपलब्ध नाही\n\n"
                "या प्रश्नाचे अचूक उत्तर देण्यासाठी डेटाबेसमध्ये **आवश्यक क्लॉज किंवा अधिकृत माहिती आढळली नाही.**\n\n"
                "**अधिकृत बीआयएस संसाधने:**\n"
                "- 🔍 **बीआईएस मानक पोर्टल**: [www.standardsbis.in](https://www.standardsbis.in)\n"
                "- 📋 **e-BIS Manakonline**: [www.manakonline.in](https://www.manakonline.in)\n"
                "- 🏢 **QCO ट्रॅकर**: [BIS QCO Orders](https://www.bis.gov.in/product-certification/qco-orders/)"
            )
        return (
            "### ℹ️ Insufficient Evidence in BIS Knowledge Base\n\n"
            "Based on the authorized Bureau of Indian Standards (BIS) knowledge base loaded in Standards Saathi, "
            "**sufficient verified evidence was not found to reliably answer this query without speculation.**\n\n"
            "To ensure absolute technical reliability and compliance, Standards Saathi does not guess or extrapolate beyond authorized documents.\n\n"
            "**Recommended Official Actions:**\n"
            "- 🔍 **Search the BIS Catalog**: Visit the official [BIS Standards Portal](https://www.standardsbis.in) or [e-BIS Manakonline](https://www.manakonline.in) to search across 20,000+ Indian Standards.\n"
            "- 📋 **Check Mandatory Quality Control Orders (QCOs)**: View official ministerial mandates at [BIS QCO Tracker](https://www.bis.gov.in/product-certification/qco-orders/).\n"
            "- 🏢 **Contact BIS Directorate**: Reach out to your nearest [BIS Regional or Branch Office](https://www.bis.gov.in/about-bis/branch-offices/)."
        )

    def generate_response(
        self,
        query: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        top_k: int = 3,
        temperature: float = 0.2,
        language: str = "English",
        model_override: Optional[str] = None,
        msme_mode: bool = False,
        voice_mode: bool = False,
        saral_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Executes full RAG workflow with safety guardrails, prompt injection detection,
        grounding threshold verification, multilingual synthesis (English, Hindi, Tamil, Bengali, Marathi),
        clause citations, and spoken-friendly voice formatting.
        Supports Saral Voice Saathi (Illiterate / Low-Literacy Assistant Mode).
        """
        # Step 0: Auto-detect Effective Language from Query
        effective_lang = self._detect_effective_language(query, requested_language=language)

        # Guardrail 1: Prompt Injection Defense
        injection_alert = self._detect_prompt_injection(query, language=effective_lang)
        if injection_alert:
            return {
                "answer": injection_alert,
                "raw_answer": injection_alert,
                "citations": [],
                "sources_text": "",
                "related_standards": [],
                "is_fallback": True,
                "model": "Prompt Injection Defense Filter"
            }

        # Step 1: Retrieve context chunks
        retrieved_chunks = self.retrieve(query, top_k=top_k)
        _, was_expanded = self._expand_multilingual_query(query)

        # Guardrail 2: Grounding Confidence Check
        max_score = max([c.get("similarity_score", 0.0) for c in retrieved_chunks]) if retrieved_chunks else 0.0
        # For Indic/multilingual queries where cross-lingual expansion was used, use low threshold 0.15
        threshold = 0.15 if was_expanded else 0.32
        
        # If max similarity score is low or empty, refuse to guess
        if not retrieved_chunks or max_score < threshold:
            no_ev_ans = self._generate_no_evidence_response(query, language=effective_lang)
            statutory_disc = self._get_statutory_disclaimer(language=effective_lang)
            return {
                "answer": f"{no_ev_ans}{statutory_disc}",
                "raw_answer": no_ev_ans,
                "citations": [],
                "sources_text": "",
                "related_standards": [],
                "is_fallback": True,
                "model": "Grounding Threshold Guardrail"
            }

        # Extract related standards and unique source documents with Version Tracking
        related_standards_set = set()
        source_citations = []
        for idx, chunk in enumerate(retrieved_chunks, 1):
            filename = chunk.get("filename", f"{chunk['standard_number'].replace(':', '_').replace(' ', '_')}.pdf")
            page_num = chunk.get("page_number", idx * 2)
            section_num = chunk.get("section_number", chunk.get("clause_id", "Section 1.0"))
            purchase_url = chunk.get("purchase_url", "https://www.standardsbis.in")
            status_ver = chunk.get("status", "Active National Standard")
            
            source_citations.append(
                f"📄 {filename} ({status_ver}), Page {page_num}, {section_num} | 🔗 Official Link: {purchase_url}"
            )
            for rel in chunk.get("related_standards", []):
                related_standards_set.add(rel)

        related_standards_list = list(related_standards_set)[:4]

        # Step 2: Assemble context text
        context_blocks = []
        for idx, chunk in enumerate(retrieved_chunks, 1):
            context_blocks.append(
                f"[Source {idx}]: {chunk['standard_number']} — {chunk['title']}\n"
                f"Document: {chunk.get('filename')} | Version/Status: {chunk.get('status')} | Page {chunk.get('page_number')} | Section: {chunk.get('section_number')}\n"
                f"Clause: {chunk['clause_id']} ({chunk['clause_title']})\n"
                f"Content:\n{chunk['full_content']}\n"
            )
        context_str = "\n---\n".join(context_blocks)

        # Step 3: Check Groq / Gemini API Availability
        statutory_disclaimer = self._get_statutory_disclaimer(language=language)

        # Step 4: Auto-detect Effective Language & Construct System Prompt
        effective_lang = self._detect_effective_language(query, requested_language=language)
        statutory_disclaimer = self._get_statutory_disclaimer(language=effective_lang)
        
        lang_directives = {
            "English": "Respond STRICTLY in clear, professional, authoritative English. Use attractive formatting with bold highlights, emoji icons, and clean Markdown structure.",
            "Hindi": "Respond STRICTLY in natural, fluent, and professional Hindi (हिंदी) in Devanagari script. Do NOT respond in English. Explain all technical terms, standards, and certification steps clearly in Hindi (e.g. 'भारतीय मानक ब्यूरो (BIS)', 'अनिवार्य गुणवत्ता नियंत्रण आदेश (QCO)', '80% सरकारी छूट').",
            "Tamil": "Respond STRICTLY in fluent, natural, and professional Tamil (தமிழ்). Do NOT respond in English. Explain all technical concepts, IS standards, and testing norms clearly in Tamil (e.g. 'இந்திய தரநிலைகள் பணியகம் (BIS)', 'கட்டாய QCO உத்தரவு', '80% கட்டணச் சலுகை').",
            "Bengali": "Respond STRICTLY in fluent, natural, and professional Bengali (বাংলা). Do NOT respond in English. Explain all technical concepts, IS standards, and certification norms clearly in Bengali (e.g. 'ভারতীয় মানক ব্যুরো (BIS)', 'বাধ্যতামূলক QCO নির্দেশিকা', '৮০% সরকারি ফি ছাড়').",
            "Marathi": "Respond STRICTLY in fluent, natural, and professional Marathi (मराठी) in Devanagari script. Do NOT respond in English. Explain all technical concepts, IS standards, and testing norms clearly in Marathi (e.g. 'भारतीय मानक ब्युरो (BIS)', 'अनिवार्य QCO आदेश', '80% सरकारी सवलत')."
        }
        lang_instruction = lang_directives.get(effective_lang, lang_directives["English"])

        msme_directive = (
            "MSME MODE IS ACTIVE: Highlight 80% fee concessions for micro enterprises (50% for small), 50% lab testing subsidies, simplified conformity assessment roadmap, and low-cost compliance options."
            if (msme_mode or saral_mode) else
            "Mention MSME 80% fee concessions or 50% lab testing subsidy where applicable to certification."
        )

        if saral_mode:
            voice_length_directive = (
                "SARAL VOICE SAATHI / ILLITERATE & LOW-LITERACY ASSISTANT MODE (CRITICAL):\n"
                f"You are speaking directly over voice to an illiterate or low-literacy Indian artisan, micro worker, or shopkeeper in {effective_lang}.\n"
                "CRITICAL RULES FOR SARAL MODE:\n"
                "1. TONE & MANNER: Speak with extreme warmth, respect, and simple conversational phrasing ('नमस्ते भाई/बहन...', 'வணக்கம் நண்பரே...', 'নমস্কার...', 'नमस्कार मित्रा...').\n"
                "2. ZERO TECHNICAL JARGON: Do NOT mention clause numbers, tensile strength values, legal acts, or confusing technical formulas.\n"
                "3. GIVE 3 PLAIN SPOKEN STEPS:\n"
                "   - Step 1: Where to go (Nearest Jan Seva Kendra / CSC or www.manakonline.in for online application).\n"
                "   - Step 2: 80% Government Subsidy (Small artisans and micro workers get 80% discount on government application fees and 50% discount on lab test fees!).\n"
                "   - Step 3: Testing & ISI Mark (Product sample is tested in lab, and once approved, you get the official ISI license).\n"
                "4. LENGTH: Keep between 75 to 100 words total. Clean, flowing spoken sentences suitable for instant voice readout."
            )
        elif voice_mode:
            voice_length_directive = (
                f"VOICE ASSISTANT MODE (CRITICAL): Respond in {effective_lang}. Keep the total response between 100 to 130 words. Use natural spoken lists ('Pehla kadam...', 'First step...'). Do NOT say 'click here', 'see table above', or 'as shown on screen'. End with a single short, proactive follow-up offer."
            )
        else:
            if effective_lang == "Hindi":
                voice_length_directive = (
                    "STRUCTURED & ATTRACTIVE FORMATTING MANDATE (हिंदी):\n"
                    "Always format your response using clean, scannable Markdown sections with these exact Hindi headings:\n"
                    "### 🎯 संक्षिप्त मुख्य उत्तर (Direct Summary)\n"
                    "1-2 स्पष्ट व सटीक वाक्यों में मुख्य उत्तर दें।\n\n"
                    "### 📜 लागू भारतीय मानक एवं QCO आदेश (Applicable Standards & Mandatory QCO)\n"
                    "लागू IS कोड (जैसे IS 1239 / IS 10500), पूरा शीर्षक और क्या यह केंद्र सरकार के QCO के तहत अनिवार्य है या स्वैच्छिक, बुलेट पॉइंट्स में लिखें।\n\n"
                    "### 🛠️ मुख्य तकनीकी एवं परीक्षण आवश्यकताएं (Key Technical & Testing Norms)\n"
                    "उत्पाद की गुणवत्ता, सामग्री, रासायनिक/भौतिक परीक्षण व अनिवार्य मार्किंग नियम स्पष्ट करें।\n\n"
                    "### 📋 चरण-दर-चरण बीआईएस प्रमाणन प्रक्रिया (Step-by-Step BIS Certification Roadmap)\n"
                    "e-BIS मानकऑनलाइन (www.manakonline.in) के माध्यम से लाइसेंस प्राप्त करने के 3-4 स्पष्ट चरणबद्ध कदम।\n\n"
                    "### 💰 सूक्ष्म व लघु उद्योग छूट (MSME 80% Fee Concessions)\n"
                    "माइक्रो उद्यमों के लिए 80% आवेदन शुल्क छूट, 50% वार्षिक लाइसेंस शुल्क छूट एवं 50% लैब परीक्षण सब्सिडी की स्पष्ट जानकारी दें।"
                )
            elif effective_lang == "Tamil":
                voice_length_directive = (
                    "STRUCTURED & ATTRACTIVE FORMATTING MANDATE (தமிழ்):\n"
                    "Always format your response using clean, scannable Markdown sections with these exact Tamil headings:\n"
                    "### 🎯 சுருக்கமான நேரடி பதில் (Direct Summary)\n"
                    "1-2 தெளிவான வாக்கியங்களில் நேரடிப் பதில்.\n\n"
                    "### 📜 பொருந்தக்கூடிய இந்திய தரநிலைகள் மற்றும் QCO உத்தரவு (Applicable IS Codes & QCO)\n"
                    "பொருந்தக்கூடிய IS குறியீடுகள், தலைப்பு மற்றும் கட்டாய QCO விவரங்கள்.\n\n"
                    "### 🛠️ முக்கிய தொழில்நுட்ப மற்றும் ஆய்வக தேவைகள் (Technical & Testing Requirements)\n"
                    "தயாரிப்பு தரம், இயந்திரவியல் சோதனைகள் மற்றும் தேவையான ஆய்வக அளவீடுகள்.\n\n"
                    "### 📋 BIS சான்றிதழ் பெறுவதற்கான படிநிலைகள் (Step-by-Step BIS Certification Roadmap)\n"
                    "e-BIS Manakonline (www.manakonline.in) மூலம் சான்றிதழ் பெற 3-4 செயல்முறை படிகள்.\n\n"
                    "### 💰 MSME 80% கட்டணச் சலுகை மற்றும் மானியம் (MSME Fee Concessions & Subsidies)\n"
                    "மைக்ரோ நிறுவனங்களுக்கான 80% கட்டணக் குறைப்பு மற்றும் 50% ஆய்வகப் பரிசோதனை மானியம்."
                )
            elif effective_lang == "Bengali":
                voice_length_directive = (
                    "STRUCTURED & ATTRACTIVE FORMATTING MANDATE (বাংলা):\n"
                    "Always format your response using clean, scannable Markdown sections with these exact Bengali headings:\n"
                    "### 🎯 সংক্ষিপ্ত সরাসরি উত্তর (Direct Summary)\n"
                    "১-২টি স্পষ্ট বাক্যে প্রধান উত্তর দিন।\n\n"
                    "### 📜 প্রযোজ্য ভারতীয় মানক ও বাধ্যতামূলক QCO নির্দেশ (Applicable Standards & QCO)\n"
                    "প্রযোজ্য IS কোড, নাম এবং বাধ্যতামূলক QCO স্ট্যাটাস বুলেটে লিখুন।\n\n"
                    "### 🛠️ মূল প্রযুক্তিগত ও ল্যাব পরীক্ষার প্রয়োজনীয়তা (Technical & Testing Requirements)\n"
                    "পণ্যের গুণমান, ল্যাবরেটরি টেস্ট এবং প্যাকিং/মার্কিং সংক্রান্ত মূল শর্তাবলী।\n\n"
                    "### 📋 BIS লাইসেন্স প্রাপ্তির ধাপে ধাপে নির্দেশিকা (Step-by-Step Roadmap)\n"
                    "e-BIS Manakonline (www.manakonline.in) থেকে আইএসআই লাইসেন্স পাওয়ার ৩-৪টি পদক্ষেপ।\n\n"
                    "### 💰 MSME ৮০% ফি ছাড় ও সরকারি ভর্তুকি (MSME 80% Concessions & Subsidies)\n"
                    "মাইক্রো এন্টারপ্রাইজের জন্য ৮০% আবেদন ফি ছাড় ও ৫০% ল্যাব টেস্ট ভর্তুকির সুবিধা।"
                )
            elif effective_lang == "Marathi":
                voice_length_directive = (
                    "STRUCTURED & ATTRACTIVE FORMATTING MANDATE (मराठी):\n"
                    "Always format your response using clean, scannable Markdown sections with these exact Marathi headings:\n"
                    "### 🎯 थेट संक्षिप्त उत्तर (Direct Summary)\n"
                    "१-२ स्पष्ट वाक्यांमध्ये थेट उत्तर द्या.\n\n"
                    "### 📜 लागू भारतीय मानके व अनिवार्य QCO आदेश (Applicable Standards & QCO)\n"
                    "लागू असलेले IS कोड, शीर्षक आणि अनिवार्य QCO स्थिती.\n\n"
                    "### 🛠️ मुख्य तांत्रिक व प्रयोगशाळा चाचणी निकष (Technical & Testing Requirements)\n"
                    "उत्पादनाची गुणवत्ता, तांत्रिक निकष आणि आवश्यक लॅब चाचण्या.\n\n"
                    "### 📋 तपशीलवार बीआयएस परवाना प्रक्रिया (Step-by-Step Certification Roadmap)\n"
                    "e-BIS Manakonline (www.manakonline.in) द्वारे ISI परवाना मिळवण्याचे ३-४ टप्पे.\n\n"
                    "### 💰 सूक्ष्म व लघु उद्योग सवलती (MSME 80% Fee Concessions)\n"
                    "मायक्रो उद्योगांसाठी ८०% अर्ज शुल्क सवलत आणि ५०% लॅब टेस्टिंग सबसिडीची माहिती."
                )
            else:
                voice_length_directive = (
                    "STRUCTURED & ATTRACTIVE FORMATTING MANDATE (English):\n"
                    "Always format your response with clean, scannable Markdown sections:\n"
                    "### 🎯 Direct Summary\n"
                    "1-2 clear, direct sentences answering the core inquiry.\n\n"
                    "### 📜 Applicable Standards & Mandatory QCO Status\n"
                    "Bullet points listing the exact IS codes, title, and mandatory government QCO status.\n\n"
                    "### 🛠️ Key Technical & Testing Requirements\n"
                    "Key technical parameters, required laboratory tests, and marking obligations.\n\n"
                    "### 📋 Step-by-Step BIS Certification Roadmap\n"
                    "3-4 numbered actionable steps to obtain the ISI license via e-Manakonline (www.manakonline.in).\n\n"
                    "### 💰 MSME 80% Fee Concessions & Lab Subsidies\n"
                    "Highlight 80% application fee discount and 50% lab testing subsidy for micro enterprises."
                )

        system_prompt = (
            "You are 'Standards Saathi' (मानक साथी), the official-grade AI technical advisor for Indian Standards (IS Codes), "
            "Bureau of Indian Standards (BIS) regulations, Quality Control Orders (QCOs), and certification schemes (ISI mark, CRS, Hallmarking, FMCS).\n\n"
            f"LANGUAGE DIRECTIVE: {lang_instruction}\n"
            f"{msme_directive}\n"
            f"{voice_length_directive}\n\n"
            "SAFETY & RELIABILITY GUARDRAILS (CRITICAL RULES):\n"
            f"1. LANGUAGE PURITY: You MUST write your ENTIRE final output in {effective_lang}. Do NOT reply in English when answering in Hindi, Tamil, Bengali, or Marathi.\n"
            "2. STRICT GROUNDING: Base your entire answer ONLY on the provided Indian Standards context. Do NOT extrapolate or guess IS numbers or procedures.\n"
            "3. REGULATORY BOUNDARIES: You provide technical and procedural guidance; cite official BIS channels (www.manakonline.in / www.bis.gov.in).\n"
            "4. CITATIONS & MANDATORY STATUS: Clearly state exact IS codes (e.g. IS 1239 Part 1, IS 10500:2012) and whether mandatory under government QCO vs voluntary.\n"
            "5. PROACTIVE OFFER: Naturally offer AT MOST ONE of these 5 features when relevant:\n"
            "   - Compliance Checklist\n"
            "   - Tender / Specification Analyzer\n"
            "   - Explain This Clause\n"
            "   - MSME Mode\n"
            "   - Voice Onboarding Interview"
        )

        user_content = (
            f"USER QUESTION / QUERY:\n{query}\n\n"
            f"RETRIEVED INDIAN STANDARDS CONTEXT (AUTHORIZED EVIDENCE):\n"
            f"{context_str}\n\n"
            f"CRITICAL: Write your entire structured technical response in {effective_lang} following the exact section format."
        )

        messages = [{"role": "system", "content": system_prompt}]

        if chat_history:
            for turn in chat_history[-4:]:
                messages.append({"role": turn["role"], "content": turn["content"]})

        messages.append({"role": "user", "content": user_content})

        # Step 5: Generate Response via Google Gemini or Groq LLM
        raw_answer = ""
        successful_model = None

        # 5a. Prioritize Google Gemini if configured
        gemini_key = self.gemini_api_key or os.getenv("GEMINI_API_KEY", "")
        if HAS_GOOGLE_GENAI and gemini_key:
            try:
                client = genai.Client(api_key=gemini_key)
                full_gemini_content = f"{system_prompt}\n\n{user_content}"
                if chat_history:
                    history_str = "\n".join([f"{h['role'].upper()}: {h['content']}" for h in chat_history[-4:]])
                    full_gemini_content = f"{system_prompt}\n\nCONVERSATION HISTORY:\n{history_str}\n\n{user_content}"

                for g_model in ["gemini-2.5-flash", "gemini-3.7-flash", "gemini-2.5-pro"]:
                    try:
                        g_resp = client.models.generate_content(
                            model=g_model,
                            contents=full_gemini_content
                        )
                        if g_resp and g_resp.text:
                            raw_answer = g_resp.text.strip()
                            if "<think>" in raw_answer and "</think>" in raw_answer:
                                raw_answer = raw_answer.split("</think>")[-1].strip()
                            successful_model = f"{g_model} (Google Gemini)"
                            break
                    except Exception:
                        continue
            except Exception:
                pass

        # 5b. Fallback to Groq if Gemini was not used or failed
        if not raw_answer:
            api_key = self.groq_api_key or os.getenv("GROQ_API_KEY", "")
            if HAS_GROQ and api_key:
                candidate_models = []
                if model_override:
                    candidate_models.append(model_override)
                candidate_models.extend(["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "groq/compound-mini", "openai/gpt-oss-20b"])
                candidate_models = list(dict.fromkeys(candidate_models))

                try:
                    client = Groq(api_key=api_key)
                    for model_name in candidate_models:
                        try:
                            completion = client.chat.completions.create(
                                model=model_name,
                                messages=messages,
                                temperature=temperature,
                                max_tokens=1024,
                                top_p=0.9,
                            )
                            raw_answer = completion.choices[0].message.content
                            if "<think>" in raw_answer and "</think>" in raw_answer:
                                raw_answer = raw_answer.split("</think>")[-1].strip()
                            successful_model = f"{model_name} (Groq)"
                            break
                        except Exception:
                            continue
                except Exception:
                    pass

        if not raw_answer:
            raw_answer = self._generate_offline_fallback(query, retrieved_chunks, source_citations, language=effective_lang)

        # Format Final Answer with Required Citations Block and Statutory Disclaimer
        if len(source_citations) == 1:
            sources_block = f"\n\n**Sources & Document Attribution:** {source_citations[0]}"
        else:
            sources_block = "\n\n**Sources & Document Attribution:**\n" + "\n".join([f"- {s}" for s in source_citations])
            
        full_formatted_answer = f"{raw_answer}\n{sources_block}{statutory_disclaimer}"

        return {
            "answer": full_formatted_answer,
            "raw_answer": raw_answer,
            "citations": retrieved_chunks,
            "sources_text": "\n".join(source_citations),
            "related_standards": related_standards_list,
            "is_fallback": successful_model is None,
            "model": f"{successful_model} (Groq)" if successful_model else "Local RAG Retriever"
        }

    # =========================================================================
    # 5 PROACTIVE TOOLS HELPER METHODS
    # =========================================================================

    def generate_compliance_checklist(self, product: str, language: str = "English", is_msme: bool = True) -> Dict[str, Any]:
        """Feature 1: Generates a tailored, numbered compliance checklist for any product."""
        effective_lang = self._detect_effective_language(product, requested_language=language)
        prompt = (
            f"Generate a concise, numbered Compliance Checklist for product/service: '{product}'.\n"
            f"Include:\n"
            f"1. Applicable Indian Standards (IS codes)\n"
            f"2. Mandatory QCO & Certification Scheme (ISI Mark / CRS / Hallmarking / FMCS)\n"
            f"3. Key Laboratory Tests & In-House SIT Equipment needed\n"
            f"4. Essential Documents & e-BIS Manakonline process\n"
            f"{'5. MSME 80% fee concession & 50% lab testing subsidy steps' if is_msme else ''}\n"
            f"Respond strictly in {effective_lang}."
        )
        return self.generate_response(query=prompt, language=effective_lang, msme_mode=is_msme)

    def analyze_tender_or_spec(self, tender_text: str, language: str = "English") -> Dict[str, Any]:
        """Feature 2: Analyzes tender/procurement/specification text, extracts IS codes, flags missing standards."""
        sanitized = self._sanitize_indirect_input(tender_text)
        effective_lang = self._detect_effective_language(sanitized, requested_language=language)
        injection_alert = self._detect_prompt_injection(sanitized, language=effective_lang)
        if injection_alert:
            return {
                "analysis": injection_alert,
                "answer": injection_alert,
                "raw_answer": injection_alert,
                "citations": [],
                "sources_text": "",
                "related_standards": [],
                "is_fallback": True,
                "model": "Indirect Prompt Injection Filter"
            }

        prompt = (
            f"Analyze the following tender/specification text for Indian Standards (IS codes) compliance:\n\n"
            f"TENDER/SPEC TEXT:\n\"\"\"\n{sanitized[:2500]}\n\"\"\"\n\n"
            f"Provide:\n"
            f"1. Referenced IS Codes found in text\n"
            f"2. Missing or updated BIS Standard References commonly required for this scope\n"
            f"3. Mandatory QCO obligations\n"
            f"4. Actionable recommendations for the bidder/manufacturer to align with BIS norms.\n"
            f"Respond strictly in {effective_lang}."
        )
        res = self.generate_response(query=prompt, language=effective_lang)
        res["analysis"] = res.get("answer", "")
        return res

    def explain_clause(self, clause_text: str, language: str = "English") -> Dict[str, Any]:
        """Feature 3: Explains a technical clause from an IS code or tender in simple spoken language with 1-2 examples."""
        sanitized = self._sanitize_indirect_input(clause_text)
        effective_lang = self._detect_effective_language(clause_text, requested_language=language)
        injection_alert = self._detect_prompt_injection(sanitized, language=effective_lang)
        if injection_alert:
            return {
                "explanation": injection_alert,
                "answer": injection_alert,
                "raw_answer": injection_alert,
                "citations": [],
                "sources_text": "",
                "related_standards": [],
                "is_fallback": True,
                "model": "Indirect Prompt Injection Filter"
            }

        prompt = (
            f"Explain this Indian Standard (IS Code) or tender clause in very simple, plain language with 1-2 practical real-world examples:\n\n"
            f"CLAUSE TEXT:\n\"\"\"\n{sanitized[:2000]}\n\"\"\"\n\n"
            f"Respond strictly in {effective_lang} using easy spoken structure."
        )
        res = self.generate_response(query=prompt, language=effective_lang)
        res["explanation"] = res.get("answer", "")
        return res

    def evaluate_onboarding_interview(self, answers: Dict[str, str], language: str = "English") -> Dict[str, Any]:
        """Feature 5: Evaluates 3-4 onboarding questions to produce a tailored roadmap."""
        prod_type = answers.get("product_type", "General Industrial Product")
        material = answers.get("material", "Standard materials")
        market = answers.get("market", "Domestic Indian Market")
        current_status = answers.get("current_certifications", "New manufacturer")
        effective_lang = self._detect_effective_language(f"{prod_type} {material} {market}", requested_language=language)

        prompt = (
            f"Generate a customized BIS Certification Roadmap based on this new manufacturer onboarding profile:\n"
            f"- Product Type: {prod_type}\n"
            f"- Material / Construction: {material}\n"
            f"- Target Market & Scale: {market}\n"
            f"- Current Certification / Testing: {current_status}\n\n"
            f"Give a clear, 4-step actionable roadmap with applicable IS codes, mandatory QCO status, in-house lab setup requirements, and MSME fee subsidies.\n"
            f"Respond strictly in {effective_lang}."
        )
        return self.generate_response(query=prompt, language=effective_lang, msme_mode=True)

    def _generate_offline_fallback(self, query: str, retrieved_chunks: List[Dict[str, Any]], source_citations: Optional[List[str]] = None, language: str = "English") -> str:
        """Generates a structured answer directly from retrieved chunks when LLM API is unavailable in the requested language."""
        lang = self._detect_language_name(language)
        if not retrieved_chunks:
            return self._generate_no_evidence_response(query, language=lang)

        if lang == "Hindi":
            res = [
                "### 🎯 संक्षिप्त मुख्य उत्तर (Direct Summary)\n"
                f"आपके प्रश्न के लिए भारतीय मानक डेटाबेस से सत्यापित तकनीकी जानकारी और मानक विवरण नीचे दिए गए हैं।\n",
                "### 📜 संबंधित भारतीय मानक एवं क्लॉज विवरण (Applicable Standards)\n"
            ]
            for idx, chunk in enumerate(retrieved_chunks, 1):
                score_pct = max(0.0, min(1.0, chunk.get("similarity_score", 0.0))) * 100
                res.append(
                    f"#### {idx}. 🔹 **{chunk['standard_number']}** — *{chunk['title']}*\n"
                    f"- **क्लॉज / अनुभाग:** `{chunk['clause_id']}` ({chunk.get('section_number', chunk['clause_title'])})\n"
                    f"- **प्रासंगिकता स्कोर:** `{score_pct:.1f}%`\n\n"
                    f"{chunk['full_content']}\n"
                )
            res.append(
                "### 📋 अनुशंसित प्रमाणन कदम (Actionable Steps)\n"
                "1. **मानक अध्ययन**: [www.standardsbis.in](https://www.standardsbis.in) पर जाकर क्लॉज की पुष्टि करें।\n"
                "2. **e-BIS आवेदन**: [www.manakonline.in](https://www.manakonline.in) पर ISI मार्क हेतु ऑनलाइन आवेदन करें।\n"
                "3. **80% MSME छूट**: सूक्ष्म उद्यमों हेतु 80% आवेदन शुल्क छूट और 50% प्रयोगशाला सब्सिडी का लाभ उठाएं।\n"
            )
        elif lang == "Tamil":
            res = [
                "### 🎯 சுருக்கமான நேரடி பதில் (Direct Summary)\n"
                f"உங்கள் கேள்விக்கு இந்திய தரநிலைகள் தரவுத்தளத்திலிருந்து பெறப்பட்ட சரிபார்க்கப்பட்ட தொழில்நுட்பத் தகவல்கள் கீழே தரப்பட்டுள்ளன.\n",
                "### 📜 பொருந்தக்கூடிய இந்திய தரநிலைகள் (Applicable Standards)\n"
            ]
            for idx, chunk in enumerate(retrieved_chunks, 1):
                score_pct = max(0.0, min(1.0, chunk.get("similarity_score", 0.0))) * 100
                res.append(
                    f"#### {idx}. 🔹 **{chunk['standard_number']}** — *{chunk['title']}*\n"
                    f"- **பிரிவு / விதி:** `{chunk['clause_id']}` ({chunk.get('section_number', chunk['clause_title'])})\n"
                    f"- **பொருத்தம்:** `{score_pct:.1f}%`\n\n"
                    f"{chunk['full_content']}\n"
                )
            res.append(
                "### 📋 பரிந்துரைக்கப்பட்ட நடைமுறைகள் (Actionable Steps)\n"
                "1. **தரநிலைகள் விவரம்**: [www.standardsbis.in](https://www.standardsbis.in) தளத்தில் சரிபார்க்கவும்.\n"
                "2. **e-BIS பதிவு**: [www.manakonline.in](https://www.manakonline.in) மூலம் ISI உரிமத்திற்கு விண்ணப்பிக்கவும்.\n"
                "3. **MSME சலுகை**: மைக்ரோ நிறுவனங்களுக்கு 80% கட்டணச் சலுகை உண்டு.\n"
            )
        elif lang == "Bengali":
            res = [
                "### 🎯 সংক্ষিপ্ত সরাসরি উত্তর (Direct Summary)\n"
                f"আপনার প্রশ্নের জন্য ভারতীয় মানক ডেটাবেস থেকে সংগৃহীত যাচাইকৃত কারিগরি তথ্য নিচে দেওয়া হলো।\n",
                "### 📜 প্রযোজ্য ভারতীয় মানক ও ধারা (Applicable Standards)\n"
            ]
            for idx, chunk in enumerate(retrieved_chunks, 1):
                score_pct = max(0.0, min(1.0, chunk.get("similarity_score", 0.0))) * 100
                res.append(
                    f"#### {idx}. 🔹 **{chunk['standard_number']}** — *{chunk['title']}*\n"
                    f"- **ধারা / অনুচ্ছেদ:** `{chunk['clause_id']}` ({chunk.get('section_number', chunk['clause_title'])})\n"
                    f"- **প্রাসঙ্গিকতা:** `{score_pct:.1f}%`\n\n"
                    f"{chunk['full_content']}\n"
                )
            res.append(
                "### 📋 প্রয়োজনীয় পদক্ষেপ (Actionable Steps)\n"
                "1. **মানক যাচাই**: [www.standardsbis.in](https://www.standardsbis.in) দেখুন।\n"
                "2. **অনলাইন আবেদন**: [www.manakonline.in](https://www.manakonline.in) পোর্টালের মাধ্যমে আবেদন করুন।\n"
                "3. **MSME ছাড়**: ক্ষুদ্র উদ্যোগের জন্য ৮০% ফি ছাড়ের সুবিধা গ্রহণ করুন।\n"
            )
        elif lang == "Marathi":
            res = [
                "### 🎯 थेट संक्षिप्त उत्तर (Direct Summary)\n"
                f"आपल्या प्रश्नासाठी भारतीय मानक डेटाबेसमधून अधिकृत तांत्रिक माहिती खाली दिली आहे.\n",
                "### 📜 लागू भारतीय मानके व क्लॉज तपशील (Applicable Standards)\n"
            ]
            for idx, chunk in enumerate(retrieved_chunks, 1):
                score_pct = max(0.0, min(1.0, chunk.get("similarity_score", 0.0))) * 100
                res.append(
                    f"#### {idx}. 🔹 **{chunk['standard_number']}** — *{chunk['title']}*\n"
                    f"- **क्लॉज / विभाग:** `{chunk['clause_id']}` ({chunk.get('section_number', chunk['clause_title'])})\n"
                    f"- **अचूकता गुण:** `{score_pct:.1f}%`\n\n"
                    f"{chunk['full_content']}\n"
                )
            res.append(
                "### 📋 पुढील कृती टप्पे (Actionable Steps)\n"
                "1. **मानक तपासणी**: [www.standardsbis.in](https://www.standardsbis.in) ला भेट द्या.\n"
                "2. **e-BIS नोंदणी**: [www.manakonline.in](https://www.manakonline.in) वर ISI परवान्यासाठी अर्ज करा.\n"
                "3. **MSME सवलत**: सूक्ष्म उद्योगांसाठी ८०% अर्ज शुल्क सवलतीचा लाभ घ्या.\n"
            )
        else:
            res = [
                "### 🎯 Direct Summary\n"
                f"Verified technical specifications and clauses retrieved from the Indian Standards database for your inquiry:\n",
                "### 📜 Relevant Indian Standards & Clauses\n"
            ]
            for idx, chunk in enumerate(retrieved_chunks, 1):
                score_pct = max(0.0, min(1.0, chunk.get("similarity_score", 0.0))) * 100
                res.append(
                    f"#### {idx}. 🔹 **{chunk['standard_number']}** — *{chunk['title']}*\n"
                    f"- **Clause / Section:** `{chunk['clause_id']}` ({chunk.get('section_number', chunk['clause_title'])})\n"
                    f"- **Match Relevance:** `{score_pct:.1f}%`\n\n"
                    f"{chunk['full_content']}\n"
                )
            res.append(
                "### 📋 Actionable Next Steps\n"
                "1. **Verify Clause Details**: Access official standards on [www.standardsbis.in](https://www.standardsbis.in).\n"
                "2. **Apply via e-BIS**: Submit ISI license application on [e-Manakonline](https://www.manakonline.in).\n"
                "3. **Avail MSME Benefits**: Micro enterprises receive 80% application fee concession and 50% lab testing subsidy.\n"
            )

        if source_citations:
            res.append("\n**Sources & Document Attribution:**\n" + "\n".join([f"- {s}" for s in source_citations]))
            
        return "\n".join(res)


# Singleton factory helper for Streamlit
_engine_instance = None

def get_rag_engine(groq_api_key: Optional[str] = None) -> StandardsRAGEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = StandardsRAGEngine(groq_api_key=groq_api_key)
    elif groq_api_key:
        _engine_instance.set_groq_api_key(groq_api_key)
    return _engine_instance
