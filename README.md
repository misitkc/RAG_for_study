# Study RAG Assistant

An intelligent Retrieval-Augmented Generation (RAG) application for studying from PDFs using LangChain, Groq, and FAISS. Upload your study materials, ask questions, and get AI-powered answers with source citations.

## Features

✨ **Smart Document Processing**
- Upload PDFs with text and images
- Automatic OCR for images in PDFs
- Intelligent text chunking for better retrieval

🤖 **AI-Powered Q&A**
- Fast responses using Groq's API
- Semantic search with FAISS vector store
- Detailed explanations for learning

📚 **Citation & Source Tracking**
- Exact page numbers for each source
- Text snippets showing where answers come from
- Complete document metadata

💾 **Conversation Memory**
- Chat history preservation
- Easy reference to previous questions
- Delete unnecessary interactions

## Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Groq API Key** - Get it free at https://console.groq.com/
3. **Tesseract OCR** - Required for PDF image processing

#### Install Tesseract (macOS)
```bash
brew install tesseract
```

#### Install Tesseract (Ubuntu/Debian)
```bash
sudo apt-get install tesseract-ocr
```

#### Install Tesseract (Windows)
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### Installation

1. **Navigate to the project directory:**
```bash
cd ~/Desktop/streamlit-rag-app
```

2. **Create a Python virtual environment (optional but recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file with your Groq API key:**
```bash
cp .env.example .env
```

Then edit `.env` and add your API key:
```
GROQ_API_KEY=your_actual_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

### 1. Upload Documents
- Click the file uploader in the sidebar
- Select one or multiple PDF files
- Click "Process & Add to Knowledge Base"
- Wait for processing to complete

### 2. Ask Questions
- Type your question in the search box
- Click "Search" or press Enter
- View the AI-generated answer and sources

### 3. Review Sources
- Each answer shows the sources used
- Click to expand and see full source details
- Check page numbers and text snippets

### 4. Manage Conversation
- View your chat history below the search box
- Delete individual interactions if needed
- Clear all documents from the sidebar

## Architecture

### Core Components

**Document Loader** (`utils/document_loader.py`)
- Extracts text from PDFs using PyPDF
- Performs OCR on images using Tesseract
- Chunks text intelligently with overlap

**Embeddings** (`utils/embeddings_handler.py`)
- Uses HuggingFace `all-MiniLM-L6-v2` model
- Converts text to semantic embeddings
- ~384 dimensions per embedding

**Vector Store** (`utils/vector_store.py`)
- FAISS index for fast similarity search
- Local storage (no external services needed)
- Metadata tracking for citations

**RAG Chain** (`utils/rag_chain.py`)
- Retrieves relevant chunks
- Prompts Groq LLM with context
- Returns answer with source tracking

### Data Flow
```
PDF Upload
    ↓
Text + Image Extraction (OCR)
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
FAISS Index Storage
    ↓
User Query
    ↓
Semantic Search
    ↓
Context Retrieval
    ↓
Groq LLM Generation
    ↓
Answer + Citations
```

## Configuration

Edit `config.py` to customize:

```python
CHUNK_SIZE = 1000              # Characters per chunk
CHUNK_OVERLAP = 200            # Overlap between chunks
TOP_K_RESULTS = 4              # Number of chunks to retrieve
TEMPERATURE = 0.3              # LLM temperature (0=deterministic)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # HuggingFace model
```

## Storage Structure

```
~/Desktop/streamlit-rag-app/
├── data/
│   ├── faiss_index             # Vector store index
│   └── metadata.json           # Chunk metadata
├── uploads/                    # Temporary upload folder
└── [other files]
```

## API Key Setup

1. Go to https://console.groq.com/
2. Sign up for a free account
3. Create an API key
4. Add it to your `.env` file as `GROQ_API_KEY`

**Note:** Groq offers free tier with good rate limits for studying!

## Troubleshooting

### "Tesseract OCR not found"
Install Tesseract using the commands above for your OS.

### "GROQ_API_KEY not found"
- Create `.env` file in the project root
- Add your actual API key: `GROQ_API_KEY=your_key_here`

### "No text extracted from PDF"
- Ensure PDF is not corrupted
- Try the PDF in Adobe Reader first
- The app will still work with text-only extraction if OCR fails

### "Slow first query"
- First query downloads the embedding model
- Subsequent queries are much faster
- FAISS index builds incrementally

## Performance Tips

1. **Chunk Size**: Smaller chunks = more retrieval overhead but better precision
2. **Model Choice**: mixtral-8x7b is fast; llama2-70b is slower but more capable
3. **Embedding Model**: all-MiniLM-L6-v2 is lightweight (~22MB)
4. **Vector Store**: FAISS scales to millions of chunks

## Limitations

- Local FAISS (single machine only)
- No authentication/multi-user support
- OCR quality depends on PDF image quality
- Groq API rate limits apply to free tier

## Future Enhancements

- [ ] Support for more document formats (DOCX, TXT, etc.)
- [ ] User accounts and document sharing
- [ ] Custom embedding models
- [ ] Conversation branching
- [ ] Document highlighting in source PDF
- [ ] Export chat as PDF/Markdown

## License

MIT License - Feel free to use for studying!

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify Tesseract is installed: `tesseract --version`
3. Verify dependencies: `pip list`
4. Check your internet connection (for Groq API)
5. View Streamlit logs: Press 'C' in the app

---

**Happy Learning! 📚**

Made with ❤️ for effective AI-assisted studying
