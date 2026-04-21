{{ config(materialized='view') }}

select
    account_id,
    account_name,
    industry,
    country,
    signup_date,
    plan_tier,
    account_age_days,
    is_trial,
    churn_flag
from {{ ref('accounts_cleaned') }}