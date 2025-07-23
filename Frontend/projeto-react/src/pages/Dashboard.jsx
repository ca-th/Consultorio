import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Aqui você pode limpar tokens, sessões ou dados do localStorage
    // localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>Menu</h2>
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
          <br></br>
          <h3>Atendimento com novos especialistas: Ortopedista, Ginecologista e Neurologista.</h3><br></br>
          <h4>Teremos campanha de vacinação contra gripe disponível de setembro às terças e quintas-feiras!</h4>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;
