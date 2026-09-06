import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="InsightWorks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = pd.read_csv("hardware_companies_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.markdown("""
<style>
.stApp {
    background: #f5f7fb;
}
header {
    visibility: hidden;
}
#MainMenu {
    visibility: hidden;
}
footer {
    visibility: hidden;
}
[data-testid="stSidebar"] {
    background: #172b4d;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.logo {
    font-size: 27px;
    font-weight: 700;
    text-align: center;
    padding: 12px 0 30px 0;
    letter-spacing: 0.5px;
}
.logo span {
    color: #5b8def;
}
.menu-title {
    font-size: 11px;
    color: #aab6ca !important;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.main-title {
    font-size: 30px;
    font-weight: 700;
    color: #18243d;
}
.subtitle {
    color: #7e899e;
    font-size: 14px;
    margin-bottom: 22px;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e9f2;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
}
.card-label {
    color: #8a94a8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.card-value {
    color: #18243d;
    font-size: 26px;
    font-weight: 700;
    margin-top: 8px;
}
.panel {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e9f2;
    margin-top: 20px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.03);
}
.panel-title {
    color: #26334f;
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 4px;
}
.panel-subtitle {
    color: #929caf;
    font-size: 12px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        '<div class="logo">Insight<span>Works</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="menu-title">MAIN MENU</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "💰 Sales",
            "📦 Products",
            "🏢 Companies",
            "🌍 Regions",
            "📈 Analytics"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        '<div class="menu-title">FILTER DATA</div>',
        unsafe_allow_html=True
    )

    selected_company = st.multiselect(
        "Company",
        sorted(df["Company"].unique()),
        default=sorted(df["Company"].unique())
    )

    selected_category = st.multiselect(
        "Category",
        sorted(df["Category"].unique()),
        default=sorted(df["Category"].unique())
    )

    selected_region = st.multiselect(
        "Region",
        sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

data = df[
    df["Company"].isin(selected_company)
    & df["Category"].isin(selected_category)
    & df["Region"].isin(selected_region)
].copy()

if data.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

total_sales = data["Sales"].sum()
total_revenue = data["Revenue"].sum()
total_units = data["Quantity"].sum()
total_companies = data["Company"].nunique()

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">Sales & Revenue Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">InsightWorks | Hardware companies performance analysis</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-label">TOTAL SALES</div>
            <div class="card-value">${total_sales:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-label">TOTAL REVENUE</div>
            <div class="card-value">${total_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
            <div class="card-label">UNITS SOLD</div>
            <div class="card-value">{total_units:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="card">
            <div class="card-label">COMPANIES</div>
            <div class="card-value">{total_companies}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Revenue Trend</div>
        <div class="panel-subtitle">Monthly revenue performance</div>
    """, unsafe_allow_html=True)

    monthly = (
        data.set_index("Date")
        .resample("ME")["Revenue"]
        .sum()
    )

    st.line_chart(monthly, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">Regional Performance</div>
            <div class="panel-subtitle">Revenue by region</div>
        """, unsafe_allow_html=True)

        regional = (
            data.groupby("Region")["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(regional, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">Top Performing Products</div>
            <div class="panel-subtitle">Top products by revenue</div>
        """, unsafe_allow_html=True)

        products = (
            data.groupby("Product")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(7)
        )

        st.bar_chart(products, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

elif page == "💰 Sales":

    st.markdown(
        '<div class="main-title">Sales Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Detailed sales performance</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Sales", f"${total_sales:,.0f}")
    c2.metric("Total Revenue", f"${total_revenue:,.0f}")
    c3.metric("Units Sold", f"{total_units:,}")

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Monthly Sales</div>
        <div class="panel-subtitle">Sales trend over time</div>
    """, unsafe_allow_html=True)

    monthly_sales = (
        data.set_index("Date")
        .resample("ME")["Sales"]
        .sum()
    )

    st.line_chart(monthly_sales, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Sales by Category</div>
        <div class="panel-subtitle">Category-wise sales performance</div>
    """, unsafe_allow_html=True)

    category_sales = (
        data.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Sales Transactions</div>
        <div class="panel-subtitle">Detailed sales records</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        data.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📦 Products":

    st.markdown(
        '<div class="main-title">Product Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Product and category performance</div>',
        unsafe_allow_html=True
    )

    product_data = (
        data.groupby("Product")
        .agg(
            Revenue=("Revenue", "sum"),
            Sales=("Sales", "sum"),
            Units=("Quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Top Products</div>
        <div class="panel-subtitle">Products ranked by revenue</div>
    """, unsafe_allow_html=True)

    st.bar_chart(
        product_data["Revenue"].head(10),
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Product Performance</div>
        <div class="panel-subtitle">Revenue, sales and units</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        product_data,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    category_data = (
        data.groupby("Category")
        .agg(
            Revenue=("Revenue", "sum"),
            Sales=("Sales", "sum"),
            Units=("Quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Category Performance</div>
        <div class="panel-subtitle">Performance by category</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        category_data,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🏢 Companies":

    st.markdown(
        '<div class="main-title">Company Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Compare hardware companies</div>',
        unsafe_allow_html=True
    )

    company_data = (
        data.groupby("Company")
        .agg(
            Revenue=("Revenue", "sum"),
            Sales=("Sales", "sum"),
            Units=("Quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Company Revenue</div>
        <div class="panel-subtitle">Revenue generated by each company</div>
    """, unsafe_allow_html=True)

    st.bar_chart(
        company_data["Revenue"],
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Company Performance</div>
        <div class="panel-subtitle">Detailed company metrics</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        company_data,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    best_company = company_data["Revenue"].idxmax()

    st.success(
        f"🏆 Top-performing company: {best_company}"
    )

elif page == "🌍 Regions":

    st.markdown(
        '<div class="main-title">Regional Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Sales and revenue across regions</div>',
        unsafe_allow_html=True
    )

    region_data = (
        data.groupby("Region")
        .agg(
            Revenue=("Revenue", "sum"),
            Sales=("Sales", "sum"),
            Units=("Quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Revenue by Region</div>
        <div class="panel-subtitle">Regional revenue comparison</div>
    """, unsafe_allow_html=True)

    st.bar_chart(
        region_data["Revenue"],
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Regional Performance</div>
        <div class="panel-subtitle">Detailed regional metrics</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        region_data,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    best_region = region_data["Revenue"].idxmax()

    st.success(
        f"🌟 Best-performing region: {best_region}"
    )

elif page == "📈 Analytics":

    st.markdown(
        '<div class="main-title">Business Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Key insights from sales and revenue data</div>',
        unsafe_allow_html=True
    )

    average_transaction = data["Revenue"].mean()

    product_revenue = (
        data.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    company_revenue = (
        data.groupby("Company")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    region_revenue = (
        data.groupby("Region")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    best_product = product_revenue.idxmax()
    best_company = company_revenue.idxmax()
    best_region = region_revenue.idxmax()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Revenue",
        f"${average_transaction:,.2f}"
    )

    c2.metric(
        "Top Product",
        best_product
    )

    c3.metric(
        "Top Company",
        best_company
    )

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Revenue by Company</div>
        <div class="panel-subtitle">Company comparison</div>
    """, unsafe_allow_html=True)

    st.bar_chart(
        company_revenue,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Revenue by Category</div>
        <div class="panel-subtitle">Category contribution to revenue</div>
    """, unsafe_allow_html=True)

    category_revenue = (
        data.groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        category_revenue,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Key Business Insights</div>
        <div class="panel-subtitle">Automatically generated insights</div>
    """, unsafe_allow_html=True)

    st.write(f"🏆 **Top Company:** {best_company}")
    st.write(f"📦 **Top Product:** {best_product}")
    st.write(f"🌍 **Top Region:** {best_region}")
    st.write(f"💰 **Total Revenue:** ${total_revenue:,.0f}")
    st.write(f"💵 **Total Sales:** ${total_sales:,.0f}")
    st.write(f"📦 **Units Sold:** {total_units:,}")

    st.markdown("</div>", unsafe_allow_html=True)