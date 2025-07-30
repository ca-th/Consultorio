from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from datetime import datetime, timedelta
from dateutil.parser import parse
import re
import logging
import dateparser as dt

from .gemini_integration import GeminiIntegration

logger = logging.getLogger(__name__)

class ActionAnalyzeSymptoms(Action):
    def name(self) -> Text:
        return "action_analyze_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        symptoms = tracker.get_slot("symptoms") or []
        
        logger.info(f"Analisando sintomas: {symptoms}")

        if not symptoms:
            entities = tracker.latest_message.get("entities", [])
            symptoms = [e.get("value") for e in entities if e.get("entity") == "symptom"]
        
        # Validação inicial
        if not symptoms:
            dispatcher.utter_message(text="Não consegui identificar sintomas específicos. Pode descrevê-los novamente?")
            return []
        
        try:
            # Sua integração com Gemini
            gemini = GeminiIntegration()
            analysis = gemini.analyze_symptoms(symptoms)
            
            # Validação da resposta do Gemini
            if not analysis or not analysis.get('specialty'):
                raise ValueError("Gemini retornou análise inválida ou vazia")
            
            # Verificar se tem erro na resposta
            if analysis.get('specialty', '').lower() in ['indefinida', 'erro', 'error', '']:
                raise ValueError(f"Gemini retornou specialty inválida: {analysis.get('specialty')}")
            
            # Mapear mensagens de urgência
            urgency_messages = {
                "emergência": "⚠ ATENÇÃO: Seus sintomas podem indicar urgência médica. Procure atendimento imediato!",
                "alta": "⚠ Recomendamos buscar atendimento médico hoje mesmo.",
                "média": "Recomendamos agendar consulta nos próximos dias.",
                "baixa": "Você pode agendar uma consulta de rotina."
            }
            
            # Montar mensagem de resposta
            message = f"""
                Análise dos seus sintomas:

                🔹 *Especialidade recomendada:* {analysis['specialty']}
                🔹 *Urgência:* {analysis['urgency']}
                🔹 *Orientação:* {analysis['explanation']}

                {urgency_messages.get(analysis['urgency'], '')}
            """
            
            if analysis.get('immediate_care'):
                message += f"\n\n*Cuidados imediatos:* {analysis['immediate_care']}"
            
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("recommended_specialty", analysis['specialty']),
                SlotSet("specialty", analysis['specialty']),
                SlotSet("symptoms_urgency", analysis['urgency']),
                SlotSet("symptoms_explanation", analysis['explanation'])
            ]
            
        except Exception as e:
            # Log detalhado do erro para debug
            logger.error(f"ERRO na análise Gemini: {str(e)}")
            logger.error(f"Sintomas recebidos: {symptoms}")
            logger.error(f"Tipo do erro: {type(e)._name_}")
            
            # Resposta de fallback amigável que mantém o fluxo
            symptoms_text = ', '.join(symptoms) if isinstance(symptoms, list) else str(symptoms)
            
            dispatcher.utter_message(text=f"""
                Entendi que você tem: {symptoms_text}

                No momento estou com dificuldades técnicas para fazer a análise automática. 
                Vamos agendar uma consulta com um *Clínico Geral* que poderá avaliar adequadamente seus sintomas.

                Posso prosseguir com o agendamento?
            """)
            
            # Retorna slots válidos mesmo com erro - NÃO quebra o fluxo
            return [
                SlotSet("recommended_specialty", "Clínico Geral"),
                SlotSet("specialty", "Clínico Geral"),
                SlotSet("symptoms_urgency", "média"),
                SlotSet("symptoms_explanation", "Consulta recomendada devido a indisponibilidade temporária da análise automática.")
            ]

class ValidateAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_appointment_form"

    def validate_patient_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if slot_value and len(slot_value) >= 2:
            return {"patient_name": slot_value}
        else:
            dispatcher.utter_message(text="Por favor, informe um nome válido.")
            return {"patient_name": None}

    def validate_patient_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        # Expressão regular simples para validar e-mail
        email_pattern = r"[^@]+@[^@]+\.[^@]+"

        if slot_value and re.match(email_pattern, slot_value):
            return {"patient_email": slot_value}
        
        dispatcher.utter_message(text="Por favor, informe um e-mail válido (ex: nome@exemplo.com).")
        return {"patient_email": None}

    def validate_appointment_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        try:
            # Tenta converter qualquer formato para datetime.date
            date_obj = dt.parse(slot_value, languages=["pt"], settings={"PREFER_DATES_FROM": "future"})

            if date_obj >= datetime.now().date():
                # Retorna data no formato brasileiro
                return {"appointment_date": date_obj.strftime("%d/%m/%Y")}
            else:
                dispatcher.utter_message(text="A data deve ser hoje ou no futuro.")
                return {"appointment_date": None}

        except Exception:
            dispatcher.utter_message(text="Por favor, informe a data no formato DD/MM/AAAA.")
            return {"appointment_date": None}


    def validate_appointment_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if slot_value:
            try:
                # Verifica formato HH:MM
                time_obj = datetime.strptime(slot_value, "%H:%M")
                hour = time_obj.hour
                
                # Verifica horário comercial (8h às 18h)
                if 8 <= hour <= 18:
                    return {"appointment_time": slot_value}
                else:
                    dispatcher.utter_message(text="Horário deve estar entre 08:00 e 18:00.")
                    return {"appointment_time": None}
            except ValueError:
                dispatcher.utter_message(text="Por favor, informe o horário no formato HH:MM (ex: 14:30).")
                return {"appointment_time": None}
        
        return {"appointment_time": None}
    
    def validate_specialty(
            self,
            slot_value: Any, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:  

        if tracker.get_slot("recommended_specialty"):
            specialty = tracker.get_slot("recommended_specialty")

        especialidades = {"clínica geral": "Clínica Geral",
                "clínico geral": "Clínica Geral",
                "clinica geral": "Clínica Geral",
                "clinico geral": "Clínica Geral",
                "pediatria": "Pediatria",
                "cardiologia": "Cardiologia",
                "dermatologia": "Dermatologia"
            }
        if specialty:
            if specialty.lower() in especialidades:
                return {"specialty": especialidades[specialty.lower()]}
            else:
                dispatcher.utter_message(text=f"Desculpe, não temos a especialidade {specialty} no nosso consultório."
                                         "Trabalhamos com: Clínica Geral, Pediatria, Cardiologia e Dermatologia"
                                         "Qual dessas você gostaria?")
                return {"specialty": None}
        else: 
            return {"specialty": None}

class ActionScheduleAppointment(Action):
    def name(self) -> Text:
        return "action_schedule_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Coleta dados do agendamento
        patient_data = {
            'name': tracker.get_slot("patient_name"),
            'phone': tracker.get_slot("patient_phone"),
            'symptoms': tracker.get_slot("symptoms") or [],
            'specialty': tracker.get_slot("specialty") or tracker.get_slot("recommended_specialty"),
            'date': tracker.get_slot("appointment_date"),
            'time': tracker.get_slot("appointment_time")
        }
        
        confirmation_message = f"""
            ✅ **Consulta Agendada com Sucesso!**

            📋 **Detalhes:**
            - **Paciente:** {patient_data['name']}
            - **Especialidade:** {patient_data['specialty']}
            - **Data:** {patient_data['date']}
            - **Horário:** {patient_data['time']}
            - **Telefone:** {patient_data['phone']}

            📱 **Próximos passos:**
            1. Você receberá SMS de confirmação
            2. Chegue 15 minutos antes do horário
            3. Traga documentos e exames anteriores

            Há algo a mais que eu possa ajudar?
        """
        
        dispatcher.utter_message(text=confirmation_message)
        
        return []
    
class ActionHandleFormInterruption(Action):
    def name(self) -> Text:
        return "action_handle_form_interruption"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Ok, entendi. Cancelei o preenchimento do formulário."
                                 "Há algo a mais que eu possa ajudar?")

        # Desativa o formulário explicitamente
        # Você precisa saber o nome do formulário que está ativo, ex: 'appointment_form'
        return [SlotSet("requested_slot", None), SlotSet("active_loop", None)]
        # ActiveLoopSet(None) desativa qualquer loop ativo.
        # SlotSet("requested_slot", None) limpa o slot que o formulário estava pedindo.