"""Main Streamlit application for RAG Study Assistant."""

import os
import tempfile
from pathlib import Path
import streamlit as st

from config import PAGE_TITLE, PAGE_ICON, MAX_UPLOAD_SIZE
from utils.document_loader import DocumentLoader
from utils.rag_chain import RAGChain


# Page config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 0rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1em;
        padding: 0.5rem 1rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #0066cc;
    }
    .answer-box {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = RAGChain()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "document_loader" not in st.session_state:
        st.session_state.document_loader = DocumentLoader()


def display_header():
    """Display header section."""
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.title(f"{PAGE_ICON} Study RAG Assistant")
        st.markdown("*Learn better with AI-powered Q&A from your documents*")
    with col2:
        st.markdown("")


def display_sidebar():
    """Display sidebar with document management."""
    with st.sidebar:
        st.header("Document Management")

        # Display document stats
        doc_info = st.session_state.rag_chain.get_documents_info()
        st.metric("Total Chunks", doc_info["total_chunks"])

        if doc_info["documents"]:
            st.subheader("Loaded Documents")
            for doc_name, chunk_count in doc_info["documents"].items():
                st.write(f"📄 {doc_name}")
                st.caption(f"{chunk_count} chunks")

        st.divider()

        # Upload section
        st.subheader("Upload New Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF files (with or without images)",
            type=["pdf"],
            accept_multiple_files=True,
            help="Max 50MB per file"
        )

        if uploaded_files:
            if st.button("Process & Add to Knowledge Base", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()

                for idx, uploaded_file in enumerate(uploaded_files):
                    try:
                        # Check file size
                        if uploaded_file.size > MAX_UPLOAD_SIZE:
                            st.error(f"{uploaded_file.name} exceeds 50MB limit")
                            continue

                        status_text.text(f"Processing {uploaded_file.name}...")

                        # Save temporarily and process
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(uploaded_file.getbuffer())
                            tmp_path = tmp_file.name

                        # Load document
                        chunks, metadata = st.session_state.document_loader.load_pdf(tmp_path)

                        # Add to RAG chain
                        st.session_state.rag_chain.add_documents(chunks)

                        # Clean up
                        os.unlink(tmp_path)

                        st.success(f"✓ Processed {uploaded_file.name} ({len(chunks)} chunks)")

                        progress_bar.progress((idx + 1) / len(uploaded_files))

                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")

                status_text.text("All documents processed!")

        st.divider()

        # Clear database button
        if st.button("Clear All Documents", help="Remove all documents from knowledge base"):
            st.session_state.rag_chain.clear_documents()
            st.session_state.chat_history = []
            st.success("Knowledge base cleared!")
            st.rerun()

        # Settings
        st.subheader("Settings")
        show_sources = st.checkbox("Always show sources", value=True)


def display_qa_section():
    """Display Q&A section."""
    st.header("Ask Questions")

    col1, col2 = st.columns([0.85, 0.15])

    with col1:
        query = st.text_input(
            "Enter your question:",
            placeholder="What is... ? Explain... How does...?",
            label_visibility="collapsed"
        )

    with col2:
        search_button = st.button("Search", type="primary", use_container_width=True)

    if search_button and query:
        doc_info = st.session_state.rag_chain.get_documents_info()
        if doc_info["total_chunks"] == 0:
            st.warning("Please upload documents first!")
            return

        with st.spinner("Searching and generating answer..."):
            answer, sources = st.session_state.rag_chain.query(query)

            # Add to chat history
            st.session_state.chat_history.append({
                "query": query,
                "answer": answer,
                "sources": sources
            })

    # Display chat history
    if st.session_state.chat_history:
        st.divider()
        st.subheader("Conversation History")

        # Display in reverse order (newest first)
        for i, interaction in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(
                f"Q: {interaction['query'][:60]}...",
                expanded=(i == 0)
            ):
                st.markdown("### Answer")
                st.markdown(
                    f'<div class="answer-box">{interaction["answer"]}</div>',
                    unsafe_allow_html=True
                )

                st.markdown("### Sources & Citations")
                sources = interaction["sources"]

                if sources:
                    for source_idx, source in enumerate(sources, 1):
                        source_html = f"""
                        <div class="source-box">
                            <strong>Source {source_idx}</strong><br/>
                            <strong>Document:</strong> {source.get('source', 'Unknown')}<br/>
                            <strong>Page:</strong> {source.get('page', '?')}<br/>
                            <strong>Content:</strong> {source.get('text', '')[:300]}...
                        </div>
                        """
                        st.markdown(source_html, unsafe_allow_html=True)
                else:
                    st.info("No sources retrieved for this query")

                if st.button("Delete this interaction", key=f"delete_{i}"):
                    st.session_state.chat_history.pop(len(st.session_state.chat_history) - 1 - i)
                    st.rerun()


def main():
    """Main application function."""
    initialize_session_state()

    display_header()
    display_sidebar()
    display_qa_section()

    # Footer
    st.divider()
    st.markdown("""
    <small>
    **Study RAG Assistant** - Powered by LangChain, Groq, and FAISS
    | Made for effective learning through AI-assisted Q&A
    </small>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
