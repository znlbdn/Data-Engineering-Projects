with distinct_district as (
SELECT DISTINCT
    kode_kab as district_id,
    nama_kab as district_name
FROM
    {{ source('jabar_covkab', 'jabar_covid_kab') }}
)
SELECT
    row_number() OVER (ORDER BY district_id, district_name) as id,
    district_id,
    district_name
FROM
    distinct_district