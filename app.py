import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(page_title="Business Dashboard", layout="wide")

st.title("📊 E-commerce Business Dashboard")

# ---------------- LOAD DATA ----------------

df = pd.read_csv("data.csv", encoding="ISO-8859-1")

# Convert InvoiceDate
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Create Revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Create Year and Month columns
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month_name()

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("📌 Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["Country"].dropna().unique().tolist())
)

if country != "All":
    df = df[df["Country"] == country]

year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(df["Year"].dropna().unique().tolist())
)

if year != "All":
    df = df[df["Year"] == year]

month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + sorted(df["Month"].dropna().unique().tolist())
)

if month != "All":
    df = df[df["Month"] == month]

# ---------------- KPIs ----------------

total_revenue = df["Revenue"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_quantity = df["Quantity"].sum()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
kpi2.metric("🛒 Total Orders", total_orders)
kpi3.metric("👥 Total Customers", total_customers)
kpi4.metric("📦 Quantity Sold", f"{total_quantity:,}")

st.divider()

# ---------------- VIEW DATA ----------------

with st.expander("📄 View Dataset"):
    st.dataframe(df)

# ---------------- CHARTS ----------------

left, right = st.columns(2)

# Revenue by Country
country_revenue = (
    df.groupby("Country")["Revenue"]
      .sum()
      .reset_index()
      .sort_values(by="Revenue", ascending=False)
)

fig1 = px.treemap(
    country_revenue,
    path=["Country"],
    values="Revenue",
    color="Revenue",
    color_continuous_scale="Blues"
)

fig1.update_layout(margin=dict(t=20, l=10, r=10, b=10))

# Top Products
top_products = (
    df.groupby("Description")["Revenue"]
      .sum()
      .reset_index()
      .sort_values(by="Revenue", ascending=False)
      .head(10)
)

fig2 = px.bar(
    top_products,
    x="Revenue",
    y="Description",
    orientation="h",
    color="Revenue"
)

# Monthly Revenue
monthly_sales = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["Revenue"]
      .sum()
      .reset_index()
)

monthly_sales["InvoiceDate"] = monthly_sales["InvoiceDate"].astype(str)

fig3 = px.line(
    monthly_sales,
    x="InvoiceDate",
    y="Revenue",
    markers=True
)

# ---------------- DISPLAY CHARTS ----------------

with left:
    st.subheader("🌍 Revenue by Country")
    st.plotly_chart(fig1, use_container_width=True)

with right:
    st.subheader("🏆 Top 10 Products")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📈 Monthly Revenue Trend")
st.plotly_chart(fig3, use_container_width=True)

# ---------------- DOWNLOAD ----------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_data.csv",
    "text/csv"
)

st.divider()

# ---------------- BUSINESS RECOMMENDATIONS ----------------

st.header("💡 Business Recommendations")

st.success("""
• The United Kingdom contributes the highest revenue, making it the primary market.

• Focus promotional campaigns on countries with lower sales to improve revenue.

• Maintain inventory for the highest-selling products to avoid stock shortages.

• Introduce loyalty rewards for repeat customers to increase retention.

• Monitor monthly revenue trends and run special offers during low-sales periods.
""")