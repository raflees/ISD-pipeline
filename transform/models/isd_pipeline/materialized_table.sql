
{{ config(
    materialized='table'
) }}

SELECT
    JSON_VALUE(records, "$.data") raw_data,
    CAST(ingest_timestamp AS TIMESTAMP) AS ingest_timestamp,
FROM {{ source('isd_raw', 'raw_integrated_surface_data') }}