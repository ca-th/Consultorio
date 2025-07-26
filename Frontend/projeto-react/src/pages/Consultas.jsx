import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import jsPDF from 'jspdf';
import './Consultas.css';

const Consultas = () => {
  const navigate = useNavigate();
  const [darkTheme, setDarkTheme] = useState(false);
  const [consultas, setConsultas] = useState([]);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setDarkTheme(savedTheme === 'dark');

    const storedConsultas = JSON.parse(localStorage.getItem('consultas')) || [];
    setConsultas(storedConsultas);
  }, []);

  useEffect(() => {
    document.body.classList.toggle('dark-theme', darkTheme);
    localStorage.setItem('theme', darkTheme ? 'dark' : 'light');
  }, [darkTheme]);

  const toggleTheme = () => setDarkTheme((prev) => !prev);

  const handleLogout = () => {
    navigate('/login');
  };

  const gerarPDF = (consulta) => {
    const doc = new jsPDF();
    doc.setFontSize(18);
    doc.text('Confirmação de Consulta', 20, 20);
    doc.setFontSize(12);
    doc.text(`Médico: ${consulta.medico}`, 20, 40);
    doc.text(`Especialidade: ${consulta.especialidade}`, 20, 50);
    doc.text(`Data: ${consulta.data}`, 20, 60);
    doc.text(`Horário: ${consulta.horario}`, 20, 70);
    doc.save(`Consulta-${consulta.id}.pdf`);
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
          {consultas.length === 0 ? (
            <p style={{ color: "" }}>Nenhuma consulta agendada.</p>
          ) : (
            consultas.map((consulta) => (
              <div key={consulta.id} className="consulta-card">
                <div className="card-header">
                  <span className="data">{consulta.data}</span>
                  <span className="horario">{consulta.horario}</span>
                </div>
                <div className="card-body">
                  <h3>{consulta.medico}</h3>
                  <p>{consulta.especialidade}</p>
                  <button className="pdf-button" onClick={() => gerarPDF(consulta)}>
                    Gerar PDF
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Consultas;
