SELECT
    SUBSTR(raw_data, 1, 2) AS station,
FROM {{ ref('isd_pipeline_unnested') }}