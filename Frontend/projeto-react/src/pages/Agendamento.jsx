import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Agendamento.css';

const Agendamento = () => {
  const [isChatbotVisible, setIsChatbotVisible] = useState(false);
  const [darkTheme, setDarkTheme] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Bem-vindo(a)! Sou a IA Aura, digite oi para começarmos.", sender: "bot" }
  ]);
  const [userInput, setUserInput] = useState('');
  const [isLoadingResponse, setIsLoadingResponse] = useState(false);
  
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setDarkTheme(savedTheme === 'dark');
  }, []);

  useEffect(() => {
    document.body.classList.toggle('dark-theme', darkTheme);
    localStorage.setItem('theme', darkTheme ? 'dark' : 'light');
  }, [darkTheme]);

  const toggleChatbot = () => setIsChatbotVisible(!isChatbotVisible);
  const closeChatbot = () => setIsChatbotVisible(false);
  const toggleTheme = () => setDarkTheme(prev => !prev);

  const sendMessage = async () => {
    if (userInput.trim() === '') return;

    const newMessage = { text: userInput, sender: "user" };
    setMessages(prev => [...prev, newMessage]);
    setUserInput('');
    setIsLoadingResponse(true);

    try {
      const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sender: "usuario_frontend", // Pode ser um UUID fixo ou gerado por sessão
          message: userInput
        }),
      });

      const data = await response.json();

      if (data.length === 0) {
        setMessages(prev => [...prev, { text: "Desculpe, não entendi sua mensagem.", sender: "bot" }]);
      } else {
        const botMessages = data.map(msg => ({
          text: msg.text || "[resposta vazia]",
          sender: "bot"
        }));
        setMessages(prev => [...prev, ...botMessages]);
      }

    } catch (error) {
      console.error("Erro ao comunicar com o Rasa:", error);
      setMessages(prev => [
        ...prev,
        { text: "Erro ao se comunicar com a IA. Tente novamente mais tarde.", sender: "bot" }
      ]);
    } finally {
      setIsLoadingResponse(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="scheduling-page">
      <div className="top-bar">
        <Link
          to="/dashboard"
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
          {messages.map((msg, index) => (
            <p key={index} className={`text-left ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}>
              <strong>{msg.sender === 'user' ? 'Você: ' : 'Aura IA: '}</strong>{msg.text}
            </p>
          ))}
          {isLoadingResponse && (
            <p className="text-left bot-message">
              <strong>Aura IA: </strong>Digitando...
            </p>
          )}
        </div>

        <div className="chatbot-input">
          <input
            type="text"
            id="userInput"
            placeholder="Digite sua mensagem..."
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoadingResponse}
          />
          <button id="sendButton" onClick={sendMessage} disabled={isLoadingResponse}>
            Enviar
          </button>
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
