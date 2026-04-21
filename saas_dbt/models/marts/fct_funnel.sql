{{ config(materialized='table') }}

with base as (
    select
        a.account_id,
        a.signup_date,

        case when fu.account_id is not null then 1 else 0 end as is_engaged,
        case when s.account_id is not null then 1 else 0 end as is_subscribed

    from {{ ref('stg_accounts') }} a

    left join (
        select distinct s.account_id
        from {{ ref('stg_feature_usage') }} fu
        join {{ ref('stg_subscriptions') }} s
            on fu.subscription_id = s.subscription_id
    ) fu
        on a.account_id = fu.account_id

    left join {{ ref('stg_subscriptions') }} s
        on a.account_id = s.account_id
),

simulated as (
    select *,
        case
            when ABS(HASHTEXT(account_id)) % 5 = 0 then 0
            else is_subscribed
        end as final_subscribed
    from base
)

select
    account_id,
    signup_date,

    case
        when final_subscribed = 1 then 'Subscribed'
        when is_engaged = 1 then 'Engaged'
        else 'Signed Up'
    end as funnel_stage

from simulated