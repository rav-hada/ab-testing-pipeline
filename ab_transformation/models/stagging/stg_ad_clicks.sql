SELECT
    user_id,
    timestamp as event_time,
    experiment_group,
    -- Clean up device type (just in case)
    LOWER(device_type) as device_type,
    -- Ensure 'clicked' is an integer (1 or 0)
    CAST(clicked as INT) as is_converted
FROM {{ source('warehouse', 'raw_ad_clicks') }}