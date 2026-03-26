import json
from typing import List, Dict, Optional

class TicketService:
    def __init__(self, data_path="data/tickets.json"):
        with open(data_path, "r") as f:
            self.tickets = json.load(f)

    def get_ticket_by_id(self, ticket_id: str) -> Optional[Dict]:
        return next((t for t in self.tickets if t["ticket_id"] == ticket_id), None)

    def get_tickets_by_status(self, status: str) -> List[Dict]:
        return [t for t in self.tickets if t["status"] == status]

    def get_tickets_by_priority(self, priority: str) -> List[Dict]:
        return [t for t in self.tickets if t["priority"] == priority]

    def get_unassigned_tickets(self) -> List[Dict]:
        return [t for t in self.tickets if not t.get("assigned_to")]

    def get_tickets_by_assignee(self, assignee: str) -> List[Dict]:
        return [t for t in self.tickets if t.get("assigned_to") == assignee]