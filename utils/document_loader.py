"""Document loader for PDFs with OCR support for images."""

import os
import json
from pathlib import Path
from typing import List, Dict, Tuple
import tempfile

from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import streamlit as st

from config import CHUNK_SIZE, CHUNK_OVERLAP


class DocumentLoader:
    """Load and process PDF documents with OCR for images."""

    def __init__(self):
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP
        self.documents = {}  # Store document metadata

    def load_pdf(self, file_path: str) -> Tuple[List[Dict], Dict]:
        """
        Load a PDF file with text and OCR for images.

        Args:
            file_path: Path to the PDF file

        Returns:
            Tuple of (chunks list, metadata dict)
        """
        file_name = Path(file_path).name
        chunks = []
        metadata = {
            "filename": file_name,
            "total_pages": 0,
            "chunks": []
        }

        try:
            # First, extract text using pypdf
            pdf_reader = PdfReader(file_path)
            total_pages = len(pdf_reader.pages)
            metadata["total_pages"] = total_pages

            text_by_page = {}
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                text_by_page[page_num] = text if text.strip() else ""

            # Convert PDF to images and perform OCR on pages with little/no text
            try:
                images = convert_from_path(file_path)
                for page_num, image in enumerate(images):
                    if page_num not in text_by_page or not text_by_page[page_num].strip():
                        # Perform OCR if page has no text or minimal text
                        ocr_text = pytesseract.image_to_string(image)
                        if ocr_text.strip():
                            text_by_page[page_num] = ocr_text
            except Exception as e:
                st.warning(f"OCR processing skipped for {file_name}: {str(e)}")
                st.info("Make sure Tesseract OCR is installed. On macOS: brew install tesseract")

            # Create chunks from all pages
            for page_num, page_text in text_by_page.items():
                if page_text.strip():
                    page_chunks = self._create_chunks(
                        page_text,
                        source_file=file_name,
                        page_number=page_num + 1
                    )
                    chunks.extend(page_chunks)
                    metadata["chunks"].append({
                        "page": page_num + 1,
                        "chunk_count": len(page_chunks)
                    })

            if not chunks:
                raise ValueError(f"No text could be extracted from {file_name}")

            return chunks, metadata

        except Exception as e:
            raise Exception(f"Error loading PDF {file_name}: {str(e)}")

    def _create_chunks(
        self,
        text: str,
        source_file: str,
        page_number: int
    ) -> List[Dict]:
        """
        Split text into chunks with metadata.

        Args:
            text: Text to chunk
            source_file: Source filename
            page_number: Page number

        Returns:
            List of chunk dictionaries
        """
        chunks = []
        words = text.split()

        current_chunk = []
        current_length = 0

        for word in words:
            word_length = len(word) + 1  # +1 for space

            if current_length + word_length > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "text": chunk_text,
                    "source": source_file,
                    "page": page_number,
                    "chunk_index": len(chunks)
                })

                # Start new chunk with overlap
                overlap_words = max(1, int(self.chunk_overlap / 5))
                current_chunk = current_chunk[-overlap_words:] + [word]
                current_length = sum(len(w) + 1 for w in current_chunk)
            else:
                current_chunk.append(word)
                current_length += word_length

        # Add last chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "source": source_file,
                "page": page_number,
                "chunk_index": len(chunks)
            })

        return chunks

    def save_metadata(self, metadata: Dict, output_path: str = "data/metadata.json"):
        """Save document metadata to file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(metadata, f, indent=2)

    def load_metadata(self, input_path: str = "data/metadata.json") -> Dict:
        """Load document metadata from file."""
        if os.path.exists(input_path):
            with open(input_path, "r") as f:
                return json.load(f)
        return {}
