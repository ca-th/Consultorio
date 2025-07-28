# Sistema de Agendamento Médico

## Descrição do Projeto

Sistema completo de agendamento médico desenvolvido para facilitar o gerenciamento de consultas, especialidades e atendimentos. A aplicação integra um chatbot inteligente para melhorar a experiência do usuário e automatizar processos de agendamento.

## Tecnologias Utilizadas

- **Backend**: Python com CRUD de atendimentos, especialidades e médicos
- **Integração**: FastApi
- **Chatbot**: Sistema de diálogo inteligente com fluxo personalizado com Rasa
- **Banco de Dados**: MySQL para modelagem e armazenamento de dados
- **Frontend**: React e CSS
- **Componentes**: Interfaces de chat e telas de agendamento responsivas

## Arquitetura do Sistema

### Backend API (Python)
Sistema robusto de gerenciamento com endpoints para:
- Gestão de atendimentos
- Cadastro de especialidades médicas
- Controle de médicos e profissionais

### Chatbot Inteligente
- Fluxo de diálogo automatizado
- Processamento de linguagem natural para agendamentos
- Interface conversacional intuitiva

### Banco de Dados
- DB em MySQL

### Interface Frontend React
- Design responsivo com CSS
- Integração com API backend
- Telas de agendamento intuitivas
- Sistema de chat em tempo real

## Grupo

### Backend - Catharina
**Responsabilidades:**
- Desenvolvimento da API backend em Python
- Implementação do CRUD de atendimentos
- Gestão de especialidades e médicos
- Arquitetura e estruturação do sistema

### Chatbot IA - Catharina, Darla, Gustavo e Luciana
**Responsabilidades:**
- Implementação do chatbot
- Fluxo de diálogo para agendamento
- Análise comportamental da IA

### Banco de Dados - Luciana
**Responsabilidades:**
- Modelagem do banco de dados
- Configuração do MySQL
- Desenvolvimento e criação de Querys

### Frontend - Gustavo, Rebeca e Darla
**Responsabilidades:**
- Desenvolvimento da interface em React
- Implementação de componentes de chat
- Criação de telas de agendamento
- Estilização com CSS

### Documentação - Rebeca
**Responsabilidades:**
- Criação da documentação técnica
- Criação do Readme

## Funcionalidades Principais

- Agendamento de consultas via chat
- Gerenciamento de especialidades médicas
- Cadastro e controle de profissionais
- Interface responsiva e moderna

## Instalação e Configuração

```bash
# Clone o repositório
git clone [url-do-repositorio]

# Backend (Python)
cd Consultorio
pip install uvicorn
criar a maquina: python -m venv venv
ativar o ven: source venv/Scripts/active(no git bash), venv\Scripts\activate.bat(cmd) 
instalar os pacotes: pip install -r requirements.txt
ao ativar o ven, usar o comando de instalação novamente: pip install uvicorn
executar: uvicorn main:app --reload ou uvicorn Backend.main:app --reload (recomendado)
Se der erro, saia da pasta Backend e rode algum dos comandos de executar novamente

# Frontend (React)
cd Consultorio
cd frontend
cd projeto-react
npm install (se for necessário)
npm install react-router-dom
npm start

# Banco de Dados
# Configure as credenciais MySQL
# Execute os scripts de SQL

# Instalação do Rasa 

cd rasa

# Crie um ambiente virtual
python -m venv venv_py

# Ative o ambiente virtual
.\venv\Scripts\activate ou source venv_py/Scripts/activate(recomendado)

#Instalação das Bibilotecas
pip install rasa google-generativeai pytz regex 

# Atualize o pip pra versão mais recente
python -m pip install --upgrade pip

#Rodar o rasa
python -m rasa train

# Ative a licença (vc tem que criar uma)
# macOS e Linux
export GEMINI_PRO_LICENSE=YOUR_LICENSE_KEY

# Windows
set GEMINI_PRO_LICENSE=YOUR_LICENSE_KEY

# Quando finalizar o treinamento, rode o comando:
rasa shell (onde vai abrir o chat)

# Por fim, abre outro terminal, entre na pasta rasa e ative o ambiente e rode o comando:
rasa run actions (criar um ambiente separado: python -m venv .venv-core, source .venv-core/Scripts/activate,  python -m pip install --upgrade pip. ai roda o comando)

##IMPORTANTE: 

##Não feche nenhum dos terminais enquanto estiver conversando com o bot. O primeiro terminal (rasa shell) é a sua interface de chat, e o segundo (rasa run actions) é o servidor que executa as ações personalizadas (como a interação com a LLM e o formulário de agendamento).

##Para fechar, use Ctrl+C em ambos os terminais.
