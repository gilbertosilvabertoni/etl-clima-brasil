with source as (

    select *
    from {{ source('clima_postgres', 'clima_diario') }}

),

renamed as (

    select
        id as clima_diario_id,
        cidade::varchar(100) as cidade,
        data::date as data_observacao,
        temp_max::numeric(5, 1) as temp_max_c,
        temp_min::numeric(5, 1) as temp_min_c,
        temp_media::numeric(5, 1) as temp_media_c,
        chuva_total_mm::numeric(7, 2) as chuva_total_mm,
        vento_max_kmh::numeric(7, 2) as vento_max_kmh,
        inserido_em::timestamp as inserido_em,
        case
            when chuva_total_mm > 10 then 'chuva forte'
            when chuva_total_mm > 0 then 'chuva leve'
            else 'sem chuva'
        end as classificacao_chuva
    from source

)

select *
from renamed
