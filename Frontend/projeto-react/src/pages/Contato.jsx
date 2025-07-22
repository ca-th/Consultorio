// Frontend/src/pages/Contato.jsx

import React, { useState, useEffect } from 'react'; // Keep useState for form data
import { Link } from 'react-router-dom';
import './Contato.css';

const Contato = () => {
    // --- Existing useEffect for theme and mobile nav (retained as you had it) ---
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

        themeChangeIcon.addEventListener('click', () => {
            let theme = 'light';
            if (document.body.classList.toggle('dark-theme')) {
                theme = 'dark';
                themeChangeIcon.classList.replace('fa-moon', 'fa-sun');
            } else {
                themeChangeIcon.classList.replace('fa-sun', 'fa-moon');
            }
            localStorage.setItem('theme', theme);
        });

        mobileNavIcon.addEventListener('click', () => {
            if (mobileNavIcon.classList.contains("fa-bars")) {
                mobileNavIcon.classList.replace("fa-bars", "fa-times"); // Changed 'fa-close' to 'fa-times' for consistency with common FontAwesome usage
                headerNavList.style.display = "flex";
                headerNavList.style.transform = "translateX(0)";
            } else {
                mobileNavIcon.classList.replace("fa-times", "fa-bars");
                headerNavList.style.display = "none";
                headerNavList.style.transform = "translateX(200%)";
            }
        });

        // Cleanup event listeners when component unmounts
        return () => {
            themeChangeIcon.removeEventListener('click', () => {}); // Needs proper reference for removal
            mobileNavIcon.removeEventListener('click', () => {}); // Needs proper reference for removal
        };
    }, []);
    // --------------------------------------------------------------------------

    // --- NEW: States for form data and submission status ---
    const [formData, setFormData] = useState({
        nome: '',
        email: '',
        assunto: '',
        mensagem: ''
    });
    const [submissionStatus, setSubmissionStatus] = useState(null); // 'success', 'error', 'loading'
    // -------------------------------------------------------

    // --- NEW: Handle input changes ---
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };
    // ---------------------------------

    // --- NEW: Handle form submission ---
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent page reload
        setSubmissionStatus('loading'); // Set loading state

        try {
            const response = await fetch('http://127.0.0.1:8000/contato', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData), // Send form data from state
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Erro ao enviar mensagem: ${response.status} - ${errorData.detail || JSON.stringify(errorData)}`);
            }

            setSubmissionStatus('success');
            setFormData({ // Clear form after success
                nome: '',
                email: '',
                assunto: '',
                mensagem: ''
            });
        } catch (error) {
            console.error('Erro ao enviar formulário de contato:', error);
            setSubmissionStatus('error');
        }
    };
    // -----------------------------------

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
                        <li><Link to="/servicos">Serviços</Link></li>
                        <li><Link to="/sobre">Sobre Nós</Link></li>
                        <li className="active"><Link to="/contato">Contato</Link></li>
                    </ul>
                    <div className="theme-change">
                        <i className="fa-solid fa-moon" id="themeChangeIcon"></i>
                    </div>
                </div>
            </section>

            <div className="content-container">
                <h2>Entre em Contato</h2>
                <p>Tem alguma dúvida ou gostaria de agendar uma consulta? Preencha o formulário abaixo ou utilize nossos canais de contato direto.</p>

                <section id="contact-info" className="mb-4">
                    <ul>
                        <li><i className="fas fa-map-marker-alt"></i> Endereço: Rua da Saúde, 123 - Centro, Cidade, Brasil</li>
                        <li><i className="fas fa-phone"></i> Telefone: (61) 9986-54583</li>
                        <li><i className="fas fa-envelope"></i> Email: contato@consultoriosaude.com.br</li>
                        <li><i className='fas fa-clock'></i> Segunda a Sexta, das 8h às 18h, e aos sábados, das 8h às 12h.</li>
                    </ul>
                </section>

                <section id="contact-form-section" className="contact-form">
                    <form onSubmit={handleSubmit}> {/* Added onSubmit event */}
                        <div className="form-group">
                            <label htmlFor="nome">Seu Nome:</label>
                            <input
                                type="text"
                                id="nome"
                                name="nome" // IMPORTANT: Match with backend schema
                                value={formData.nome} // Control the input with state
                                onChange={handleChange} // Update state on change
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="email">Seu E-mail:</label>
                            <input
                                type="email"
                                id="email"
                                name="email" // IMPORTANT: Match with backend schema
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="assunto">Assunto:</label>
                            <input
                                type="text"
                                id="assunto"
                                name="assunto" // IMPORTANT: Match with backend schema
                                value={formData.assunto}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="mensagem">Sua Mensagem:</label>
                            <textarea
                                id="mensagem"
                                name="mensagem" // IMPORTANT: Match with backend schema
                                value={formData.mensagem}
                                onChange={handleChange}
                                required
                            ></textarea>
                        </div>
                        <button type="submit" disabled={submissionStatus === 'loading'}>
                            {submissionStatus === 'loading' ? 'Enviando...' : 'Enviar Mensagem'}
                        </button>

                        {/* NEW: Display submission status messages */}
                        {submissionStatus === 'success' && (
                            <p className="success-message">Mensagem enviada com sucesso! Entraremos em contato em breve.</p>
                        )}
                        {submissionStatus === 'error' && (
                            <p className="error-message">Houve um erro ao enviar sua mensagem. Por favor, tente novamente.</p>
                        )}
                    </form>
                </section>
            </div>
        </div>
    );
};

export default Contato;