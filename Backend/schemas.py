from pydantic import BaseModel
from datetime import datetime

class Usuario(BaseModel):
    nome: str
    email:str

class Medico(BaseModel):
    nome: str
    especialidade: str

class Horario(BaseModel):
    data_hora: datetime

class Consulta(BaseModel):
    especialidade: str
    medico: str

class Agendamento(BaseModel):
    horario: datetime
    medico: str
    usuario: str


class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str