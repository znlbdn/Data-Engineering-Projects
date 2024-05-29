with union_value as (
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'suspect_discarded' as status,
        suspect_discarded as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'probable_discarded' as status,
        probable_discarded as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'closecontact_discarded' as status,
        closecontact_discarded as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'probable_meninggal' as status,
        probable_meninggal as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'probable_diisolasi' as status,
        probable_diisolasi as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'closecontact_meninggal' as status,
        closecontact_meninggal as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'closecontact_dikarantina' as status,
        closecontact_dikarantina as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'confirmation_meninggal' as status,
        confirmation_meninggal as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'confirmation_sembuh' as status,
        confirmation_sembuh as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'suspect_meninggal' as status,
        suspect_meninggal as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
    UNION ALL
    SELECT
        tanggal,
        kode_kab,
        kode_prov,
        'suspect_diisolasi' as status,
        suspect_diisolasi as value
    FROM 
        {{ source('jabar_covkab', 'jabar_covid_kab') }}
)
SELECT
    row_number() OVER (ORDER BY status) as id,
    kode_kab as district_id,
    kode_prov as province_id,
    tanggal as date,
    status,
    value as total
FROM union_value