import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();

  const [darkTheme, setDarkTheme] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setDarkTheme(savedTheme === 'dark');
  }, []);

  useEffect(() => {
    document.body.classList.toggle('dark-theme', darkTheme);
    localStorage.setItem('theme', darkTheme ? 'dark' : 'light');
  }, [darkTheme]);

  const toggleTheme = () => setDarkTheme(prev => !prev);

  const handleLogout = () => {
    // Exemplo: localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>Menu</h2>

        <div className="theme-change" onClick={toggleTheme}>
          <i className={`fa-solid ${darkTheme ? 'fa-sun' : 'fa-moon'}`}></i>
        </div>

        <nav>
          <ul>
            <li><Link to="/perfil">Perfil</Link></li>
            <li><Link to="/consultas">Consultas</Link></li>
            <li><Link to="/agendamento">Agendamento</Link></li>
            <li>
              <button 
                onClick={handleLogout} 
                type="button"
                aria-label="Fazer logout"
                className="logout-button"
              >
                Logout
              </button>
            </li>
          </ul>
        </nav>
      </aside>

      <main className="content">
        <h1>Bem-vindo ao Consultório Saúde+</h1>
        <section className="noticias">
          <h2>Notícias do consultório</h2>
          <br />
          <h3>Atendimento com novos especialistas: Ortopedista, Ginecologista e Neurologista.</h3>
          <br />
          <h4>Teremos campanha de vacinação contra gripe disponível de setembro às terças e quintas-feiras!</h4>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;
