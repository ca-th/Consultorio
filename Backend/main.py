print("###### ESTOU NO ARQUIVO MAIN.PY MODIFICADO! ######")

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from Backend import models # IMPORTAÇÃO ABSOLUTA
from Backend import crud   # IMPORTAÇÃO ABSOLUTA
from Backend import schemas # IMPORTAÇÃO ABSOLUTA
from Backend.database import engine, Base, get_db # IMPORTAÇÃO ABSOLUTA

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("DEBUG: Database tables created/checked on startup.")

@app.get("/")
def root():
    return {"message": "API rodando! Acesse /usuarios para interagir."}

@app.get("/usuarios", response_model=list[schemas.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud.get_usuarios(db)

@app.post("/usuarios", response_model=schemas.Usuario)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db, usuario)

@app.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def atualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_editado = crud.update_usuario(db, usuario_id, usuario)
    if not usuario_editado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario_editado

@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    deletado = crud.delete_usuario(db, usuario_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": "Usuário deletado com sucesso"}

@app.get("/especialidades", response_model=list[schemas.Especialidade])
def listar_especialidades(db: Session = Depends(get_db)):
    return crud.get_especialidades(db)

@app.post("/especialidades", response_model=schemas.Especialidade)
def criar_especialidade(especialidade: schemas.EspecialidadeCreate, db: Session = Depends(get_db)):
    return crud.create_especialidade(db, especialidade)

@app.put("/especialidades/{especialidade_id}", response_model=schemas.Especialidade)
def atualizar_especialidade(especialidade_id: int, especialidade: schemas.EspecialidadeCreate, db: Session = Depends(get_db)):
    especialidade_editada = crud.update_especialidade(db, especialidade_id, especialidade)
    if not especialidade_editada:
        raise HTTPException(status_code=404, detail="Especialidade não encontrada")
    return especialidade_editada

@app.delete("/especialidades/{especialidade_id}")
def deletar_especialidade(especialidade_id: int, db: Session = Depends(get_db)):
    deletado = crud.delete_especialidade(db, especialidade_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Especialidade não encontrada")
    return {"mensagem": "Especialidade deletada com sucesso"}

@app.get("/medicos", response_model=list[schemas.Medico])
def listar_medicos(db: Session = Depends(get_db)):
    return crud.get_medicos(db)

@app.post("/medicos", response_model=schemas.Medico)
def criar_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    return crud.create_medico(db, medico)

@app.put("/medicos/{medico_id}", response_model=schemas.Medico)
def atualizar_medico(medico_id: int, medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    medico_editado = crud.update_medico(db, medico_id, medico)
    if not medico_editado:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico_editado

@app.delete("/medicos/{medico_id}")
def deletar_medico(medico_id: int, db: Session = Depends(get_db)):
    deletado = crud.delete_medico(db, medico_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return {"mensagem": "Médico deletado com sucesso"}

@app.get("/horarios", response_model=list[schemas.Horario])
def listar_horarios(db: Session = Depends(get_db)):
    return crud.get_horarios(db)

@app.post("/horarios", response_model=schemas.Horario)
def criar_horario(horario: schemas.HorarioCreate, db: Session = Depends(get_db)):
    return crud.create_horario(db, horario)

@app.put("/horarios/{horario_id}", response_model=schemas.Horario)
def atualizar_horario(horario_id: int, horario: schemas.HorarioCreate, db: Session = Depends(get_db)):
    horario_editado = crud.update_horario(db, horario_id, horario)
    if not horario_editado:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    return horario_editado

@app.delete("/horarios/{horario_id}")
def deletar_horario(horario_id: int, db: Session = Depends(get_db)):
    deletado = crud.delete_horario(db, horario_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    return {"mensagem": "Horário deletado com sucesso"}

@app.get("/consultas", response_model=list[schemas.Consulta])
def listar_consultas(db: Session = Depends(get_db)):
    return crud.get_consultas(db)

@app.post("/consultas", response_model=schemas.Consulta)
def criar_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    return crud.create_consulta(db, consulta)

@app.put("/consultas/{consulta_id}", response_model=schemas.Consulta)
def atualizar_consulta(consulta_id: int, consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    consulta_editada = crud.update_consulta(db, consulta_id, consulta)
    if not consulta_editada:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta_editada

@app.delete("/consultas/{consulta_id}")
def deletar_consulta(consulta_id: int, db: Session = Depends(get_db)):
    deletado = crud.delete_consulta(db, consulta_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return {"mensagem": "Consulta deletada com sucesso"}

@app.get("/agendamentos", response_model=list[schemas.Agendamento])
def listar_agendamentos(db: Session = Depends(get_db)):
    return crud.get_agendamentos(db)

@app.post("/agendamentos", response_model=schemas.Agendamento)
def criar_agendamento(agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db)):
    return crud.create_agendamento(db, agendamento)

@app.put("/agendamentos/{agendamento_id}", response_model=schemas.Agendamento)
def atualizar_agendamento(agendamento_id: int, agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db)):
    agendamento_editado = crud.update_agendamento(db, agendamento_id, agendamento)
    if not agendamento_editado:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento_editado

@app.delete("/agendamentos/{agendamento_id}")
def deletar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    deletado = crud.delete_agendamento(db, agendamento_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return {"mensagem": "Agendamento deletado com sucesso"}

@app.get("/verificacoes", response_model=list[schemas.Verificacao])
def listar_verificacoes(db: Session = Depends(get_db)):
    return crud.get_verificacoes(db)

@app.post("/verificacoes", response_model=schemas.Verificacao)
def criar_verificacao(verificacao: schemas.VerificacaoCreate, db: Session = Depends(get_db)):
    return crud.create_verificacao(db, verificacao)

@app.put("/verificacoes/{verificacao_id}", response_model=schemas.Verificacao)
def atualizar_verificacao(verificacao_id: int, verificacao: schemas.VerificacaoCreate, db: Session = Depends(get_db)):
    verificacao_editada = crud.update_verificacao(db, verificacao_id, verificacao)
    if not verificacao_editada:
        raise HTTPException(status_code=404, detail="Verificação não encontrada")
    return verificacao_editada

@app.delete("/verificacoes/{verificacao_id}")
def deletar_verificacao(verificacao_id: int, db: Session = Depends(get_db)):
    deletado = crud.delete_verificacao(db, verificacao_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Verificação não encontrada")
    return {"mensagem": "Verificação deletada com sucesso"}

@app.post("/chat", response_model=schemas.ChatResponse)
async def chat_with_aura(chat_message: schemas.ChatMessage):
    user_input = chat_message.message
    if "oi" in user_input.lower() or "ola" in user_input.lower():
        response_text = "Olá! Eu sou a IA Aura. Como posso ajudar você com agendamentos ou informações?"
    elif "agendamento" in user_input.lower():
        response_text = "Para agendar uma consulta, posso te ajudar a encontrar médicos e horários. Qual sua especialidade desejada?"
    elif "medicos" in user_input.lower():
        response_text = "Temos médicos especializados em diversas áreas. Posso listar algumas para você, ou você já tem uma em mente?"
    elif "horarios" in user_input.lower():
        response_text = "Os horários de agendamento variam conforme a disponibilidade dos médicos. Qual especialidade ou médico você procura?"
    elif "quem é você" in user_input.lower() or "o que você faz" in user_input.lower():
        response_text = "Eu sou a IA Aura, sua assistente virtual para agendamentos e informações no Consultório Saúde +. Estou aqui para simplificar sua experiência!"
    else:
        response_text = "Desculpe, não entendi sua pergunta. Poderia reformular ou perguntar algo relacionado a agendamentos, médicos, especialidades?"
    return {"response": response_text}

@app.post("/contato")
async def handle_contact_form(form_data: schemas.ContactForm, db: Session = Depends(get_db)):
    crud.create_contact_message(db=db, contact_form=form_data)
    return {"message": "Mensagem recebida e salva com sucesso!"}