{{ config(
    alias='isd_pipeline_unnest_records'
) }}

SELECT
    JSON_VALUE(record, "$.data") raw_data,
    ingest_timestamp,
    _FILE_NAME AS file_uri,
FROM {{ source('isd_raw', 'raw_integrated_surface_data') }}