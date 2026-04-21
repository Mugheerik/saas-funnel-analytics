{{ config(materialized='table') }}

select
    c.account_id,
    c.churn_date,

    -- ✅ derive churn_flag
    case 
        when c.churn_date is not null then 1
        else 0
    end as churn_flag,

    c.reason_code,
    c.feedback_text,
    c.refund_amount_usd

from {{ ref('stg_churn_events') }} c