import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Servicos.css';

const Servicos = () => {
    useEffect(() => {
        const themeChangeIcon = document.getElementById("themeChangeIcon");
        const mobileNavIcon = document.getElementById("mobileNavIcon");
        const headerNavList = document.getElementById("headerNavList");

        const applyTheme = (theme) => {
            if (theme === 'dark') {
                document.body.classList.add('dark-theme');
                themeChangeIcon.classList.replace('fa-moon', 'fa-sun');
            } else {
                document.body.classList.remove('dark-theme');
                themeChangeIcon.classList.replace('fa-sun', 'fa-moon');
            }
        };

        const savedTheme = localStorage.getItem('theme') || 'light';
        applyTheme(savedTheme);

        const handleThemeChange = () => {
            let theme = 'light';
            if (document.body.classList.toggle('dark-theme')) {
                theme = 'dark';
                themeChangeIcon.classList.replace('fa-moon', 'fa-sun');
            } else {
                themeChangeIcon.classList.replace('fa-sun', 'fa-moon');
            }
            localStorage.setItem('theme', theme);
        };

        const handleMobileNavToggle = () => {
            if (mobileNavIcon.classList.contains("fa-bars")) {
                mobileNavIcon.classList.replace("fa-bars", "fa-close");
                headerNavList.style.display = "flex";
                headerNavList.style.transform = "translateX(0)";
            } else {
                mobileNavIcon.classList.replace("fa-close", "fa-bars");
                headerNavList.style.display = "none";
                headerNavList.style.transform = "translateX(200%)";
            }
        };

        themeChangeIcon.addEventListener('click', handleThemeChange);
        mobileNavIcon.addEventListener('click', handleMobileNavToggle);

        return () => {
            themeChangeIcon.removeEventListener('click', handleThemeChange);
            mobileNavIcon.removeEventListener('click', handleMobileNavToggle);
        };
    }, []);

    return (
        <div className="home-page">
            <section className="header-section">
                <div className="header-logo">
                    <p>Consultório <span>Saúde+</span></p>
                </div>
                <div className="header-nav">
                    <div className="mobile-nav-icon">
                        <i className="fa-solid fa-bars" id="mobileNavIcon"></i>
                    </div>
                    <ul className="header-nav-list" id="headerNavList">
                        <li><Link to="/">Home</Link></li>
                        <li className="active"><Link to="/servicos">Serviços</Link></li>
                        <li><Link to="/sobre">Sobre Nós</Link></li>
                        <li><Link to="/contato">Contato</Link></li>
                    </ul>
                    <div className="theme-change">
                        <i className="fa-solid fa-moon" id="themeChangeIcon"></i>
                    </div>
                </div>
            </section>

            <div className="content-container">
                <section id="our-services" className="mb-4">
                    <h2>Nossos Serviços</h2>
                    <p>Oferecemos uma variedade de serviços médicos para atender suas necessidades:</p>
                    <ul>
                        <li>Consulta Geral - Dr. João Silva</li>
                        <li>Pediatria - Dra. Maria Oliveira</li>
                        <li>Cardiologia - Dr. Carlos Mendes</li>
                        <li>Dermatologia - Dra. Ana Souza</li>
                    </ul>
                </section>

                <section id="service-hours" className="mb-4">
                    <h2>Serviços e Horários</h2>
                    <p>Confira nossos serviços e horários de funcionamento:</p>
                    <ul>
                        <li>Dr. João Silva (Consulta Geral) - Segunda a Sexta: 8h às 12h</li>
                        <li>Dra. Maria Oliveira (Pediatria) - Segunda a Sexta: 13h às 17h</li>
                        <li>Dr. Carlos Mendes (Cardiologia) - Terça e Quinta: 9h às 15h</li>
                        <li>Dra. Ana Souza (Dermatologia) - Quarta e Sexta: 10h às 16h</li>
                    </ul>
                </section>
            </div>
        </div>
    );
};

export default Servicos;
