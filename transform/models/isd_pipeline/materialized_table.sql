
{{ config(
    materialized='table'
) }}

SELECT
    *
FROM {{ source('isd_raw', 'raw_integrated_surface_data') }}