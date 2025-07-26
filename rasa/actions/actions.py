from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop, FollowupAction, AllSlotsReset
from rasa_sdk.forms import FormValidationAction

# Importar bibliotecas para Gemini e variáveis de ambiente
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Biblioteca para manipulação de datas
from datetime import datetime, timedelta
import dateparser

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# ====================================================================
# AÇÃO DE PERGUNTA GENÉRICA USANDO LLM
# Esta ação responde a perguntas que não fazem parte do formulário.
# ====================================================================
class ActionPerguntarLLM(Action):

    def name(self) -> Text:
        """Define o nome único da ação personalizada."""
        return "action_perguntar_llm"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Executa a lógica para enviar a pergunta do usuário ao modelo Gemini
        e enviar a resposta de volta ao usuário, com um prompt de contexto.
        """
        user_message = tracker.latest_message.get("text")

        if not user_message:
            dispatcher.utter_message(text="Desculpe, não consegui entender sua pergunta.")
            return []

        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        if not GEMINI_API_KEY:
            dispatcher.utter_message(text="Desculpe, a chave da API do Gemini não está configurada. Por favor, avise o desenvolvedor.")
            return []

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        try:
            # PROMPT DE CONTEXTUALIZAÇÃO PARA A LLM
            system_prompt = (
                "Você é um assistente virtual de agendamento de consultas médicas. "
                "Seu principal objetivo é ajudar o usuário a agendar consultas, fornecendo informações "
                "sobre especialidades, médicos, horários e procedimentos. "
                "Responda apenas a perguntas relacionadas à saúde e agendamentos. "
                "Se o usuário fizer uma pergunta não relacionada, gentilmente o redirecione para o agendamento."
            )
            
            prompt_para_llm = f"{system_prompt}\n\nUsuário: {user_message}"

            # Usa await para a chamada assíncrona ao LLM
            response = await model.generate_content_async(prompt_para_llm)
            llm_response = response.text

            # Envia a resposta diretamente ao usuário
            dispatcher.utter_message(text=llm_response)

        except Exception as e:
            dispatcher.utter_message(text=f"Desculpe, tive um problema ao tentar responder a sua pergunta. Erro: {e}")
            
        return []

# ====================================================================
# AÇÃO DE PERGUNTAR SLOTS USANDO LLM
# Esta é a ação que vamos usar para gerar as perguntas do formulário.
# ====================================================================
class ActionPerguntarSlotLLM(Action):
    def name(self) -> Text:
        return "action_perguntar_slot_llm"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        latest_question_slot = tracker.get_latest_question_slot_name()

        # Mapeia os slots para prompts amigáveis para o LLM
        prompt_map = {
            "motivo_consulta_tipo": "Gere uma pergunta para saber se a consulta é de rotina ou por algum sintoma.",
            "especialidade": "Gere uma pergunta para pedir a especialidade médica para o agendamento.",
            "data_consulta": "Gere uma pergunta para pedir a data da consulta médica.",
            "hora_consulta": "Gere uma pergunta para pedir a hora da consulta.",
            "nome_medico": "Gere uma pergunta para pedir o nome do médico para o agendamento.",
            "motivo_consulta": "Gere uma pergunta para que o usuário descreva o motivo da consulta.",
        }

        prompt_para_llm = prompt_map.get(
            latest_question_slot,
            f"Gere uma pergunta para pedir ao usuário a informação de '{latest_question_slot}'."
        )

        try:
            GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
            if not GEMINI_API_KEY:
                dispatcher.utter_message(text=f"Qual {latest_question_slot}?")
                return []
            
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = await model.generate_content_async(prompt_para_llm)
            llm_response = response.text
            dispatcher.utter_message(text=llm_response)

        except Exception as e:
            dispatcher.utter_message(text=f"Qual {latest_question_slot}?")
            return []

        return []

# ====================================================================
# AÇÕES DE VALIDAÇÃO DE FORMULÁRIO
# ====================================================================
class ValidateAgendamentoConsultaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_agendamento_consulta_form"

    def validate_motivo_consulta_tipo(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `motivo_consulta_tipo` value."""
        if any(keyword in slot_value.lower() for keyword in ["rotina", "rotineira", "exames"]):
            return {"motivo_consulta_tipo": "rotina"}
        elif any(keyword in slot_value.lower() for keyword in ["sintoma", "dor", "doente"]):
            return {"motivo_consulta_tipo": "sintoma"}
        else:
            dispatcher.utter_message(text="Desculpe, não entendi. É uma consulta de rotina ou por causa de algum sintoma?")
            return {"motivo_consulta_tipo": None}

    def validate_especialidade(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `especialidade` value."""
        especialidades_disponiveis = ["pediatria", "cardiologia", "dermatologia", "clinico geral", "gastroenterologia", "ortopedia", "odontologia", "ginecologia", "urologia"]
        
        if slot_value.lower() in especialidades_disponiveis:
            return {"especialidade": slot_value}
        else:
            dispatcher.utter_message(text=f"Não temos a especialidade de {slot_value}. Por favor, escolha entre: Pediatria, Cardiologia, Dermatologia, Clínico Geral, Gastroenterologia, Ortopedia, Odontologia, Ginecologia ou Urologia.")
            return {"especialidade": None}

    def validate_data_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `data_consulta` value and ensure it is in the future."""
        # Usa dateparser para reconhecer datas em linguagem natural
        parsed_date = dateparser.parse(slot_value)
        
        if parsed_date and parsed_date >= datetime.now() - timedelta(days=1):
            return {"data_consulta": parsed_date.strftime("%d-%m-%Y")}
        else:
            dispatcher.utter_message(text="Essa não parece ser uma data válida ou é uma data no passado. Por favor, me diga o dia (ex: 'amanhã', 'quarta-feira', '25 de julho').")
            return {"data_consulta": None}

    def validate_hora_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `hora_consulta` value and ensure it is in the correct format."""
        try:
            # Tenta converter o valor para um formato de hora para validação
            if "h" in slot_value:
                # Remove 'h' e tenta converter para um horário
                hora_str = slot_value.replace("h", "").strip()
                if len(hora_str) <= 2:
                    datetime.strptime(hora_str, "%H")
                else:
                    datetime.strptime(hora_str, "%H:%M")
            else:
                # Se não tiver 'h', tenta outros formatos
                datetime.strptime(slot_value, "%H:%M")
            return {"hora_consulta": slot_value}
        except (ValueError, TypeError):
            dispatcher.utter_message(text="Esse não parece ser um horário válido. Por favor, me diga a hora (ex: '10h da manhã', 'às 14:30').")
            return {"hora_consulta": None}

    def validate_nome_medico(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `nome_medico` value."""
        # Aumentei o mínimo para 2, pois nomes de médicos podem ser curtos.
        if len(slot_value) >= 2 and all(c.isalpha() or c.isspace() for c in slot_value):
            return {"nome_medico": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, me diga um nome de médico válido (somente letras, no mínimo 2 caracteres).")
            return {"nome_medico": None}

    def validate_motivo_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `motivo_consulta` value."""
        if len(slot_value) > 5:
            return {"motivo_consulta": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, descreva um pouco mais o motivo da sua consulta (mínimo de 6 caracteres).")
            return {"motivo_consulta": None}

class ActionSubmitAgendamento(Action):
    def name(self) -> Text:
        return "action_submit_agendamento"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        especialidade = tracker.get_slot("especialidade")
        data_consulta = tracker.get_slot("data_consulta")
        hora_consulta = tracker.get_slot("hora_consulta")
        nome_medico = tracker.get_slot("nome_medico")
        motivo_consulta = tracker.get_slot("motivo_consulta")

        print(f"Agendamento confirmado: Especialidade: {especialidade}, Data: {data_consulta}, Hora: {hora_consulta}, Médico: {nome_medico}, Motivo: {motivo_consulta}")

        dispatcher.utter_message(text="Ok, seu agendamento está quase pronto! Entraremos em contato em breve para confirmar os detalhes. Agradecemos a sua preferência.")
        
        return [AllSlotsReset()]