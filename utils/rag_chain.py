"""RAG chain implementation with Groq integration."""

from typing import List, Dict, Tuple
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from utils.vector_store import VectorStore
from config import GROQ_API_KEY, GROQ_MODEL, TOP_K_RESULTS, TEMPERATURE


class RAGChain:
    """RAG chain for Q&A with citations."""

    def __init__(self):
        """Initialize RAG chain."""
        self.vector_store = VectorStore()
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=TEMPERATURE
        )

    def query(self, query: str) -> Tuple[str, List[Dict]]:
        """
        Answer a question using RAG.

        Args:
            query: Question text

        Returns:
            Tuple of (answer text, source chunks)
        """
        # Retrieve relevant chunks
        retrieved_chunks = self.vector_store.search(query, top_k=TOP_K_RESULTS)

        if not retrieved_chunks:
            return "No relevant documents found in the knowledge base.", []

        # Build context from chunks
        context = self._build_context(retrieved_chunks)

        # Generate answer
        answer = self._generate_answer(query, context)

        return answer, retrieved_chunks

    def _build_context(self, chunks: List[Dict]) -> str:
        """Build context string from chunks."""
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            source = chunk.get("source", "Unknown")
            page = chunk.get("page", "?")
            text = chunk.get("text", "")
            context_parts.append(
                f"[Source {i}: {source}, Page {page}]\n{text}\n"
            )
        return "\n".join(context_parts)

    def _generate_answer(self, query: str, context: str) -> str:
        """Generate answer using Groq LLM."""
        system_prompt = """You are a helpful study assistant. Your task is to:
1. Answer the user's question clearly and comprehensively
2. Base your answer on the provided context
3. Explain concepts thoroughly for learning purposes
4. Be accurate and avoid making up information
5. If the context doesn't contain information to answer the question, say so clearly

Always provide clear, educational explanations."""

        user_prompt = f"""Context from documents:
{context}

Question: {query}

Please provide a comprehensive answer with explanations. Cite which documents and pages you're using."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.llm.invoke(messages)
        return response.content

    def add_documents(self, chunks: List[Dict]) -> None:
        """Add documents to the RAG system."""
        self.vector_store.add_chunks(chunks)

    def clear_documents(self) -> None:
        """Clear all documents from the RAG system."""
        self.vector_store.clear_index()

    def get_documents_info(self) -> Dict:
        """Get information about loaded documents."""
        return {
            "total_chunks": self.vector_store.get_total_chunks(),
            "documents": self.vector_store.get_documents_info()
        }
