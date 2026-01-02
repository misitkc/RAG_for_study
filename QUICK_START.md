# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Tesseract (One-time setup)

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki

### Step 2: Get Your Groq API Key

1. Go to https://console.groq.com/
2. Sign up (free)
3. Create API key
4. Copy it

### Step 3: Setup Project

```bash
cd ~/Desktop/streamlit-rag-app
bash setup.sh
```

This will:
- Create a virtual environment
- Install all Python dependencies
- Create `.env` file from template

### Step 4: Configure API Key

Edit `.env` file and add your Groq API key:
```
GROQ_API_KEY=your_key_here
```

### Step 5: Run the App

```bash
source venv/bin/activate
streamlit run app.py
```

The app opens at: `http://localhost:8501`

---

## 📖 How to Use

### Upload Documents
1. In the sidebar, click "Upload PDF files"
2. Select one or multiple PDFs (supports images!)
3. Click "Process & Add to Knowledge Base"
4. Wait for green checkmark

### Ask Questions
1. Type your question in the search box
2. Click "Search"
3. Get answer with source citations

### Review Sources
- Each answer shows which documents were used
- Exact page numbers included
- Text snippets show context

---

## ✨ Key Features Explained

**PDF Support with Images**
- Extracts text normally
- Uses OCR (Tesseract) for images in PDFs
- Handles mixed text+image PDFs

**Semantic Search**
- Uses AI to understand meaning, not just keywords
- Finds relevant content even if words don't match exactly
- Powered by HuggingFace embeddings

**Fast Responses**
- Groq API returns answers in seconds
- Mixture of Experts (MoE) architecture is super fast
- Great for real-time study sessions

**Citation Tracking**
- Exact page numbers for each source
- Shows the text snippet used
- Helps verify and follow up on answers

**Chat Memory**
- All your questions stored in session
- Expand any question to review answer
- Delete unwanted interactions

---

## 🔍 Example Workflows

### Biology Study
1. Upload your biology textbook PDFs
2. Ask: "What are the functions of mitochondria?"
3. Get comprehensive answer with page references
4. Follow up: "Explain ATP production"

### History Learning
1. Upload history notes and documents
2. Ask: "What caused the fall of Roman Empire?"
3. Get structured explanation with sources
4. Ask follow-ups: "What role did Christianity play?"

### Math/Physics
1. Upload problem sets and solutions
2. Ask: "How do I solve quadratic equations?"
3. Get step-by-step explanation
4. Ask: "Can you show an example?"

---

## 🛠️ Customization

Edit `config.py` to customize:

```python
CHUNK_SIZE = 1000           # Larger = fewer, bigger chunks
CHUNK_OVERLAP = 200         # Overlap for better context
TOP_K_RESULTS = 4           # How many sources to use
TEMPERATURE = 0.3           # 0=focused, 1=creative
GROQ_MODEL = "mixtral-8x7b-32768"  # Different Groq models
```

---

## ❓ Common Questions

**Q: Can I use my own documents?**
A: Yes! Upload PDFs in the sidebar. Supports text and image-heavy PDFs.

**Q: Is this free?**
A: Yes! Groq offers free tier with good rate limits.

**Q: Can I use offline?**
A: No, Groq API requires internet. Vector search is local though.

**Q: How long do documents stay?**
A: Until you click "Clear All Documents" in sidebar.

**Q: Can I export conversations?**
A: Currently in session only. You can copy-paste from the UI.

**Q: Multiple users?**
A: Currently single-user. Each person needs their own instance.

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Tesseract not found" | Install tesseract for your OS |
| "API key error" | Add GROQ_API_KEY to .env file |
| "No text extracted" | PDF might be corrupted, try another |
| "Very slow first query" | Normal - downloading embedding model |
| "Port 8501 in use" | streamlit run app.py --server.port 8502 |

---

## 📚 Next Steps

1. **Upload your study materials** - PDFs, notes, textbooks
2. **Start asking questions** - Use natural language
3. **Explore sources** - Click on sources to see full context
4. **Build knowledge** - Use for review and learning

---

## 💡 Tips for Best Results

✓ Use clear, specific questions
✓ Upload complete documents (not just excerpts)
✓ Keep PDF quality good for OCR
✓ Review source citations for accuracy
✓ Use follow-up questions for deeper understanding

---

**Happy Studying! 🎓**

For detailed information, see `README.md`
