"""
Policy Document Indexer (RAG Ingestion Pipeline)
------------------------------------------------
Phase 1 Responsibility:
1. Load a policy file (PDF or text) from the data/ or uploads/ directory.
2. Split the document into semantic chunks with overlap.
3. Compute vector embeddings using an embedding model (e.g. OpenAI text-embedding-3-small).
4. Upsert vectors and text payload into Qdrant vector database (collection: 'policy_clauses').
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from app.config import settings
from app.core.db import get_qdrant_client


def get_embedding_model() -> OpenAIEmbeddings:
    """
    Returns the configured OpenAI embedding model.
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=settings.OPENAI_API_KEY,
    )


def load_and_chunk_document(file_path: str) -> List[Document]:
    """
    Loads a document (PDF or Text) from file_path and splits it into semantic chunks.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document not found at: {file_path}")

    # Step 1: Select the right loader based on file extension
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    raw_docs = loader.load()

    # Step 2: Split text into chunks with overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = text_splitter.split_documents(raw_docs)
    return chunks


def index_policy_document(file_path: str) -> int:
    """
    Ingests and indexes a policy document into Qdrant.
    Returns the number of indexed chunks.
    """
    print(f"\n[1/3] Loading and chunking document: {file_path}...")
    chunks = load_and_chunk_document(file_path)
    print(f"      Generated {len(chunks)} chunks.")

    if not chunks:
        print("[!] No chunks found to index.")
        return 0

    print(f"[2/3] Generating embeddings & uploading to Qdrant collection '{settings.POLICY_COLLECTION_NAME}'...")
    embeddings = get_embedding_model()

    # Store chunks & vectors into Qdrant using Qdrant URL
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=settings.QDRANT_URL,
        collection_name=settings.POLICY_COLLECTION_NAME,
    )

    print(f"[3/3] [✓] Successfully indexed {len(chunks)} policy clauses into Qdrant!")
    return len(chunks)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sample_file = os.path.join(base_dir, "data", "sample_expense_policy.txt")

    print("=" * 60)
    print("Testing Policy Ingestion Pipeline")
    print("=" * 60)
    indexed_count = index_policy_document(sample_file)
    print(f"\nCompleted! Total clauses stored: {indexed_count}")
