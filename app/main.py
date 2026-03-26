from fastapi import FastAPI
from app.routes import knowledge_base, ticket_lookup

app = FastAPI()

app.include_router(knowledge_base.router, prefix="/api", tags=["knowledge_base"])
app.include_router(ticket_lookup.router, prefix="/api", tags=["ticket_lookup"])