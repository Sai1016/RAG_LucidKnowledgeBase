#PDF Text extraction, cleaning and chunking

import re
import fitz  # PyMuPDF - better for large PDFs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb


class PDFProcessor:
    def __init__(self, pdf_path="data/LucidManual.pdf"):
        self.pdf_path = pdf_path  # Path to PDF file
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")  # Pretrained embedding model
        self.chroma_client = chromadb.Client()  # Initialize ChromaDB connection
        self.collection = self.chroma_client.get_or_create_collection("manual_chunks")  # Vector storage

    # ==========================================================
    # Extract & Clean Text — optimized for large PDFs
    # ==========================================================
    def extract_text(self):
        """
        Extract and clean text page-by-page using PyMuPDF.
        This avoids memory overload for very large PDFs.
        """
        doc = fitz.open(self.pdf_path)
        all_text = ""

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text") or ""
            cleaned = self.clean_text(text)
            all_text += cleaned + "\n\n"
            print(f"🧹 Cleaned and extracted page {page_num}/{len(doc)}")

        doc.close()
        print("✅ Finished extracting and cleaning PDF.")
        return all_text

    # ==========================================================
    # Clean Text (Redefined for large PDFs)
    # ==========================================================
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize raw PDF text.
        Designed to handle large documents efficiently.
        """
        # Remove non-ASCII characters
        text = re.sub(r"[^\x00-\x7F]+", " ", text)

        # Collapse multiple newlines into one
        text = re.sub(r"\n+", "\n", text)

        # Remove common bullet or decorative symbols
        text = re.sub(r"[•◦▪▶■□◆●→]", " ", text)

        # Collapse multiple spaces into one
        text = re.sub(r"\s{2,}", " ", text)

        # Remove hyphenated line breaks (e.g., manu-\nfacturer → manufacturer)
        text = re.sub(r"-\n", "", text)

        # Remove page headers/footers (e.g., “Page 12 of 300”)
        text = re.sub(r"Page\s\d+\sof\s\d+", "", text)

        # Trim whitespace
        return text.strip()

    # ==========================================================
    # Chunk Text
    # ==========================================================
    def chunk_text(self, text, chunk_size=500, overlap=50):
        """
        Split cleaned text into overlapping chunks for embedding.
        """
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        return splitter.split_text(text)

    # ==========================================================
    # Build Index (Extract → Clean → Chunk → Embed → Store)
    # ==========================================================
    def build_index(self):
        """
        Full pipeline to prepare embeddings from the PDF and store them in ChromaDB.
        """
        text = self.extract_text()  # Extract and clean text in one go
        chunks = self.chunk_text(text)

        embeddings = self.embed_model.encode(chunks).tolist()

        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            self.collection.add(ids=[str(i)], documents=[chunk], embeddings=[emb])

        print(f"✅ Indexed {len(chunks)} cleaned chunks from {self.pdf_path}")

    # ==========================================================
    # Retrieve Relevant Chunks
    # ==========================================================
    def retrieve(self, query, k=3):
        """
        Retrieve top-k most relevant text chunks for a query using semantic similarity.
        """
        query_emb = self.embed_model.encode([query]).tolist()[0]
        results = self.collection.query(query_embeddings=[query_emb], n_results=k)
        return results["documents"][0]
# while running first: error msg:NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020. solution: urllib3 v1.26.16 installed # pip install urllib3==1.26.16. from previous version 2.3.0
