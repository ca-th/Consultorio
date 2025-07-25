import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Dashboard.css';

const noticias = [
  {
    id: 1,
    titulo: 'Novos especialistas disponíveis!',
    descricao: 'Atendimento com Proctologista, Otorrino, Obstetrísta e Alergista já disponível.',
  },
  {
    id: 2,
    titulo: 'Vacinação contra a gripe',
    descricao: 'Disponível às terças e quintas a partir de setembro.',
  },
  {
    id: 3,
    titulo: 'Como está a sua Saúde Mental? (10 de agosto às 18h)',
    descricao: 'Palestra com Dra. Camila Vieira',
  },
  {
    id: 4,
    titulo: 'Atenção!',
    descricao: 'Agora fazemos agendamento pelo portal.',
  },
  {
    id: 5,
    titulo: 'Mês da Saúde',
    descricao: 'Check-ups preventivos com descontos especiais em outubro.',
  },
  {
    id: 6,
    titulo: 'Evento de Bem-Estar (20/08 às 8:00)',
    descricao: 'Venha participar deste evento, onde teremos: Meditação, fisioterapia e nutrição. Venha e participe!',
  },
];

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
          <div className="cards-container">
            {noticias.map(noticia => (
              <div key={noticia.id} className="card-noticia">
                <div className="icone">{noticia.icone}</div>
                <h3>{noticia.titulo}</h3>
                <p>{noticia.descricao}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;
