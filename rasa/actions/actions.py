# actions/actions.py

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.forms import FormValidationAction # Mantido apenas esta importação de forms

# --- Importações de bibliotecas externas ---
import requests
# from datetime import datetime, timedelta # Descomente se for usar para validação de datas

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
        especialidades_validas = [
            "cardiologia", "dermatologia", "pediatria", "ortopedia", "ginecologia",
            "clínico geral", "odontologia", "neurologia", "oftalmologia", "urologia",
            "consulta geral", # Adicionado do NLU
        ]
        if slot_value and slot_value.lower() in especialidades_validas:
            dispatcher.utter_message(text=f"Entendido, especialidade: {slot_value.capitalize()}.")
            return {"especialidade": slot_value}
        elif slot_value:
            dispatcher.utter_message(text="Desculpe, essa especialidade não está disponível ou não entendi. Poderia informar novamente?")
            return {"especialidade": None}
        else:
            return {"especialidade": None} # Mantém o slot sem preencher

    async def validate_data_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'data_consulta'."""
        # TODO: Implementar validação de data mais robusta aqui (ex: usar dateparser, verificar futuro)
        if slot_value:
            # Exemplo básico: apenas confirma que recebeu algo.
            # Você deve adicionar lógica para garantir que é uma data real e futura, etc.
            dispatcher.utter_message(text=f"Data selecionada: {slot_value}.")
            return {"data_consulta": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, forneça uma data válida para a consulta. Ex: 'amanhã', '25 de julho'.")
            return {"data_consulta": None}

    async def validate_hora_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'hora_consulta'."""
        # TODO: Implementar validação de hora mais robusta (ex: HH:MM, dentro do horário de funcionamento)
        if slot_value and (":" in slot_value or "h" in slot_value.lower()):
            dispatcher.utter_message(text=f"Horário: {slot_value}.")
            return {"hora_consulta": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, insira um horário válido. Ex: '10h', '14:30'.")
            return {"hora_consulta": None}

    async def validate_nome_medico(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'nome_medico'."""
        if slot_value and len(slot_value) >= 3: # Exemplo: nome com pelo menos 3 caracteres
            dispatcher.utter_message(text=f"Médico(a) escolhido(a): {slot_value}.")
            return {"nome_medico": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, me diga o nome completo do médico ou se não tem preferência.")
            return {"nome_medico": None}

    async def validate_motivo_consulta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'motivo_consulta'."""
        if slot_value and len(slot_value) > 5: # Exemplo: motivo precisa ter mais de 5 caracteres
            dispatcher.utter_message(text="Motivo registrado.")
            return {"motivo_consulta": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, descreva o motivo da consulta com mais detalhes.")
            return {"motivo_consulta": None}

    async def validate_nome(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'nome' (nome do paciente)."""
        if slot_value and len(slot_value) >= 3:
            dispatcher.utter_message(text=f"Seu nome: {slot_value.capitalize()}.")
            return {"nome": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, informe seu nome completo.")
            return {"nome": None}

    async def validate_cadastro_pessoa_f(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o slot 'cadastro_pessoa_f' (CPF)."""
        # Exemplo de validação de CPF (muito básica)
        # TODO: Implementar validação de CPF real (formato, dígitos verificadores)
        if slot_value and (len(slot_value) == 11 or len(slot_value) == 14 and '-' in slot_value):
            dispatcher.utter_message(text=f"CPF registrado: {slot_value}.")
            return {"cadastro_pessoa_f": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, informe um CPF válido (somente números ou com pontos e hífen).")
            return {"cadastro_pessoa_f": None}

# --- Ação para submeter o agendamento (após confirmação do resumo) ---
class ActionSubmitAgendamento(Action):
    def name(self) -> Text:
        return "action_submit_agendamento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        # Recuperar os valores dos slots
        especialidade = tracker.get_slot("especialidade")
        data_consulta = tracker.get_slot("data_consulta")
        hora_consulta = tracker.get_slot("hora_consulta")
        nome_medico = tracker.get_slot("nome_medico")
        motivo_consulta = tracker.get_slot("motivo_consulta")
        nome_paciente = tracker.get_slot("nome")
        cadastro = tracker.get_slot("cadastro_pessoa_f")

        # --- Lógica para FINALIZAR o agendamento real ---
        # Aqui você faria a integração com seu sistema de agendamento (API, BD, etc.)
        dispatcher.utter_message(text=f"✅ Agendamento de {especialidade} com Dr(a). {nome_medico} em {data_consulta} às {hora_consulta} para {nome_paciente} (CPF: {cadastro}) foi registrado com sucesso! Um e-mail/SMS de confirmação será enviado.")

        # Limpar os slots após o agendamento concluído
        return [
            SlotSet("especialidade", None),
            SlotSet("data_consulta", None),
            SlotSet("hora_consulta", None),
            SlotSet("nome_medico", None),
            SlotSet("motivo_consulta", None),
            SlotSet("nome", None),
            SlotSet("cadastro_pessoa_f", None),
            SlotSet("requested_slot", None) # Importante para resetar o formulário
        ]

# --- Ação para Customizar as Perguntas dos Slots usando LLM (ou lógica simples) ---
class ActionPerguntarSlotLLM(Action):
    def name(self) -> Text:
        return "action_perguntar_slot_llm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

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
        elif current_slot == "cadastro_pessoa_f":
            pergunta_customizada = "Para o registro, qual o seu CPF? (Apenas números ou com pontos e hífen)"
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