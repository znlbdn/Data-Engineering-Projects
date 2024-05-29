SELECT
    row_number() OVER(ORDER BY T1.date) as id,
    T1.district_id as district_id,
    T2.case_id as case_id,
    T1.date as date,
    SUM(T1.total) as total
FROM 
    {{ ref('fact_total_case') }} as T1
LEFT JOIN
    {{ ref('dim_case') }} as T2
ON T1.status = T2.status
GROUP BY district_id, case_id, date