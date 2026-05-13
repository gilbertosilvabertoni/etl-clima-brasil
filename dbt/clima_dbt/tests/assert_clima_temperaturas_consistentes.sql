select *
from {{ ref('stg_clima_diario') }}
where
    temp_min_c > temp_media_c
    or temp_media_c > temp_max_c
