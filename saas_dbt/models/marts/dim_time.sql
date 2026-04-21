{{ config(materialized='table') }}

with dates as (
    select generate_series(min(signup_date), current_date, interval '1 day') as date
    from {{ ref('stg_accounts') }}
)
select
    date,
    extract(day from date) as day,
    to_char(date, 'Month') as month_name,
    extract(month from date) as month_number,
    extract(quarter from date) as quarter,
    extract(dow from date) as weekday,
    extract(year from date) as year
from dates