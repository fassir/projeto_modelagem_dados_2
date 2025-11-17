import random
import string
from datetime import datetime, timedelta

# Quantidade de registros
N_CLIENTES = 5000
N_VEICULOS = 800
N_FUNCIONARIOS = 30
N_SERVICOS = 800
N_PECAS = 2000
N_ORDENS = 12000

# Geradores auxiliares
def nome_aleatorio():
    nomes = ['João', 'Maria', 'Carlos', 'Ana', 'Pedro', 'Lucas', 'Julia', 'Marcos', 'Fernanda', 'Rafael']
    sobrenomes = ['Silva', 'Souza', 'Oliveira', 'Costa', 'Pereira', 'Rodrigues', 'Almeida', 'Nascimento', 'Lima', 'Gomes']
    return f"{random.choice(nomes)} {random.choice(sobrenomes)}"

def telefone_aleatorio():
    return f"({random.randint(11,99)})9{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def email_aleatorio(nome):
    dominios = ['gmail.com', 'hotmail.com', 'yahoo.com']
    return f"{nome.lower().replace(' ','.')}@{random.choice(dominios)}"

def placa_aleatoria():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=4))
    return f"{letras}-{numeros}"

def modelo_aleatorio():
    modelos = ['Gol', 'Fiesta', 'Civic', 'Corolla', 'Uno', 'Palio', 'HB20', 'Onix', 'Ka', 'Sandero']
    return random.choice(modelos)

def funcao_aleatoria():
    funcoes = ['Mecânico', 'Recepcionista', 'Eletricista', 'Gerente', 'Auxiliar']
    return random.choice(funcoes)

def servico_aleatorio(n):
    tipos = ['Troca de óleo', 'Revisão geral', 'Alinhamento', 'Balanceamento', 'Troca de pneus', 'Limpeza de bicos', 'Troca de pastilhas', 'Diagnóstico eletrônico', 'Inspeção', 'Regulagem', 'Substituição', 'Teste', 'Ajuste']
    servicos = []
    for i in range(1, n+1):
        tipo = random.choice(tipos)
        desc = f"{tipo} {random.choice(string.ascii_uppercase)}{random.randint(1,999)}"
        valor = random.randint(50, 500)
        servicos.append((i, desc, valor))
    return servicos

def peca_aleatoria(n):
    tipos = ['Filtro', 'Pneu', 'Pastilha', 'Amortecedor', 'Bateria', 'Correia', 'Vela', 'Disco', 'Radiador', 'Sensor', 'Bomba', 'Farol', 'Lanterna', 'Parafuso', 'Rolamento', 'Coxim', 'Termostato', 'Junta', 'Cabo']
    nomes = []
    for i in range(1, n+1):
        tipo = random.choice(tipos)
        nome = f"{tipo} {random.choice(string.ascii_uppercase)}{random.randint(1,999)}"
        nomes.append(nome)
    return nomes

# Geração dos dados
clientes = []
for i in range(1, N_CLIENTES+1):
    nome = nome_aleatorio()
    clientes.append((i, nome, telefone_aleatorio(), email_aleatorio(nome)))

veiculos = []
for i in range(1, N_VEICULOS+1):
    veiculos.append((i, placa_aleatoria(), modelo_aleatorio(), random.randint(2000,2023), random.randint(1, N_CLIENTES)))

funcionarios = []
for i in range(1, N_FUNCIONARIOS+1):
    funcionarios.append((i, nome_aleatorio(), funcao_aleatoria()))

servicos = servico_aleatorio(N_SERVICOS)

pecas = []
for i, nome in enumerate(peca_aleatoria(N_PECAS), 1):
    pecas.append((i, nome, random.randint(10, 100), random.randint(20, 500)))

ordens = []
ordem_servico_servico = []
ordem_servico_peca = []
for i in range(1, N_ORDENS+1):
    data = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 320))
    id_cliente = random.randint(1, N_CLIENTES)
    id_veiculo = random.randint(1, N_VEICULOS)
    id_funcionario = random.randint(1, N_FUNCIONARIOS)
    valor_total = 0
    # Serviços
    servicos_ordem = random.sample(range(1, N_SERVICOS+1), random.randint(1, 3))
    for id_servico in servicos_ordem:
        quantidade = random.randint(1, 2)
        valor_servico = [s[2] for s in servicos if s[0] == id_servico][0]
        valor_total += valor_servico * quantidade
        ordem_servico_servico.append((i, id_servico, quantidade))
    # Peças
    pecas_ordem = random.sample(range(1, N_PECAS+1), random.randint(0, 3))
    for id_peca in pecas_ordem:
        quantidade = random.randint(1, 4)
        valor_peca = [p[3] for p in pecas if p[0] == id_peca][0]
        valor_total += valor_peca * quantidade
        ordem_servico_peca.append((i, id_peca, quantidade))
    ordens.append((i, data.strftime('%Y-%m-%d'), id_cliente, id_veiculo, id_funcionario, round(valor_total,2)))

# Função para gerar SQL

def gerar_insert(tabela, colunas, dados):
    linhas = []
    for d in dados:
        valores = []
        for v in d:
            if isinstance(v, str):
                valores.append(f"'{v}'")
            else:
                valores.append(str(v))
        linhas.append(f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({', '.join(valores)});")
    return '\n'.join(linhas)

if __name__ == "__main__":
    print('-- Clientes')
    print(gerar_insert('Cliente', ['id_cliente','nome','telefone','email'], clientes))
    print('\n-- Veiculos')
    print(gerar_insert('Veiculo', ['id_veiculo','placa','modelo','ano','id_cliente'], veiculos))
    print('\n-- Funcionarios')
    print(gerar_insert('Funcionario', ['id_funcionario','nome','funcao'], funcionarios))
    print('\n-- Servicos')
    print(gerar_insert('Servico', ['id_servico','descricao','valor'], servicos))
    print('\n-- Pecas')
    print(gerar_insert('Peca', ['id_peca','nome','quantidade_estoque','valor_unitario'], pecas))
    print('\n-- Ordens de Servico')
    print(gerar_insert('Ordem_Servico', ['id_ordem','data','id_cliente','id_veiculo','id_funcionario','valor_total'], ordens))
    print('\n-- Ordem_Servico_Servico')
    print(gerar_insert('Ordem_Servico_Servico', ['id_ordem','id_servico','quantidade'], ordem_servico_servico))
    print('\n-- Ordem_Servico_Peca')
    print(gerar_insert('Ordem_Servico_Peca', ['id_ordem','id_peca','quantidade'], ordem_servico_peca))
