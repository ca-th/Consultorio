from fastapi import APIRouter, HTTPException
import requests
from Backend import schemas  

#usario e rasa
router = APIRouter()

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@router.post("/chat", response_model=schemas.ChatResponse)
async def chat_with_rasa(chat_message: schemas.ChatMessage):
    payload = {
        "sender": "usuario123", 
        "message": chat_message.message
    }

    try:
        response = requests.post(RASA_URL, json=payload)
        response.raise_for_status()
        rasa_reply = response.json()

        if rasa_reply:
            return {"response": rasa_reply[0]["text"]}
        else:
            return {"response": "Desculpe, não recebi resposta da IA."}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Rasa: {str(e)}")