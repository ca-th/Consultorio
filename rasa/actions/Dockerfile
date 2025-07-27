# actions/Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

# Copia os requisitos das suas ações personalizadas
# Certifique-se de ter um arquivo 'requirements-actions.txt' dentro da pasta 'actions/'
COPY requirements-actions.txt .

# Instala as dependências das ações personalizadas
RUN pip install --no-cache-dir -r requirements-actions.txt

# Copia todos os seus arquivos de ações personalizadas
COPY . /app

EXPOSE 5055

CMD ["rasa", "run", "actions", "--port", "5055"]