import google.generativeai as genai
import os
from typing import List, Dict, Any
import json

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
        
        Responda em formato JSON:
        {{
            "specialty": "especialidade",
            "urgency": "nível",
            "explanation": "explicação",
            "immediate_care": "cuidados ou null"
        }}
        
        IMPORTANTE: Esta é apenas uma orientação inicial. Sempre consulte um médico.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
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