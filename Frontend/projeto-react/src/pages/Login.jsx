import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
  const [cpf, setCpf] = useState('');
  const [senha, setSenha] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const themeChangeIcon = document.getElementById("themeChangeIcon");

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

    themeChangeIcon.addEventListener('click', handleThemeChange);

    return () => {
      themeChangeIcon.removeEventListener('click', handleThemeChange);
    };
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    // Simulação de login
    if (cpf === '12345678900' && senha === '1234') {
      alert('Login efetuado!');
      navigate('/dashboard');
    } else {
      alert('CPF ou senha inválidos!');
    }
  };

  return (
    <div className="login-page">

      <div className="login-container">
        <form onSubmit={handleLogin}>
          <div className="theme-change">
            <i className="fa-solid fa-moon" id="themeChangeIcon"></i>
          </div>
          <div className="back-button">
            <Link to="/">
              <i className="fa-solid fa-arrow-left"></i>
            </Link>
            </div>
          <h2>Login</h2>

          <div className="input-group">
            <label htmlFor="cpf">CPF</label>
            <input
              type="text"
              id="cpf"
              placeholder="Digite seu CPF"
              value={cpf}
              onChange={(e) => setCpf(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="senha">Senha</label>
            <input
              type="password"
              id="senha"
              placeholder="Digite sua senha"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
            />
          </div>

          <button type="login">Entrar</button>

        </form>
      </div>
    </div>
  );
};

export default Login;
