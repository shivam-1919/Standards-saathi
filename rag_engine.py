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
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

# Groq Client
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
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
                print(f"[RAG Engine Warning] Could not load SentenceTransformer '{self.model_name}': {e}")
                self.embedding_model = None

        # 2. Ingest Sample Standards
        self.chunks = get_flattened_chunks()
        
        # 3. Build Vector Index
        self.rebuild_index()
        self.is_initialized = True

    @property
    def is_degraded(self) -> bool:
        """Returns True if the semantic embedding model or FAISS index failed to initialize."""
        return self.embedding_model is None or self.faiss_index is None

    def set_groq_api_key(self, api_key: str):
        """Updates the Groq API key dynamically."""
        self.groq_api_key = api_key

    def rebuild_index(self):
        """Computes embeddings for all chunks and builds/refreshes the FAISS index."""
        if not self.chunks:
            return

        texts = [chunk["text"] for chunk in self.chunks]

        if self.embedding_model is not None:
            # Generate 384-dimensional dense embeddings
            raw_embeddings = self.embedding_model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
            # Normalize vectors for Cosine Similarity
            faiss.normalize_L2(raw_embeddings) if HAS_FAISS else None
            self.chunk_embeddings = raw_embeddings.astype(np.float32)
        else:
            # Fallback lightweight deterministic keyword/hash vectorizer
            self.chunk_embeddings = self._fallback_embed_batch(texts)

        # Build FAISS index
        if HAS_FAISS and self.chunk_embeddings is not None:
            dim = self.chunk_embeddings.shape[1]
            # IndexFlatIP with normalized vectors computes exact Cosine Similarity
            self.faiss_index = faiss.IndexFlatIP(dim)
            self.faiss_index.add(self.chunk_embeddings)
        else:
            self.faiss_index = None

    def _fallback_embed_batch(self, texts: List[str], dim: int = 128) -> np.ndarray:
        """Lightweight bag-of-words fallback embedding if transformer is offline."""
        embeddings = []
        for text in texts:
            vec = np.zeros(dim, dtype=np.float32)
            words = re.findall(r'\w+', text.lower())
            for word in words:
                h = abs(hash(word)) % dim
                vec[h] += 1.0
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            embeddings.append(vec)
        return np.array(embeddings, dtype=np.float32)

    def _embed_query(self, query: str) -> np.ndarray:
        """Embeds a single user query."""
        if self.embedding_model is not None:
            query_vec = self.embedding_model.encode([query], convert_to_numpy=True).astype(np.float32)
            if HAS_FAISS:
                faiss.normalize_L2(query_vec)
            return query_vec
        else:
            vec = self._fallback_embed_batch([query], dim=self.chunk_embeddings.shape[1] if self.chunk_embeddings is not None else 128)
            return vec

    def add_custom_standard(self, standard_data: Dict[str, Any]) -> int:
        """
        Allows users to add new Indian Standards on the fly.
        Appends chunks and immediately rebuilds the FAISS vector index.
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

        # Re-index all chunks into FAISS
        self.rebuild_index()
        return len(self.chunks)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves the top_k most relevant chunks using FAISS cosine similarity.
        """
        if not self.chunks:
            return []

        top_k = min(top_k, len(self.chunks))
        query_vec = self._embed_query(query)

        if HAS_FAISS and self.faiss_index is not None:
            scores, indices = self.faiss_index.search(query_vec, top_k)
            retrieved = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.chunks) and idx >= 0:
                    chunk_data = dict(self.chunks[idx])
                    # Score is cosine similarity (-1.0 to 1.0, scaled to percentage)
                    chunk_data["similarity_score"] = float(score)
                    retrieved.append(chunk_data)
            return retrieved
        else:
            # Fallback Dot Product
            if self.chunk_embeddings is not None:
                sims = np.dot(self.chunk_embeddings, query_vec.T).squeeze()
                top_indices = np.argsort(sims)[::-1][:top_k]
                retrieved = []
                for idx in top_indices:
                    chunk_data = dict(self.chunks[idx])
                    chunk_data["similarity_score"] = float(sims[idx])
                    retrieved.append(chunk_data)
                return retrieved

        return self.chunks[:top_k]

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
        Executes full RAG workflow with citations and related standards.
        """
        # Step 1: Retrieve context chunks
        retrieved_chunks = self.retrieve(query, top_k=top_k)

        # Extract related standards and unique source documents
        related_standards_set = set()
        source_citations = []
        for idx, chunk in enumerate(retrieved_chunks, 1):
            filename = chunk.get("filename", f"{chunk['standard_number'].replace(':', '_').replace(' ', '_')}.pdf")
            page_num = chunk.get("page_number", idx * 2)
            section_num = chunk.get("section_number", chunk.get("clause_id", "Section 1.0"))
            purchase_url = chunk.get("purchase_url", "https://www.manakonline.in/MANAK/home")
            
            source_citations.append(
                f"📄 {filename}, Page {page_num}, {section_num} | 🔗 Purchase: {purchase_url}"
            )
            for rel in chunk.get("related_standards", []):
                related_standards_set.add(rel)

        related_standards_list = list(related_standards_set)[:4]

        # Step 2: Assemble context text
        context_blocks = []
        for idx, chunk in enumerate(retrieved_chunks, 1):
            context_blocks.append(
                f"[Source {idx}]: {chunk['standard_number']} — {chunk['title']}\n"
                f"Document: {chunk.get('filename')} | Page {chunk.get('page_number')} | Section: {chunk.get('section_number')}\n"
                f"Clause: {chunk['clause_id']} ({chunk['clause_title']})\n"
                f"Content:\n{chunk['full_content']}\n"
            )
        context_str = "\n---\n".join(context_blocks)

        # Step 3: Check Groq API Availability
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY", "")
        
        if not api_key:
            fallback_answer = self._generate_offline_fallback(query, retrieved_chunks, source_citations)
            return {
                "answer": fallback_answer,
                "citations": retrieved_chunks,
                "sources_text": "\n".join(source_citations),
                "related_standards": related_standards_list,
                "is_fallback": True,
                "model": "Local RAG Retriever"
            }

        # Step 4: Construct System Prompt & Messages for Groq LLM
        lang_instruction = (
            "Respond in clear, professional English."
            if language == "English"
            else "Respond in natural, professional Hindi (हिंदी / Hinglish) with clear Devanagari or Hinglish explanations."
        )

        system_prompt = (
            "You are 'Standards Saathi' (मानक साथी), the official-grade AI technical advisor for Indian Standards (IS Codes), "
            "Bureau of Indian Standards (BIS) regulations, Quality Control Orders (QCOs), and certification schemes.\n\n"
            f"LANGUAGE DIRECTIVE: {lang_instruction}\n\n"
            "INSTRUCTIONS:\n"
            "1. Answer the question accurately, authoritatively, and concisely based strictly on the retrieved context.\n"
            "2. Structure your response with a Direct Answer (1-2 sentences), followed by a clean Markdown Table (if comparing limits/grades), followed by 2-3 key bullet points.\n"
            "3. Mention whether mandatory Quality Control Orders (QCO) or ISI mark applies.\n"
            "4. Mention MSME 80% fee concession or verification via BIS Care App if applicable.\n"
            "5. Do NOT include generic disclaimers. End your response neatly."
        )

        user_content = (
            f"USER QUESTION:\n{query}\n\n"
            f"RETRIEVED INDIAN STANDARDS CONTEXT:\n"
            f"{context_str}\n\n"
            f"Please provide an accurate answer directly addressing the user's question."
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
        candidate_models.extend(["groq/compound-mini", "llama-3.1-8b-instant", "qwen/qwen3.6-27b", "allam-2-7b"])
        candidate_models = list(dict.fromkeys(candidate_models))

        client = Groq(api_key=api_key)
        raw_answer = ""

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
                break
            except Exception as e:
                continue

        if not raw_answer:
            raw_answer = self._generate_offline_fallback(query, retrieved_chunks, source_citations)

        # Format Final Answer with Required Citations Block
        if len(source_citations) == 1:
            sources_block = f"\n\n**Sources:** {source_citations[0]}"
        else:
            sources_block = "\n\n**Sources:**\n" + "\n".join([f"- {s}" for s in source_citations])
        full_formatted_answer = f"{raw_answer}\n{sources_block}"

        return {
            "answer": full_formatted_answer,
            "raw_answer": raw_answer,
            "citations": retrieved_chunks,
            "sources_text": "\n".join(source_citations),
            "related_standards": related_standards_list,
            "is_fallback": False,
            "model": f"{model_name} (Groq)"
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
