# actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop, FollowupAction, AllSlotsReset

# Importar bibliotecas para Gemini e variáveis de ambiente
import google.generativeai as genai
import os
from dotenv import load_dotenv # Importa load_dotenv para carregar .env

# Importa a classe FormValidationAction para validação de formulários (se você usa)
from rasa_sdk.forms import FormValidationAction

# Carrega as variáveis de ambiente do arquivo .env
# Certifique-se de ter um arquivo .env na raiz do seu projeto Rasa
# com GEMINI_API_KEY="SUA_CHAVE_AQUI"
load_dotenv()

class ActionPerguntarLLM(Action):

    def name(self) -> Text:
        """Define o nome único da ação personalizada."""
        return "action_perguntar_llm"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Executa a lógica para enviar a pergunta do usuário ao modelo Gemini
        e enviar a resposta de volta ao usuário.
        """
        # Obtenha a última mensagem do usuário do tracker
        user_message = tracker.latest_message.get("text")

        # Verifica se a mensagem do usuário não está vazia
        if not user_message:
            dispatcher.utter_message(text="Desculpe, não consegui entender sua pergunta.")
            return []

        # Obtenha a chave da API do Gemini das variáveis de ambiente
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        # Verifica se a chave da API foi configurada
        if not GEMINI_API_KEY:
            dispatcher.utter_message(text="Desculpe, a chave da API do Gemini não está configurada. Por favor, avise o desenvolvedor.")
            return []

        # Configura a API do Gemini com a chave
        genai.configure(api_key=GEMINI_API_KEY)

        # Inicializa o modelo Gemini (você pode escolher 'gemini-pro' ou outros modelos disponíveis)
        model = genai.GenerativeModel('gemini-1.5-flash')

        try:
            # Envie uma mensagem inicial para o usuário enquanto o LLM processa
            # Isso usa a resposta 'utter_ask_llm' definida no domain.yml
            dispatcher.utter_message(response="utter_ask_llm")

            # Gera conteúdo usando o modelo Gemini
            # O user_message é enviado como o prompt para o LLM
            # Usamos await model.generate_content_async para chamadas assíncronas
            response = await model.generate_content_async(user_message)
            # Acessa o texto da resposta gerada pelo Gemini
            llm_response = response.text

            # Envia a resposta do LLM de volta ao usuário
            dispatcher.utter_message(text=llm_response)

        except Exception as e:
            # Captura e trata qualquer erro que ocorra durante a chamada à API do Gemini
            dispatcher.utter_message(text=f"Desculpe, tive um problema ao tentar responder a sua pergunta com a IA. Erro: {e}")

        # Retorna uma lista de eventos (aqui vazia, pois não alteramos slots, etc.
        # Se precisar resetar slots ou ativar algo, adicione eventos aqui)
        return []


# ====================================================================
# Ações de Validação de Formulário (MANTIDAS DO SEU CÓDIGO)
# Adapte conforme suas necessidades de validação
# ====================================================================
class ValidateAgendamentoConsultaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_agendamento_consulta_form"

    # @staticmethod
    # def especialidade_db() -> List[Text]:
    #     return ["pediatria", "cardiologia", "dermatologia", "clinico geral"]

    def validate_especialidade(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `especialidade` value."""
        if slot_value.lower() in ["pediatria", "cardiologia", "dermatologia", "clinico geral"]:
            # validation succeeded, set the value of the "especialidade" slot to value
            return {"especialidade": slot_value}
        else:
            dispatcher.utter_message(text=f"Não temos a especialidade de {slot_value}. Por favor, escolha entre Pediatria, Cardiologia, Dermatologia ou Clínico Geral.")
            return {"especialidade": None} # Manter o slot vazio para pedir novamente

    def validate_data_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `data_consulta` value."""
        # Implemente sua lógica de validação de data aqui
        # Por exemplo, verificar se a data é futura ou em um formato válido
        if len(slot_value) > 3: # Exemplo simples de validação
            return {"data_consulta": slot_value}
        else:
            dispatcher.utter_message(text="Essa não parece ser uma data válida. Por favor, me diga o dia (ex: 'amanhã', 'quarta-feira', '25 de julho').")
            return {"data_consulta": None}

    def validate_hora_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `hora_consulta` value."""
        # Implemente sua lógica de validação de hora aqui
        if "h" in slot_value: # Exemplo simples de validação
            return {"hora_consulta": slot_value}
        else:
            dispatcher.utter_message(text="Esse não parece ser um horário válido. Por favor, me diga a hora (ex: '10h da manhã', 'às 14h').")
            return {"hora_consulta": None}

    def validate_nome_medico(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `nome_medico` value."""
        # Implemente sua lógica de validação de nome do médico aqui
        # Ex: verificar se o nome existe em uma lista de médicos
        if len(slot_value) > 2: # Exemplo simples
            return {"nome_medico": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, me diga um nome de médico válido.")
            return {"nome_medico": None}

    def validate_motivo_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `motivo_consulta` value."""
        if len(slot_value) > 5: # Exemplo simples: motivo com mais de 5 caracteres
            return {"motivo_consulta": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, descreva um pouco mais o motivo da sua consulta.")
            return {"motivo_consulta": None}

class ActionSubmitAgendamento(Action):
    def name(self) -> Text:
        return "action_submit_agendamento"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Aqui você implementaria a lógica para salvar o agendamento
        # em um banco de dados ou chamar uma API externa.

        especialidade = tracker.get_slot("especialidade")
        data_consulta = tracker.get_slot("data_consulta")
        hora_consulta = tracker.get_slot("hora_consulta")
        nome_medico = tracker.get_slot("nome_medico")
        motivo_consulta = tracker.get_slot("motivo_consulta")

        # Exemplo de como você poderia usar as informações:
        print(f"Agendamento confirmado: Especialidade: {especialidade}, Data: {data_consulta}, Hora: {hora_consulta}, Médico: {nome_medico}, Motivo: {motivo_consulta}")

        dispatcher.utter_message(text="Ok, seu agendamento está quase pronto! Entraremos em contato em breve para confirmar os detalhes. Agradecemos a sua preferência.")
        
        # Resetar os slots após o envio do formulário
        return [AllSlotsReset()]