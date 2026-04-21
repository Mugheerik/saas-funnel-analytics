{{ config(materialized='view') }}

select
    usage_id,
    subscription_id,
    usage_date,
    feature_name,
    usage_count,
    usage_duration_secs,
    error_count,
    is_beta_feature
from {{ ref('feature_usage_cleaned') }}