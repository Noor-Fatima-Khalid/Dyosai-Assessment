from fastapi import APIRouter, HTTPException
from app.services.rag import RAGPipeline
from app.services.query_classifier import QueryClassifier
from app.schemas import (
    QueryRequest,
    KnowledgeBaseResponse,
    AmbiguityResponse,
    UnsupportedResponse
)

router = APIRouter()
rag = RAGPipeline()

@router.post("/knowledge_base", response_model=KnowledgeBaseResponse)
async def query_knowledge_base(request: QueryRequest):
    classification = QueryClassifier.classify(request.query)

    if classification == "AMBIGUOUS":
        return AmbiguityResponse(
            confidence=0.9,
            final_answer={
                "message": "Your query is ambiguous. Could you clarify?",
                "suggested_clarifications": [
                    "Are you asking about a specific ticket? If so, please provide the ticket ID.",
                    "Are you asking about a specific account or integration issue? If so, please provide more details."
                ]
            }
        )

    elif classification == "UNSUPPORTED":
        return UnsupportedResponse(
            confidence=0.9,
            final_answer={
                "message": "I’m sorry, but I don’t have the information to answer your question."
            }
        )

    else:
        try:
            result = rag.answer(request.query)
            return KnowledgeBaseResponse(
                route="KNOWLEDGE_BASE",
                confidence=0.82,
                used_sources=result["sources"],
                used_tools=[],
                needs_clarification=False,
                final_answer=result["answer"],
                classification="ANSWERED"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))