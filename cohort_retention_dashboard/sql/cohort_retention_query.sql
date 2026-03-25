WITH subscribers AS (
    SELECT
        subscriber_id,
        DATE_TRUNC('month', signup_date) AS cohort_month,
        DATE_TRUNC('month', activity_date) AS activity_month
    FROM analytics.subscriber_activity
),
cohorts AS (
    SELECT
        cohort_month,
        activity_month,
        COUNT(DISTINCT subscriber_id) AS active_subscribers,
        DATE_PART('month', AGE(activity_month, cohort_month)) AS months_since_signup
    FROM subscribers
    GROUP BY 1,2
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT subscriber_id) AS cohort_size
    FROM analytics.subscriber_activity
    GROUP BY 1
)
SELECT
    c.cohort_month,
    c.activity_month,
    c.months_since_signup,
    c.active_subscribers,
    s.cohort_size,
    ROUND(c.active_subscribers::numeric / NULLIF(s.cohort_size,0), 4) AS retention_rate
FROM cohorts c
JOIN cohort_sizes s USING (cohort_month)
ORDER BY cohort_month, months_since_signup;
