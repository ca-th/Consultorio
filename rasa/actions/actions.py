from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from datetime import datetime, timedelta
import re
import logging
import json

import phonenumbers
from phonenumbers import geocoder, carrier

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

    #def validate_patient_cpf(
       # self,
       # slot_value: Any,
       # dispatcher: CollectingDispatcher,
       # tracker: Tracker,
       # domain: DomainDict,
    #) -> Dict[Text, Any]:
        
       # if slot_value:
            # Remove formatação
           # cpf_digits = re.sub(r'\D', '', slot_value)
           # if len(cpf_digits) == 11:
             #   return {"patient_cpf": slot_value}
        
       # dispatcher.utter_message(text="Por favor, informe um CPF válido (ex: 123.456.789-00).")
       # return {"patient_cpf": None}

    def validate_appointment_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if slot_value:
            try:
                # Tenta converter a data
                date_obj = datetime.strptime(slot_value, "%d/%m/%Y")
                # Verifica se a data não é no passado
                if date_obj.date() >= datetime.now().date():
                    return {"appointment_date": slot_value}
                else:
                    dispatcher.utter_message(text="A data deve ser hoje ou no futuro.")
                    return {"appointment_date": None}
            except ValueError:
                dispatcher.utter_message(text="Por favor, informe a data no formato DD/MM/AAAA.")
                return {"appointment_date": None}
        
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

# class ActionSetHasSymptoms(Action):
#     def name(self) -> str:
#         return "action_set_has_symptoms"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict):

#         # Pega a última intent detectada
#         last_intent = tracker.get_intent_of_latest_message()

#         # Define o valor do slot com base na intent
#         if last_intent == "inform_symptoms":
#             return [SlotSet("has_symptoms", True)]
#         elif last_intent == "deny_symptoms":
#             return [SlotSet("has_symptoms", False)]
#         else:
#             return []

class ActionRecommendSpecialty(Action):
    def name(self) -> Text:
        return "action_recommend_specialty"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        specialty = tracker.get_slot("recommended_specialty")
        
        if specialty:
            dispatcher.utter_message(text=f"Gostaria de agendar uma consulta com {specialty}?")
        
        return []

class ActionCheckAvailability(Action):
    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Simulação de verificação de disponibilidade
        # Em produção, conectar com sistema de agendamento real
        
        specialty = tracker.get_slot("specialty")
        date = tracker.get_slot("appointment_date")
        
        available_times = ["09:00", "10:30", "14:00", "15:30", "16:00"]
        
        message = f"Horários disponíveis para {specialty} no dia {date}:\n"
        for time in available_times:
            message += f"• {time}\n"
        
        dispatcher.utter_message(text=message)
        
        return []

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
            'cpf': tracker.get_slot("patient_cpf"),
            'symptoms': tracker.get_slot("symptoms") or [],
            'specialty': tracker.get_slot("specialty"),
            'date': tracker.get_slot("appointment_date"),
            'time': tracker.get_slot("appointment_time")
        }
        
        # Aqui você salvaria no banco de dados
        # save_appointment_to_database(patient_data)
        
        # Gera resumo com Gemini
        gemini = GeminiIntegration()
        summary = gemini.generate_appointment_summary(patient_data)
        
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

{summary}
        """
        
        dispatcher.utter_message(text=confirmation_message)
        
        return []

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

    def validate_patient_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if slot_value:
            # Remove formatação e verifica se tem pelo menos 10 dígitos
            phone_digits = re.sub(r'\D', '', slot_value)
            if len(phone_digits) >= 10:
                return {"patient_phone": slot_value}
        
        dispatcher.utter_message(text="Por favor, informe um telefone válido (ex: (11) 99999-9999).")
        return {"patient_phone": None}

    def validate_patient_cpf(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if slot_value:
            # Remove formatação
            cpf_digits = re.sub(r'\D', '', slot_value)
            if len(cpf_digits) == 11:
                return {"patient_cpf": slot_value}
        
        dispatcher.utter_message(text="Por favor, informe um CPF válido (ex: 123.456.789-00).")
        return {"patient_cpf": None}

    def validate_appointment_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if slot_value:
            try:
                # Tenta converter a data
                date_obj = datetime.strptime(slot_value, "%d/%m/%Y")
                # Verifica se a data não é no passado
                if date_obj.date() >= datetime.now().date():
                    return {"appointment_date": slot_value}
                else:
                    dispatcher.utter_message(text="A data deve ser hoje ou no futuro.")
                    return {"appointment_date": None}
            except ValueError:
                dispatcher.utter_message(text="Por favor, informe a data no formato DD/MM/AAAA.")
                return {"appointment_date": None}
        
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