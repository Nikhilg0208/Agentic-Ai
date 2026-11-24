"""
Policy Q&A Generation Chain (RAG Generation Pipeline)
-----------------------------------------------------
Phase 3 Responsibility (Generation):
1. Receive user query (e.g., "Can I expense beer or wine with dinner?").
2. Retrieve relevant policy clauses from Qdrant using `retrieve_relevant_clauses()`.
3. Construct a strictly grounded prompt with retrieved clauses as context.
4. Call an LLM (e.g., GPT-4o-mini / Gemini) to generate an accurate, human-readable answer.
5. Return the answer along with cited policy clauses and confidence scores.
"""

from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.config import settings
from app.rag.retriever import retrieve_relevant_clauses


POLICY_QA_PROMPT = """You are the official Policy & Claims Copilot. 
Your job is to answer employee questions about company policies accurately, professionally, and strictly based on the provided policy clauses.

STRICT GUIDELINES:
1. ONLY use information from the POLICY CONTEXT below.
2. If the policy context does not contain the answer, say: "I could not find specific guidance in the policy for this question. Please check with your manager or Finance."
3. Cite the relevant policy section numbers or titles whenever available (e.g., "According to Section 1: Meal Reimbursements...").
4. Be concise, direct, and clear.

POLICY CONTEXT:
{context}

EMPLOYEE QUESTION:
{question}

HELPFUL & GROUNDED ANSWER:"""


def get_llm(model_name: str = "gpt-4o-mini", temperature: float = 0.0) -> ChatOpenAI:
    """
    Returns an instance of ChatOpenAI with zero temperature for factual grounding.
    """
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=settings.OPENAI_API_KEY,
    )


def answer_policy_question(
    question: str,
    top_k: int = 2,
    model_name: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    """
    Complete RAG Pipeline: Retrieval + Grounded LLM Generation.
    
    Args:
        question: The user's query.
        top_k: Number of relevant policy clauses to retrieve from Qdrant.
        model_name: Model identifier (defaults to gpt-4o-mini).
        
    Returns:
        Dict containing:
            - question: original question
            - answer: generated grounded answer
            - cited_clauses: list of retrieved policy chunks used for context
    """
    # 1. RETRIEVAL STEP (from Qdrant)
    retrieved_clauses = retrieve_relevant_clauses(query=question, top_k=top_k)

    if not retrieved_clauses:
        return {
            "question": question,
            "answer": "No relevant policy documents could be found in the knowledge base.",
            "cited_clauses": [],
        }

    # Format the retrieved chunks into a clean context string
    context_blocks = []
    for idx, clause in enumerate(retrieved_clauses, 1):
        context_blocks.append(f"--- [Clause Reference #{idx}] ---\n{clause['content']}")
    context_text = "\n\n".join(context_blocks)

    # 2. GENERATION STEP (LLM Call)
    prompt = ChatPromptTemplate.from_template(POLICY_QA_PROMPT)
    llm = get_llm(model_name=model_name)
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "context": context_text,
        "question": question,
    })

    return {
        "question": question,
        "answer": answer.strip(),
        "cited_clauses": retrieved_clauses,
    }
