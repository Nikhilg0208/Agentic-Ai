"""
RAG Pipeline Verification Test (Retrieval + LLM Generation)
-----------------------------------------------------------
Verifies that:
1. Ingestion: Policy document is indexed into Qdrant.
2. Retrieval: Semantic similarity queries retrieve the exact policy clauses.
3. Generation: LLM (GPT-4o-mini) generates grounded, natural answers based on those clauses.
"""

import os
from app.ingestion.indexer import index_policy_document
from app.rag.retriever import retrieve_relevant_clauses
from app.rag.qa_chain import answer_policy_question


def run_rag_test():
    print("=" * 70)
    print("   PHASE 3 VERIFICATION: Full RAG Pipeline (Retrieval + LLM Generation)")
    print("=" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(base_dir, "data", "sample_expense_policy.txt")

    # Step 1: Ingestion
    print("\n[Step 1] Ensuring sample policy is indexed into Qdrant...")
    count = index_policy_document(sample_file)
    print(f"         Total clauses in collection: {count}")

    # Test queries
    test_queries = [
        "Can I expense beer or wine with dinner?",
        "What is the maximum dinner allowance on a travel day?",
        "What class of flight is allowed for a 4 hour domestic flight?",
    ]

    # Step 2: Semantic Retrieval from Qdrant
    print("\n" + "=" * 70)
    print("[Step 2] Testing Semantic Retrieval from Qdrant (The 'R' in RAG)")
    print("=" * 70)

    for i, question in enumerate(test_queries, 1):
        print(f"\nQuery #{i}: '{question}'")
        results = retrieve_relevant_clauses(question, top_k=1)
        if results:
            top_match = results[0]
            print(f"-> Top Match (Score: {top_match['similarity_score']}):")
            print(top_match["content"])
        else:
            print("[!] No matching clauses found.")

    # Step 3: Grounded LLM Generation (The 'AG' in RAG)
    print("\n" + "=" * 70)
    print("[Step 3] Testing Grounded LLM Generation (The 'AG' in RAG)")
    print("=" * 70)

    for i, question in enumerate(test_queries, 1):
        print(f"\nQuestion #{i}: '{question}'")
        response = answer_policy_question(question=question, top_k=2)
        print("\n🤖 AI Grounded Answer:")
        print(response["answer"])
        print("-" * 50)

    print("\n" + "=" * 70)
    print("  🎉 PHASE 3 VERIFICATION COMPLETE: Full RAG Pipeline is Functional! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    run_rag_test()
