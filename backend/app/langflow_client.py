import httpx
import json
from .config import settings
from .schemas import AgentQuery, AgentResult


async def call_langflow(query: AgentQuery) -> AgentResult:
    url = f"{settings.LANGFLOW_URL}/api/v1/run/{settings.LANGFLOW_FLOW_ID}"

    payload = {
        "input_value": query.message,
        "input_type": "chat",
        "output_type": "chat",
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": settings.LANGFLOW_API_KEY,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()

    raw = response.json()

    try:
        container = raw["outputs"][0]["outputs"][0]

        if "messages" in container and len(container["messages"]) > 0:
            message_str = container["messages"][0]["message"]

        elif (
            "results" in container
            and "message" in container["results"]
            and "text" in container["results"]["message"]
        ):
            message_str = container["results"]["message"]["text"]

        else:
            raise KeyError(f"Structure inattendue : {container}")

    except Exception as e:
        raise RuntimeError(
            f"Impossible d'extraire le message final depuis LangFlow : {e}\nRéponse brute : {raw}"
        )

    # Parse JSON contenu dans la chaine
    try:
        parsed = json.loads(message_str)
    except Exception as e:
        raise RuntimeError(f"Le message renvoyé n’est pas un JSON valide : {e}\nMessage brut : {message_str}")

    # Validate via Pydantic
    return AgentResult.model_validate(parsed)
