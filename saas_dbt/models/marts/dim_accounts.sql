{{ config(materialized='table') }}

select
    account_id,
    account_name,
    industry,
    country,
    signup_date,
    plan_tier,
    account_age_days
from {{ ref('stg_accounts') }}