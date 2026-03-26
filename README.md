# AI Query Routing System

A modular AI system for routing and handling different types of queries, including knowledge base lookups, ticket/account lookups, ambiguity handling, and unsupported questions.

## **Features**
- **Knowledge Base Lookup**: Retrieve answers from a set of Markdown documents.
- **Ticket Lookup**: Fetch ticket details from a JSON database.
- **Ambiguity Handling**: Detect and ask for clarification on vague queries.
- **Unsupported Questions**: Inform users when a query cannot be answered.

## **Project Structure**
ai_app/
├── app/
│   ├── data/
│   │   ├── tickets.json
│   │   ├── refund_policy.md
│   │   ├── account_upgrade.md
│   │   ├── api_rate_limits.md
│   │   ├── security_practices.md
│   │   └── integration_setup.md
│   ├── services/
│   │   ├── rag.py
│   │   ├── ticket_service.py
│   │   └── query_classifier.py
│   ├── routes/
│   │   ├── knowledge_base.py
│   │   ├── ticket_lookup.py
│   ├── schemas.py
│   └── main.py
├── .env.example
├── requirements.txt
└── README.md


## **Setup Instructions**

### **1. Prerequisites**
- Python 3.9+
- Virtual environment 

### **2. Clone the Repository**
```bash
git clone https://github.com/Noor-Fatima-Khalid/Dyosai-Assessment/
cd ai_app
### **3. Create a virtual environment**
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
Running the System
1. Start the FastAPI Server
uvicorn app.main\:app --reload

2. Access the API
Swagger UI: Open http://localhost:8000/docs in your browser to interact with the API.

Example Queries
1. Knowledge Base Queries
Endpoint: POST /api/knowledge_base
Request:
{
  "query": "What is the refund policy?"
}
Response:
{
  "route": "KNOWLEDGE_BASE",
  "confidence": 0.82,
  "used_sources": ["data/refund_policy.md"],
  "used_tools": [],
  "needs_clarification": false,
  "final_answer": "Our refund policy allows for full refunds within 30 days of purchase...",
  "classification": "ANSWERED"
}

2. Ticket Lookup Queries
Endpoint: POST /api/ticket_lookup
Request:
{
  "query": "What is the status of ticket T-2001?"
}
Response:
{
  "route": "TICKET_LOOKUP",
  "confidence": 0.99,
  "used_sources": ["tickets.json"],
  "used_tools": ["ticket_lookup"],
  "needs_clarification": false,
  "final_answer": {
    "ticket": {
      "ticket_id": "T-2001",
      "status": "open",
      "assigned_to": "Sara",
      "priority": "urgent"
    }
  },
  "classification": "ANSWERED"
}

3. Ambiguous Queries
Endpoint: POST /api/knowledge_base or POST /api/ticket_lookup
Request:
{
  "query": "Can you check that ticket for me?"
}

Response:
{
  "route": "AMBIGUOUS",
  "confidence": 0.9,
  "used_sources": [],
  "used_tools": ["ambiguity_handler"],
  "needs_clarification": true,
  "final_answer": {
    "message": "Your query is ambiguous. Could you clarify?",
    "suggested_clarifications": [
      "Are you asking about a specific ticket? If so, please provide the ticket ID.",
      "Are you asking about a specific account or integration issue?"
    ]
  },
  "classification": "AMBIGUOUS"
}

4. Unsupported Queries
Endpoint: POST /api/knowledge_base or POST /api/ticket_lookup
Request:
{
  "query": "Do you support on-premise deployment?"
}

Response:
{
  "route": "UNSUPPORTED",
  "confidence": 0.9,
  "used_sources": [],
  "used_tools": ["unsupported_handler"],
  "needs_clarification": false,
  "final_answer": {
    "message": "I’m sorry, but I don’t have the information to answer your question."
  },
  "classification": "UNSUPPORTED"
}


Troubleshooting

404 Errors: Ensure the FastAPI server is running and you’re accessing the correct endpoint.
Missing Data: Verify that tickets.json and Markdown files are in the data/ directory.
API Key Issues: Double-check your .env file for the correct GOOGLE_API_KEY.
