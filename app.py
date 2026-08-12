from charts import (
    monthly_recovery_chart,
    monthly_outstanding_chart,
    recovery_location_chart,
    recovery_sho_chart,
    product_outstanding_chart,
    recovery_rate_product_chart,
    loan_status_chart,
    bucket_outstanding_chart,
    bucket_recovery_chart,
    dpd_distribution_chart,
    top_customers_chart,
    top_sho_chart,
)
# ==========================================================
# Loan Recovery Dashboard
# ==========================================================

import streamlit as st
import pandas as pd

from utils import (
    load_data,
    filter_dataframe,
    calculate_kpis,
    get_business_insights,
    format_currency
)

from charts import (
    monthly_recovery_chart,
    monthly_outstanding_chart,
    recovery_location_chart,
    recovery_sho_chart
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Loan Recovery Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LOAD CSS
# ==========================================================

try:
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def get_data():
    return load_data("data/loan_data.xlsx")

df = get_data()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image(
        "assets/logo.png",
        width=170
    )

    st.title("Loan Recovery Dashboard")

    st.markdown("---")

    locations = st.multiselect(
        "Location",
        sorted(df["Location"].dropna().unique())
    )

    shos = st.multiselect(
        "SHO Name",
        sorted(df["SHO_Name"].dropna().unique())
    )

    products = st.multiselect(
        "Product",
        sorted(df["Product"].dropna().unique())
    )

    buckets = st.multiselect(
        "Bucket",
        sorted(df["Bucket"].dropna().unique())
    )

    status = st.multiselect(
        "Loan Status",
        sorted(df["Loan_Status"].dropna().unique())
    )

    dpd = st.slider(
        "DPD Range",
        int(df["DPD"].min()),
        int(df["DPD"].max()),
        (
            int(df["DPD"].min()),
            int(df["DPD"].max())
        )
    )

    customer = st.text_input(
        "Search Customer"
    )

    st.markdown("---")

    if st.button("Reset Filters"):

        st.rerun()

# ==========================================================
# FILTER DATA
# ==========================================================

filtered_df = filter_dataframe(
    df,
    location=locations,
    sho=shos,
    product=products,
    bucket=buckets,
    status=status,
    dpd_range=dpd,
    search=customer
)

# ==========================================================
# HEADER
# ==========================================================

st.title("📊 Loan Recovery Analytics Dashboard")

st.caption(
    "Interactive Banking & NBFC Recovery Dashboard"
)

st.markdown("---")

# ==========================================================
# KPI SECTION
# ==========================================================

kpis = calculate_kpis(filtered_df)

st.subheader("📈 Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "👥 Total Customers",
        f"{kpis['customers']:,}"
    )

with c2:
    st.metric(
        "💰 Outstanding",
        format_currency(kpis["outstanding"])
    )

with c3:
    st.metric(
        "✅ Recovery",
        format_currency(kpis["recovery"])
    )

with c4:
    st.metric(
        "📊 Recovery %",
        f"{kpis['recovery_pct']:.2f}%"
    )

with c5:
    st.metric(
        "📅 Avg DPD",
        f"{kpis['avg_dpd']:.0f}"
    )


c6, c7, c8, c9, c10, c11 = st.columns(6)

with c6:
    st.metric(
        "📦 Avg Outstanding",
        format_currency(kpis["avg_outstanding"])
    )

with c7:
    st.metric(
        "💵 Avg Recovery",
        format_currency(kpis["avg_recovery"])
    )

with c8:
    st.metric(
        "🟢 Active Loans",
        kpis["active"]
    )

with c9:
    st.metric(
        "🔵 Closed Loans",
        kpis["closed"]
    )

with c10:
    st.metric(
        "📍 Locations",
        kpis["locations"]
    )

with c11:
    st.metric(
        "👨‍💼 SHO",
        kpis["sho"]
    )

st.markdown("---")

# ==========================================================
# CHARTS
# ==========================================================

st.subheader("📊 Dashboard Analytics")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        monthly_recovery_chart(filtered_df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        monthly_outstanding_chart(filtered_df),
        use_container_width=True
    )

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        recovery_location_chart(filtered_df),
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        recovery_sho_chart(filtered_df),
        use_container_width=True
    )

st.markdown("---")

col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(
        product_outstanding_chart(filtered_df),
        use_container_width=True
    )

with col6:
    st.plotly_chart(
        recovery_rate_product_chart(filtered_df),
        use_container_width=True
    )

col7, col8 = st.columns(2)

with col7:
    st.plotly_chart(
        loan_status_chart(filtered_df),
        use_container_width=True
    )

with col8:
    st.plotly_chart(
        bucket_recovery_chart(filtered_df),
        use_container_width=True
    )

col9, col10 = st.columns(2)

with col9:
    st.plotly_chart(
        bucket_outstanding_chart(filtered_df),
        use_container_width=True
    )

with col10:
    st.plotly_chart(
        dpd_distribution_chart(filtered_df),
        use_container_width=True
    )

st.markdown("---")

# ==========================================================
# TOP ANALYSIS
# ==========================================================

st.subheader("🏆 Top Performance Analysis")

col11, col12 = st.columns(2)

with col11:
    st.plotly_chart(
        top_customers_chart(filtered_df),
        use_container_width=True
    )

with col12:
    st.plotly_chart(
        top_sho_chart(filtered_df),
        use_container_width=True
    )

st.markdown("---")

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

st.subheader("💡 Business Insights")

insights = get_business_insights(filtered_df)

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"🏆 Top Performer SHO : {insights['top_sho']}"
    )

    st.info(
        f"📍 Highest Recovery Location : {insights['best_location']}"
    )

with col2:

    st.warning(
        f"⚠️ Worst Performing Location : {insights['worst_location']}"
    )

    st.error(
        f"🚨 Most Risky Bucket : {insights['risky_bucket']}"
    )

st.markdown("---")

# ==========================================================
# HIGH RISK CUSTOMERS
# ==========================================================

st.subheader("🚨 High Risk Customers (DPD > 90)")

high_risk = filtered_df[filtered_df["DPD"] > 90]

st.dataframe(
    high_risk,
    use_container_width=True,
    height=350
)

# ==========================================================
# TOP DEFAULTERS
# ==========================================================

st.subheader("❌ Top 10 Defaulters")

top_defaulters = (
    filtered_df
    .sort_values(
        "Outstanding_Amount",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_defaulters,
    use_container_width=True
)

# ==========================================================
# HIGHEST RECOVERY
# ==========================================================

st.subheader("🏆 Highest Recovery Customers")

highest_recovery = (
    filtered_df
    .sort_values(
        "Recovery_Amount",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    highest_recovery,
    use_container_width=True
)

# ==========================================================
# COMPLETE DATA
# ==========================================================

st.subheader("📋 Detailed Transaction Table")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

# ==========================================================
# DOWNLOAD CSV
# ==========================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="Loan_Recovery_Data.csv",
    mime="text/csv"
)