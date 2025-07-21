import google.generativeai as genai

genai.configure(api_key='AIzaSyA-enVCB7JUblq5a734bKLQKEue6Elf0t0')
model = genai.GenerativeModel('gemini-2.5-flash')

def prompt_formatado(prompt):
    return f"""
    Você é um assistente virtual especializado em responder perguntas de forma clara e concisa.
    Nós somos o Consulta Saúde+ fundado desde 2025.
    Fazemos atendimentos de segunda a sexta, das 8h às 18h, e aos sábados, das 8h às 12h.
    Oferecemos uma variedade de serviços médicos para atender suas necessidades:
    Consulta Geral - Dr. João Silva
    Pediatria - Dra. Maria Oliveira
    Cardiologia - Dr. Carlos Mendes
    Dermatologia - Dra. Ana Souza
    Pergunta: {prompt}
    """

while True:
    pergunta = input()
    response = model.generate_content(prompt_formatado(pergunta))
    print(response.text)


