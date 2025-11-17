-- query.sql
-- Consultas para análise dos dados da oficina

-- 1. Quais clientes mais utilizaram os serviços da oficina?
SELECT c.nome, COUNT(o.id_ordem) AS total_ordens
FROM Cliente c
JOIN Ordem_Servico o ON c.id_cliente = o.id_cliente
GROUP BY c.nome
ORDER BY total_ordens DESC
LIMIT 10;

-- 2. Qual o faturamento mensal da oficina?
SELECT EXTRACT(MONTH FROM data) AS mes, SUM(valor_total) AS faturamento
FROM Ordem_Servico
GROUP BY mes
ORDER BY mes;

-- 3. Quais peças foram mais utilizadas em determinado período?
SELECT p.nome, SUM(osp.quantidade) AS total_utilizado
FROM Ordem_Servico_Peca osp
JOIN Peca p ON osp.id_peca = p.id_peca
JOIN Ordem_Servico o ON osp.id_ordem = o.id_ordem
WHERE o.data BETWEEN '2025-01-01' AND '2025-11-16'
GROUP BY p.nome
ORDER BY total_utilizado DESC
LIMIT 10;

-- 4. Quais funcionários realizaram mais atendimentos?
SELECT f.nome, COUNT(o.id_ordem) AS atendimentos
FROM Funcionario f
JOIN Ordem_Servico o ON f.id_funcionario = o.id_funcionario
GROUP BY f.nome
ORDER BY atendimentos DESC
LIMIT 10;

-- 5. Quais veículos passaram por revisões completas?
SELECT v.placa, v.modelo, COUNT(oss.id_servico) AS total_servicos
FROM Veiculo v
JOIN Ordem_Servico o ON v.id_veiculo = o.id_veiculo
JOIN Ordem_Servico_Servico oss ON o.id_ordem = oss.id_ordem
GROUP BY v.placa, v.modelo
HAVING total_servicos >= 5
ORDER BY total_servicos DESC;

-- 6. Qual o histórico de serviços de um determinado cliente?
SELECT c.nome, o.id_ordem, o.data, s.descricao, oss.quantidade
FROM Cliente c
JOIN Ordem_Servico o ON c.id_cliente = o.id_cliente
JOIN Ordem_Servico_Servico oss ON o.id_ordem = oss.id_ordem
JOIN Servico s ON oss.id_servico = s.id_servico
WHERE c.nome = 'João Silva'
ORDER BY o.data DESC;

-- 7. Faturamento por funcionário
SELECT f.nome, SUM(o.valor_total) AS faturamento
FROM Funcionario f
JOIN Ordem_Servico o ON f.id_funcionario = o.id_funcionario
GROUP BY f.nome
ORDER BY faturamento DESC;

-- 8. Peças com estoque abaixo de 20 unidades
SELECT nome, quantidade_estoque
FROM Peca
WHERE quantidade_estoque < 20
ORDER BY quantidade_estoque ASC;

-- 9. Clientes que possuem mais de 3 veículos cadastrados
SELECT c.nome, COUNT(v.id_veiculo) AS total_veiculos
FROM Cliente c
JOIN Veiculo v ON c.id_cliente = v.id_cliente
GROUP BY c.nome
HAVING total_veiculos > 3
ORDER BY total_veiculos DESC;

-- 10. Serviços mais realizados na oficina
SELECT s.descricao, SUM(oss.quantidade) AS total_realizado
FROM Servico s
JOIN Ordem_Servico_Servico oss ON s.id_servico = oss.id_servico
GROUP BY s.descricao
ORDER BY total_realizado DESC
LIMIT 10;
