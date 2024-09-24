{{ config(
    materialized='table',
) }}

SELECT * FROM UNNEST([STRUCT<data_source_flag STRING, description STRING>
    ('1', 'USAF SURFACE HOURLY observation, candidate for merge with NCEI SURFACE HOURLY (not yet merged, element cross-checks)'),
    ('2', 'NCEI SURFACE HOURLY observation, candidate for merge with USAF SURFACE HOURLY (not yet merged, failed element cross-checks)'),
    ('3', 'USAF SURFACE HOURLY/NCEI SURFACE HOURLY merged observation'),
    ('4', 'USAF SURFACE HOURLY observation'),
    ('5', 'NCEI SURFACE HOURLY observation'),
    ('6', 'ASOS/AWOS observation from NCEI'),
    ('7', 'ASOS/AWOS observation merged with USAF SURFACE HOURLY observation'),
    ('8', 'MAPSO observation (NCEI)'),
    ('A', 'USAF SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation, candidate for merge with NCEI SURFACE HOURLY (not yet merged, failed element cross-checks)'),
    ('B', 'NCEI SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation, candidate for merge with USAF SURFACE HOURLY (not yet merged, failed element cross-checks)'),
    ('C', 'USAF SURFACE HOURLY/NCEI SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation'),
    ('D', 'USAF SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation'),
    ('E', 'NCEI SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation'),
    ('F', 'Form OMR/1001 – Weather Bureau city office (keyed data)'),
    ('G', 'SAO surface airways observation, pre-1949 (keyed data)'),
    ('H', 'SAO surface airways observation, 1965-1981 format/period (keyed data)'),
    ('I', 'Climate Reference Network observation'),
    ('J', 'Cooperative Network observation'),
    ('K', 'Radiation Network observation'),
    ('L', 'Data from Climate Data Modernization Program (CDMP) data source'),
    ('M', 'Data from National Renewable Energy Laboratory (NREL) data source'),
    ('N', 'NCAR / NCEI cooperative effort (various national datasets)'),
    ('O', 'Summary observation created by NCEI using hourly observations that may not share the same data source flag.'),
    ('9', 'Missing')
])