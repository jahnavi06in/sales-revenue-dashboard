import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SalesUI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DATA ----------------
df = pd.read_csv("hardware_companies_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------------- STYLE ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:#f5f7fb;
}

header, footer, #MainMenu {
    visibility:hidden;
}

[data-testid="stSidebar"] {
    background:#111d4b;
    width:235px !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top:25px;
}

[data-testid="stSidebar"] * {
    color:white !important;
}

.brand {
    font-size:25px;
    font-weight:700;
    padding:5px 15px 35px;
}

.brand span {
    color:#4b8cff;
}

.menu-label {
    color:#8995b5 !important;
    font-size:10px;
    font-weight:600;
    letter-spacing:1px;
    margin:0 15px 10px;
}

.menu {
    padding:12px 15px;
    margin:4px 8px;
    border-radius:7px;
    font-size:13px;
    color:#cbd3e8 !important;
}

.menu.active {
    background:#26386f;
    color:white !important;
}

.top {
    background:white;
    height:60px;
    margin:-1rem -1rem 25px;
    padding:0 25px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    border-bottom:1px solid #e9edf4;
}

.top-title {
    font-size:20px;
    font-weight:600;
    color:#202b4c;
}

.top-icons {
    color:#8993a9;
    font-size:14px;
}

.heading {
    color:#202b4c;
    font-size:27px;
    font-weight:700;
    margin-bottom:3px;
}

.subheading {
    color:#929caf;
    font-size:12px;
    margin-bottom:20px;
}

.card {
    background:#ffffff;
    border:1px solid #e9edf4;
    border-radius:10px;
    padding:19px 21px;
    min-height:112px;
    box-shadow:0 2px 10px rgba(30,45,80,.04);
}

.card-label {
    color:#929caf;
    font-size:10px;
    font-weight:600;
    letter-spacing:.3px;
}

.card-value {
    color:#202b4c;
    font-size:25px;
    font-weight:700;
    margin-top:10px;
}

.card-icon {
    float:right;
    font-size:18px;
}

.panel {
    background:white;
    border:1px solid #e9edf4;
    border-radius:10px;
    padding:19px;
    box-shadow:0 2px 10px rgba(30,45,80,.04);
}

.panel-title {
    color:#26324f;
    font-size:14px;
    font-weight:600;
}

.panel-subtitle {
    color:#9aa3b6;
    font-size:10px;
    margin-top:3px;
    margin-bottom:12px;
}

.stMultiSelect label {
    font-size:11px !important;
    color:#68738b !important;
}

div[data-baseweb="select"] {
    border-radius:7px;
}

.stDataFrame {
    border-radius:10px;
}

section[data-testid="stSidebar"] .stMarkdown {
    margin-bottom:0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown(
        '<div class="brand">Sales<span>UI</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="menu-label">MAIN MENU</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="menu active">▣ &nbsp; Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu">◉ &nbsp; Sales</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu">▤ &nbsp; Products</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu">◫ &nbsp; Companies</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu">◌ &nbsp; Regions</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu">⌁ &nbsp; Analytics</div>', unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="menu-label">GENERAL</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="menu">⚙ &nbsp; Settings</div>', unsafe_allow_html=True)

# ---------------- TOP BAR ----------------
st.markdown("""
<div class="top">
    <div class="top-title">Dashboard</div>
    <div class="top-icons">⌕ &nbsp;&nbsp; ◇ &nbsp;&nbsp; ●</div>
</div>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<div class="heading">Sales & Revenue Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subheading">Hardware companies performance analysis</div>',
    unsafe_allow_html=True
)

# ---------------- FILTERS ----------------
f1, f2, f3 = st.columns(3)

with f1:
    companies = st.multiselect(
        "Company",
        sorted(df["Company"].unique()),
        default=sorted(df["Company"].unique())
    )

with f2:
    categories = st.multiselect(
        "Category",
        sorted(df["Category"].unique()),
        default=sorted(df["Category"].unique())
    )

with f3:
    regions = st.multiselect(
        "Region",
        sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

data = df[
    df["Company"].isin(companies) &
    df["Category"].isin(categories) &
    df["Region"].isin(regions)
]

# ---------------- KPI ----------------
total_sales = data["Sales"].sum()
total_revenue = data["Revenue"].sum()
total_units = data["Quantity"].sum()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="card">
        <span class="card-icon">💰</span>
        <div class="card-label">TOTAL SALES</div>
        <div class="card-value">${total_sales:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
        <span class="card-icon">📈</span>
        <div class="card-label">TOTAL REVENUE</div>
        <div class="card-value">${total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
        <span class="card-icon">📦</span>
        <div class="card-label">UNITS SOLD</div>
        <div class="card-value">{total_units:,}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="card">
        <span class="card-icon">🏢</span>
        <div class="card-label">COMPANIES</div>
        <div class="card-value">{data["Company"].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- REVENUE + REGION ----------------
left, right = st.columns([1.65, 1])

with left:

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

    st.line_chart(
        monthly,
        height=310,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Regional Performance</div>
        <div class="panel-subtitle">Revenue distribution by region</div>
    """, unsafe_allow_html=True)

    regional = (
        data.groupby("Region")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        regional,
        height=310,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ---------------- LOWER PANELS ----------------
p1, p2, p3 = st.columns(3)

with p1:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Top Performing Products</div>
        <div class="panel-subtitle">Products ranked by revenue</div>
    """, unsafe_allow_html=True)

    products = (
        data.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(7)
    )

    st.bar_chart(
        products,
        height=270,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

with p2:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Company Performance</div>
        <div class="panel-subtitle">Revenue generated by company</div>
    """, unsafe_allow_html=True)

    company_data = (
        data.groupby("Company")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        company_data,
        height=270,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

with p3:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Sales by Category</div>
        <div class="panel-subtitle">Category-wise sales performance</div>
    """, unsafe_allow_html=True)

    category_data = (
        data.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        category_data,
        height=270,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ---------------- TABLE ----------------
st.markdown("""
<div class="panel">
    <div class="panel-title">Sales Data</div>
    <div class="panel-subtitle">Detailed transaction records</div>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    data,
    use_container_width=True,
    hide_index=True
)