-- schema.sql
-- Estrutura do banco de dados para Oficina Mecânica

CREATE TABLE Cliente (
  id_cliente INT PRIMARY KEY,
  nome VARCHAR(100),
  telefone VARCHAR(20),
  email VARCHAR(100)
);

CREATE TABLE Veiculo (
  id_veiculo INT PRIMARY KEY,
  placa VARCHAR(10),
  modelo VARCHAR(50),
  ano INT,
  id_cliente INT,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);

CREATE TABLE Funcionario (
  id_funcionario INT PRIMARY KEY,
  nome VARCHAR(100),
  funcao VARCHAR(50)
);

CREATE TABLE Servico (
  id_servico INT PRIMARY KEY,
  descricao VARCHAR(100),
  valor DECIMAL(10,2)
);

CREATE TABLE Peca (
  id_peca INT PRIMARY KEY,
  nome VARCHAR(100),
  quantidade_estoque INT,
  valor_unitario DECIMAL(10,2)
);

CREATE TABLE Ordem_Servico (
  id_ordem INT PRIMARY KEY,
  data DATE,
  id_cliente INT,
  id_veiculo INT,
  id_funcionario INT,
  valor_total DECIMAL(10,2),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  FOREIGN KEY (id_veiculo) REFERENCES Veiculo(id_veiculo),
  FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario)
);

CREATE TABLE Ordem_Servico_Servico (
  id_ordem INT,
  id_servico INT,
  quantidade INT,
  PRIMARY KEY (id_ordem, id_servico),
  FOREIGN KEY (id_ordem) REFERENCES Ordem_Servico(id_ordem),
  FOREIGN KEY (id_servico) REFERENCES Servico(id_servico)
);

CREATE TABLE Ordem_Servico_Peca (
  id_ordem INT,
  id_peca INT,
  quantidade INT,
  PRIMARY KEY (id_ordem, id_peca),
  FOREIGN KEY (id_ordem) REFERENCES Ordem_Servico(id_ordem),
  FOREIGN KEY (id_peca) REFERENCES Peca(id_peca)
);
