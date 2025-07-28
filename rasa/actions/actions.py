# actions/actions.py

from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset, FollowupAction
from rasa_sdk.forms import FormValidationAction # Mantido apenas esta importação de forms

import pymysql
import os
from dotenv import load_dotenv

import dateparser as dt

# --- Importações de bibliotecas externas ---
import requests
# from datetime import datetime, timedelta # Descomente se for usar para validação de datas

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

import logging

logging.basicConfig(level=logging.INFO)

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
        self.connection: Optional[pymysql.connections.Connection] = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self) -> Optional[pymysql.connections.Connection]:
        if self.connection:
            return self.connection
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            return self.connection
        except pymysql.MySQLError as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_write(self, query: str, params: Union[tuple, dict] = ()) -> bool:
        """
        Executa comandos de escrita: INSERT, UPDATE, DELETE.
        Retorna True se executado com sucesso, False se houve erro.
        """
        connection = self.connect()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                return True
        except pymysql.MySQLError as e:
            logging.error(f"Erro ao executar comando de escrita: {e}")
            return False
        finally:
            self.close()

    def execute_fetchall(self, query: str, params: Union[tuple, dict] = ()) -> Optional[List[Dict[str, Any]]]:
        """
        Executa SELECT e retorna todos os resultados como lista de dicionários.
        """
        connection = self.connect()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            logging.error(f"Erro ao executar SELECT (fetchall): {e}")
            return None
        finally:
            self.close()

    def execute_fetchone(self, query: str, params: Union[tuple, dict] = ()) -> Optional[Dict[str, Any]]:
        """
        Executa SELECT e retorna o primeiro resultado como dicionário.
        """
        connection = self.connect()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            logging.error(f"Erro ao executar SELECT (fetchone): {e}")
            return None
        finally:
            self.close()


# --- Ação para perguntar ao LLM ---
class ActionPerguntarLLM(Action):
    def name(self) -> Text:
        return "action_perguntar_llm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text")
        llm_resposta = "Desculpe, não consegui conectar ao LLM neste momento."

        # --- EXEMPLO: Lógica para chamar um LLM real ---
        # Certifique-se de que o servidor LLM esteja acessível (pode ser outro container Docker ou uma API externa)
        try:
            # Substitua esta URL pela URL real do seu serviço LLM
            # Se você estiver usando a biblioteca google-generativeai, a lógica será diferente.
            # Este é um exemplo para uma API REST genérica de LLM.
            llm_api_url = "http://localhost:5000/api/llm_query" # <<< MUDE ISSO PARA O SEU ENDPOINT DO LLM!

            # Formato da requisição ao LLM
            payload = {"query": user_message}

            # Faz a chamada POST para o LLM
            response = requests.post(llm_api_url, json=payload, timeout=10) # Timeout de 10 segundos
            response.raise_for_status() # Lança um erro para status HTTP ruins (4xx ou 5xx)

            llm_resposta = response.json().get("response", "Não consegui uma resposta clara do LLM.")

        except requests.exceptions.Timeout:
            llm_resposta = "O LLM demorou muito para responder. Por favor, tente novamente mais tarde."
        except requests.exceptions.RequestException as e:
            llm_resposta = f"Não foi possível conectar ao LLM. Erro: {e}. Verifique se o serviço está rodando."
        except Exception as e:
            llm_resposta = f"Um erro inesperado ocorreu ao processar a pergunta ao LLM: {e}"
        # --- FIM DO EXEMPLO ---

        dispatcher.utter_message(text=llm_resposta)
        return [SlotSet("llm_response", llm_resposta)] # Opcional: Salvar a resposta no slot llm_response

