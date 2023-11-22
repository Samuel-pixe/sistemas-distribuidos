CREATE DATABASE hotel_db;

CREATE TABLE tb_usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL
);

CREATE TABLE tb_quartos (
    id_quarto INT AUTO_INCREMENT PRIMARY KEY,
    numero_quarto INT NOT NULL,
    tipo_quarto VARCHAR(50) NOT NULL,
    preco_diaria DECIMAL(10, 2) NOT NULL
);

CREATE TABLE tb_reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_quarto INT,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    nome_cliente VARCHAR(100) NOT NULL
);


INSERT INTO tb_quartos (numero_quarto, tipo_quarto, preco_diaria)
VALUES
    (101, 'standard', 100.00),
    (102, 'standard', 100.00),
    (201, 'luxo', 150.00),
    (202, 'luxo', 150.00),
    (301, 'suíte', 200.00),
    (302, 'suíte', 200.00),
    (401, 'standard', 100.00),
    (402, 'standard', 100.00),
    (501, 'luxo', 150.00),
    (502, 'luxo', 150.00);



