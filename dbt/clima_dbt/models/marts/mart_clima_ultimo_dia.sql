with clima as (

    select *
    from {{ ref('stg_clima_diario') }}

),

ultimo_dia as (

    select max(data_observacao) as data_observacao
    from clima

)

select
    clima.cidade,
    clima.data_observacao,
    clima.temp_max_c,
    clima.temp_min_c,
    clima.temp_media_c,
    clima.chuva_total_mm,
    clima.vento_max_kmh,
    clima.classificacao_chuva,
    dense_rank() over (order by clima.temp_max_c desc) as ranking_temp_max,
    dense_rank() over (order by clima.chuva_total_mm desc) as ranking_chuva
from clima
inner join ultimo_dia
    on clima.data_observacao = ultimo_dia.data_observacao
