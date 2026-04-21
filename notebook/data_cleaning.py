import os
import pandas as pd

# ---------------------------
# Utility Functions
# ---------------------------

def clean_columns(df):
    """Standardize column names: lowercase and strip spaces."""
    df.columns = df.columns.str.strip().str.lower()
    return df

def convert_bool(df, columns):
    """Convert boolean-like columns to 0/1 integers."""
    for bool_col in columns:
        df[bool_col] = df[bool_col].astype(str).str.lower().map({
            "true": 1, "false": 0, "1": 1, "0": 0
        }).fillna(0).astype(int)
    return df

# ---------------------------
# Ensure Processed Folder Exists
# ---------------------------
os.makedirs("data/processed", exist_ok=True)

# ---------------------------
# Load Data
# ---------------------------
accounts = pd.read_csv("data/raw/accounts.csv")
subscriptions = pd.read_csv("data/raw/subscriptions.csv")
churn_events = pd.read_csv("data/raw/churn_events.csv")
feature_usage = pd.read_csv("data/raw/feature_usage.csv")

# ---------------------------
# Clean Column Names
# ---------------------------
accounts = clean_columns(accounts)
subscriptions = clean_columns(subscriptions)
churn_events = clean_columns(churn_events)
feature_usage = clean_columns(feature_usage)

# ---------------------------
# Convert Date Columns
# ---------------------------
date_columns = {
    "accounts": ["signup_date"],
    "subscriptions": ["start_date", "end_date"],
    "churn_events": ["churn_date"],
    "feature_usage": ["usage_date"]
}

for col in date_columns["accounts"]:
    accounts[col] = pd.to_datetime(accounts[col], errors='coerce')
for col in date_columns["subscriptions"]:
    subscriptions[col] = pd.to_datetime(subscriptions[col], errors='coerce')
for col in date_columns["churn_events"]:
    churn_events[col] = pd.to_datetime(churn_events[col], errors='coerce')
for col in date_columns["feature_usage"]:
    feature_usage[col] = pd.to_datetime(feature_usage[col], errors='coerce')

# ---------------------------
# Handle Missing Values
# ---------------------------
accounts.fillna({
    "industry": "Unknown",
    "country": "Unknown",
    "referral_source": "Unknown",
    "plan_tier": "Unknown"
}, inplace=True)

subscriptions.fillna({
    "mrr_amount": 0,
    "arr_amount": 0
}, inplace=True)

churn_events.fillna({
    "refund_amount_usd": 0,
    "reason_code": "Unknown"
}, inplace=True)

feature_usage.fillna({
    "usage_count": 0,
    "usage_duration_secs": 0,
    "error_count": 0
}, inplace=True)

# ---------------------------
# Convert Boolean Columns
# ---------------------------
accounts = convert_bool(accounts, ["is_trial", "churn_flag"])
subscriptions = convert_bool(subscriptions, [
    "is_trial", "upgrade_flag", "downgrade_flag",
    "churn_flag", "auto_renew_flag"
])
churn_events = convert_bool(churn_events, [
    "preceding_upgrade_flag", "preceding_downgrade_flag", "is_reactivation"
])
feature_usage = convert_bool(feature_usage, ["is_beta_feature"])

# ---------------------------
# Derived Columns
# ---------------------------

# Account Age (days)
accounts["account_age_days"] = (pd.Timestamp.today() - accounts["signup_date"]).dt.days

# Subscription Duration (days)
subscriptions["subscription_duration_days"] = (
    (subscriptions["end_date"] - subscriptions["start_date"]).dt.days
)

# Active Subscription Flag
subscriptions["is_active"] = subscriptions["end_date"].isna().astype(int)

# Calculated MRR (use mrr_amount, fallback to arr_amount / 12)
subscriptions["calculated_mrr"] = subscriptions["mrr_amount"].fillna(
    subscriptions["arr_amount"] / 12
)

# Ensure numeric type
subscriptions["calculated_mrr"] = pd.to_numeric(subscriptions["calculated_mrr"], errors="coerce").fillna(0)

# ---------------------------
# Save Cleaned Data
# ---------------------------
accounts.to_csv("data/processed/accounts_cleaned.csv", index=False)
subscriptions.to_csv("data/processed/subscriptions_cleaned.csv", index=False)
churn_events.to_csv("data/processed/churn_events_cleaned.csv", index=False)
feature_usage.to_csv("data/processed/feature_usage_cleaned.csv", index=False)

print("✅ Data cleaned and saved to data/processed/")