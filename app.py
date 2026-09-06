import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="InsightWorks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = pd.read_csv("sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.markdown("""
<style>
.stApp {
    background: #f4f6fa;
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
    background: #17345f;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.logo {
    font-size: 28px;
    font-weight: 700;
    text-align: center;
    padding: 12px 0 28px;
}

.logo span {
    color: #61a0ff;
}

.side-title {
    font-size: 11px;
    letter-spacing: 1px;
    color: #aebbd0 !important;
    font-weight: 600;
    margin-bottom: 10px;
}

.page-title {
    font-size: 30px;
    font-weight: 700;
    color: #17233d;
}

.page-subtitle {
    font-size: 13px;
    color: #7e899e;
    margin-bottom: 22px;
}

.kpi {
    background: white;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #e4e8f0;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
}

.kpi-name {
    color: #8a94a8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .5px;
}

.kpi-value {
    color: #17233d;
    font-size: 25px;
    font-weight: 700;
    margin-top: 7px;
}

.box {
    background: white;
    border-radius: 12px;
    padding: 18px;
    border: 1px solid #e4e8f0;
    box-shadow: 0 3px 12px rgba(0,0,0,0.035);
    margin-top: 20px;
}

.box-title {
    color: #26334e;
    font-size: 16px;
    font-weight: 600;
}

.box-subtitle {
    color: #929bad;
    font-size: 11px;
    margin-bottom: 12px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.markdown(
        '<div class="logo">Insight<span>Works</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-title">MAIN MENU</div>',
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
        '<div class="side-title">FILTERS</div>',
        unsafe_allow_html=True
    )

    companies = st.multiselect(
        "Company",
        sorted(df["Company"].unique()),
        default=sorted(df["Company"].unique())
    )

    categories = st.multiselect(
        "Category",
        sorted(df["Category"].unique()),
        default=sorted(df["Category"].unique())
    )

    regions = st.multiselect(
        "Region",
        sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

data = df[
    df["Company"].isin(companies)
    & df["Category"].isin(categories)
    & df["Region"].isin(regions)
].copy()

if data.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

total_sales = data["Sales"].sum()
total_revenue = data["Revenue"].sum()
total_units = data["Quantity"].sum()
company_count = data["Company"].nunique()

data["Month"] = data["Date"].dt.to_period("M").astype(str)

monthly = (
    data.groupby("Month")
    .agg(
        Sales=("Sales", "sum"),
        Revenue=("Revenue", "sum")
    )
    .reset_index()
)

regional = (
    data.groupby("Region")["Revenue"]
    .sum()
    .reset_index()
)

products = (
    data.groupby("Product")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
    .head(8)
)

company_data = (
    data.groupby("Company")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

category_data = (
    data.groupby("Category")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="page-title">Sales & Revenue Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">InsightWorks • Hardware business performance dashboard</div>',
        unsafe_allow_html=True
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-name">TOTAL SALES</div>
            <div class="kpi-value">${total_sales:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-name">TOTAL REVENUE</div>
            <div class="kpi-value">${total_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-name">UNITS SOLD</div>
            <div class="kpi-value">{total_units:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-name">COMPANIES</div>
            <div class="kpi-value">{company_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="box">
        <div class="box-title">Monthly Sales & Revenue</div>
        <div class="box-subtitle">Performance across the selected period</div>
    """, unsafe_allow_html=True)

    chart = alt.Chart(monthly).transform_fold(
        ["Sales", "Revenue"],
        as_=["Metric", "Value"]
    ).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4
    ).encode(
        x=alt.X(
            "Month:N",
            sort=list(monthly["Month"]),
            title=None,
            axis=alt.Axis(labelAngle=-45)
        ),
        y=alt.Y(
            "Value:Q",
            title="Amount"
        ),
        color=alt.Color(
            "Metric:N",
            title=None
        ),
        tooltip=[
            alt.Tooltip("Month:N", title="Month"),
            alt.Tooltip("Metric:N", title="Metric"),
            alt.Tooltip("Value:Q", title="Amount", format=",.0f")
        ]
    ).properties(height=330)

    st.altair_chart(chart, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])

    with left:

        st.markdown("""
        <div class="box">
            <div class="box-title">Revenue Trend</div>
            <div class="box-subtitle">Monthly revenue movement</div>
        """, unsafe_allow_html=True)

        area_chart = alt.Chart(monthly).mark_area(
            opacity=0.65,
            line=True
        ).encode(
            x=alt.X(
                "Month:N",
                sort=list(monthly["Month"]),
                title=None,
                axis=alt.Axis(labelAngle=-45)
            ),
            y=alt.Y(
                "Revenue:Q",
                title="Revenue"
            ),
            tooltip=[
                alt.Tooltip("Month:N", title="Month"),
                alt.Tooltip(
                    "Revenue:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        ).properties(height=280)

        st.altair_chart(
            area_chart,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown("""
        <div class="box">
            <div class="box-title">Regional Revenue</div>
            <div class="box-subtitle">Revenue distribution by region</div>
        """, unsafe_allow_html=True)

        donut = alt.Chart(regional).mark_arc(
            innerRadius=65,
            outerRadius=105
        ).encode(
            theta=alt.Theta(
                "Revenue:Q",
                stack=True
            ),
            color=alt.Color(
                "Region:N",
                title="Region"
            ),
            tooltip=[
                alt.Tooltip("Region:N", title="Region"),
                alt.Tooltip(
                    "Revenue:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        ).properties(height=280)

        st.altair_chart(
            donut,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="box">
        <div class="box-title">Top Performing Products</div>
        <div class="box-subtitle">Products ranked by revenue</div>
    """, unsafe_allow_html=True)

    product_chart = alt.Chart(products).mark_bar(
        cornerRadiusEnd=5
    ).encode(
        x=alt.X(
            "Revenue:Q",
            title="Revenue"
        ),
        y=alt.Y(
            "Product:N",
            sort="-x",
            title=None
        ),
        tooltip=[
            alt.Tooltip("Product:N", title="Product"),
            alt.Tooltip(
                "Revenue:Q",
                title="Revenue",
                format=",.0f"
            )
        ]
    ).properties(height=300)

    st.altair_chart(
        product_chart,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "💰 Sales":

    st.markdown(
        '<div class="page-title">Sales Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Detailed sales performance and trends</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    a.metric("Total Sales", f"${total_sales:,.0f}")
    b.metric("Total Revenue", f"${total_revenue:,.0f}")
    c.metric("Units Sold", f"{total_units:,}")

    st.markdown("""
    <div class="box">
        <div class="box-title">Sales Trend</div>
        <div class="box-subtitle">Monthly sales performance</div>
    """, unsafe_allow_html=True)

    sales_chart = alt.Chart(monthly).mark_line(
        point=True
    ).encode(
        x=alt.X(
            "Month:N",
            sort=list(monthly["Month"]),
            title=None,
            axis=alt.Axis(labelAngle=-45)
        ),
        y=alt.Y(
            "Sales:Q",
            title="Sales"
        ),
        tooltip=[
            alt.Tooltip("Month:N", title="Month"),
            alt.Tooltip(
                "Sales:Q",
                title="Sales",
                format=",.0f"
            )
        ]
    ).properties(height=350)

    st.altair_chart(
        sales_chart,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="box">
        <div class="box-title">Sales by Category</div>
        <div class="box-subtitle">Category-wise sales performance</div>
    """, unsafe_allow_html=True)

    sales_category = (
        data.groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    category_chart = alt.Chart(sales_category).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X("Category:N", title=None),
        y=alt.Y("Sales:Q", title="Sales"),
        tooltip=[
            alt.Tooltip("Category:N", title="Category"),
            alt.Tooltip(
                "Sales:Q",
                title="Sales",
                format=",.0f"
            )
        ]
    ).properties(height=320)

    st.altair_chart(
        category_chart,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="box">
        <div class="box-title">Transaction Data</div>
        <div class="box-subtitle">Filtered sales records</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        data.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📦 Products":

    st.markdown(
        '<div class="page-title">Product Performance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Product revenue and sales analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="box">
        <div class="box-title">Top Products by Revenue</div>
        <div class="box-subtitle">Highest revenue-generating products</div>
    """, unsafe_allow_html=True)

    product_chart = alt.Chart(products).mark_bar(
        cornerRadiusEnd=6
    ).encode(
        x=alt.X(
            "Revenue:Q",
            title="Revenue"
        ),
        y=alt.Y(
            "Product:N",
            sort="-x",
            title=None
        ),
        tooltip=[
            alt.Tooltip("Product:N", title="Product"),
            alt.Tooltip(
                "Revenue:Q",
                title="Revenue",
                format=",.0f"
            )
        ]
    ).properties(height=380)

    st.altair_chart(
        product_chart,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="box">
        <div class="box-title">Product Performance Table</div>
        <div class="box-subtitle">Revenue, sales and units sold</div>
    """, unsafe_allow_html=True)

    product_table = (
        data.groupby("Product")
        .agg(
            Revenue=("Revenue", "sum"),
            Sales=("Sales", "sum"),
            Units=("Quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    st.dataframe(
        product_table,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🏢 Companies":

    st.markdown(
        '<div class="page-title">Company Performance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Compare hardware companies by revenue</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="box">
        <div class="box-title">Company Revenue</div>
        <div class="box-subtitle">Revenue comparison across companies</div>
    """, unsafe_allow_html=True)

    company_chart = alt.Chart(company_data).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X(
            "Company:N",
            title=None,
            sort="-y"
        ),
        y=alt.Y(
            "Revenue:Q",
            title="Revenue"
        ),
        tooltip=[
            alt.Tooltip("Company:N", title="Company"),
            alt.Tooltip(
                "Revenue:Q",
                title="Revenue",
                format=",.0f"
            )
        ]
    ).properties(height=380)

    st.altair_chart(
        company_chart,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="box">
        <div class="box-title">Company Ranking</div>
        <div class="box-subtitle">Performance details</div>
    """, unsafe_allow_html=True)

    company_table = (
        data.groupby("Company")
        .agg(
            Revenue=("Revenue", "sum"),
            Sales=("Sales", "sum"),
            Units=("Quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    st.dataframe(
        company_table,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    best_company = company_table.index[0]

    st.success(
        f"🏆 Leading company: {best_company}"
    )

elif page == "🌍 Regions":

    st.markdown(
        '<div class="page-title">Regional Performance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Revenue and sales distribution across regions</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        st.markdown("""
        <div class="box">
            <div class="box-title">Regional Revenue</div>
            <div class="box-subtitle">Revenue distribution</div>
        """, unsafe_allow_html=True)

        donut = alt.Chart(regional).mark_arc(
            innerRadius=70,
            outerRadius=120
        ).encode(
            theta=alt.Theta("Revenue:Q"),
            color=alt.Color("Region:N", title="Region"),
            tooltip=[
                alt.Tooltip("Region:N", title="Region"),
                alt.Tooltip(
                    "Revenue:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        ).properties(height=350)

        st.altair_chart(
            donut,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown("""
        <div class="box">
            <div class="box-title">Regional Comparison</div>
            <div class="box-subtitle">Revenue by region</div>
        """, unsafe_allow_html=True)

        region_bar = alt.Chart(regional).mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x=alt.X("Region:N", title=None),
            y=alt.Y("Revenue:Q", title="Revenue"),
            tooltip=[
                alt.Tooltip("Region:N", title="Region"),
                alt.Tooltip(
                    "Revenue:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        ).properties(height=350)

        st.altair_chart(
            region_bar,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    region_table = (
        data.groupby("Region")
        .agg(
            Revenue=("Revenue", "sum"),
            Sales=("Sales", "sum"),
            Units=("Quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    st.markdown("""
    <div class="box">
        <div class="box-title">Regional Performance Table</div>
        <div class="box-subtitle">Detailed regional metrics</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        region_table,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📈 Analytics":

    st.markdown(
        '<div class="page-title">Business Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Key business insights from the selected data</div>',
        unsafe_allow_html=True
    )

    best_product = products.iloc[0]["Product"]
    best_company = company_data.iloc[0]["Company"]
    best_region = regional.sort_values(
        "Revenue",
        ascending=False
    ).iloc[0]["Region"]

    average_revenue = data["Revenue"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average Revenue",
        f"${average_revenue:,.0f}"
    )

    c2.metric(
        "Top Product",
        best_product
    )

    c3.metric(
        "Top Company",
        best_company
    )

    c4.metric(
        "Top Region",
        best_region
    )

    st.markdown("""
    <div class="box">
        <div class="box-title">Company Revenue Analysis</div>
        <div class="box-subtitle">Revenue contribution by company</div>
    """, unsafe_allow_html=True)

    company_chart = alt.Chart(company_data).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X(
            "Company:N",
            sort="-y",
            title=None
        ),
        y=alt.Y(
            "Revenue:Q",
            title="Revenue"
        ),
        tooltip=[
            alt.Tooltip("Company:N", title="Company"),
            alt.Tooltip(
                "Revenue:Q",
                title="Revenue",
                format=",.0f"
            )
        ]
    ).properties(height=350)

    st.altair_chart(
        company_chart,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="box">
        <div class="box-title">Category Revenue</div>
        <div class="box-subtitle">Revenue contribution by category</div>
    """, unsafe_allow_html=True)

    category_chart = alt.Chart(category_data).mark_bar(
        cornerRadiusEnd=5
    ).encode(
        x=alt.X(
            "Revenue:Q",
            title="Revenue"
        ),
        y=alt.Y(
            "Category:N",
            sort="-x",
            title=None
        ),
        tooltip=[
            alt.Tooltip("Category:N", title="Category"),
            alt.Tooltip(
                "Revenue:Q",
                title="Revenue",
                format=",.0f"
            )
        ]
    ).properties(height=320)

    st.altair_chart(
        category_chart,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="box">
        <div class="box-title">Business Insights</div>
        <div class="box-subtitle">Automatically calculated from the dashboard data</div>
    """, unsafe_allow_html=True)

    st.write(f"🏆 **Top-performing company:** {best_company}")
    st.write(f"📦 **Top-performing product:** {best_product}")
    st.write(f"🌍 **Top-performing region:** {best_region}")
    st.write(f"💰 **Total revenue:** ${total_revenue:,.0f}")
    st.write(f"💵 **Total sales:** ${total_sales:,.0f}")
    st.write(f"📦 **Units sold:** {total_units:,}")

    st.markdown("</div>", unsafe_allow_html=True)