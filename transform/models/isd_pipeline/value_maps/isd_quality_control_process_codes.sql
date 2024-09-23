{{ config(
    materialized='table',
) }}

SELECT * FROM UNNEST([STRUCT<quality_control_process_code STRING, description STRING>
    ('V01', 'No A or M Quality Control applied'),
    ('V02', 'Automated Quality Control'),
    ('V03', 'subjected to Quality Control')
])