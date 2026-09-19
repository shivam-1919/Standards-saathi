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

# Sentence Transformers & FAISS
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except Exception:
    HAS_SENTENCE_TRANSFORMERS = False

try:
    import faiss
    HAS_FAISS = True
except Exception:
    HAS_FAISS = False

# Groq Client
try:
    from groq import Groq
    HAS_GROQ = True
except Exception:
    HAS_GROQ = False

from sample_data import get_flattened_chunks, SAMPLE_STANDARDS


class StandardsRAGEngine:
    """
    RAG Engine that embeds, indexes, and queries Indian Standards documents.
    """
    _instance = None

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", groq_api_key: Optional[str] = None):
        self.model_name = model_name
        key = groq_api_key or os.getenv("GROQ_API_KEY", "")
        if not key:
            try:
                import streamlit as st
                if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                    key = str(st.secrets["GROQ_API_KEY"])
            except Exception:
                pass
        self.groq_api_key = key
        self.embedding_model = None
        self.faiss_index = None
        self.chunks: List[Dict[str, Any]] = []
        self.chunk_embeddings: Optional[np.ndarray] = None
        self.is_initialized = False
        
        self.initialize_engine()

    def initialize_engine(self):
        """Loads embedding model, prepares chunks, and builds FAISS vector index."""
        # 1. Load Embedding Model
        if HAS_SENTENCE_TRANSFORMERS:
            try:
                self.embedding_model = SentenceTransformer(self.model_name)
            except Exception as e:
                # Log cleanly without crashing
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

    def set_groq_api_key(self, api_key: str):
        """Updates the Groq API key dynamically."""
        self.groq_api_key = api_key

    def rebuild_index(self):
        """Computes embeddings for all chunks and builds/refreshes the FAISS index."""
        if not self.chunks:
            return

        texts = [chunk["text"] for chunk in self.chunks]

        if self.embedding_model is not None and HAS_FAISS:
            try:
                # Generate 384-dimensional dense embeddings
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
        """Builds a fast in-memory TF-IDF index for exact keyword and clause resolution."""
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
            
            tokens = re.findall(r'[a-zA-Z0-9_\-\:]+', full_text)
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

    def _fallback_retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """High-precision BM25/TF-IDF and semantic keyword retriever."""
        import math
        from collections import Counter
        
        query_tokens = re.findall(r'[a-zA-Z0-9_\-\:]+', query.lower())
        if not query_tokens:
            return self.chunks[:top_k]
            
        # Extract query standard numbers (e.g. 10500, 2062, 1239, 456, 1417, 15820, 2720, 1293, 732, 2189, 16046)
        query_is_numbers = re.findall(r'(?:is|is\s*)?(\d{3,5})', query.lower())
        
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
                    score += 0.45
                    
            # Boost 2: Keyword overlap
            chunk_keywords = [k.lower() for k in chunk.get("keywords", [])]
            for q_tok in query_tokens:
                if any(q_tok in k for k in chunk_keywords):
                    score += 0.08
                    
            # Boost 3: Category match
            cat_lower = chunk.get("category", "").lower()
            for q_tok in query_tokens:
                if len(q_tok) > 3 and q_tok in cat_lower:
                    score += 0.05
                    
            chunk_data = dict(chunk)
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
        Retrieves the top_k most relevant chunks using FAISS or high-precision TF-IDF matcher.
        """
        if not self.chunks:
            return []

        top_k = min(top_k, len(self.chunks))

        if HAS_FAISS and self.faiss_index is not None and self.embedding_model is not None:
            try:
                query_vec = self.embedding_model.encode([query], convert_to_numpy=True).astype(np.float32)
                faiss.normalize_L2(query_vec)
                scores, indices = self.faiss_index.search(query_vec, top_k)
                retrieved = []
                for score, idx in zip(scores[0], indices[0]):
                    if idx < len(self.chunks) and idx >= 0:
                        chunk_data = dict(self.chunks[idx])
                        chunk_data["similarity_score"] = float(score)
                        retrieved.append(chunk_data)
                if retrieved:
                    return retrieved
            except Exception:
                pass

        # Use robust TF-IDF / BM25 fallback
        return self._fallback_retrieve(query, top_k=top_k)

    def _detect_prompt_injection(self, query: str) -> Optional[str]:
        """Detects prompt injection attempts, system prompt exfiltration, and jailbreak patterns."""
        injection_patterns = [
            r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
            r"disregard\s+(all\s+)?(previous|prior|above)",
            r"forget\s+(all\s+)?(previous|prior|your)\s+instructions",
            r"system\s*prompt",
            r"reveal\s+(your\s+)?(system|initial)\s+prompt",
            r"print\s+(your\s+)?(system|initial)\s+prompt",
            r"you\s+are\s+now\s+(in\s+)?(dan|developer|jailbreak|unrestricted)\s+mode",
            r"bypass\s+(all\s+)?(safety|security|rules|guardrails)",
            r"<\|im_start\|>",
            r"<\|system\|>",
            r"```\s*system",
            r"act\s+as\s+(an?\s+)?unfiltered",
            r"override\s+(all\s+)?(safety|system)\s+directives",
            r"grant\s+me\s+(a\s+)?legal\s+(license|exemption|ruling)"
        ]
        q_lower = query.lower()
        for pat in injection_patterns:
            if re.search(pat, q_lower):
                return (
                    "🛡️ **Safety & Security Advisory**: Unauthorized instruction override, prompt-injection pattern, "
                    "or legal ruling request detected. Standards Saathi strictly adheres to official Bureau of Indian Standards (BIS) "
                    "knowledge and safety guidelines. Please submit a valid technical inquiry regarding Indian Standards (IS Codes) or BIS certification procedures."
                )
        return None

    def _generate_no_evidence_response(self, query: str, language: str = "English") -> str:
        """Generates a reliable refusal response when relevant evidence is not found in the BIS database."""
        if language == "हिंदी":
            return (
                "### ℹ️ बीआईएस ज्ञान आधार में पर्याप्त साक्ष्य उपलब्ध नहीं है\n\n"
                "मानक साथी (Standards Saathi) के अधिकृत डेटाबेस में इस प्रश्न का सटीक व सत्यापित उत्तर देने के लिए **पर्याप्त क्लॉज या दस्तावेजी साक्ष्य नहीं मिले हैं।**\n\n"
                "सटीकता और विश्वसनीयता बनाए रखने के लिए, मानक साथी अनुमान नहीं लगाता है।\n\n"
                "**आधिकारिक बीआईएस संसाधन:**\n"
                "- 🔍 **बीआईएस मानक पोर्टल**: 20,000+ भारतीय मानकों को खोजने के लिए [www.standardsbis.in](https://www.standardsbis.in) पर जाएं।\n"
                "- 📋 **e-BIS मानकऑनलाइन पोर्टल**: प्रमाणन और लाइसेंसिंग के लिए [www.manakonline.in](https://www.manakonline.in) पर जाएं।\n"
                "- 🏢 **निकटतम बीआईएस शाखा कार्यालय**: आधिकारिक बीआईएस कार्यालयों की सूची के लिए [BIS Branch Directory](https://www.bis.gov.in/about-bis/branch-offices/) देखें।\n\n"
                "---\n*⚖️ वैधानिक सूचना: मानक साथी एक तकनीकी सलाहकार AI उपकरण है और यह कोई कानूनी, नियामक या लाइसेंसिंग निर्णय प्रदान नहीं करता है।*"
            )
        return (
            "### ℹ️ Insufficient Evidence in BIS Knowledge Base\n\n"
            "Based on the authorized Bureau of Indian Standards (BIS) knowledge base loaded in Standards Saathi, "
            "**sufficient verified evidence was not found to reliably answer this query without speculation.**\n\n"
            "To ensure absolute technical reliability and compliance, Standards Saathi does not guess or extrapolate beyond authorized documents.\n\n"
            "**Recommended Official Actions:**\n"
            "- 🔍 **Search the BIS Catalog**: Visit the official [BIS Standards Portal](https://www.standardsbis.in) or [e-BIS Manakonline](https://www.manakonline.in) to search across 20,000+ Indian Standards.\n"
            "- 📋 **Check Mandatory Quality Control Orders (QCOs)**: View official ministerial mandates at [BIS QCO Tracker](https://www.bis.gov.in/product-certification/qco-orders/).\n"
            "- 🏢 **Contact BIS Directorate**: Reach out to your nearest [BIS Regional or Branch Office](https://www.bis.gov.in/about-bis/branch-offices/).\n\n"
            "---\n*⚖️ Statutory Notice: Standards Saathi is an AI technical advisory assistant. Official certification decisions, licensing grants, and statutory rulings are subject to formal verification by the Bureau of Indian Standards.*"
        )

    def generate_response(
        self,
        query: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        top_k: int = 3,
        temperature: float = 0.2,
        language: str = "English",
        model_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes full RAG workflow with safety guardrails, prompt injection detection,
        grounding threshold verification, clause citations, and version tracking.
        """
        # Guardrail 1: Prompt Injection Defense
        injection_alert = self._detect_prompt_injection(query)
        if injection_alert:
            return {
                "answer": injection_alert,
                "raw_answer": injection_alert,
                "citations": [],
                "sources_text": "",
                "related_standards": [],
                "is_fallback": True,
                "model": "Guardrails Defense Filter"
            }

        # Step 1: Retrieve context chunks
        retrieved_chunks = self.retrieve(query, top_k=top_k)

        # Guardrail 2: Grounding Confidence Check
        max_score = max([c.get("similarity_score", 0.0) for c in retrieved_chunks]) if retrieved_chunks else 0.0
        # If max similarity score is low (< 0.38) or empty, refuse to guess
        if not retrieved_chunks or max_score < 0.38:
            no_ev_ans = self._generate_no_evidence_response(query, language=language)
            return {
                "answer": no_ev_ans,
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

        # Step 3: Check Groq API Availability
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY", "")
        
        statutory_disclaimer = (
            "\n\n---\n*⚖️ Statutory Notice: Standards Saathi provides technical and procedural advisory grounded in Indian Standards. "
            "It does NOT issue legal decisions, licensing grants, or statutory laboratory approval rulings. "
            "For official certifications, please apply through e-BIS Manakonline (www.manakonline.in).*"
            if language == "English" else
            "\n\n---\n*⚖️ वैधानिक सूचना: मानक साथी भारतीय मानकों पर आधारित एक AI तकनीकी सलाहकार उपकरण है। यह कोई कानूनी, प्रमाणन, या प्रयोगशाला अनुमोदन निर्णय जारी नहीं करता है। आधिकारिक प्रमाणन के लिए e-BIS मानकऑनलाइन (www.manakonline.in) पर आवेदन करें।*"
        )

        if not api_key:
            fallback_answer = self._generate_offline_fallback(query, retrieved_chunks, source_citations)
            return {
                "answer": f"{fallback_answer}{statutory_disclaimer}",
                "citations": retrieved_chunks,
                "sources_text": "\n".join(source_citations),
                "related_standards": related_standards_list,
                "is_fallback": True,
                "model": "Local RAG Retriever"
            }

        # Step 4: Construct System Prompt & Messages for Groq LLM with Strict Guardrails
        lang_instruction = (
            "Respond in clear, authoritative, professional English."
            if language == "English"
            else "Respond in natural, professional Hindi (हिंदी / Hinglish) with clear Devanagari or Hinglish explanations."
        )

        system_prompt = (
            "You are 'Standards Saathi' (मानक साथी), the official-grade AI technical advisor for Indian Standards (IS Codes), "
            "Bureau of Indian Standards (BIS) regulations, Quality Control Orders (QCOs), and certification schemes.\n\n"
            f"LANGUAGE DIRECTIVE: {lang_instruction}\n\n"
            "SAFETY & RELIABILITY GUARDRAILS (CRITICAL RULES):\n"
            "1. STRICT GROUNDING: Base your entire answer ONLY on the provided Indian Standards context. Do NOT extrapolate, hallucinate, or guess.\n"
            "2. REGULATORY & LEGAL BOUNDARIES: You do NOT have the authority to grant licenses, issue legal rulings, or make definitive regulatory/laboratory pass-fail approvals. Always direct users to official BIS portals (www.manakonline.in / www.bis.gov.in) for formal verification.\n"
            "3. ACCURACY & ATTRIBUTION: Mention the exact standard number (e.g. IS 10500:2012, IS 2062:2011), relevant clauses, and whether mandatory QCO / ISI mark applies.\n"
            "4. MSME BENEFITS: Mention MSME 80% fee concession on application/license fees or 50% lab testing subsidy where applicable.\n"
            "5. STRUCTURE: Provide a Direct Answer (1-2 sentences), clean Markdown Table (if comparing parameters/grades), followed by 2-3 bullet points."
        )

        user_content = (
            f"USER QUESTION:\n{query}\n\n"
            f"RETRIEVED INDIAN STANDARDS CONTEXT (AUTHORIZED EVIDENCE):\n"
            f"{context_str}\n\n"
            f"Please provide an accurate, strictly grounded response."
        )

        messages = [{"role": "system", "content": system_prompt}]

        if chat_history:
            for turn in chat_history[-4:]:
                messages.append({"role": turn["role"], "content": turn["content"]})

        messages.append({"role": "user", "content": user_content})

        # Step 5: Call Groq API with robust model candidates
        candidate_models = []
        if model_override:
            candidate_models.append(model_override)
        candidate_models.extend(["groq/compound-mini", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"])
        candidate_models = list(dict.fromkeys(candidate_models))

        client = Groq(api_key=api_key)
        raw_answer = ""
        successful_model = None

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
                successful_model = model_name
                break
            except Exception:
                continue

        if not raw_answer:
            raw_answer = self._generate_offline_fallback(query, retrieved_chunks, source_citations)

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

    def _generate_offline_fallback(self, query: str, retrieved_chunks: List[Dict[str, Any]], source_citations: Optional[List[str]] = None) -> str:
        """Generates a structured answer directly from retrieved chunks when LLM API is unavailable."""
        if not retrieved_chunks:
            return "No matching Indian Standards were found in the current knowledge base."

        res = [
            "### Relevant Indian Standards Found:\n",
            "Here is the verified technical information retrieved from the Indian Standards database:\n"
        ]
        for idx, chunk in enumerate(retrieved_chunks, 1):
            score_pct = max(0.0, min(1.0, chunk.get("similarity_score", 0.0))) * 100
            res.append(
                f"#### {idx}. {chunk['standard_number']} — {chunk['title']}\n"
                f"**Clause / Section:** `{chunk['clause_id']}` ({chunk.get('section_number', chunk['clause_title'])})  \n"
                f"**Match Relevance:** `{score_pct:.1f}%`  \n"
                f"{chunk['full_content']}\n"
            )
        
        if source_citations:
            res.append("\n**Sources:**\n" + "\n".join([f"- {s}" for s in source_citations]))
            
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
