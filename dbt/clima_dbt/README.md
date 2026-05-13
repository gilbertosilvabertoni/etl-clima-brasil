# dbt — Clima Brasil

Projeto dbt responsavel pela camada analitica em cima da tabela `public.clima_diario`,
carregada pelo pipeline Python/Airflow no PostgreSQL.

## Estrutura

- `models/staging`: padronizacao da fonte operacional.
- `models/marts`: tabelas analiticas para consumo.
- `tests`: testes singulares de qualidade de dados.

## Como executar

```bash
docker exec clima_dbt dbt debug --project-dir /usr/app/dbt/clima_dbt
docker exec clima_dbt dbt run --project-dir /usr/app/dbt/clima_dbt
docker exec clima_dbt dbt test --project-dir /usr/app/dbt/clima_dbt
```

## Modelos principais

- `stg_clima_diario`: fonte limpa e padronizada.
- `mart_clima_resumo_cidade`: ranking e indicadores por cidade.
- `mart_clima_resumo_semanal`: resumo semanal executivo.
- `mart_clima_ultimo_dia`: comparacao entre cidades no ultimo dia carregado.
- `mart_clima_alertas`: eventos de chuva forte, calor, frio e vento.
