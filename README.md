<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1F9BD4,50:2E75B6,100:16265F&height=200&section=header&text=Modelagem%20—%20Oficina%20Mecânica&fontSize=42&fontColor=ffffff&fontAlignY=38&desc=ER%20→%20Lógica%20→%20Física%20→%20Dados%20→%20Consultas&descAlignY=58&descSize=18" width="100%"/>

[![SQL](https://img.shields.io/badge/SQL-Modelagem%20Relacional-003B57?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

[![SQL](https://img.shields.io/badge/SQL-003B57?style=flat-square&logo=postgresql&logoColor=white)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![ER Diagram](https://img.shields.io/badge/ER%20Diagram-Incluído-green?style=flat-square)](https://github.com/fassir)
[![Faker](https://img.shields.io/badge/Faker-Dados%20Sintéticos-9C27B0?style=flat-square)](https://faker.readthedocs.io/)

</div>

---

## 🎯 Sobre o Projeto

Banco de dados relacional completo para uma **oficina mecânica**, desenvolvido do zero seguindo todas as etapas da engenharia de dados: modelagem ER → modelo lógico → modelo físico (DDL) → inserção de dados → consultas analíticas. Inclui diagrama ER, scripts SQL e gerador de dados sintéticos em Python.

---

## 🗂️ Estrutura do Repositório

```
projeto_modelagem_dados_2/
├── diagrama_er.png / diagrama_er.pdf   # Diagrama Entidade-Relacionamento
├── schema.sql                           # DDL — modelo físico completo
├── data.sql                             # DML — dados de exemplo
├── query.sql                            # Consultas analíticas
├── gerador_de_dados.py                  # Gerador de dados sintéticos
└── README.md
```

---

## 🔄 Etapas do Projeto

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  1. Modelo   │───▶│  2. Modelo   │───▶│  3. Modelo   │
│     ER       │    │    Lógico    │    │    Físico    │
│ (entidades,  │    │ (tabelas,    │    │ (DDL SQL,    │
│  relações)   │    │  atributos,  │    │  constraints,│
│              │    │  chaves)     │    │  índices)    │
└──────────────┘    └──────────────┘    └──────┬───────┘
                                               │
                    ┌──────────────┐    ┌──────▼───────┐
                    │  5. Consul-  │◀───│  4. Inserção │
                    │  tas (query) │    │  de Dados    │
                    │              │    │  (data.sql + │
                    │              │    │  gerador.py) │
                    └──────────────┘    └──────────────┘
```

---

## 🧩 Diagrama ER

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Cliente   │─────────│    Veículo   │─────────│    OS       │
│             │  possui │              │  possui │ (Ordem de   │
│ ClienteID   │         │  VeiculoID   │         │  Serviço)   │
│ Nome        │         │  Placa       │         │ OSID        │
│ CPF/CNPJ    │         │  Modelo      │         │ DataAbertura│
│ Telefone    │         │  Ano         │         │ DataFechamento│
│ Endereco    │         │  Marca       │         │ Status      │
└─────────────┘         └──────────────┘         │ ValorTotal  │
                                                  └──────┬──────┘
                                                         │
                              ┌──────────────────────────┤
                              │                          │
                     ┌────────▼──────┐         ┌────────▼──────┐
                     │  OS_Servico   │         │   OS_Peca     │
                     │  (N:N)        │         │   (N:N)       │
                     └───────┬───────┘         └───────┬───────┘
                             │                         │
                    ┌────────▼──────┐         ┌────────▼──────┐
                    │   Serviço     │         │     Peça      │
                    │               │         │               │
                    │ ServicoID     │         │ PecaID        │
                    │ Descricao     │         │ Nome          │
                    │ Valor         │         │ Codigo        │
                    │ Duracao_h     │         │ Preco         │
                    └───────────────┘         │ Estoque_qtd   │
                                              └───────────────┘
                    ┌────────────────┐
                    │  Funcionário   │──────────── (responsável pela OS)
                    │                │
                    │ FuncID         │
                    │ Nome           │
                    │ Especialidade  │
                    │ Salario        │
                    └────────────────┘
```

---

## 📐 Modelo Físico (schema.sql)

<details>
<summary><strong>🗄️ DDL — Tabelas principais</strong></summary>

```sql
CREATE TABLE Cliente (
    ClienteID   INT          PRIMARY KEY AUTO_INCREMENT,
    Nome        VARCHAR(100) NOT NULL,
    Documento   VARCHAR(18)  UNIQUE NOT NULL,  -- CPF ou CNPJ
    Tipo        ENUM('PF','PJ') NOT NULL,
    Telefone    VARCHAR(20),
    Email       VARCHAR(100),
    Endereco    VARCHAR(200)
);

CREATE TABLE Veiculo (
    VeiculoID   INT          PRIMARY KEY AUTO_INCREMENT,
    ClienteID   INT          NOT NULL,
    Placa       CHAR(8)      UNIQUE NOT NULL,
    Marca       VARCHAR(50)  NOT NULL,
    Modelo      VARCHAR(100) NOT NULL,
    Ano         YEAR         NOT NULL,
    Cor         VARCHAR(30),
    Quilometragem INT,
    FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID)
);

CREATE TABLE OrdemServico (
    OSID            INT         PRIMARY KEY AUTO_INCREMENT,
    VeiculoID       INT         NOT NULL,
    FuncionarioID   INT         NOT NULL,
    DataAbertura    DATETIME    DEFAULT CURRENT_TIMESTAMP,
    DataFechamento  DATETIME,
    Status          ENUM('aberta','em_andamento','aguardando_peca',
                         'pronta','entregue','cancelada') DEFAULT 'aberta',
    Descricao       TEXT,
    ValorTotal      DECIMAL(10,2),
    FOREIGN KEY (VeiculoID)     REFERENCES Veiculo(VeiculoID),
    FOREIGN KEY (FuncionarioID) REFERENCES Funcionario(FuncID)
);
```

</details>

<details>
<summary><strong>🔗 Tabelas associativas (N:N)</strong></summary>

```sql
-- OS × Serviço (N:N)
CREATE TABLE OS_Servico (
    OSID        INT     NOT NULL,
    ServicoID   INT     NOT NULL,
    Quantidade  INT     NOT NULL DEFAULT 1,
    ValorCobrado DECIMAL(10,2),
    PRIMARY KEY (OSID, ServicoID),
    FOREIGN KEY (OSID)      REFERENCES OrdemServico(OSID),
    FOREIGN KEY (ServicoID) REFERENCES Servico(ServicoID)
);

-- OS × Peça (N:N)
CREATE TABLE OS_Peca (
    OSID        INT     NOT NULL,
    PecaID      INT     NOT NULL,
    Quantidade  INT     NOT NULL DEFAULT 1,
    ValorUnit   DECIMAL(10,2),
    PRIMARY KEY (OSID, PecaID),
    FOREIGN KEY (OSID)   REFERENCES OrdemServico(OSID),
    FOREIGN KEY (PecaID) REFERENCES Peca(PecaID)
);
```

</details>

---

## 💡 Tecnologias

<div align="center">

[![My Skills](https://skillicons.dev/icons?i=mysql,python&theme=dark)](https://mysql.com/)

</div>

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| MySQL | 8.0 | Banco de dados relacional |
| SQL DDL/DML | — | Schema, constraints, inserção |
| Python | 3.10+ | Gerador de dados sintéticos |
| Faker (pt_BR) | 18+ | Dados realistas em português |
| draw.io / dbdiagram.io | — | Diagrama ER |

---

## 🔍 Consultas Analíticas (query.sql)

<details>
<summary><strong>📊 Consultas implementadas</strong></summary>

```sql
-- OSes abertas por mecânico
SELECT f.Nome AS mecanico, COUNT(os.OSID) AS ordens_abertas
FROM Funcionario f
JOIN OrdemServico os ON os.FuncionarioID = f.FuncID
WHERE os.Status IN ('aberta', 'em_andamento')
GROUP BY f.FuncID
ORDER BY ordens_abertas DESC;

-- Serviços mais realizados
SELECT s.Descricao, COUNT(oss.OSID) AS vezes_realizado,
       SUM(oss.ValorCobrado) AS receita_total
FROM Servico s
JOIN OS_Servico oss ON oss.ServicoID = s.ServicoID
GROUP BY s.ServicoID
ORDER BY vezes_realizado DESC
LIMIT 10;

-- Peças com estoque crítico (< 5 unidades)
SELECT Nome, Codigo, Estoque_qtd, Preco
FROM Peca
WHERE Estoque_qtd < 5
ORDER BY Estoque_qtd ASC;

-- Ticket médio por OS por mês
SELECT DATE_FORMAT(DataAbertura, '%Y-%m') AS mes,
       COUNT(*) AS total_os,
       ROUND(AVG(ValorTotal), 2) AS ticket_medio,
       SUM(ValorTotal) AS receita_mensal
FROM OrdemServico
WHERE Status = 'entregue'
GROUP BY mes
ORDER BY mes;
```

</details>

---

## 🤖 Gerador de Dados (gerador_de_dados.py)

<details>
<summary><strong>🐍 Geração de dados sintéticos em português</strong></summary>

```python
from faker import Faker
import random, mysql.connector

fake = Faker('pt_BR')

MARCAS_MODELOS = {
    'Fiat':      ['Uno', 'Palio', 'Argo', 'Mobi', 'Cronos'],
    'Volkswagen':['Gol', 'Polo', 'T-Cross', 'Virtus'],
    'Chevrolet': ['Onix', 'Tracker', 'S10', 'Montana'],
}

def gerar_veiculo():
    marca  = random.choice(list(MARCAS_MODELOS.keys()))
    modelo = random.choice(MARCAS_MODELOS[marca])
    return {
        'placa': fake.license_plate(),
        'marca': marca, 'modelo': modelo,
        'ano':   random.randint(2000, 2024),
        'quilometragem': random.randint(0, 300000)
    }

# python gerador_de_dados.py --clientes 200 --os 500
```

</details>

---

## 🚀 Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/fassir/projeto_modelagem_dados_2.git
cd projeto_modelagem_dados_2

# 2. Crie o banco e execute o schema
mysql -u root -p -e "CREATE DATABASE oficina_db;"
mysql -u root -p oficina_db < schema.sql

# 3. Insira dados de exemplo
mysql -u root -p oficina_db < data.sql

# 4. Ou use o gerador sintético
pip install faker mysql-connector-python
python gerador_de_dados.py

# 5. Execute as consultas analíticas
mysql -u root -p oficina_db < query.sql
```

---

## 👤 Autor

<div align="center">

**Fabio Piassi**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/fabio-piassi)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/fassir)

</div>

---

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:16265F,50:2E75B6,100:1F9BD4&height=120&section=footer" width="100%"/>
