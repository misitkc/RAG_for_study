#!/bin/bash

echo "==================================="
echo "Study RAG Assistant Setup"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✓ Virtual environment created and activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Check for Tesseract
echo "Checking for Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    echo "✓ Tesseract found: $(tesseract --version | head -1)"
else
    echo "⚠ Tesseract OCR not found. Please install it:"
    echo "  macOS: brew install tesseract"
    echo "  Ubuntu: sudo apt-get install tesseract-ocr"
    echo "  Windows: https://github.com/UB-Mannheim/tesseract/wiki"
fi

echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠ Please edit .env and add your GROQ_API_KEY"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GROQ_API_KEY"
echo "2. Run: source venv/bin/activate"
echo "3. Run: streamlit run app.py"
echo ""
