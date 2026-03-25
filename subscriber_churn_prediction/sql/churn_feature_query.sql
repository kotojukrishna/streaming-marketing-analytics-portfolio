WITH subscriber_base AS (
    SELECT
        subscriber_id,
        signup_date,
        plan_type,
        region,
        acquisition_channel,
        monthly_price,
        promo_applied,
        watch_minutes_30d,
        active_days_30d,
        titles_watched_30d,
        sports_view_share,
        kids_view_share,
        drama_view_share,
        customer_service_tickets_90d,
        payment_failures_90d,
        days_since_last_watch,
        tenure_months,
        churned
    FROM analytics.streaming_subscribers
),
features AS (
    SELECT
        subscriber_id,
        plan_type,
        region,
        acquisition_channel,
        monthly_price,
        promo_applied,
        watch_minutes_30d,
        active_days_30d,
        titles_watched_30d,
        sports_view_share,
        kids_view_share,
        drama_view_share,
        customer_service_tickets_90d,
        payment_failures_90d,
        days_since_last_watch,
        tenure_months,
        CASE WHEN watch_minutes_30d < 300 THEN 1 ELSE 0 END AS low_watch_flag,
        CASE WHEN active_days_30d <= 3 THEN 1 ELSE 0 END AS low_activity_flag,
        CASE WHEN payment_failures_90d > 0 THEN 1 ELSE 0 END AS payment_risk_flag,
        churned
    FROM subscriber_base
)
SELECT *
FROM features;
