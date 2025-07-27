# actions/actions.py

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType # Adicionado EventType para ClearOtherSlots
from rasa_sdk.forms import FormValidationAction, FormAction # Importa FormAction

# --- Importações de bibliotecas externas (Adicione aqui as que suas ações REALMENTE usam) ---
# Exemplo: Se você for integrar com um LLM via API, 'requests' é comum.
# Se não for usar, pode remover a linha abaixo e do requirements-actions.txt
import requests

# Exemplo: Se precisar de manipulação de data/hora (muito comum em agendamento)
# from datetime import datetime, timedelta

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
            llm_api_url = "http://seu-servico-llm.com/api/pergunta" # <<< MUDE ISSO!
            
            # Formato da requisição ao LLM
            payload = {"query": user_message}
            
            # Faz a chamada POST para o LLM
            response = requests.post(llm_api_url, json=payload, timeout=10) # Timeout de 10 segundos
            response.raise_for_status() # Lança um erro para status HTTP ruins (4xx ou 5xx)
            
            llm_resposta = response.json().get("response", "Não consegui uma resposta clara do LLM.")
            
        except requests.exceptions.Timeout:
            llm_resposta = "O LLM demorou muito para responder. Por favor, tente novamente mais tarde."
        except requests.exceptions.RequestException as e:
            llm_resposta = f"Não foi possível conectar ao LLM. Erro: {e}"
        except Exception as e:
            llm_resposta = f"Um erro inesperado ocorreu ao processar a pergunta ao LLM: {e}"
        # --- FIM DO EXEMPLO ---

        dispatcher.utter_message(text=llm_resposta)
        return []

