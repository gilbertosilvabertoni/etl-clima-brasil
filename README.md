# Pipeline ETL — Clima Brasil

Pipeline de dados que coleta informações climáticas de 5 capitais
brasileiras via API pública, transforma em resumo diário, armazena
em banco PostgreSQL e disponibiliza consultas analíticas.

## Tecnologias
- Python 3.x · Pandas · Requests · python-dotenv · psycopg2
- PostgreSQL 16
- Docker · Docker Compose
- Airflow 2.9
- dbt · dbt-postgres
- Git/GitHub

## Estrutura
```text
etl-clima-brasil/
├── docker/
│   ├── docker-compose.yml   # containers PostgreSQL, Airflow, pgAdmin e dbt
│   ├── Dockerfile.dbt       # imagem do dbt
│   └── .env.db              # credenciais do banco
├── dags/
│   └── dag_clima_brasil.py  # orquestracao diaria no Airflow
├── dbt/
│   ├── profiles.yml         # conexao dbt com PostgreSQL
│   └── clima_dbt/           # projeto dbt
├── sql/
│   ├── 001_create_tables.sql      # schema da tabela
│   └── 002_queries_analiticas.sql # consultas do cliente
├── src/
│   ├── extract.py    # coleta da API Open-Meteo
│   ├── transform.py  # limpeza e agregação diária
│   ├── load.py       # relatório de qualidade
│   └── database.py   # carregamento no PostgreSQL
├── data/
│   ├── raw/          # dados brutos da API (não versionado)
│   └── processed/    # dados transformados (não versionado)
├── .env.example      # variáveis de ambiente necessárias
├── requirements.txt  # dependências do projeto
└── README.md
```

## Como rodar

### 1. Clone o repositório
git clone https://github.com/gilbertosilvabertoni/etl-clima-brasil.git
cd etl-clima-brasil

### 2. Crie o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

### 3. Instale as dependências
pip install -r requirements.txt

### 4. Configure as variáveis de ambiente
cp .env.example .env

### 5. Suba os containers
cd docker
docker compose up -d
cd ..

### 6. Execute o pipeline completo
python src/extract.py && python src/transform.py && python src/load.py

### 7. Carregue os dados no banco
python src/database.py

### 8. Execute as transformações dbt
```bash
docker exec clima_dbt dbt debug --project-dir /usr/app/dbt/clima_dbt
docker exec clima_dbt dbt run --project-dir /usr/app/dbt/clima_dbt
docker exec clima_dbt dbt test --project-dir /usr/app/dbt/clima_dbt
```

### 9. Consulte os dados
Consultas SQL originais:
```bash
docker exec clima_brasil_db psql -U clima_user -d clima_brasil \
  -c "$(cat sql/002_queries_analiticas.sql)"
```

Marts criados pelo dbt:
```bash
docker exec clima_brasil_db psql -U clima_user -d clima_brasil \
  -c "select * from mart_clima_resumo_cidade order by media_temp_max_c desc;"
```

## Dados coletados
| Campo | Descrição |
|---|---|
| cidade | Nome da capital |
| data | Data do resumo |
| temp_max | Temperatura máxima do dia (°C) |
| temp_min | Temperatura mínima do dia (°C) |
| temp_media | Temperatura média do dia (°C) |
| chuva_total_mm | Chuva acumulada no dia (mm) |
| vento_max_kmh | Velocidade máxima do vento (km/h) |

## Cidades cobertas
São Paulo · Rio de Janeiro · Curitiba · Salvador · Manaus

## Consultas analíticas disponíveis
- Dias com chuva forte por cidade (acima de 10mm)
- Ranking de cidades mais quentes do período
- Resumo semanal por cidade
- Dias mais frios por cidade
- Comparação entre cidades no dia mais recente

## Modelos dbt
- `stg_clima_diario`: padroniza a tabela `clima_diario`.
- `mart_clima_resumo_cidade`: indicadores consolidados por cidade.
- `mart_clima_resumo_semanal`: resumo semanal por cidade.
- `mart_clima_ultimo_dia`: comparação das cidades no dia mais recente.
- `mart_clima_alertas`: alertas de chuva forte, calor, frio e vento.

## Fonte dos dados
[Open-Meteo](https://open-meteo.com/) — API meteorológica gratuita e aberta.

## Projetos da trilha
| Projeto | Descrição | Stack |
|---|---|---|
| 1 — ETL local | Coleta, transforma e salva em CSV | Python · Pandas · Git |
| 2 — Banco relacional | Modela schema e carrega no PostgreSQL | PostgreSQL · Docker · SQL |
| 3 — Orquestração | Automatiza o pipeline com DAG | Airflow · Docker Compose |
| 4 — Transformações | Organiza SQL com modelos dbt | dbt · PostgreSQL |
| 5 — Nuvem | Escala para cloud com Data Lake | AWS S3 · Redshift ou GCP |
