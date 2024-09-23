{{ config(
    alias='isd_hashed',
    materialized='table'
) }}

SELECT
    FARM_FINGERPRINT(raw_data) AS row_hash,
    * EXCEPT (raw_data)
FROM {{ ref('t2_isd_unnest_fields') }}