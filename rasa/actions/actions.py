# actions.py

from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset, FollowupAction
from rasa_sdk.forms import FormValidationAction

import pymysql
import os
from dotenv import load_dotenv
import dateparser as dt
import logging
import datetime
import re # Adicionado para validação de email/telefone
import google.generativeai as genai

load_dotenv()
logging.basicConfig(level=logging.INFO)

class DatabaseConnection:
    # Sua classe DatabaseConnection completa aqui (sem alterações)
    def __init__(self):
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
        self.connection: Optional[pymysql.connections.Connection] = None
    def __enter__(self):
        self.connect(); return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    def connect(self) -> Optional[pymysql.connections.Connection]:
        if self.connection: return self.connection
        try:
            self.connection = pymysql.connect(
                host=self.host, user=self.user, password=self.password,
                database=self.database, cursorclass=pymysql.cursors.DictCursor
            )
            return self.connection
        except pymysql.MySQLError as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}"); return None
    def close(self):
        if self.connection:
            self.connection.close(); self.connection = None
    def execute_fetchall(self, query: str, params: Union[tuple, dict] = ()) -> Optional[List[Dict[str, Any]]]:
        connection = self.connect()
        if not connection: return None
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(f"Erro ao executar SELECT (fetchall): {e}"); return None
        finally:
            self.close()
    def execute_fetchone(self, query: str, params: Union[tuple, dict] = ()) -> Optional[Dict[str, Any]]:
        connection = self.connect()
        if not connection: return None
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            logging.error(f"Erro ao executar SELECT (fetchone): {e}"); return None
        finally:
            self.close()

# --- AÇÕES DO FLUXO INTELIGENTE ---

class ActionAskMotivoConsulta(Action):
    def name(self) -> Text: return "action_ask_motivo_consulta"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_ask_motivo_consulta")
        return []

class ActionAskNomeMedico(Action):
    def name(self) -> Text: return "action_ask_nome_medico"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        motivo = tracker.get_slot("motivo_consulta") or ""
        especialidade = tracker.get_slot("especialidade")
        try:
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            logging.error(f"Erro ao configurar Gemini: {e}")
            dispatcher.utter_message(response="utter_ask_nome_medico"); return []

        if especialidade:
            with DatabaseConnection() as db:
                medicos = db.execute_fetchall("SELECT nome FROM medicos WHERE especialidade = %s", (especialidade,))
            if medicos:
                lista_medicos = ", ".join([m['nome'] for m in medicos])
                prompt = f"Aja como um assistente de clínica. O usuário precisa de um médico para '{especialidade}'. Os médicos disponíveis são: {lista_medicos}. Apresente essa lista de forma amigável e pergunte qual deles o usuário prefere para o agendamento."
                resposta_llm = model.generate_content(prompt).text; dispatcher.utter_message(text=resposta_llm)
            else:
                dispatcher.utter_message(text=f"Puxa, no momento não temos médicos para a especialidade de '{especialidade}'."); return [FollowupAction("action_cancelar_agendamento")]
        elif "rotina" not in motivo.lower():
            with DatabaseConnection() as db:
                especialidades_db = db.execute_fetchall("SELECT nome FROM especialidades")
            if not especialidades_db:
                dispatcher.utter_message(text="Desculpe, não consegui consultar nossas especialidades no momento."); return [FollowupAction("action_cancelar_agendamento")]
            
            lista_especialidades = ", ".join([e['nome'] for e in especialidades_db])
            prompt_especialidade = f"Analise o sintoma do usuário: '{motivo}'. Com base nesse sintoma, qual das seguintes especialidades médicas é a mais indicada? Especialidades disponíveis: {lista_especialidades}. Responda apenas com o nome da especialidade. Exemplo: Cardiologia"
            especialidade_sugerida = model.generate_content(prompt_especialidade).text.strip()
            with DatabaseConnection() as db:
                medicos = db.execute_fetchall("SELECT nome FROM medicos WHERE especialidade = %s", (especialidade_sugerida,))
            
            if medicos:
                lista_medicos = ", ".join([m['nome'] for m in medicos])
                prompt_recomendacao = f"Aja como um assistente de clínica. Com base no sintoma '{motivo}', a especialidade recomendada é {especialidade_sugerida}. Os especialistas disponíveis são: {lista_medicos}. Recomende o primeiro médico da lista e pergunte se o usuário deseja agendar com ele, ou se prefere outro da lista."
                resposta_llm = model.generate_content(prompt_recomendacao).text
                dispatcher.utter_message(text=resposta_llm)
                return [SlotSet("especialidade", especialidade_sugerida)]
            else:
                dispatcher.utter_message(text=f"Com base nos seus sintomas, a especialidade seria {especialidade_sugerida}, mas não encontramos médicos disponíveis."); return [FollowupAction("action_cancelar_agendamento")]
        else:
            dispatcher.utter_message(response="utter_ask_nome_medico")
        return []

