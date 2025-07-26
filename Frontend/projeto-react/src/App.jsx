import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Site from './pages/Site';
import Servicos from './pages/Servicos';
import Sobre from './pages/Sobre';
import Contato from './pages/Contato';
import Agendamento from './pages/Agendamento';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Consultas from './pages/Consultas';
import Perfil from './pages/Perfil';
function App() {
  return (
    <Router>
      

      <Routes>
        <Route path="/" element={<Site />} />
        <Route path="/servicos" element={<Servicos />} />
        <Route path="/sobre" element={<Sobre />} />
        <Route path="/contato" element={<Contato />} />
        <Route path="/agendamento" element={<Agendamento />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="consultas" element={<Consultas />} />
        <Route path="/perfil" element={<Perfil />} />
      </Routes>
    </Router>
  );
}

export default App;