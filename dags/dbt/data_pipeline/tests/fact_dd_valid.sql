SELECT 
    *
FROM
    {{ ref('fact_province_daily') }}
WHERE
    total < 0