# --- VALIDAÇÃO DO FORMULÁRIO PRINCIPAL (VERSÃO COMPLETA E FLEXÍVEL) ---
class ValidateAgendamentoConsultaForm(FormValidationAction):
    def name(self) -> Text: return "validate_agendamento_consulta_form"

    def validate_especialidade(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        with DatabaseConnection() as db:
            result = db.execute_fetchone("SELECT nome FROM especialidades WHERE LOWER(nome) = %s", (slot_value.lower(),))
        if result:
            return {"especialidade": result["nome"]}
        else:
            dispatcher.utter_message(text=f"Desculpe, não temos a especialidade '{slot_value}'.")
            return {"especialidade": None}

    def validate_data_consulta(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        parsed_date = dt.parse(slot_value, languages=['pt'])
        if parsed_date and parsed_date.date() >= datetime.date.today():
            return {"data_consulta": parsed_date.strftime('%Y-%m-%d')}
        else:
            dispatcher.utter_message(text="Essa não parece ser uma data válida ou é uma data no passado. Por favor, me diga uma data futura.")
            return {"data_consulta": None}

    def validate_motivo_consulta(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value and 5 < len(slot_value) < 255:
            return {"motivo_consulta": slot_value}
        else:
            # Se for 'rotina', também é válido.
            if "rotina" in slot_value.lower(): return {"motivo_consulta": slot_value}
            dispatcher.utter_message(text="Por favor, descreva o motivo com um pouco mais de detalhe.")
            return {"motivo_consulta": None}

    def validate_nome_medico(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        with DatabaseConnection() as db:
            result = db.execute_fetchone("SELECT nome FROM medicos WHERE LOWER(nome) LIKE %s", (f"%{slot_value.lower()}%",))
        if result:
            return {"nome_medico": result["nome"]}
        else:
            dispatcher.utter_message(text=f"Desculpe, não encontrei um médico chamado '{slot_value}'.")
            return {"nome_medico": None}

    async def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Ótimo, escolhas anotadas! Para finalizar, preciso de alguns dados seus.")
        return [FollowupAction("dados_paciente_form")]

# --- VALIDAÇÃO E AÇÕES PARA O FORMULÁRIO DE DADOS DO PACIENTE ---
class ValidateDadosPacienteForm(FormValidationAction):
    def name(self) -> Text: return "validate_dados_paciente_form"

    def validate_nome(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value and len(slot_value) > 2:
            return {"nome": slot_value}
        dispatcher.utter_message(text="Por favor, insira um nome válido.")
        return {"nome": None}

    def validate_telefone(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        # Validação simples que busca por 10 ou 11 dígitos
        if slot_value and re.match(r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$', slot_value):
            return {"telefone": slot_value}
        dispatcher.utter_message(text="Não entendi. Por favor, digite um telefone válido com DDD (ex: (11) 98765-4321).")
        return {"telefone": None}

    def validate_email(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value and "@" in slot_value and "." in slot_value:
            return {"email": slot_value}
        dispatcher.utter_message(text="Este não parece ser um e-mail válido. Por favor, verifique.")
        return {"email": None}

class ActionAskNome(Action):
    def name(self) -> Text: return "action_ask_nome"
    def run(self, dispatcher, tracker, domain): dispatcher.utter_message(response="utter_ask_nome"); return []

class ActionAskTelefone(Action):
    def name(self) -> Text: return "action_ask_telefone"
    def run(self, dispatcher, tracker, domain): dispatcher.utter_message(response="utter_ask_telefone"); return []

class ActionAskEmail(Action):
    def name(self) -> Text: return "action_ask_email"
    def run(self, dispatcher, tracker, domain): dispatcher.utter_message(response="utter_ask_email"); return []

# --- AÇÕES FINAIS E GENÉRICAS ---
class ActionConfirmarAgendamento(Action):
    def name(self) -> Text: return "action_confirmar_agendamento"
    def run(self, dispatcher, tracker, domain):
        # A LÓGICA FINAL DE 'INSERT' NO BANCO DE DADOS DEVE IR AQUI
        dispatcher.utter_message(response="utter_agendamento_finalizado"); return [AllSlotsReset()]

class ActionCancelarAgendamento(Action):
    def name(self) -> Text: return "action_cancelar_agendamento"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Tudo bem, agendamento cancelado. Se precisar de algo mais, é só chamar."); return [AllSlotsReset()]

class ActionPerguntarLLM(Action):
    def name(self) -> Text: return "action_perguntar_llm"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Lógica do LLM genérico aqui."); return []