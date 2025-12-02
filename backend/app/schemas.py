from typing import Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

class AgentMetadata(BaseModel):
    locale: Optional[str] = None
    app_version: Optional[str] = None
    extras: Dict[str, Any] = Field(default_factory=dict)


class AgentQuery(BaseModel):
    message: str
    channel: Literal["webchat", "slack", "email", "api", "other"] = "webchat"
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    metadata: Optional[AgentMetadata] = None


class Ticket(BaseModel):
    title: str
    description: str
    priority: Literal["low", "medium", "high"] = "medium"
    category: Literal["question", "incident", "feature_request", "billing", "other"] = "question"
    user_email: Optional[str] = None


class AgentResult(BaseModel):
    answer: str
    intent: str
    confidence: float
    needs_ticket: bool
    ticket: Optional[Ticket] = None


class AgentResponse(BaseModel):
    answer: str
    intent: str
    needs_ticket: bool
    ticket: Optional[Ticket] = None
    ticket_created: bool = False
    ticket_reference: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

