import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Site from './pages/Site';
import Servicos from './pages/Servicos';
import Sobre from './pages/Sobre';
import Contato from './pages/Contato';
import Agendamento from './pages/Agendamento';

function App() {
  return (
    <Router>
      

      <Routes>
        <Route path="/" element={<Site />} />
        <Route path="/servicos" element={<Servicos />} />
        <Route path="/sobre" element={<Sobre />} />
        <Route path="/contato" element={<Contato />} />
        <Route path="/agendamento" element={<Agendamento />} />
      </Routes>
    </Router>
  );
}

export default App;