import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("hardware_companies_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {font-family:Inter,sans-serif;}

.stApp {background:#f6f8fc;}

[data-testid="stSidebar"] {
    background:#111d4b;
}

[data-testid="stSidebar"] * {
    color:white;
}

.title {
    font-size:28px;
    font-weight:700;
    color:#202b4c;
}

.subtitle {
    color:#8d97aa;
    font-size:13px;
    margin-bottom:20px;
}

.card {
    background:white;
    padding:22px;
    border-radius:12px;
    border:1px solid #edf0f5;
    box-shadow:0 3px 12px rgba(30,45,80,.05);
}

.label {
    color:#8d97aa;
    font-size:11px;
    font-weight:600;
}

.value {
    color:#202b4c;
    font-size:25px;
    font-weight:700;
    margin-top:8px;
}

.box {
    background:white;
    padding:20px;
    border-radius:12px;
    border:1px solid #edf0f5;
    box-shadow:0 3px 12px rgba(30,45,80,.05);
}

.box h3 {
    color:#202b4c;
    font-size:15px;
    margin:0;
}

.box p {
    color:#9aa3b5;
    font-size:11px;
}

.side-title {
    font-size:24px;
    font-weight:700;
    padding:15px 10px 35px;
}

.side-item {
    padding:13px;
    margin:4px 0;
    border-radius:8px;
    color:#cbd3ea !important;
}

.active {
    background:#263970;
    color:white !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        '<div class="side-title">Sales<span style="color:#4b8cff">UI</span></div>',
        unsafe_allow_html=True
    )

    st.caption("MAIN MENU")

    st.markdown('<div class="side-item active">▣  Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-item">◉  Sales</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-item">▤  Products</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-item">◫  Companies</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-item">◌  Regions</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-item">⌁  Analytics</div>', unsafe_allow_html=True)

    st.write("")
    st.caption("GENERAL")
    st.markdown('<div class="side-item">⚙  Settings</div>', unsafe_allow_html=True)

st.markdown('<div class="title">Sales & Revenue Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Hardware companies sales performance overview</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    company = st.multiselect(
        "Company",
        sorted(df["Company"].unique()),
        default=sorted(df["Company"].unique())
    )

with f2:
    category = st.multiselect(
        "Category",
        sorted(df["Category"].unique()),
        default=sorted(df["Category"].unique())
    )

with f3:
    region = st.multiselect(
        "Region",
        sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

data = df[
    df["Company"].isin(company) &
    df["Category"].isin(category) &
    df["Region"].isin(region)
]

sales = data["Sales"].sum()
revenue = data["Revenue"].sum()
units = data["Quantity"].sum()

a, b, c = st.columns(3)

with a:
    st.markdown(f"""
    <div class="card">
    <div class="label">TOTAL SALES</div>
    <div class="value">${sales:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="card">
    <div class="label">TOTAL REVENUE</div>
    <div class="value">${revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="card">
    <div class="label">UNITS SOLD</div>
    <div class="value">{units:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

left, right = st.columns([1.7, 1])

with left:
    st.markdown("""
    <div class="box">
    <h3>Revenue Trend</h3>
    <p>Monthly revenue performance</p>
    """, unsafe_allow_html=True)

    monthly = data.set_index("Date").resample("ME")["Revenue"].sum()
    st.line_chart(monthly, height=300)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="box">
    <h3>Regional Performance</h3>
    <p>Revenue by region</p>
    """, unsafe_allow_html=True)

    regional = data.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
    st.bar_chart(regional, height=300)

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

left, middle, right = st.columns(3)

with left:
    st.markdown("""
    <div class="box">
    <h3>Top Products</h3>
    <p>Best performing products</p>
    """, unsafe_allow_html=True)

    products = data.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(7)
    st.bar_chart(products)

    st.markdown("</div>", unsafe_allow_html=True)

with middle:
    st.markdown("""
    <div class="box">
    <h3>Company Performance</h3>
    <p>Revenue by company</p>
    """, unsafe_allow_html=True)

    companies = data.groupby("Company")["Revenue"].sum().sort_values(ascending=False)
    st.bar_chart(companies)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="box">
    <h3>Sales by Category</h3>
    <p>Category performance</p>
    """, unsafe_allow_html=True)

    categories = data.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    st.bar_chart(categories)

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

st.markdown("""
<div class="box">
<h3>Sales Data</h3>
<p>Detailed sales and revenue records</p>
</div>
""", unsafe_allow_html=True)

st.dataframe(data, use_container_width=True, hide_index=True)