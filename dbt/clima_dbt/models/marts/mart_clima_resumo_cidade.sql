with clima as (

    select *
    from {{ ref('stg_clima_diario') }}

)

select
    cidade,
    min(data_observacao) as data_inicio,
    max(data_observacao) as data_fim,
    count(*) as dias_coletados,
    round(avg(temp_max_c), 1) as media_temp_max_c,
    max(temp_max_c) as maior_temp_max_c,
    min(temp_min_c) as menor_temp_min_c,
    round(avg(temp_media_c), 1) as media_temp_media_c,
    round(sum(chuva_total_mm), 1) as chuva_acumulada_mm,
    round(avg(chuva_total_mm), 1) as media_chuva_diaria_mm,
    count(*) filter (where chuva_total_mm > 0) as dias_com_chuva,
    count(*) filter (where chuva_total_mm > 10) as dias_com_chuva_forte,
    round(
        100.0 * count(*) filter (where chuva_total_mm > 0)
        / nullif(count(*), 0),
        1
    ) as pct_dias_com_chuva,
    max(vento_max_kmh) as maior_vento_kmh,
    current_timestamp as atualizado_em
from clima
group by cidade
