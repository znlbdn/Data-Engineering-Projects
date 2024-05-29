SELECT
    id as case_id,
    status_name,
    status_detail,
    LOWER(status) as status
FROM
    {{ ref('dim_covcase') }}