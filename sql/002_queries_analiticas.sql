-- ================================================
-- CONSULTAS ANALÍTICAS — CLIMA BRASIL
-- ================================================

-- 1. Dias com chuva forte por cidade (acima de 10mm)
-- Útil para: escalar menos funcionários nesses dias
SELECT
    cidade,
    data,
    chuva_total_mm,
    temp_max
FROM clima_diario
WHERE chuva_total_mm > 10
ORDER BY chuva_total_mm DESC;


-- 2. Ranking de cidades mais quentes do período
-- Útil para: antecipar pico de vendas de combustível
SELECT
    cidade,
    ROUND(AVG(temp_max), 1)    AS media_temp_max,
    ROUND(MAX(temp_max), 1)    AS maior_temp,
    ROUND(MIN(temp_min), 1)    AS menor_temp
FROM clima_diario
GROUP BY cidade
ORDER BY media_temp_max DESC;


-- 3. Resumo semanal por cidade
-- Útil para: relatório executivo toda segunda-feira
SELECT
    cidade,
    MIN(data)                       AS inicio_semana,
    MAX(data)                       AS fim_semana,
    ROUND(AVG(temp_media), 1)       AS temp_media_semana,
    ROUND(SUM(chuva_total_mm), 1)   AS chuva_acumulada_mm,
    COUNT(*)                        AS dias_coletados
FROM clima_diario
GROUP BY cidade
ORDER BY cidade;


-- 4. Dias mais frios por cidade
-- Útil para: campanhas de produtos de inverno
SELECT
    cidade,
    data,
    temp_min,
    temp_max
FROM clima_diario
WHERE temp_min = (
    SELECT MIN(temp_min)
    FROM clima_diario d2
    WHERE d2.cidade = clima_diario.cidade
)
ORDER BY temp_min;


-- 5. Comparação entre cidades num dia específico
-- Útil para: visão geral operacional do dia
SELECT
    cidade,
    data,
    temp_max,
    temp_min,
    chuva_total_mm,
    CASE
        WHEN chuva_total_mm > 10 THEN 'chuva forte'
        WHEN chuva_total_mm > 0  THEN 'chuva leve'
        ELSE 'sem chuva'
    END AS condicao_chuva
FROM clima_diario
WHERE data = (SELECT MAX(data) FROM clima_diario)
ORDER BY cidade;