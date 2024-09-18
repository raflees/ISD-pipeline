
{{ config(
    materialized='table'
) }}

SELECT
    JSON_VALUE(records, "$.data") raw_data,
    CAST(ingest_timestamp AS TIMESTAMP) AS ingest_timestamp,
    _FILE_NAME AS file_name,
FROM {{ source('isd_raw', 'i_dont_exist') }}