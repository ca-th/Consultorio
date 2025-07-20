// Frontend/src/pages/Agendamento.jsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Agendamento.css';

const Agendamento = () => {
  const [isChatbotVisible, setIsChatbotVisible] = useState(false);
  const [darkTheme, setDarkTheme] = useState(false);
  // --- Novos estados para o chatbot ---
  const [messages, setMessages] = useState([
    { text: "Bem-vindo(a)! Sou a IA Aura, digite oi para começarmos.", sender: "bot" }
  ]);
  const [userInput, setUserInput] = useState('');
  const [isLoadingResponse, setIsLoadingResponse] = useState(false); // Para mostrar carregamento
  // ------------------------------------

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setDarkTheme(savedTheme === 'dark');
  }, []);

  useEffect(() => {
    document.body.classList.toggle('dark-theme', darkTheme);
    localStorage.setItem('theme', darkTheme ? 'dark' : 'light');
  }, [darkTheme]);

  const toggleChatbot = () => {
    setIsChatbotVisible(!isChatbotVisible);
  };

  const closeChatbot = () => {
    setIsChatbotVisible(false);
  };

  const toggleTheme = () => setDarkTheme(prev => !prev);

  // --- Função para enviar mensagem ao backend (API da IA) ---
  const sendMessage = async () => {
    if (userInput.trim() === '') return; // Não envia mensagens vazias

    const newMessage = { text: userInput, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, newMessage]); // Adiciona a mensagem do usuário
    setUserInput(''); // Limpa o input

    setIsLoadingResponse(true); // Começa a mostrar o carregamento

    try {
      // URL do endpoint do seu backend para o chatbot/IA
      // VOCÊ PRECISARÁ ADAPTAR ESTA URL E O CORPO DA REQUISIÇÃO
      // Conforme o endpoint que você tem para interagir com a IA no seu FastAPI.
      // Exemplo: se você tem uma rota @app.post("/chat") que espera um JSON {"message": "..."}
      const response = await fetch('http://127.0.0.1:8000/chat', { // <-- MUDAR PARA SEU ENDPOINT DA IA
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }), // <-- MUDAR SE O SEU ENDPOINT ESPERAR OUTRO FORMATO
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Erro do servidor: ${response.status} - ${errorData.detail || JSON.stringify(errorData)}`);
      }

      const botResponse = await response.json();
      // Assumindo que a resposta do backend vem no formato { "response": "Texto da resposta da IA" }
      const botMessage = { text: botResponse.response || "Não entendi sua mensagem.", sender: "bot" }; // <-- ADAPTAR CONFORME O FORMATO DA RESPOSTA DO SEU BACKEND
      setMessages((prevMessages) => [...prevMessages, botMessage]);

    } catch (error) {
      console.error("Erro ao comunicar com a IA:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Desculpe, houve um erro ao processar sua solicitação. Tente novamente mais tarde.", sender: "bot" }
      ]);
    } finally {
      setIsLoadingResponse(false); // Termina o carregamento
    }
  };

  // Lidar com o Enter no input
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="scheduling-page">
      <div className="top-bar">
        <Link
          to="/"
          className="back-link"
          id="backLink"
          style={{ display: isChatbotVisible ? 'none' : 'flex' }}
        >
          &#8592; Voltar
        </Link>

        <div className="theme-change" onClick={toggleTheme}>
          <i className={`fa-solid ${darkTheme ? 'fa-sun' : 'fa-moon'}`}></i>
        </div>
      </div>

      <div
        className="header"
        id="schedulingHeader"
        style={{ display: isChatbotVisible ? 'none' : 'block' }}
      >
        Bem Vindo(a) ao Agendamento Consultório Saúde +
      </div>

      <div
        className="chatbot-container card"
        id="chatbotContainer"
        style={{ display: isChatbotVisible ? 'flex' : 'none' }}
      >
        <div className="card-header">
          <h3 className="h5 mb-0">Chatbot</h3>
          <button
            className="btn btn-sm btn-danger"
            id="closeChatbot"
            onClick={closeChatbot}
          >
            X
          </button>
        </div>
        <div className="card-body chatbot-body">
          {/* Renderização das mensagens do chat */}
          {messages.map((msg, index) => (
            <p key={index} className={`text-left ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}>
              <strong>{msg.sender === 'user' ? 'Você: ' : 'Aura IA: '}</strong>{msg.text}
            </p>
          ))}
          {isLoadingResponse && <p className="text-left bot-message"><strong>Aura IA: </strong> Digitanto...</p>}
        </div>
        <div className="chatbot-input">
          <input
            type="text"
            id="userInput"
            placeholder="Digite sua mensagem..."
            value={userInput} // Conecta o input ao estado
            onChange={(e) => setUserInput(e.target.value)} // Atualiza o estado ao digitar
            onKeyPress={handleKeyPress} // Chama sendMessage ao pressionar Enter
            disabled={isLoadingResponse} // Desabilita enquanto espera resposta
          />
          <button id="sendButton" onClick={sendMessage} disabled={isLoadingResponse}>Enviar</button>
        </div>
      </div>

      <div
        className="informations"
        id="informationsText"
        style={{ display: isChatbotVisible ? 'none' : 'block' }}
      >
        <section>
          Para iniciarmos, fale em nosso chat clicando no botão começar.
        </section>
      </div>

      <button
        className="magic-button"
        id="magicButton"
        onClick={toggleChatbot}
        style={{ display: isChatbotVisible ? 'none' : 'block' }}
      >
        Começar
      </button>
    </div>
  );
};

export default Agendamento;