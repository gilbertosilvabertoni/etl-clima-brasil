select *
from {{ ref('stg_clima_diario') }}
where
    chuva_total_mm < 0
    or vento_max_kmh < 0
