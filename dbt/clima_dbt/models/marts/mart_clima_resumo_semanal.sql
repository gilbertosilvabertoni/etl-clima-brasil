with clima as (

    select *
    from {{ ref('stg_clima_diario') }}

),

semanal as (

    select
        cidade,
        date_trunc('week', data_observacao)::date as inicio_semana,
        max(data_observacao) as fim_semana,
        count(*) as dias_coletados,
        round(avg(temp_media_c), 1) as temp_media_semana_c,
        round(avg(temp_max_c), 1) as media_temp_max_c,
        round(min(temp_min_c), 1) as menor_temp_min_c,
        round(sum(chuva_total_mm), 1) as chuva_acumulada_mm,
        max(vento_max_kmh) as maior_vento_kmh,
        count(*) filter (where chuva_total_mm > 10) as dias_com_chuva_forte
    from clima
    group by
        cidade,
        date_trunc('week', data_observacao)::date

)

select
    md5(cidade || '|' || inicio_semana::text) as cidade_semana_id,
    *
from semanal
