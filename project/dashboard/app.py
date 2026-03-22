import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Sales Dashboard", layout="wide", page_icon="📊")

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {background-color: #0E1117;}
.stMetric {background-color: #1c1f26; padding: 15px; border-radius: 10px;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE CONNECTION
# =========================
engine = create_engine(
    "postgresql+psycopg2://hussain:hussainali@localhost:5432/Storedb"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=10)
def load_data():
    df = pd.read_sql("SELECT * FROM store", engine)
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df

df = load_data()

# =========================
# TITLE
# =========================
st.markdown("<h1 style='text-align:center;'>📊 Sales Dashboard</h1>", unsafe_allow_html=True)

# =========================
# QUICK DATE FILTER BUTTONS
# =========================
st.markdown("### ⏱️ Quick Filters")

col_q1, col_q2, col_q3, col_q4 = st.columns(4)

today = datetime.today()

if col_q1.button("Today"):
    start_date = today
    end_date = today
elif col_q2.button("Last 7 Days"):
    start_date = today - timedelta(days=7)
    end_date = today
elif col_q3.button("Last 30 Days"):
    start_date = today - timedelta(days=30)
    end_date = today
elif col_q4.button("All Time"):
    start_date = df["sale_date"].min()
    end_date = df["sale_date"].max()
else:
    start_date = df["sale_date"].min()
    end_date = df["sale_date"].max()

# =========================
# TOP FILTER BAR
# =========================
st.markdown("### 🔍 Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    date_range = st.date_input(
        "📅 Date Range",
        [start_date, end_date]
    )

with col2:
    search_city = st.text_input("🔎 Search City")
    city_options = df["city"].dropna().unique()
    city_options = [c for c in city_options if search_city.lower() in c.lower()]
    city = st.multiselect("🏙️ City", options=city_options, default=city_options)

with col3:
    search_cat = st.text_input("🔎 Search Category")
    category_options = df["product_category"].dropna().unique()
    category_options = [c for c in category_options if search_cat.lower() in c.lower()]
    category = st.multiselect("📦 Category", options=category_options, default=category_options)

with col4:
    top_n = st.slider("🏆 Top N Products", 5, 20, 10)

# RESET BUTTON
if st.button("🔄 Reset Filters"):
    st.experimental_rerun()

st.markdown("---")

# =========================
# APPLY FILTERS
# =========================
filtered_df = df[
    (df["city"].isin(city)) &
    (df["product_category"].isin(category)) &
    (df["sale_date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

st.caption(f"Showing {len(filtered_df)} records")

# =========================
# KPIs
# =========================
col_k1, col_k2, col_k3 = st.columns(3)

col_k1.metric("💰 Total Sales", f"{filtered_df['sales_amount'].sum():,.0f}")
col_k2.metric("📦 Quantity", int(filtered_df["quantity"].sum()))
col_k3.metric("🧾 Orders", len(filtered_df))

# =========================
# SALES TREND
# =========================
st.subheader("📈 Sales Trend")
trend = filtered_df.groupby("sale_date")["sales_amount"].sum()
st.line_chart(trend)

# =========================
# CHARTS
# =========================
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.subheader("🏙️ Sales by City")
    st.bar_chart(filtered_df.groupby("city")["sales_amount"].sum())

with col_c2:
    st.subheader("📦 Sales by Category")
    st.bar_chart(filtered_df.groupby("product_category")["sales_amount"].sum())

# =========================
# TOP PRODUCTS
# =========================
st.subheader(f"🏆 Top {top_n} Products")

top_products = (
    filtered_df.groupby("product_name")["sales_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

st.bar_chart(top_products)

# =========================
# DOWNLOAD BUTTON
# =========================
st.subheader("📥 Export Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# =========================
# DATA TABLE
# =========================
st.subheader("📋 Data Preview")
st.dataframe(filtered_df, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Created by Hussain Ali</p>
        <p>Email: ha7803832gmail.com</p>
        <p>Phone: 03357897412 | 03318782469</p>
    </div>
    """,
    unsafe_allow_html=True
)