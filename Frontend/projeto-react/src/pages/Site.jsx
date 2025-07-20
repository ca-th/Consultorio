import React, { useEffect, useState } from 'react';
import './Site.css';
import { Link } from 'react-router-dom';
import Imagem from '../assets/img/ImagemExemploConsultorio.jpg';

export default function Site() {
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
            <li className="active"><Link to="/">Home</Link></li>
            <li><Link to="/servicos">Serviços</Link></li>
            <li><Link to="/sobre">Sobre</Link></li>
             <li><Link to="/contato">Contato</Link></li>
          </ul>
          <div className="theme-change" onClick={toggleTheme}>
            <i className={`fa-solid ${darkTheme ? 'fa-sun' : 'fa-moon'}`}></i>
          </div>
        </div>
      </section>

      <section className="hero-section">
        <div className="hero-content">
          <p className="content-header">
            Bem-vindo(a)
          </p>
          <p className="content-body">
            Nós somos o Consulta Saúde+ fundado desde 2025.
            <br /><span>Fazemos atendimentos de segunda a sexta, das 8h às 18h, e aos sábados, das 8h às 12h.</span>
            <br /><span>Deseja agendar uma consulta? Clique no botão abaixo.</span>
          </p>
          <div className="hero-btn">
            <Link to="/agendamento">
              <button className="resume-btn">Agende sua Consulta</button>
            </Link>
          </div>
        </div>

        <div className="hero-image">
          <img src={Imagem} alt="Imagem do Consultório Médico" className="main-img protected-image" />
        </div>

        
      </section>
    </div>
  );
}
