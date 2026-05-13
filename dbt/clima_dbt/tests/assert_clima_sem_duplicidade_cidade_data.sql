select
    cidade,
    data_observacao,
    count(*) as total_registros
from {{ ref('stg_clima_diario') }}
group by
    cidade,
    data_observacao
having count(*) > 1
