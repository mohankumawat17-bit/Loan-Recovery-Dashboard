import pandas as pd


# ==========================
# LOAD DATA
# ==========================

def load_data(file_path):
    """
    Load Excel file and perform basic cleaning.
    """

    df = pd.read_excel(file_path, engine="openpyxl")

    # Date
    df["Collection_Date"] = pd.to_datetime(
        df["Collection_Date"],
        errors="coerce"
    )

    # Numeric columns
    numeric_cols = [
        "Outstanding_Amount",
        "Recovery_Amount",
        "DPD"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    return df


# ==========================
# FILTER DATA
# ==========================

def filter_dataframe(
    df,
    location=None,
    sho=None,
    product=None,
    bucket=None,
    status=None,
    dpd_range=None,
    search=""
):

    filtered = df.copy()

    if location:
        filtered = filtered[
            filtered["Location"].isin(location)
        ]

    if sho:
        filtered = filtered[
            filtered["SHO_Name"].isin(sho)
        ]

    if product:
        filtered = filtered[
            filtered["Product"].isin(product)
        ]

    if bucket:
        filtered = filtered[
            filtered["Bucket"].isin(bucket)
        ]

    if status:
        filtered = filtered[
            filtered["Loan_Status"].isin(status)
        ]

    if dpd_range:
        filtered = filtered[
            (
                filtered["DPD"] >= dpd_range[0]
            ) &
            (
                filtered["DPD"] <= dpd_range[1]
            )
        ]

    if search:

        search = str(search).lower()

        filtered = filtered[
            filtered["Customer_Name"]
            .astype(str)
            .str.lower()
            .str.contains(search)
            |
            filtered["Customer_ID"]
            .astype(str)
            .str.lower()
            .str.contains(search)
        ]

    return filtered


# ==========================
# FORMAT CURRENCY
# ==========================

def format_currency(value):

    if value >= 10000000:
        return f"₹ {value/10000000:.2f} Cr"

    if value >= 100000:
        return f"₹ {value/100000:.2f} L"

    return f"₹ {value:,.0f}"


# ==========================
# KPI CALCULATIONS
# ==========================

def calculate_kpis(df):

    total_customers = df["Customer_ID"].nunique()

    total_outstanding = df["Outstanding_Amount"].sum()

    total_recovery = df["Recovery_Amount"].sum()

    recovery_pct = (
        total_recovery /
        total_outstanding * 100
        if total_outstanding > 0 else 0
    )

    avg_outstanding = df["Outstanding_Amount"].mean()

    avg_recovery = df["Recovery_Amount"].mean()

    avg_dpd = df["DPD"].mean()

    active_loans = (
        df["Loan_Status"]
        .astype(str)
        .str.lower()
        .eq("active")
        .sum()
    )

    closed_loans = (
        df["Loan_Status"]
        .astype(str)
        .str.lower()
        .eq("closed")
        .sum()
    )

    total_locations = df["Location"].nunique()

    total_sho = df["SHO_Name"].nunique()

    return {
        "customers": total_customers,
        "outstanding": total_outstanding,
        "recovery": total_recovery,
        "recovery_pct": recovery_pct,
        "avg_outstanding": avg_outstanding,
        "avg_recovery": avg_recovery,
        "avg_dpd": avg_dpd,
        "active": active_loans,
        "closed": closed_loans,
        "locations": total_locations,
        "sho": total_sho
    }


# ==========================
# BUSINESS INSIGHTS
# ==========================

def get_business_insights(df):

    top_sho = (
        df.groupby("SHO_Name")["Recovery_Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    worst_location = (
        df.groupby("Location")["Recovery_Amount"]
        .sum()
        .sort_values()
        .head(1)
    )

    risky_bucket = (
        df.groupby("Bucket")["Outstanding_Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    high_risk = df[df["DPD"] > 90]

    return {
        "top_sho": top_sho,
        "worst_location": worst_location,
        "risky_bucket": risky_bucket,
        "high_risk": high_risk
    }


# ==========================
# TOP TABLES
# ==========================

def top_defaulters(df, n=10):

    return (
        df.sort_values(
            "Outstanding_Amount",
            ascending=False
        )
        .head(n)
    )


def highest_recovery(df, n=10):

    return (
        df.sort_values(
            "Recovery_Amount",
            ascending=False
        )
        .head(n)
    )


def high_risk_customers(df):

    return df[df["DPD"] > 90]

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

def get_business_insights(df):

    insights = {}

    # Top Performer SHO
    top_sho = (
        df.groupby("SHO_Name")["Recovery_Amount"]
        .sum()
        .idxmax()
    )

    # Worst Location
    worst_location = (
        df.groupby("Location")["Recovery_Amount"]
        .sum()
        .idxmin()
    )

    # Highest Recovery Location
    best_location = (
        df.groupby("Location")["Recovery_Amount"]
        .sum()
        .idxmax()
    )

    # Most Risky Bucket
    risky_bucket = (
        df.groupby("Bucket")["Outstanding_Amount"]
        .sum()
        .idxmax()
    )

    insights["top_sho"] = top_sho
    insights["worst_location"] = worst_location
    insights["best_location"] = best_location
    insights["risky_bucket"] = risky_bucket

    return insights