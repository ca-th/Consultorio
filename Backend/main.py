from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from schemas import ChatMessage, ChatResponse 

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# ver se ta rodando
@app.get("/")
def root():
    return {"message": "API rodando! Acesse /chat para conversar com a IA."}

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.post("/chat", response_model=ChatResponse)
async def chat_with_rasa(chat_message: ChatMessage):
    payload = {
        "sender": "usuario123",  # pode ser dinâmico
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