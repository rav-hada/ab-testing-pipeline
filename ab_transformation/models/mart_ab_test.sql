-- 1. Aggregate to User Level first
-- (We don't care how MANY times they clicked, just IF they clicked)
WITH user_level AS (
    SELECT
        user_id,
        experiment_group,
        MAX(is_converted) as converted -- 1 if they clicked at least once, 0 otherwise
    FROM {{ ref('stg_ad_clicks') }}
    GROUP BY 1, 2
),

-- 2. Aggregate to Experiment Group Level
group_level AS (
    SELECT
        experiment_group,
        COUNT(user_id) as total_users,
        SUM(converted) as total_conversions,
        -- Calculate Conversion Rate (Probability p)
        SUM(converted)::FLOAT / COUNT(user_id) as conversion_rate
    FROM user_level
    GROUP BY 1
)

SELECT 
    experiment_group,
    total_users,
    total_conversions,
    ROUND(conversion_rate::numeric, 4) as conversion_rate,
    -- Standard Error Formula: sqrt(p * (1-p) / n)
    -- This is crucial for calculating Statistical Significance later
    SQRT( (conversion_rate * (1 - conversion_rate)) / total_users ) as std_error
FROM group_level