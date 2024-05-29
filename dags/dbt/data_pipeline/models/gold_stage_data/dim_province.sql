with distinct_province as (
SELECT DISTINCT
    kode_prov as province_id,
    nama_prov as province_name
FROM
    {{ source('jabar_covkab', 'jabar_covid_kab') }}
)
SELECT
    row_number() OVER (ORDER BY province_id, province_name) as id,
    province_id,
    province_name
FROM
    distinct_province