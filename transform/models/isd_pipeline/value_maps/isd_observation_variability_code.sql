{{ config(
    materialized='table',
) }}

SELECT * FROM UNNEST([STRUCT<observation_variability_code STRING, description STRING>
    ('N', 'Not variable'),
    ('V', 'Variable'),
    ('9', 'Missing')
])