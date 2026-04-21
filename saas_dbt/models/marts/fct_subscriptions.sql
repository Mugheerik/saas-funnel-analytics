{{ config(materialized='table') }}

select
    s.subscription_id,
    s.account_id,
    s.start_date,
    s.end_date,
    s.plan_tier,
    s.seats,
    s.mrr_amount,
    s.arr_amount,
    s.subscription_duration_days,
    s.is_active,
    s.calculated_mrr
from {{ ref('stg_subscriptions') }} s