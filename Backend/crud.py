from sqlalchemy.orm import Session
from Backend import models, schemas

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.model_dump())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if db_usuario:
        for key, value in usuario.model_dump().items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    return False

def get_especialidades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Especialidade).offset(skip).limit(limit).all()

def create_especialidade(db: Session, especialidade: schemas.EspecialidadeCreate):
    db_especialidade = models.Especialidade(**especialidade.model_dump())
    db.add(db_especialidade)
    db.commit()
    db.refresh(db_especialidade)
    return db_especialidade

def update_especialidade(db: Session, especialidade_id: int, especialidade: schemas.EspecialidadeCreate):
    db_especialidade = db.query(models.Especialidade).filter(models.Especialidade.id_especialidade == especialidade_id).first()
    if db_especialidade:
        for key, value in especialidade.model_dump().items():
            setattr(db_especialidade, key, value)
        db.commit()
        db.refresh(db_especialidade)
    return db_especialidade

def delete_especialidade(db: Session, especialidade_id: int):
    db_especialidade = db.query(models.Especialidade).filter(models.Especialidade.id_especialidade == especialidade_id).first()
    if db_especialidade:
        db.delete(db_especialidade)
        db.commit()
        return True
    return False

def get_medicos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Medico).offset(skip).limit(limit).all()

def create_medico(db: Session, medico: schemas.MedicoCreate):
    db_medico = models.Medico(**medico.model_dump())
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

def update_medico(db: Session, medico_id: int, medico: schemas.MedicoCreate):
    db_medico = db.query(models.Medico).filter(models.Medico.id_medico == medico_id).first()
    if db_medico:
        for key, value in medico.model_dump().items():
            setattr(db_medico, key, value)
        db.commit()
        db.refresh(db_medico)
    return db_medico

def delete_medico(db: Session, medico_id: int):
    db_medico = db.query(models.Medico).filter(models.Medico.id_medico == medico_id).first()
    if db_medico:
        db.delete(db_medico)
        db.commit()
        return True
    return False

def get_horarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Horario).offset(skip).limit(limit).all()

def create_horario(db: Session, horario: schemas.HorarioCreate):
    db_horario = models.Horario(**horario.model_dump())
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario

def update_horario(db: Session, horario_id: int, horario: schemas.HorarioCreate):
    db_horario = db.query(models.Horario).filter(models.Horario.id_horario == horario_id).first()
    if db_horario:
        for key, value in horario.model_dump().items():
            setattr(db_horario, key, value)
        db.commit()
        db.refresh(db_horario)
    return db_horario

def delete_horario(db: Session, horario_id: int):
    db_horario = db.query(models.Horario).filter(models.Horario.id_horario == horario_id).first()
    if db_horario:
        db.delete(db_horario)
        db.commit()
        return True
    return False

def get_consultas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Consulta).offset(skip).limit(limit).all()

def create_consulta(db: Session, consulta: schemas.ConsultaCreate):
    db_consulta = models.Consulta(**consulta.model_dump())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

def update_consulta(db: Session, consulta_id: int, consulta: schemas.ConsultaCreate):
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id_consulta == consulta_id).first()
    if db_consulta:
        for key, value in consulta.model_dump().items():
            setattr(db_consulta, key, value)
        db.commit()
        db.refresh(db_consulta)
    return db_consulta

def delete_consulta(db: Session, consulta_id: int):
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id_consulta == consulta_id).first()
    if db_consulta:
        db.delete(db_consulta)
        db.commit()
        return True
    return False

def get_agendamentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Agendamento).offset(skip).limit(limit).all()

def create_agendamento(db: Session, agendamento: schemas.AgendamentoCreate):
    db_agendamento = models.Agendamento(**agendamento.model_dump())
    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento

def update_agendamento(db: Session, agendamento_id: int, agendamento: schemas.AgendamentoCreate):
    db_agendamento = db.query(models.Agendamento).filter(models.Agendamento.id_agendamento == agendamento_id).first()
    if db_agendamento:
        for key, value in agendamento.model_dump().items():
            setattr(db_agendamento, key, value)
        db.commit()
        db.refresh(db_agendamento)
    return db_agendamento

def delete_agendamento(db: Session, agendamento_id: int):
    db_agendamento = db.query(models.Agendamento).filter(models.Agendamento.id_agendamento == agendamento_id).first()
    if db_agendamento:
        db.delete(db_agendamento)
        db.commit()
        return True
    return False

def get_verificacoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Verificacao).offset(skip).limit(limit).all()

def create_verificacao(db: Session, verificacao: schemas.VerificacaoCreate):
    db_verificacao = models.Verificacao(**verificacao.model_dump())
    db.add(db_verificacao)
    db.commit()
    db.refresh(db_verificacao)
    return db_verificacao

def update_verificacao(db: Session, verificacao_id: int, verificacao: schemas.VerificacaoCreate):
    db_verificacao = db.query(models.Verificacao).filter(models.Verificacao.id_verificacao == verificacao_id).first()
    if db_verificacao:
        for key, value in verificacao.model_dump().items():
            setattr(db_verificacao, key, value)
        db.commit()
        db.refresh(db_verificacao)
    return db_verificacao

def delete_verificacao(db: Session, verificacao_id: int):
    db_verificacao = db.query(models.Verificacao).filter(models.Verificacao.id_verificacao == verificacao_id).first()
    if db_verificacao:
        db.delete(db_verificacao)
        db.commit()
        return True
    return False

def create_contact_message(db: Session, contact_form: schemas.ContactForm):
    db_contact = models.Contato(
        nome=contact_form.nome,
        email=contact_form.email,
        assunto=contact_form.assunto,
        mensagem=contact_form.mensagem
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact