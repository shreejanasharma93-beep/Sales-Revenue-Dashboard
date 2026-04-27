import streamlit as st
import pandas as pd
st.title("📊 Sales & Revenue Dashboard")
try:
    df = pd.read_csv("sales_data.csv")
except:
    st.error("❌ File not found. Please check your file location.")
    st.stop()
df["Order_Date"] = pd.to_datetime(df["Order_Date"], dayfirst=True)

st.subheader("🔑 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹ {df['Sales'].sum():,}")
col2.metric("Total Revenue", f"₹ {df['Revenue'].sum():,}")
col3.metric("Total Profit", f"₹ {df['Profit'].sum():,}")

st.sidebar.header("🔍 Filter Data")

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]
st.subheader("📊 Sales by Category")
sales_category = filtered_df.groupby("Category")["Sales"].sum()
st.bar_chart(sales_category)
st.subheader("🌍 Revenue by Region")
revenue_region = filtered_df.groupby("Region")["Revenue"].sum()
st.bar_chart(revenue_region)
st.subheader("📈 Sales Over Time")
df_sorted = filtered_df.sort_values("Order_Date")
st.line_chart(df_sorted.set_index("Order_Date")["Sales"])
st.subheader("🏆 Top 5 Products by Revenue")
top_products = (
    filtered_df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
st.bar_chart(top_products)
st.subheader("📄 Data Table")
st.dataframe(filtered_df)