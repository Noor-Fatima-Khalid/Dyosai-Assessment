import re
from typing import Literal

class QueryClassifier:
    @staticmethod
    def classify(query: str) -> Literal["AMBIGUOUS", "UNSUPPORTED", "KNOWLEDGE_BASE", "TICKET_LOOKUP"]:
        query = query.lower()

        # Check for ambiguity
        ambiguous_keywords = [
            r"check that ticket",
            r"what is going on with",
            r"look at the",
            r"can you check",
            r"what about",
            r"tell me about"
        ]
        if any(re.search(keyword, query) for keyword in ambiguous_keywords):
            return "AMBIGUOUS"

        # Check for unsupported queries
        unsupported_keywords = [
            r"on-premise",
            r"legal policies for",
            r"deployment options",
            r"hardware requirements"
        ]
        if any(re.search(keyword, query) for keyword in unsupported_keywords):
            return "UNSUPPORTED"

        # Check for ticket lookup
        if re.search(r"ticket\s+[a-zA-Z0-9\-]+", query):
            return "TICKET_LOOKUP"

        # Default to knowledge base
        return "KNOWLEDGE_BASE"