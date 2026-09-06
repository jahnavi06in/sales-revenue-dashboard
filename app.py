import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
df = pd.read_csv("sales_revenue_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Title
st.title("📊 Sales & Revenue Analysis Dashboard")
st.caption("Interactive dashboard for sales, revenue, products, categories and regional performance.")

# Sidebar filters
st.sidebar.header("🔎 Filters")

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

products = st.sidebar.multiselect(
    "Product",
    sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

filtered = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Product"].isin(products))
]

# KPIs
total_sales = filtered["Sales"].sum()
total_revenue = filtered["Revenue"].sum()
total_quantity = filtered["Quantity"].sum()
avg_revenue = filtered["Revenue"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Sales", f"${total_sales:,.0f}")
c2.metric("📈 Total Revenue", f"${total_revenue:,.0f}")
c3.metric("📦 Units Sold", f"{total_quantity:,}")
c4.metric("💵 Average Revenue", f"${avg_revenue:,.0f}")

st.divider()

# Revenue trend
st.subheader("📈 Revenue Trend")

monthly = (
    filtered.set_index("Date")
    .resample("ME")["Revenue"]
    .sum()
)

st.line_chart(monthly)

st.divider()

# Product and category charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Performing Products")

    top_products = (
        filtered.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_products)

with col2:
    st.subheader("📊 Sales by Category")

    category_sales = (
        filtered.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

st.divider()

# Regional performance
st.subheader("🌍 Regional Performance")

region_sales = (
    filtered.groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(region_sales)

st.divider()

# Data table
st.subheader("📋 Sales Data")

st.dataframe(
    filtered,
    use_container_width=True
)

st.success("Dashboard successfully loaded and ready for analysis!")