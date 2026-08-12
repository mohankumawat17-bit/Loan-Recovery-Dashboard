import pandas as pd
import plotly.express as px

# -----------------------------
# Dashboard Theme
# -----------------------------

COLOR_SEQUENCE = [
    "#2563EB",  # Blue
    "#10B981",  # Green
    "#F59E0B",  # Orange
    "#EF4444",  # Red
    "#8B5CF6",  # Purple
    "#06B6D4"   # Cyan
]


def apply_layout(fig, title):
    """
    Apply a common professional layout to all charts.
    """
    fig.update_layout(
        title=title,
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title="",
        hovermode="x unified",
        font=dict(size=13),
        title_font=dict(size=18),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#E5E7EB")

    return fig


# ======================================================
# Monthly Recovery Trend
# ======================================================

def monthly_recovery_chart(df):

    temp = df.copy()

    temp["Month"] = (
        temp["Collection_Date"]
        .dt.to_period("M")
        .astype(str)
    )

    chart = (
        temp.groupby("Month")["Recovery_Amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        chart,
        x="Month",
        y="Recovery_Amount",
        markers=True,
        color_discrete_sequence=["#10B981"]
    )

    return apply_layout(
        fig,
        "Monthly Recovery Trend"
    )


# ======================================================
# Monthly Outstanding Trend
# ======================================================

def monthly_outstanding_chart(df):

    temp = df.copy()

    temp["Month"] = (
        temp["Collection_Date"]
        .dt.to_period("M")
        .astype(str)
    )

    chart = (
        temp.groupby("Month")["Outstanding_Amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        chart,
        x="Month",
        y="Outstanding_Amount",
        markers=True,
        color_discrete_sequence=["#2563EB"]
    )

    return apply_layout(
        fig,
        "Monthly Outstanding Trend"
    )


# ======================================================
# Recovery by Location
# ======================================================

def recovery_location_chart(df):

    chart = (
        df.groupby("Location")["Recovery_Amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Recovery_Amount",
            ascending=False
        )
    )

    fig = px.bar(
        chart,
        x="Location",
        y="Recovery_Amount",
        color="Recovery_Amount",
        color_continuous_scale="Blues"
    )

    return apply_layout(
        fig,
        "Recovery by Location"
    )


# ======================================================
# Recovery by SHO
# ======================================================

def recovery_sho_chart(df):

    chart = (
        df.groupby("SHO_Name")["Recovery_Amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Recovery_Amount",
            ascending=False
        )
    )

    fig = px.bar(
        chart,
        x="SHO_Name",
        y="Recovery_Amount",
        color="Recovery_Amount",
        color_continuous_scale="Greens"
    )

    return apply_layout(
        fig,
        "Recovery by SHO"
    )

# ======================================================
# Outstanding by Product
# ======================================================

def product_outstanding_chart(df):

    chart = (
        df.groupby("Product")["Outstanding_Amount"]
        .sum()
        .reset_index()
        .sort_values("Outstanding_Amount", ascending=False)
    )

    fig = px.bar(
        chart,
        x="Product",
        y="Outstanding_Amount",
        color="Outstanding_Amount",
        color_continuous_scale="Blues"
    )

    return apply_layout(fig, "Outstanding by Product")


# ======================================================
# Recovery Rate by Product
# ======================================================

def recovery_rate_product_chart(df):

    chart = (
        df.groupby("Product")[["Outstanding_Amount", "Recovery_Amount"]]
        .sum()
        .reset_index()
    )

    chart["Recovery_Rate"] = (
        chart["Recovery_Amount"] /
        chart["Outstanding_Amount"] * 100
    ).fillna(0)

    fig = px.bar(
        chart,
        x="Product",
        y="Recovery_Rate",
        color="Recovery_Rate",
        color_continuous_scale="Greens"
    )

    return apply_layout(fig, "Recovery Rate by Product")


# ======================================================
# Loan Status Distribution
# ======================================================

def loan_status_chart(df):

    chart = (
        df.groupby("Loan_Status")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        chart,
        names="Loan_Status",
        values="Count",
        hole=.45,
        color_discrete_sequence=COLOR_SEQUENCE
    )

    return apply_layout(fig, "Loan Status Distribution")


# ======================================================
# Bucket Wise Outstanding
# ======================================================

def bucket_outstanding_chart(df):

    chart = (
        df.groupby("Bucket")["Outstanding_Amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        chart,
        x="Bucket",
        y="Outstanding_Amount",
        color="Outstanding_Amount",
        color_continuous_scale="Oranges"
    )

    return apply_layout(fig, "Bucket Wise Outstanding")


# ======================================================
# Bucket Wise Recovery
# ======================================================

def bucket_recovery_chart(df):

    chart = (
        df.groupby("Bucket")["Recovery_Amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        chart,
        x="Bucket",
        y="Recovery_Amount",
        color="Recovery_Amount",
        color_continuous_scale="Greens"
    )

    return apply_layout(fig, "Bucket Wise Recovery")


# ======================================================
# DPD Distribution
# ======================================================

def dpd_distribution_chart(df):

    fig = px.histogram(
        df,
        x="DPD",
        nbins=25,
        color_discrete_sequence=["#2563EB"]
    )

    return apply_layout(fig, "DPD Distribution")

# ======================================================
# Top 10 Customers by Outstanding
# ======================================================

def top_customers_chart(df):

    chart = (
        df.groupby("Customer_Name")["Outstanding_Amount"]
        .sum()
        .reset_index()
        .sort_values("Outstanding_Amount", ascending=False)
        .head(10)
    )

    fig = px.bar(
        chart,
        x="Outstanding_Amount",
        y="Customer_Name",
        orientation="h",
        color="Outstanding_Amount",
        color_continuous_scale="Reds"
    )

    return apply_layout(fig, "Top 10 Customers by Outstanding")


# ======================================================
# Top 10 SHO by Recovery
# ======================================================

def top_sho_chart(df):

    chart = (
        df.groupby("SHO_Name")["Recovery_Amount"]
        .sum()
        .reset_index()
        .sort_values("Recovery_Amount", ascending=False)
        .head(10)
    )

    fig = px.bar(
        chart,
        x="Recovery_Amount",
        y="SHO_Name",
        orientation="h",
        color="Recovery_Amount",
        color_continuous_scale="Greens"
    )

    return apply_layout(fig, "Top 10 SHO by Recovery")