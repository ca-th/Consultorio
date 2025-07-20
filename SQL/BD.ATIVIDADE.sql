CREATE DATABASE consultorio;

USE consultorio;
CREATE TABLE usuarios ( 
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(20) NOT NULL
); 
CREATE TABLE especialidades (
    id_especialidade INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);
CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_especialidade INT NOT NULL,
    FOREIGN KEY (id_especialidade) REFERENCES especialidades(id_especialidade)
);
CREATE TABLE horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    data_hora DATETIME NOT NULL
);
CREATE TABLE consultas (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_especialidade INT NOT NULL,
    id_medico INT NOT NULL,
    FOREIGN KEY (id_especialidade) REFERENCES especialidades(id_especialidade),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);
CREATE TABLE agendamentos (
    id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
    id_horario INT NOT NULL,
    id_medico INT NOT NULL,
    id_usuario INT NOT NULL,
    UNIQUE (id_horario, id_medico), -- impede conflito de agendamento com o mesmo médico no mesmo horário
    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
CREATE TABLE verificacoes (
    id_verificacao INT AUTO_INCREMENT PRIMARY KEY,
    id_horario INT NOT NULL,
    id_consulta INT NOT NULL,
    id_agendamento INT NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    FOREIGN KEY (id_agendamento) REFERENCES agendamentos(id_agendamento),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
INSERT INTO especialidades (nome) VALUES
('Clínica Geral'),
('Cardiologia'),
('Dermatologia'),
('Pediatria'),
('Ortopedia'),
('Ginecologia'),
('Neurologia');
INSERT INTO medicos (nome, id_especialidade) VALUES
('Dra. Alessandra', 1),  -- Clínica Geral
('Dr. João Cardoso', 2), -- Cardiologia
('Dra. Ana Luiza', 3),    -- Dermatologia
('Dr. Carlos', 4), -- Pediatria
('Dra. Paula Costa', 5), -- Ortopedia
('Dr. Ricardo Alves', 6),-- Ginecologia
('Dra. Luisa Neves', 7); -- Neurologia
INSERT INTO horarios (data_hora) VALUES
('2025-06-10 08:00:00'),
('2025-06-10 09:00:00'),
('2025-06-10 10:00:00'),
('2025-06-11 08:00:00'),
('2025-06-11 09:00:00'),
('2025-06-12 10:00:00'),
('2025-06-13 11:00:00'),
('2025-06-14 14:00:00'),
('2025-06-14 15:00:00'),
('2025-06-14 16:00:00');