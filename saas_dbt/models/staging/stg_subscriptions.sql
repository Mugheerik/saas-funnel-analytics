{{ config(materialized='view') }}

select
    subscription_id,
    account_id,
    start_date,
    end_date,
    plan_tier,
    seats,
    mrr_amount,
    arr_amount,
    subscription_duration_days,
    is_trial,
    upgrade_flag,
    downgrade_flag,
    churn_flag,
    auto_renew_flag,
    -- fallback calculated MRR
    coalesce(arr_amount / 12, 0) as calculated_mrr,
    case when end_date is null or end_date >= current_date then 1 else 0 end as is_active
from {{ ref('subscriptions_cleaned') }}