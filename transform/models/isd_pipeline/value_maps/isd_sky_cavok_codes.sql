{{ config(
    materialized='table',
) }}

SELECT * FROM UNNEST([STRUCT<sky_cavok_code STRING, description STRING>
    ('N', 'No'),
    ('Y', 'Yes'),
    ('9', 'Missing')
])