import streamlit as st
import pandas as pd
import math

# ---------------------------------------------------------
# PAGE
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------
df = pd.read_csv("hardware_companies_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background: #f7f9fc;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #101d4a;
    min-width: 235px;
    max-width: 235px;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 25px;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 700;
    padding: 5px 20px 35px 20px;
}

.menu-title {
    color: #8e9abb !important;
    font-size: 11px;
    font-weight: 600;
    padding: 0 20px 12px 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.menu-item {
    padding: 13px 20px;
    margin: 3px 10px;
    border-radius: 7px;
    font-size: 13px;
    color: #cbd3eb !important;
}

.menu-active {
    background: #24366f;
    color: white !important;
}

/* TOP BAR */
.topbar {
    height: 65px;
    background: white;
    border-bottom: 1px solid #e9edf5;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 25px;
    margin: -1rem -1rem 20px -1rem;
}

.top-title {
    font-size: 21px;
    font-weight: 600;
    color: #202b4c;
}

.top-right {
    color: #7e89a5;
    font-size: 13px;
}

/* PAGE */
.page-title {
    font-size: 25px;
    font-weight: 700;
    color: #202b4c;
    margin-bottom: 4px;
}

.page-subtitle {
    color: #8993aa;
    font-size: 12px;
    margin-bottom: 22px;
}

/* KPI CARDS */
.kpi-card {
    background: white;
    border: 1px solid #edf0f5;
    border-radius: 10px;
    padding: 19px 20px;
    height: 118px;
    box-shadow: 0 2px 8px rgba(31, 45, 80, 0.035);
}

.kpi-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.kpi-name {
    color: #8993aa;
    font-size: 11px;
    font-weight: 500;
}

.kpi-icon {
    width: 35px;
    height: 35px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}

.blue-icon {
    background: #e8f1ff;
}

.green-icon {
    background: #e7faf2;
}

.pink-icon {
    background: #fceafa;
}

.kpi-value {
    font-size: 24px;
    font-weight: 700;
    color: #202b4c;
    margin-top: 8px;
}

.kpi-small {
    font-size: 10px;
    color: #45bd8a;
    margin-left: 5px;
}

/* PANELS */
.panel {
    background: white;
    border: 1px solid #edf0f5;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(31, 45, 80, 0.035);
}

.panel-title {
    font-size: 14px;
    font-weight: 600;
    color: #283452;
    margin-bottom: 3px;
}

.panel-subtitle {
    font-size: 10px;
    color: #9aa3b8;
}

/* CHART */
.chart-area {
    width: 100%;
    overflow: hidden;
}

svg {
    width: 100%;
}

/* TABLE */
.data-box {
    background: white;
    border: 1px solid #edf0f5;
    border-radius: 10px;
    padding: 20px;
}

/* STREAMLIT SELECTBOX */
.stSelectbox label,
.stMultiSelect label {
    color: #68728c !important;
    font-size: 11px !important;
}

/* BUTTON */
.stButton button {
    background: #24366f;
    color: white;
    border: none;
    border-radius: 7px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:

    st.markdown('<div class="sidebar-title">Sales<span style="color:#4b8cff;">UI</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="menu-title">Main Menu</div>', unsafe_allow_html=True)

    st.markdown('<div class="menu-item menu-active">▣ &nbsp; Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">◉ &nbsp; Sales</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">▤ &nbsp; Products</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">◫ &nbsp; Companies</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">◌ &nbsp; Regions</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">⌁ &nbsp; Analytics</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="menu-title">General</div>', unsafe_allow_html=True)

    st.markdown('<div class="menu-item">⚙ &nbsp; Settings</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TOP BAR
# ---------------------------------------------------------
st.markdown("""
<div class="topbar">
    <div class="top-title">Dashboard</div>
    <div class="top-right">⌕ &nbsp;&nbsp; ♧ &nbsp;&nbsp; ●</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FILTERS
# ---------------------------------------------------------
st.markdown('<div class="page-title">Sales & Revenue Overview</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Hardware companies performance analysis</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    companies_filter = st.multiselect(
        "Company",
        sorted(df["Company"].unique()),
        default=sorted(df["Company"].unique())
    )

with f2:
    categories_filter = st.multiselect(
        "Category",
        sorted(df["Category"].unique()),
        default=sorted(df["Category"].unique())
    )

with f3:
    regions_filter = st.multiselect(
        "Region",
        sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

data = df[
    df["Company"].isin(companies_filter)
    & df["Category"].isin(categories_filter)
    & df["Region"].isin(regions_filter)
]

# ---------------------------------------------------------
# KPI
# ---------------------------------------------------------
total_sales = data["Sales"].sum()
total_revenue = data["Revenue"].sum()
total_units = data["Quantity"].sum()

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-name">TOTAL SALES</div>
            <div class="kpi-icon blue-icon">💰</div>
        </div>
        <div class="kpi-value">${total_sales:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-name">TOTAL REVENUE</div>
            <div class="kpi-icon green-icon">📈</div>
        </div>
        <div class="kpi-value">${total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-name">TOTAL UNITS SOLD</div>
            <div class="kpi-icon pink-icon">📦</div>
        </div>
        <div class="kpi-value">{total_units:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MONTHLY REVENUE
# ---------------------------------------------------------
monthly = (
    data.set_index("Date")
    .resample("ME")["Revenue"]
    .sum()
)

if len(monthly) > 0:

    values = monthly.values.tolist()
    labels = [x.strftime("%b") for x in monthly.index]

    width = 900
    height = 300

    max_val = max(values) if values else 1
    min_val = min(values) if values else 0

    points = []

    for i, value in enumerate(values):
        x = 40 + (i * (width - 80) / max(len(values) - 1, 1))
        y = 235 - ((value - min_val) / max(max_val - min_val, 1)) * 185
        points.append((x, y))

    point_string = " ".join(f"{x},{y}" for x, y in points)

    circles = ""
    label_text = ""

    for i, ((x, y), label) in enumerate(zip(points, labels)):
        circles += f'<circle cx="{x}" cy="{y}" r="4" fill="#4b8cff"/>'
        label_text += f'<text x="{x}" y="270" text-anchor="middle" fill="#9aa3b8" font-size="11">{label}</text>'

    grid = ""

    for y in [50, 95, 140, 185, 230]:
        grid += f'<line x1="40" y1="{y}" x2="860" y2="{y}" stroke="#edf0f5" stroke-width="1"/>'

    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Revenue Trend</div>
        <div class="panel-subtitle">Monthly revenue performance</div>

        <div class="chart-area">
        <svg viewBox="0 0 {width} {height}" preserveAspectRatio="none">

            {grid}

            <polyline
                points="{point_string}"
                fill="none"
                stroke="#4b8cff"
                stroke-width="3"
                stroke-linecap="round"
                stroke-linejoin="round"
            />

            {circles}
            {label_text}

        </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOWER DASHBOARD
# ---------------------------------------------------------
left, middle, right = st.columns([1.1, 1.2, 1.2])

# ---------------------------------------------------------
# TOP PRODUCTS
# ---------------------------------------------------------
with left:

    product_data = (
        data.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(6)
    )

    max_product = product_data.max() if len(product_data) else 1

    bars = ""

    for product, value in product_data.items():

        percentage = (value / max_product) * 100

        bars += f"""
        <div style="margin:15px 0;">
            <div style="
                display:flex;
                justify-content:space-between;
                font-size:10px;
                color:#737d97;
                margin-bottom:6px;">
                <span>{product}</span>
                <span>${value:,.0f}</span>
            </div>

            <div style="
                height:7px;
                background:#edf1f7;
                border-radius:10px;">

                <div style="
                    width:{percentage}%;
                    height:7px;
                    background:#4b8cff;
                    border-radius:10px;">
                </div>

            </div>
        </div>
        """

    st.markdown(f"""
    <div class="panel" style="height:370px;">
        <div class="panel-title">Top Performing Products</div>
        <div class="panel-subtitle">Products by revenue</div>
        {bars}
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# COMPANY REVENUE
# ---------------------------------------------------------
with middle:

    company_data = (
        data.groupby("Company")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(7)
    )

    max_company = company_data.max() if len(company_data) else 1

    company_bars = ""

    for company, value in company_data.items():

        percentage = (value / max_company) * 100

        company_bars += f"""
        <div style="margin:14px 0;">

            <div style="
                display:flex;
                justify-content:space-between;
                font-size:10px;
                color:#737d97;
                margin-bottom:5px;">

                <span>{company}</span>
                <span>${value:,.0f}</span>

            </div>

            <div style="
                height:7px;
                background:#edf1f7;
                border-radius:10px;">

                <div style="
                    width:{percentage}%;
                    height:7px;
                    background:#52c9a0;
                    border-radius:10px;">
                </div>

            </div>
        </div>
        """

    st.markdown(f"""
    <div class="panel" style="height:370px;">
        <div class="panel-title">Company Performance</div>
        <div class="panel-subtitle">Revenue by company</div>
        {company_bars}
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# REGIONAL DONUT
# ---------------------------------------------------------
with right:

    region_data = (
        data.groupby("Region")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    total_region = region_data.sum()

    if total_region > 0:

        first = region_data.iloc[0]
        first_percent = int((first / total_region) * 100)

        radius = 65
        circumference = 2 * math.pi * radius

        first_length = circumference * first_percent / 100

        st.markdown(f"""
        <div class="panel" style="height:370px;">

            <div class="panel-title">Regional Performance</div>
            <div class="panel-subtitle">Revenue distribution</div>

            <div style="
                display:flex;
                justify-content:center;
                align-items:center;
                margin-top:22px;
                margin-bottom:12px;">

                <svg width="170" height="170" viewBox="0 0 170 170">

                    <circle
                        cx="85"
                        cy="85"
                        r="{radius}"
                        fill="none"
                        stroke="#edf1f7"
                        stroke-width="22"/>

                    <circle
                        cx="85"
                        cy="85"
                        r="{radius}"
                        fill="none"
                        stroke="#4b8cff"
                        stroke-width="22"
                        stroke-dasharray="{first_length} {circumference}"
                        stroke-linecap="round"
                        transform="rotate(-90 85 85)"/>

                    <text
                        x="85"
                        y="80"
                        text-anchor="middle"
                        font-size="23"
                        font-weight="700"
                        fill="#202b4c">
                        {first_percent}%
                    </text>

                    <text
                        x="85"
                        y="100"
                        text-anchor="middle"
                        font-size="9"
                        fill="#9aa3b8">
                        {region_data.index[0]}
                    </text>

                </svg>

            </div>
        """, unsafe_allow_html=True)

        region_html = ""

        for region, value in region_data.items():

            percent = (value / total_region) * 100

            region_html += f"""
            <div style="
                display:flex;
                justify-content:space-between;
                margin:8px 8px;
                font-size:10px;
                color:#737d97;">

                <span>● &nbsp;{region}</span>
                <span>{percent:.0f}%</span>

            </div>
            """

        st.markdown(
            region_html + "</div>",
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------
st.markdown("""
<div class="data-box">
<div class="panel-title">Sales Data</div>
<div class="panel-subtitle">Detailed transaction records</div>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    data,
    use_container_width=True,
    hide_index=True
)