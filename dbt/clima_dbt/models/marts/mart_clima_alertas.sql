with clima as (

    select *
    from {{ ref('stg_clima_diario') }}

),

alertas as (

    select
        cidade,
        data_observacao,
        'chuva_forte' as tipo_alerta,
        case
            when chuva_total_mm >= 25 then 'alta'
            else 'media'
        end as severidade,
        chuva_total_mm as valor_observado,
        'mm' as unidade,
        'Chuva forte registrada no dia' as mensagem
    from clima
    where chuva_total_mm > 10

    union all

    select
        cidade,
        data_observacao,
        'calor_intenso' as tipo_alerta,
        case
            when temp_max_c >= 35 then 'alta'
            else 'media'
        end as severidade,
        temp_max_c as valor_observado,
        'C' as unidade,
        'Temperatura maxima elevada' as mensagem
    from clima
    where temp_max_c >= 30

    union all

    select
        cidade,
        data_observacao,
        'frio_intenso' as tipo_alerta,
        case
            when temp_min_c <= 10 then 'alta'
            else 'media'
        end as severidade,
        temp_min_c as valor_observado,
        'C' as unidade,
        'Temperatura minima baixa' as mensagem
    from clima
    where temp_min_c <= 15

    union all

    select
        cidade,
        data_observacao,
        'vento_forte' as tipo_alerta,
        case
            when vento_max_kmh >= 50 then 'alta'
            else 'media'
        end as severidade,
        vento_max_kmh as valor_observado,
        'km/h' as unidade,
        'Vento forte registrado no dia' as mensagem
    from clima
    where vento_max_kmh >= 30

)

select
    md5(cidade || '|' || data_observacao::text || '|' || tipo_alerta) as alerta_id,
    *
from alertas
