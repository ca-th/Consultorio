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
cd projeto-IA-final (duas vezes)
cd Backend
pip install uvicorn
ativar o ven: source venv/Scripts/active(no git bash)
ao ativar o ven, usar o comando de instalação novamente: pip install uvicorn
executar: uvicorn main:app --reload ou uvicorn Backend.main:app --reload (recomendado)
Se der erro, saia da pasta Backend e rode algum dos comandos de executar novamente
# Frontend (React)
cd projeto-IA-final (duas vezes)
cd frontend
cd projeto-react
npm install (se for necessário)
npm install react-router-dom
npm start

# Banco de Dados
# Configure as credenciais MySQL
# Execute os scripts de SQL

# Instalação do Rasa Pro

cd rasa

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
.\venv\Scripts\activate

# Instale o package manager do uv
# macOS e Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Instale o uv
pip install uv

# Atualize o pip pra versão mais recente
python -m pip install --upgrade pip

# Instale o Rasa Pro
uv pip install rasa-pro

# Crie um ambiente virtual
python -m venv venv

# Ative a licença do Rasa Pro (O Hash está no arquivo .env na pasta rasa)
# macOS e Linux
export RASA_PRO_LICENSE=YOUR_LICENSE_KEY

# Windows
set RASA_PRO_LICENSE=YOUR_LICENSE_KEY

# Verifique a instalação
rasa --version