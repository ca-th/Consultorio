import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Sobre.css';

export default function Sobre() {
  const [darkTheme, setDarkTheme] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setDarkTheme(savedTheme === 'dark');
  }, []);

  useEffect(() => {
    document.body.classList.toggle('dark-theme', darkTheme);
    localStorage.setItem('theme', darkTheme ? 'dark' : 'light');
  }, [darkTheme]);

  const toggleTheme = () => setDarkTheme(prev => !prev);
  const toggleMobileMenu = () => setMobileMenuOpen(prev => !prev);

  return (
    <div className="home-page">
      <section className="header-section">
        <div className="header-logo">
          <p>Consultório <span>Saúde+</span></p>
        </div>
        <div className="header-nav">
          <div className="mobile-nav-icon" onClick={toggleMobileMenu}>
            <i className={`fa-solid ${mobileMenuOpen ? 'fa-close' : 'fa-bars'}`}></i>
          </div>
          <ul
            className="header-nav-list"
            style={{
              display: mobileMenuOpen ? 'flex' : '',
              transform: mobileMenuOpen ? 'translateX(0)' : ''
            }}
          >
            <li><Link to="/">Home</Link></li>
            <li><Link to="/servicos">Serviços</Link></li>
            <li className="active"><Link to="/sobre">Sobre Nós</Link></li>
            <li><Link to="/contato">Contato</Link></li>
          </ul>
          <div className="theme-change" onClick={toggleTheme}>
            <i className={`fa-solid ${darkTheme ? 'fa-sun' : 'fa-moon'}`}></i>
          </div>
        </div>
      </section>

      <div className="content-container">
        <h2>Sobre o Consultório Saúde+</h2>
        <p>
          Bem-vindo ao <strong>Consultório Saúde+</strong>, seu parceiro dedicado à saúde e bem-estar. Desde a nossa fundação em 2005, temos o compromisso de oferecer atendimento médico de excelência, com foco na atenção humanizada e no cuidado integral dos nossos pacientes.
        </p>
        <p>
          Nossa missão é promover a saúde e a qualidade de vida, por meio de uma equipe multidisciplinar altamente qualificada e tecnologia de ponta. Acreditamos que um ambiente acolhedor e a comunicação clara são essenciais para construir uma relação de confiança com cada pessoa que nos procura.
        </p>

        <h3>Nossos Valores</h3>
        <ul>
          <li><strong>Humanização:</strong> Priorizamos o cuidado empático e respeitoso.</li>
          <li><strong>Excelência:</strong> Buscamos aprimoramento contínuo em todas as áreas.</li>
          <li><strong>Integridade:</strong> Agimos com ética e transparência em todas as nossas condutas.</li>
          <li><strong>Inovação:</strong> Investimos em novas tecnologias e abordagens para um diagnóstico preciso e tratamentos eficazes.</li>
        </ul>
        <p>No Consultório Saúde+, sua saúde é a nossa prioridade. Estamos sempre prontos para recebê-lo e oferecer o melhor cuidado.</p>
      </div>

      
    </div>
  );
}
