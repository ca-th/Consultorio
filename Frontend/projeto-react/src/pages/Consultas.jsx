import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Consultas.css';

const consultas = [
  {
    id: 1,
    data: '25/07/2025',
    horario: '14:30',
    medico: 'Dra. Juliana Almeida',
    especialidade: 'Ginecologia',
  },
  {
    id: 2,
    data: '26/07/2025',
    horario: '09:00',
    medico: 'Dr. Carlos Moreira',
    especialidade: 'Ortopedia',
  },
  {
    id: 3,
    data: '27/07/2025',
    horario: '16:00',
    medico: 'Dra. Fabiana Lopes',
    especialidade: 'Neurologia',
  },
];

const Consultas = () => {
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

  const toggleTheme = () => setDarkTheme((prev) => !prev);

  const handleLogout = () => {
    // Exemplo: localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="card-dashboard">
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


        <div className="container-card">

        
        <div className="cards-wrapper">
        {consultas.map((consulta) => (
            <div key={consulta.id} className="consulta-card">
            <div className="card-header">
                <span className="data">{consulta.data}</span>
                <span className="horario">{consulta.horario}</span>
            </div>
            <div className="card-body">
                <h3>{consulta.medico}</h3>
                <p>{consulta.especialidade}</p>
            </div>
            </div>
        ))}
        </div>
        </div>
        

    </div>
  );
};

export default Consultas;
