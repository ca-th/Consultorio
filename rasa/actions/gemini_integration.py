import google.generativeai as genai
import os
from typing import List, Dict, Any
import logging
import re

logger = logging.getLogger(__name__)

class GeminiIntegration:
    def __init__(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_symptoms(self, symptoms: List[str]) -> Dict[str, Any]:
        """
        Analisa sintomas e recomenda especialidade médica
        """
        symptoms_text = ", ".join(symptoms)
        
        prompt = f"""
        Você é um assistente médico especializado em triagem de pacientes.
        
        Sintomas relatados: {symptoms_text}
        
        Com base nos sintomas, forneça:
        1. Especialidade médica mais adequada
        2. Urgência (baixa, média, alta, emergência)
        3. Breve explicação da recomendação
        4. Cuidados imediatos se necessário

        Responda em formato JSON (Sem markdown):
        {{
            "specialty": "especialidade",
            "urgency": "nível",
            "explanation": "explicação",
            "immediate_care": "cuidados ou null"
        }}
        """
        logger.debug(f"Sintomas: {symptoms_text}")
        try:
            response = self.model.generate_content(prompt)
            logger.debug(f"Resposta bruta do Gemini: {response}")
            logger.debug(hasattr(response, 'text'))
            logger.debug(response.text)

            if hasattr(response, 'text'):
                response_text = response.text
                logger.debug(f"Conteúdo de response.text '{response_text}'")

                # --- EXTRAÇÃO SEM JSON AQUI ---
                specialty_match = re.search(r"\"specialty\": \"(.*)\"", response_text)
                urgency_match = re.search(r"\"urgency\": \"(.*)\"", response_text)
                explanation_match = re.search(r"\"explanation\": \"(.*)\"", response_text)
                immediate_care_match = re.search(r"\"immediate_care\": \"(.*)\"", response_text)


                analysis_data = {
                    "specialty": specialty_match.group(1).strip() if specialty_match else "Clínico Geral",
                    "urgency": urgency_match.group(1).strip() if urgency_match else "baixa",
                    "explanation": explanation_match.group(1).strip() if explanation_match else "Não foi possível obter uma explicação detalhada no momento.",
                    "immediate_care": immediate_care_match.group(1).strip() if immediate_care_match else "Procure um médico se os sintomas persistirem ou piorarem."
                }
                
                logger.debug(f"Resposta extraída (sem JSON): {analysis_data}")
                return analysis_data

            else:
                logger.error("Gemini não retornou nenhum candidato (texto gerado vazio).")
                if response.prompt_feedback:
                    logger.error(f"Feedback do prompt do Gemini: {response.prompt_feedback.block_reason}")
                    if response.prompt_feedback.safety_ratings:
                        for rating in response.prompt_feedback.safety_ratings:
                            logger.error(f"Segurança: Categoria='{rating.category}', Probabilidade='{rating.probability}'")
                return {}

        except Exception as e:
            print(f"Erro na análise de sintomas: {e}")
            return {
                "specialty": "Indefinida (Erro na IA)",
                "urgency": "baixa",
                "explanation": "Não foi possível analisar seus sintomas com precisão no momento. Por favor, tente descrever de outra forma ou agende uma consulta com um clínico geral.",
                "immediate_care": None
            }
    
    def generate_appointment_summary(self, patient_data: Dict[str, Any]) -> str:
        """
        Gera resumo do agendamento
        """
        prompt = f"""
        Gere um resumo profissional para o agendamento:
        
        Paciente: {patient_data.get('name')}
        Telefone: {patient_data.get('phone')}
        Sintomas: {', '.join(patient_data.get('symptoms', []))}
        Especialidade: {patient_data.get('specialty')}
        Data: {patient_data.get('date')}
        Horário: {patient_data.get('time')}
        
        Crie um resumo em português, profissional e conciso.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erro ao gerar resumo: {e}")
            return f"Consulta agendada para {patient_data.get('name')} em {patient_data.get('date')} às {patient_data.get('time')}"

    def suggest_questions(self, specialty: str) -> List[str]:
        """
        Sugere perguntas específicas para a especialidade
        """
        prompt = f"""
        Para uma consulta de {specialty}, liste 3-5 perguntas importantes 
        que o médico pode fazer ao paciente durante a anamnese.
        
        Responda como uma lista simples, uma pergunta por linha.
        """
        
        try:
            response = self.model.generate_content(prompt)
            questions = response.text.strip().split('\n')
            return [q.strip('- ').strip() for q in questions if q.strip()]
        except Exception as e:
            print(f"Erro ao sugerir perguntas: {e}")
            return []