# --- Ação de Formulário: agendamento_consulta_form ---
class AgendamentoConsultaForm(FormAction):
    def name(self) -> Text:
        return "agendamento_consulta_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """Uma lista de slots que o formulário precisa preencher."""
        return [
            "especialidade",
            "data_consulta",
            "hora_consulta",
            "nome_medico",
            "motivo_consulta",
            "nome",
            "cadastro_pessoa_f"
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """Um dicionário para mapear as intenções/entidades para os slots."""
        return {
            "especialidade": self.from_entity(entity="especialidade"),
            "data_consulta": self.from_entity(entity="data_consulta"),
            "hora_consulta": self.from_entity(entity="hora_consulta"),
            "nome_medico": self.from_entity(entity="nome_medico"),
            "motivo_consulta": self.from_entity(entity="motivo_consulta"),
            "nome": self.from_entity(entity="nome"),
            "cadastro_pessoa_f": self.from_entity(entity="cadastro_pessoa_f")
            # Exemplo de mapeamento para pergunta sim/não para 'cadastro_pessoa_f'
            # "cadastro_pessoa_f": [
            #     self.from_intent(intent="affirm", value="sim"),
            #     self.from_intent(intent="deny", value="não"),
            #     self.from_entity(entity="cadastro_pessoa_f") # Caso a entidade seja extraída diretamente
            # ]
        }

    # --- Métodos de validação de slots (opcional, mas recomendado) ---
    # async def validate_data_consulta(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
    #     # Exemplo de validação de data
    #     # Você pode usar uma biblioteca como 'dateparser' ou 'datetime' para isso.
    #     # if is_valid_date(slot_value):
    #     #     return {"data_consulta": slot_value}
    #     # else:
    #     #     dispatcher.utter_message(text="Essa data não parece válida. Por favor, insira uma data no formato DD/MM/AAAA.")
    #     #     return {"data_consulta": None}
    #     return {"data_consulta": slot_value} # Por enquanto, apenas retorna o valor

    # async def validate_hora_consulta(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
    #     # Exemplo de validação de hora
    #     # if is_valid_time(slot_value):
    #     #     return {"hora_consulta": slot_value}
    #     # else:
    #     #     dispatcher.utter_message(text="Esse horário não parece válido. Por favor, insira um horário como HH:MM.")
    #     #     return {"hora_consulta": None}
    #     return {"hora_consulta": slot_value} # Por enquanto, apenas retorna o valor

    # async def validate_cadastro_pessoa_f(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
    #     # Exemplo de validação para sim/não
    #     if slot_value.lower() in ["sim", "s", "yes"]:
    #         return {"cadastro_pessoa_f": "sim"}
    #     elif slot_value.lower() in ["não", "nao", "n", "no"]:
    #         return {"cadastro_pessoa_f": "não"}
    #     else:
    #         dispatcher.utter_message(text="Por favor, responda 'sim' ou 'não'.")
    #         return {"cadastro_pessoa_f": None}
    
    def submit(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: DomainDict) -> List[Dict[Text, Any]]:
        """Define o que fazer quando o formulário é submetido (todos os slots preenchidos)."""
        # Esta função é chamada automaticamente pelo Rasa quando todos os slots obrigatórios são preenchidos.
        # Você pode adicionar lógica aqui para verificar disponibilidade, etc.
        dispatcher.utter_message(response="utter_submit_agendamento_consulta_form")
        return []

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
        # Exemplo:
        # try:
        #     api_response = requests.post(
        #         "http://sua-api-de-agendamento.com/agendar",
        #         json={
        #             "especialidade": especialidade,
        #             "data": data_consulta,
        #             "hora": hora_consulta,
        #             "medico": nome_medico,
        #             "motivo": motivo_consulta,
        #             "paciente": nome_paciente,
        #             "cadastrado": cadastro
        #         }
        #     )
        #     api_response.raise_for_status()
        #     dispatcher.utter_message(text=f"Seu agendamento foi confirmado com sucesso para {data_consulta} às {hora_consulta}.")
        # except requests.exceptions.RequestException as e:
        #     dispatcher.utter_message(text=f"Desculpe, não consegui finalizar seu agendamento devido a um erro no sistema: {e}")
        #     return []

        dispatcher.utter_message(text=f"✅ Agendamento de {especialidade} com Dr(a). {nome_medico} em {data_consulta} às {hora_consulta} para {nome_paciente} foi registrado com sucesso! Um e-mail/SMS de confirmação será enviado.")
        
        # Limpar os slots após o agendamento concluído
        return [
            SlotSet("especialidade", None),
            SlotSet("data_consulta", None),
            SlotSet("hora_consulta", None),
            SlotSet("nome_medico", None),
            SlotSet("motivo_consulta", None),
            SlotSet("nome", None),
            SlotSet("cadastro_pessoa_f", None)
            # SlotSet("requested_slot", None) # Se você quiser limpar o slot de controle do formulário
        ]

# --- Ação action_agendar_consulta ---
# Você mencionou 'action_agendar_consulta' no domain.yml.
# Se esta ação é apenas para ativar o formulário, e a rule já faz isso:
# - rule: Ativar agendamento consulta
#   steps:
#     - intent: agendar_consulta
#     - action: agendamento_consulta_form  <- aqui ativa o form diretamente
#     - active_loop: agendamento_consulta_form
# Então você não precisa de uma classe Python separada para 'action_agendar_consulta'.
# O nome do FormAction (agendamento_consulta_form) já serve como a ação para ativá-lo.
# Se você tiver uma lógica customizada para essa ação, ela iria aqui:
# class ActionAgendarConsulta(Action):
#     def name(self) -> Text:
#         return "action_agendar_consulta"
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(text="Preparando para agendar sua consulta...")
#         return [SlotSet("algum_slot_extra", "valor")]

# --- Ação action_cancelar_agendamento ---
# Você mencionou 'action_cancelar_agendamento' no domain.yml.
# Se você não tem uma rule ou story usando-a, ela não será disparada.
# Se você quiser uma ação para limpar slots e desativar loops em caso de cancelamento:
class ActionCancelarAgendamento(Action):
    def name(self) -> Text:
        return "action_cancelar_agendamento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Cancelando o agendamento e limpando as informações.")
        # Limpa todos os slots relacionados ao agendamento
        return [
            SlotSet("especialidade", None),
            SlotSet("data_consulta", None),
            SlotSet("hora_consulta", None),
            SlotSet("nome_medico", None),
            SlotSet("motivo_consulta", None),
            SlotSet("nome", None),
            SlotSet("cadastro_pessoa_f", None),
            SlotSet("requested_slot", None) # Limpa o slot do formulário
 ]