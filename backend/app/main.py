from fastapi import FastAPI, HTTPException
from .schemas import AgentQuery, AgentResponse
from .langflow_client import call_langflow
from .config import settings
import httpx

app = FastAPI(title="Support AI", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/agent/query", response_model=AgentResponse)
async def agent_query(payload: AgentQuery):

    try:
        result = await call_langflow(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur LangFlow : {e}")

    ticket_created = False
    ticket_reference = None

    # Gestion interne du ticket sans n8n ?
    if result.needs_ticket and result.ticket:
        ticket_created = False
        ticket_reference = None


    return AgentResponse(
        answer=result.answer,
        intent=result.intent,
        needs_ticket=result.needs_ticket,
        ticket=result.ticket,
        ticket_created=ticket_created,
        ticket_reference=ticket_reference,
        metadata={"confidence": result.confidence}
    )

