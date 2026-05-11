-- Cria a tabela principal de clima diário
CREATE TABLE IF NOT EXISTS clima_diario (
    id            SERIAL PRIMARY KEY,
    cidade        VARCHAR(100) NOT NULL,
    data          DATE NOT NULL,
    temp_max      NUMERIC(5,1),
    temp_min      NUMERIC(5,1),
    temp_media    NUMERIC(5,1),
    chuva_total_mm NUMERIC(7,2),
    vento_max_kmh  NUMERIC(7,2),
    inserido_em   TIMESTAMP DEFAULT NOW(),

    -- Garante que não existam duplicatas para a mesma cidade e data
    UNIQUE (cidade, data)
);

-- Índices para acelerar as consultas mais comuns
CREATE INDEX IF NOT EXISTS idx_clima_cidade
    ON clima_diario (cidade);

CREATE INDEX IF NOT EXISTS idx_clima_data
    ON clima_diario (data);

CREATE INDEX IF NOT EXISTS idx_clima_cidade_data
    ON clima_diario (cidade, data);