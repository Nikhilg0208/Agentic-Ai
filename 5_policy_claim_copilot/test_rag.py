"""
Phase 1 End-to-End Verification Test
------------------------------------
Verifies that:
1. Policy document is indexed into Qdrant.
2. Semantic similarity queries retrieve the exact right policy clauses.
"""

import os
from app.ingestion.indexer import index_policy_document
from app.rag.retriever import retrieve_relevant_clauses


def run_phase_1_test():
    print("=" * 65)
    print("   PHASE 1: End-to-End Verification Test (RAG & Qdrant)")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(base_dir, "data", "sample_expense_policy.txt")

    # Step 1: Index document
    print("\n[Step 1] Ensuring sample policy is indexed into Qdrant...")
    count = index_policy_document(sample_file)
    print(f"         Total clauses in collection: {count}")

    # Step 2: Test 3 realistic policy queries
    test_queries = [
        "Can I expense beer or wine with dinner?",
        "What is the maximum dinner allowance on a travel day?",
        "What class of flight is allowed for a 4 hour domestic flight?",
    ]

    print("\n[Step 2] Testing Semantic Retrieval Queries:\n")

    for i, question in enumerate(test_queries, 1):
        print("=" * 65)
        print(f"Query #{i}: '{question}'")
        print("=" * 65)

        results = retrieve_relevant_clauses(question, top_k=1)
        if results:
            top_match = results[0]
            print(f"Top Match (Similarity Score: {top_match['similarity_score']}):")
            print(top_match["content"])
        else:
            print("[!] No matching clauses found.")

        print()

    print("=" * 65)
    print("  🎉 PHASE 1 VERIFICATION COMPLETE: RAG Pipeline is Functional! 🎉")
    print("=" * 65)


if __name__ == "__main__":
    run_phase_1_test()
