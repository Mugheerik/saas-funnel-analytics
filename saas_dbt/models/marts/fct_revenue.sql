{{ config(materialized='table') }}

select
    s.account_id,
    date_trunc('month', s.start_date) as revenue_month,
    sum(s.calculated_mrr) as total_mrr
from {{ ref('stg_subscriptions') }} s
group by 1,2