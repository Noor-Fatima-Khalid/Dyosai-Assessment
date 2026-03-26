from pydantic import BaseModel
from typing import Literal, List, Any, Optional

class QueryRequest(BaseModel):
    query: str

class KnowledgeBaseResponse(BaseModel):
    route: str
    confidence: float
    used_sources: List[str]
    used_tools: List[str]
    needs_clarification: bool
    final_answer: str
    classification: Literal["ANSWERED", "AMBIGUOUS", "UNSUPPORTED"] = "ANSWERED"
    clarification_message: Optional[str] = None

class AmbiguityResponse(BaseModel):
    route: Literal["AMBIGUOUS"] = "AMBIGUOUS"
    confidence: float
    used_sources: List[str] = []
    used_tools: List[str] = ["ambiguity_handler"]
    needs_clarification: Literal[True] = True
    final_answer: dict
    classification: Literal["AMBIGUOUS"] = "AMBIGUOUS"
    clarification_message: Optional[str] = None

class UnsupportedResponse(BaseModel):
    route: Literal["UNSUPPORTED"] = "UNSUPPORTED"
    confidence: float
    used_sources: List[str] = []
    used_tools: List[str] = ["unsupported_handler"]
    needs_clarification: Literal[False] = False
    final_answer: dict
    classification: Literal["UNSUPPORTED"] = "UNSUPPORTED"
    clarification_message: Optional[str] = None

class TicketQueryRequest(BaseModel):
    query: str

class TicketQueryResponse(BaseModel):
    route: str
    confidence: float
    used_sources: list[str]
    used_tools: list[str]
    needs_clarification: bool
    final_answer: Any
    classification: Literal["ANSWERED", "AMBIGUOUS", "UNSUPPORTED"] = "ANSWERED"
    clarification_message: Optional[str] = None