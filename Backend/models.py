from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Backend.database import Base # IMPORTAÇÃO ABSOLUTA COM NOME DO PACOTE

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    telefone = Column(String(20), nullable=False)
    agendamentos = relationship("Agendamento", back_populates="usuario")
    verificacoes = relationship("Verificacao", back_populates="usuario")

class Especialidade(Base):
    __tablename__ = "especialidades"
    id_especialidade = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    medicos = relationship("Medico", back_populates="especialidade")
    consultas = relationship("Consulta", back_populates="especialidade")

class Medico(Base):
    __tablename__ = "medicos"
    id_medico = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    id_especialidade = Column(Integer, ForeignKey("especialidades.id_especialidade"), nullable=False)
    especialidade = relationship("Especialidade", back_populates="medicos")
    agendamentos = relationship("Agendamento", back_populates="medico")
    consultas = relationship("Consulta", back_populates="medico")

class Horario(Base):
    __tablename__ = "horarios"
    id_horario = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, nullable=False)
    agendamentos = relationship("Agendamento", back_populates="horario")
    verificacoes = relationship("Verificacao", back_populates="horario")

class Consulta(Base):
    __tablename__ = "consultas"
    id_consulta = Column(Integer, primary_key=True, index=True)
    id_especialidade = Column(Integer, ForeignKey("especialidades.id_especialidade"), nullable=False)
    id_medico = Column(Integer, ForeignKey("medicos.id_medico"), nullable=False)
    especialidade = relationship("Especialidade", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")
    verificacoes = relationship("Verificacao", back_populates="consulta")

class Agendamento(Base):
    __tablename__ = "agendamentos"
    __table_args__ = (
        UniqueConstraint('id_horario', 'id_medico', name='unique_horario_medico'),
    )
    id_agendamento = Column(Integer, primary_key=True, index=True)
    id_horario = Column(Integer, ForeignKey("horarios.id_horario"), nullable=False)
    id_medico = Column(Integer, ForeignKey("medicos.id_medico"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    horario = relationship("Horario", back_populates="agendamentos")
    medico = relationship("Medico", back_populates="agendamentos")
    usuario = relationship("Usuario", back_populates="agendamentos")
    verificacoes = relationship("Verificacao", back_populates="agendamento")

class Verificacao(Base):
    __tablename__ = "verificacoes"
    id_verificacao = Column(Integer, primary_key=True, index=True)
    id_horario = Column(Integer, ForeignKey("horarios.id_horario"), nullable=False)
    id_consulta = Column(Integer, ForeignKey("consultas.id_consulta"), nullable=False)
    id_agendamento = Column(Integer, ForeignKey("agendamentos.id_agendamento"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    horario = relationship("Horario", back_populates="verificacoes")
    consulta = relationship("Consulta", back_populates="verificacoes")
    agendamento = relationship("Agendamento", back_populates="verificacoes")
    usuario = relationship("Usuario", back_populates="verificacoes")

class Contato(Base):
    __tablename__ = "contatos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), index=True, nullable=False)
    assunto = Column(String(255), nullable=True)
    mensagem = Column(Text, nullable=False)
    data_envio = Column(DateTime, server_default=func.now())