# --- CLASSE DE VALIDAÇÃO DO FORMULÁRIO: agendamento_consulta_form ---
# Esta classe é responsável por validar os slots do formulário.
# REMOVIDA A CLASSE FormAction QUE ESTAVA CAUSANDO O ERRO.
class ValidateAgendamentoConsultaForm(FormValidationAction):
    def name(self) -> Text:
        """Define o nome da ação de validação do formulário."""
        return "validate_agendamento_consulta_form"

    # --- Métodos de validação para cada slot requerido no domain.yml ---
    # O Rasa chamará automaticamente validate_<slot_name>
    async def validate_especialidade(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'especialidade'."""

        especialidade = tracker.get_slot("especialidade")

        if especialidade:
            try:
                # Consulta as especialidades disponíveis no banco de dados
                with DatabaseConnection() as db:
                    query = "SELECT * FROM especialidades WHERE LOWER(nome) = %s"
                    params = (especialidade.lower(),)  # Certifique-se de que o valor esteja em minúsculas
                    result = db.execute_fetchone(query, params)

                    if result:
                        return [SlotSet("especialidade", especialidade)]
                    else:
                        dispatcher.utter_message(text="Desculpe, não encontramos essa especialidade. Por favor, tente novamente.")
                        return [SlotSet("especialidade", None)]

            except Exception as e:
                dispatcher.utter_message(
                    text=f"Erro ao consultar especialidades: {e}"
                )
                return [SlotSet("especialidade", None)]

        # Caso o slot não tenha sido preenchido ainda
        return [SlotSet("especialidade", None)]

    async def validate_data_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'data_consulta'."""
        # TODO: Implementar validação de data mais robusta aqui (ex: usar dateparser, verificar futuro)

        data = tracker.get_slot("data_consulta")
        if data:
            # Usa dateparser para reconhecer datas em linguagem natural
            parsed_date = dt.parse(data)
            if parsed_date and parsed_date >= dt.datetime.now() - dt.timedelta(days=1):
                with DatabaseConnection() as db:
                    try:
                        # Verifica se já existe agendamento disponível para essa data
                        query = "SELECT * FROM datas WHERE data = %s"
                        params = (parsed_date.strftime('%Y-%m-%d'),)
                        result = db.execute_fetchone(query, params)

                        if result:
                            return [SlotSet("data_consulta", parsed_date.strftime('%Y-%m-%d'))]
                        else:
                            dispatcher.utter_message(text="Desculpe, não encontramos disponibilidade para essa data. Por favor, escolha outra.")
                            return [SlotSet("data_consulta", None)]
                    except Exception as e:
                        dispatcher.utter_message(
                            text=f"Erro ao consultar datas: {e}"
                            )
                        return [SlotSet("data_consulta", None)]
            else:
                dispatcher.utter_message(
                    text="Essa não parece ser uma data válida ou é uma data no passado. " \
                    "Por favor, me diga o dia (ex: 'amanhã', 'quarta-feira', '25 de julho')."
                    )
                return [SlotSet("data_consulta", None)]
        
        return [SlotSet("data_consulta", None)]

    async def validate_hora_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'hora_consulta'."""
        hora = tracker.get_slot("hora_consulta")

        if hora:
            # Usa dateparser para reconhecer horários em linguagem natural
            parsed_time = dt.parse(hora, settings={'TIMEZONE': 'UTC'})
            if parsed_time:
                with DatabaseConnection() as db:
                    try:
                        # Verifica se já existe agendamento disponível para essa hora
                        query = "SELECT * FROM horarios WHERE hora = %s"
                        params = (parsed_time.strftime('%H:%M:00'),)  # Formato de hora
                        result = db.execute_fetchone(query, params)

                        if result:
                            return [SlotSet("hora_consulta", parsed_time.strftime('%H:%M'))]
                        else:
                            dispatcher.utter_message(text="Desculpe, não tem disponibilidade para esse horário. Por favor, escolha outro.")
                            return [SlotSet("hora_consulta", None)]
                    except Exception as e:
                        dispatcher.utter_message(
                            text=f"Erro ao consultar horários: {e}"
                            )
                        return [SlotSet("hora_consulta", None)]
        
        return [SlotSet("hora_consulta", None)]

    async def validate_nome_medico(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'nome_medico'."""

        medico = tracker.get_slot("nome_medico")

        if medico:
            with DatabaseConnection() as db:
                try:
                    query = "SELECT * FROM medicos WHERE LOWER(nome) LIKE %s"
                    params = (f"%{medico.lower()}%",)  # Busca por nome similar
                    result = db.execute_fetchone(query, params)

                    if result:
                        return [SlotSet("nome_medico", result["nome"])] # Retorna o primeiro médico encontrado
                    else:
                        dispatcher.utter_message(text="Desculpe, não encontramos esse médico. Por favor, tente novamente.")
                        return [SlotSet("nome_medico", None)]

                except Exception as e:
                    dispatcher.utter_message(
                        text=f"Erro ao consultar médicos: {e}"
                        )
                    return [SlotSet("nome_medico", None)]
        
        return [SlotSet("nome_medico", None)]
                   
    async def validate_motivo_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'motivo_consulta'."""
        motivo_consulta = tracker.get_slot("motivo_consulta")

        if motivo_consulta and len(motivo_consulta) > 5 and len(motivo_consulta) < 255:
            dispatcher.utter_message(
                text="Motivo registrado."
                )
            return [SlotSet("motivo_consulta", motivo_consulta)]
        else:
            dispatcher.utter_message(
                text="Por favor, descreva o motivo novamente "
                "(mínimo de 5 caracteres e máximo de 255)."
                )
            return [SlotSet("motivo_consulta", None)]

    async def validate_nome(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'nome' (nome do paciente)."""
        nome_paciente = tracker.get_slot("nome")
        
        if nome_paciente and len(nome_paciente) >= 3 and len(nome_paciente) <= 100:
            dispatcher.utter_message(
                text="Nome registrado com sucesso!"
                )
            return [SlotSet("nome", nome_paciente)]
        else:
            dispatcher.utter_message(
                text="Por favor, informe seu nome novamente."
                )
            return [SlotSet("nome", None)]
    
    async def validate_disponibilidade(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida a disponibilidade de agendamento na agenda do médico."""

        especialidade = tracker.get_slot("especialidade")
        data_str = tracker.get_slot("data_consulta")
        hora_str = tracker.get_slot("hora_consulta")
        nome_medico = tracker.get_slot("nome_medico")

        if especialidade and data_str and hora_str and nome_medico:
            try:
                data_consulta = dt.parse(data_str)
                hora_consulta = dt.parse(hora_str, settings={'TIMEZONE': 'UTC'})
            except Exception as e:
                dispatcher.utter_message(text="Data ou hora inválida.")
                return [SlotSet("disponibilidade", False)]

            with DatabaseConnection() as db:
                try:
                    # 1. Buscar id_medico
                    query_medico = "SELECT id_medico FROM medicos WHERE LOWER(nome) LIKE %s"
                    result_medico = db.execute_fetchone(query_medico, (f"%{nome_medico.lower()}%",))
                    if not result_medico:
                        dispatcher.utter_message(text="Médico não encontrado.")
                        return [SlotSet("disponibilidade", False)]
                    id_medico = result_medico["id_medico"]

                    # 2. Buscar id_data
                    query_data = "SELECT id_data FROM datas WHERE data = %s"
                    result_data = db.execute_fetchone(query_data, (data_consulta.strftime('%Y-%m-%d'),))
                    if not result_data:
                        dispatcher.utter_message(text="Data não disponível.")
                        return [SlotSet("disponibilidade", False)]
                    id_data = result_data["id_data"]

                    # 3. Buscar id_horario
                    query_hora = "SELECT id_horario FROM horarios WHERE hora = %s"
                    result_hora = db.execute_fetchone(query_hora, (hora_consulta.strftime('%H:%M'),))
                    if not result_hora:
                        dispatcher.utter_message(text="Horário não disponível.")
                        return [SlotSet("disponibilidade", False)]
                    id_horario = result_hora["id_horario"]

                    # 4. Verificar disponibilidade na agenda
                    query_agenda = """
                        SELECT disponivel FROM agenda
                        WHERE id_medico = %s AND id_data = %s AND id_horario = %s
                    """
                    params = (id_medico, id_data, id_horario)
                    result = db.execute_fetchone(query_agenda, params)

                    if result and result["disponivel"]:
                        dispatcher.utter_message(
                            text=f"Disponibilidade confirmada para {especialidade} com Dr(a). {nome_medico} em {data_str} às {hora_str}."
                        )
                        return [SlotSet("disponibilidade", True)]
                    else:
                        dispatcher.utter_message(
                            text="Desculpe, o médico já tem um agendamento nesse horário. Por favor, escolha outro horário ou data."
                        )
                        return [SlotSet("disponibilidade", False)]

                except Exception as e:
                    dispatcher.utter_message(text=f"Erro ao verificar disponibilidade: {e}")
                    return [SlotSet("disponibilidade", False)]

        dispatcher.utter_message(
            text="Não foi possível confirmar a disponibilidade. Por favor, verifique os dados informados."
        )
        return [SlotSet("disponibilidade", False)]
    
    async def submit(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        
        especialidade = tracker.get_slot("especialidade")
        data_consulta = dt.parse(tracker.get_slot("data_consulta")).strftime('%d-%m-%y') if tracker.get_slot("data_consulta") else None
        hora_consulta = dt.parse((tracker.get_slot("hora_consulta")), settings={'TIMEZONE': 'UTC'}).strftime('%H:%M') if tracker.get_slot("hora_consulta") else None
        nome_medico = tracker.get_slot("nome_medico")
        motivo_consulta = tracker.get_slot("motivo_consulta")
        nome_paciente = tracker.get_slot("nome")

        dispatcher.utter_message(
            text=f"Vamos revisar seu agendamento:\n\n"
                f"👤 {nome_paciente}\n"
                f"📋 {especialidade}\n"
                f"👨‍⚕️ {nome_medico}\n"
                f"📅 {data_consulta} às {hora_consulta}\n"
                f"📝 Motivo: {motivo_consulta}\n\n"
                f"👉 Você confirma esse agendamento? (sim/não)"
            )

        return [
            SlotSet("requested_slot", None),
            FollowupAction("action_confirmar_agendamento")
        ]

class ActionConfirmarAgendamento(Action):
    def name(self) -> Text:
        return "action_confirmar_agendamento"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> List[EventType]:

        intent = tracker.latest_message.get['intent'].get('name').lower()

        if intent == "affirm":
            especialidade = tracker.get_slot("especialidade")
            data_consulta = dt.parse(tracker.get_slot("data_consulta")).strftime('%y-%m-%d') if tracker.get_slot("data_consulta") else None
            hora_consulta = dt.parse((tracker.get_slot("hora_consulta")), settings={'TIMEZONE': 'UTC'}).strftime('%H:%M:00') if tracker.get_slot("hora_consulta") else None
            nome_medico = tracker.get_slot("nome_medico")
            motivo_consulta = tracker.get_slot("motivo_consulta")
            nome_paciente = tracker.get_slot("nome")

            if especialidade is None or data_consulta is None or hora_consulta is None or nome_medico is None or nome_paciente is None:
                dispatcher.utter_message(text="Desculpe, não consegui completar o agendamento. Por favor, verifique os dados informados.")
                return []
        
            with DatabaseConnection() as db:
                try:
                    # 1. Buscar id_medico
                    query_medico = "SELECT id_medico FROM medicos WHERE LOWER(nome) LIKE %s"
                    result_medico = db.execute_fetchone(query_medico, (f"%{nome_medico.lower()}%",))
                    if not result_medico:
                        dispatcher.utter_message(text="Médico não encontrado.")
                        return []
                    id_medico = result_medico["id_medico"]

                    # 2. Buscar id_data
                    query_data = "SELECT id_data FROM datas WHERE data = %s"
                    result_data = db.execute_fetchone(query_data, (data_consulta,))
                    if not result_data:
                        dispatcher.utter_message(text="Data não disponível.")
                        return []
                    id_data = result_data["id_data"]

                    # 3. Buscar id_horario
                    query_hora = "SELECT id_horario FROM horarios WHERE hora = %s"
                    result_hora = db.execute_fetchone(query_hora, (hora_consulta,))
                    if not result_hora:
                        dispatcher.utter_message(text="Horário não disponível.")
                        return []
                    id_horario = result_hora["id_horario"]

                    # 4. Buscar id_especialidade
                    query_especialidade = "SELECT id_especialidade FROM especialidades WHERE LOWER(nome) LIKE %s"
                    result_especialidade = db.execute_fetchone(query_especialidade, (especialidade.lower(),))
                    if not result_especialidade:
                        dispatcher.utter_message(text="Especialidade não encontrada.")
                        return []
                    id_especialidade = result_especialidade["id_especialidade"]

                    # 4. Inserir agendamento na tabela agenda
                    query_insert = """
                        INSERT INTO agenda (id_data, id_horario, id_especialidade, id_medico, motivo_consulta, nome_paciente)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    params_insert = (id_data, id_horario, id_especialidade, id_medico, motivo_consulta, nome_paciente)
                    
                    if not db.execute_write(query_insert, params_insert):
                        dispatcher.utter_message(text="Erro ao registrar o agendamento no banco de dados.")
                        return []

                except Exception as e:
                    dispatcher.utter_message(text=f"Erro ao processar o agendamento: {e}")
                    return []

            dispatcher.utter_message(text=f"✅ Agendamento de {especialidade} com Dr(a). {nome_medico} em {data_consulta} às {hora_consulta} para {nome_paciente}) foi registrado com sucesso!")

            # Limpar os slots após o agendamento concluído
            return [
                AllSlotsReset(), 
                SlotSet("requested_slot", None)
            ]
        
        if intent == "deny":
            dispatcher.utter_message(
                text="Ok, o agendamento foi cancelado. Se precisar de ajuda, estou aqui!"
            )
            # Limpa todos os slots relacionados ao agendamento e o requested_slot
            return [
                AllSlotsReset(), 
                SlotSet("requested_slot", None)
            ]
        
        else:
            dispatcher.utter_message(
                text="Desculpe, não entendi sua resposta. Por favor, responda com 'sim' para confirmar ou 'não' para cancelar o agendamento."
            )
            return []


# --- Ação para Customizar as Perguntas dos Slots usando LLM (ou lógica simples) ---
class ActionPerguntarSlotLLM(Action):
    def name(self) -> Text:
        return "agendamento_consulta_form"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> List[Dict[Text, Any]]:

        current_slot = tracker.get_slot("requested_slot")
        # TODO: Integrar sua lógica de LLM aqui para gerar a pergunta dinâmica.
        # Por enquanto, usaremos mensagens hardcoded ou do domain.yml.

        pergunta_customizada = None

        if current_slot == "especialidade":
            pergunta_customizada = "Para qual especialidade médica específica você busca atendimento hoje? (Ex: Cardiologia, Pediatria)"
        elif current_slot == "data_consulta":
            pergunta_customizada = "Para qual dia você gostaria de agendar sua consulta? Por favor, seja o mais claro possível. (Ex: 'amanhã', '28 de julho')"
        elif current_slot == "hora_consulta":
            pergunta_customizada = "Qual horário seria o ideal para você? (Ex: '10h', 'às 14:30')"
        elif current_slot == "nome_medico":
            pergunta_customizada = "Você tem alguma preferência por um profissional específico? Se sim, qual o nome completo do médico(a)?"
        elif current_slot == "motivo_consulta":
            pergunta_customizada = "Poderia me dar um breve resumo do motivo da sua consulta? Isso nos ajuda a direcioná-lo melhor."
        elif current_slot == "nome":
            pergunta_customizada = "Por favor, para finalizar o agendamento, qual é o seu nome completo?"
        else:
            # Fallback: se não for um dos slots customizados, usa a resposta padrão do domain.yml
            dispatcher.utter_message(response=f"utter_ask_{current_slot}")
            return [] # Não enviar 'text' se for 'response'

        if pergunta_customizada:
            dispatcher.utter_message(text=pergunta_customizada)
        return []

# --- Ação para cancelar agendamento (exemplo) ---
class ActionCancelarAgendamento(Action):
    def name(self) -> Text:
        return "action_cancelar_agendamento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Ok, o agendamento foi cancelado e todas as informações foram limpas.")
        # Limpa todos os slots relacionados ao agendamento e o requested_slot
        return [
            SlotSet("especialidade", None),
            SlotSet("data_consulta", None),
            SlotSet("hora_consulta", None),
            SlotSet("nome_medico", None),
            SlotSet("motivo_consulta", None),
            SlotSet("nome", None),
            SlotSet("cadastro_pessoa_f", None),
            SlotSet("requested_slot", None) # Limpa o slot de controle do formulário
        ]

# --- Ação ValidateAgendamentoConsultaForm (exemplo) ---
# Ações de validação de slot foram movidas para a classe ValidateAgendamentoConsultaForm acima.
# Se você tinha métodos de validação aqui, eles devem ser integrados lá.
# Ex: class ValidateMeuSlot(FormValidationAction): ...