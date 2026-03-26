from fastapi import APIRouter, HTTPException
from app.services.ticket_service import TicketService
from app.services.query_classifier import QueryClassifier
from app.schemas import (
    TicketQueryRequest,
    TicketQueryResponse,
    AmbiguityResponse,
    UnsupportedResponse
)

router = APIRouter()
ticket_service = TicketService()

@router.post("/ticket_lookup", response_model=TicketQueryResponse)
async def ticket_lookup(request: TicketQueryRequest):
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
            # Your ticket lookup logic here
            ticket_id = request.query.split()[-1].upper()
            ticket = ticket_service.get_ticket_by_id(ticket_id)

            if not ticket:
                return KnowledgeBaseResponse(
                    route="TICKET_LOOKUP",
                    confidence=0.9,
                    used_sources=["tickets.json"],
                    used_tools=["ticket_lookup"],
                    needs_clarification=False,
                    final_answer=f"No ticket found with ID {ticket_id}.",
                    classification="ANSWERED"
                )

            return TicketQueryResponse(
                route="TICKET_LOOKUP",
                confidence=0.99,
                used_sources=["tickets.json"],
                used_tools=["ticket_lookup"],
                needs_clarification=False,
                final_answer={"ticket": ticket},
                classification="ANSWERED"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))