"""
Policy Retriever Module (RAG Query Pipeline)
--------------------------------------------
Phase 1 Responsibility:
1. Connect to Qdrant vector store (`policy_clauses` collection).
2. Given a user query (e.g. "dinner reimbursement limit"), convert it to an embedding.
3. Perform similarity search in Qdrant and return top matching policy clauses with relevance scores.
"""

from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from app.config import settings
from app.core.db import get_qdrant_client


def get_vector_store() -> QdrantVectorStore:
    """
    Returns an instance of QdrantVectorStore connected to the policy_clauses collection.
    """
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=settings.OPENAI_API_KEY,
    )
    client = get_qdrant_client()

    return QdrantVectorStore(
        client=client,
        collection_name=settings.POLICY_COLLECTION_NAME,
        embedding=embeddings,
    )


def retrieve_relevant_clauses(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Search Qdrant for policy clauses semantically relevant to the given query.
    Returns a list of matching chunks with text, score, and source metadata.
    """
    vector_store = get_vector_store()

    # similarity_search_with_score returns a list of (Document, float_score)
    # Higher score = closer semantic similarity
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k,
    )

    formatted_clauses = []
    for doc, score in results:
        formatted_clauses.append({
            "content": doc.page_content.strip(),
            "metadata": doc.metadata,
            "similarity_score": round(float(score), 4),
        })

    return formatted_clauses


if __name__ == "__main__":
    test_query = "What is the maximum dinner allowance on a business trip?"
    print("=" * 60)
    print(f"Testing Retriever with query: '{test_query}'")
    print("=" * 60)

    clauses = retrieve_relevant_clauses(test_query, top_k=2)
    for idx, clause in enumerate(clauses, 1):
        print(f"\n[Match #{idx}] (Score: {clause['similarity_score']})")
        print(clause['content'])
        print("-" * 50)
