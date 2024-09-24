{{ config(
    materialized='table',
) }}

SELECT * FROM UNNEST([STRUCT<wind_observation_type_code STRING, description STRING>
    ('A', 'Abridged Beaufort'),
    ('B', 'Beaufort'),
    ('C', 'Calm'),
    ('H', '5-Minute Average Speed'),
    ('N', 'Normal'),
    ('R', '60-Minute Average Speed'),
    ('Q', 'Squall'),
    ('T', '180 Minute Average Speed'),
    ('V', 'Variable'),
    ('9', 'Missing')
])