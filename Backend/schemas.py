# Exemplo de schemas.py, adapte se você tiver importações de models aqui
from pydantic import BaseModel
from datetime import datetime

# Se você tiver algo como 'from models import Usuario' aqui, mude para:
# from Backend.models import Usuario

class UsuarioBase(BaseModel):
    nome: str
    cpf: str
    telefone: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id_usuario: int
    class Config:
        from_attributes = True

class EspecialidadeBase(BaseModel):
    nome: str

class EspecialidadeCreate(EspecialidadeBase):
    pass

class Especialidade(EspecialidadeBase):
    id_especialidade: int
    class Config:
        from_attributes = True

class MedicoBase(BaseModel):
    nome: str
    id_especialidade: int

class MedicoCreate(MedicoBase):
    pass

class Medico(MedicoBase):
    id_medico: int
    class Config:
        from_attributes = True

class HorarioBase(BaseModel):
    data_hora: datetime

class HorarioCreate(HorarioBase):
    pass

class Horario(HorarioBase):
    id_horario: int
    class Config:
        from_attributes = True

class ConsultaBase(BaseModel):
    id_especialidade: int
    id_medico: int

class ConsultaCreate(ConsultaBase):
    pass

class Consulta(ConsultaBase):
    id_consulta: int
    class Config:
        from_attributes = True

class AgendamentoBase(BaseModel):
    id_horario: int
    id_medico: int
    id_usuario: int

class AgendamentoCreate(AgendamentoBase):
    pass

class Agendamento(AgendamentoBase):
    id_agendamento: int
    class Config:
        from_attributes = True

class VerificacaoBase(BaseModel):
    id_horario: int
    id_consulta: int
    id_agendamento: int
    id_usuario: int

class VerificacaoCreate(VerificacaoBase):
    pass

class Verificacao(VerificacaoBase):
    id_verificacao: int
    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ContactForm(BaseModel):
    nome: str
    email: str
    assunto: str = None
    mensagem: str

class ContactMessage(ContactForm):
    id: int
    data_envio: datetime
    class Config:
        from_attributes = True