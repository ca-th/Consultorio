CREATE DATABASE consultorio;

USE consultorio;
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
CREATE TABLE datas (
    id_data INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL UNIQUE
);
CREATE TABLE horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    hora TIME NOT NULL
);
CREATE TABLE agenda (
    id_agenda INT AUTO_INCREMENT PRIMARY KEY,
    id_medico INT NOT NULL,
    id_data INT NOT NULL,
    id_horario INT NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_data) REFERENCES datas(id_data),
    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
    UNIQUE (id_medico, id_data, id_horario)
);
CREATE TABLE consultas (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_data INT NOT NULL,
    id_horario INT NOT NULL,
    id_especialidade INT NOT NULL,
    id_medico INT NOT NULL,
    motivo_consulta VARCHAR(255) NOT NULL,
    nome_paciente VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_data) REFERENCES datas(id_data),
    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
    FOREIGN KEY (id_especialidade) REFERENCES especialidades(id_especialidade),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
    UNIQUE (id_data, id_horario, id_medico)
);
-- CREATE TABLE agendamentos (
--     id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
--     id_horario INT NOT NULL,
--     id_medico INT NOT NULL,
--     id_usuario INT NOT NULL,
--     UNIQUE (id_horario, id_medico), -- impede conflito de agendamento com o mesmo médico no mesmo horário
--     FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
--     FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
--     FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
-- );
-- CREATE TABLE verificacoes (
--     id_verificacao INT AUTO_INCREMENT PRIMARY KEY,
--     id_horario INT NOT NULL,
--     id_consulta INT NOT NULL,
--     id_agendamento INT NOT NULL,
--     id_usuario INT NOT NULL,
--     FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
--     FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
--     FOREIGN KEY (id_agendamento) REFERENCES agendamentos(id_agendamento),
--     FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
-- );
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
INSERT INTO horarios (hora) VALUES
('08:00:00'),
('09:00:00'),
('10:00:00'),
('11:00:00'),
('13:00:00'),
('14:00:00'),
('15:00:00'),
('16:00:00'),
('17:00:00'),
('18:00:00');
INSERT INTO datas (data) VALUES
('2025-08-01'),
('2025-08-02'),
('2025-08-03'),
('2025-08-04'),
('2025-08-05'),
('2025-08-06'),
('2025-08-07'),
('2025-08-08'),
('2025-08-09'),
('2025-08-10');
-- Inserindo horários na agenda para cada médico com base nas regras especificadas
-- Dra. Alessandra (id = 1): atende até 12h
INSERT INTO agenda (id_medico, id_data, id_horario)
SELECT 1, d.id_data, h.id_horario
FROM datas d
JOIN horarios h ON h.hora <= '12:00:00';

-- Dr. João Cardoso (id = 2): todos os horários, exceto sexta-feira (2025-08-01 e 2025-08-08)
INSERT INTO agenda (id_medico, id_data, id_horario)
SELECT 2, d.id_data, h.id_horario
FROM datas d
JOIN horarios h ON d.data NOT IN ('2025-08-01', '2025-08-08'); -- Excluindo sextas-feiras

-- Dra. Ana Luiza (id = 3): somente horários da tarde
INSERT INTO agenda (id_medico, id_data, id_horario)
SELECT 3, d.id_data, h.id_horario
FROM datas d
JOIN horarios h ON h.hora >= '13:00:00';

-- Dr. Carlos (id = 4): dias pares
INSERT INTO agenda (id_medico, id_data, id_horario)
SELECT 4, d.id_data, h.id_horario
FROM datas d
JOIN horarios h ON DAY(d.data) % 2 = 0;

-- Dra. Paula Costa (id = 5): todos os dias e horários, exceto sábados e domingos
INSERT INTO agenda (id_medico, id_data, id_horario)
SELECT 5, d.id_data, h.id_horario
FROM datas d
JOIN horarios h ON DAYOFWEEK(d.data) NOT IN (1, 7); -- 1 = Domingo, 7 = Sábado

-- Dr. Ricardo Alves (id = 6): apenas segundas e quartas (2025-08-04, 2025-08-06)
INSERT INTO agenda (id_medico, id_data, id_horario)
SELECT 6, d.id_data, h.id_horario
FROM datas d
JOIN horarios h ON d.data IN ('2025-08-04', '2025-08-06'); -- Segundas e quartas

-- Dra. Luisa Neves (id = 7): dias ímpares e até 15h
INSERT INTO agenda (id_medico, id_data, id_horario)
SELECT 7, d.id_data, h.id_horario
FROM datas d
JOIN horarios h ON DAY(d.data) % 2 = 1 AND h.hora <= '15:00:00';