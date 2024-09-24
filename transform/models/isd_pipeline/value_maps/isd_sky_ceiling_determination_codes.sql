{{ config(
    materialized='table',
) }}

SELECT * FROM UNNEST([STRUCT<sky_ceiling_determination_code STRING, description STRING>
    ('A', 'Aircraft'),
    ('B', 'Balloon'),
    ('C', 'Statistically derived'),
    ('D', 'Persistent cirriform ceiling (pre-1950 data)'),
    ('E', 'Estimated'),
    ('M', 'Measured'),
    ('P', 'Precipitation ceiling (pre-1950 data)'),
    ('R', 'Radar'),
    ('S', 'ASOS augmented'),
    ('U', 'Unknown ceiling (pre-1950 data)'),
    ('V', 'Variable ceiling (pre-1950 data)'),
    ('W', 'Obscured'),
    ('9', 'Missing')
])