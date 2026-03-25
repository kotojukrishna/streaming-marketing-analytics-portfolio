WITH channel_daily AS (
    SELECT
        event_date,
        channel,
        SUM(impressions) AS impressions,
        SUM(clicks) AS clicks,
        SUM(landing_page_visits) AS visits,
        SUM(trial_starts) AS trial_starts,
        SUM(paid_conversions) AS paid_conversions,
        SUM(marketing_spend) AS marketing_spend
    FROM marketing.channel_performance
    GROUP BY 1, 2
),
metrics AS (
    SELECT
        event_date,
        channel,
        impressions,
        clicks,
        visits,
        trial_starts,
        paid_conversions,
        marketing_spend,
        ROUND(clicks::numeric / NULLIF(impressions, 0), 4) AS ctr,
        ROUND(visits::numeric / NULLIF(clicks, 0), 4) AS visit_rate,
        ROUND(trial_starts::numeric / NULLIF(visits, 0), 4) AS trial_start_rate,
        ROUND(paid_conversions::numeric / NULLIF(trial_starts, 0), 4) AS trial_to_paid_rate,
        ROUND(marketing_spend::numeric / NULLIF(paid_conversions, 0), 2) AS cac
    FROM channel_daily
)
SELECT *
FROM metrics
ORDER BY event_date, channel;
