{{ config(
    materialized='table'
) }}

SELECT
    file_name,
    raw_data,
    SUBSTR(raw_data, 1, 4) AS total_variable_characters,
    SUBSTR(raw_data, 5, 6) AS weather_station_catalog_id,
    SUBSTR(raw_data, 11, 5) AS weather_station_wban_id,
    SUBSTR(raw_data, 16, 8) AS observation_date,
    SUBSTR(raw_data, 24, 4) AS observation_time,
    SUBSTR(raw_data, 28, 1) AS data_source_flag,
    SUBSTR(raw_data, 29, 6) AS latitude,
    SUBSTR(raw_data, 35, 6) AS longitude,
    SUBSTR(raw_data, 42, 5) AS report_type_code,
    SUBSTR(raw_data, 47, 5) AS elevation_in_meters,
    SUBSTR(raw_data, 52, 5) AS station_call_letter_id,
    SUBSTR(raw_data, 57, 4) AS quality_control_process_code,
    SUBSTR(raw_data, 61, 3) AS wind_direction_angle,
    SUBSTR(raw_data, 64, 1) AS wind_direction_quality_code,
    SUBSTR(raw_data, 65, 1) AS wind_observation_type_code,
    SUBSTR(raw_data, 66, 4) AS wind_speed_meters_per_second,
    SUBSTR(raw_data, 70, 1) AS wind_speed_quality_code,
    SUBSTR(raw_data, 71, 5) AS sky_ceiling_height_in_meters,
    SUBSTR(raw_data, 76, 1) AS sky_ceiling_quality_code,
    SUBSTR(raw_data, 77, 1) AS sky_ceiling_determination_code,
    SUBSTR(raw_data, 78, 1) AS sky_cavok_code,
    SUBSTR(raw_data, 79, 6) AS max_observation_distance_in_meters,
FROM {{ ref('isd_pipeline_unnest_records') }}