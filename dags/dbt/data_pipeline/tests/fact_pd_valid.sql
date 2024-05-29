SELECT 
    *
FROM
    {{ ref('fact_district_daily') }}
WHERE
    total < 0