{{ config(
    materialized='table'
) }}

SELECT
    FARM_FINGERPRINT(raw_data) AS row_hash,
    * EXCEPT (raw_data)
FROM {{ ref('isd_pipeline_unnest_fields') }}