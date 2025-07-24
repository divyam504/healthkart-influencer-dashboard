import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

st.set_page_config(page_title="HealthKart Influencer Dashboard", layout="wide")
st.title("📊 HealthKart Influencer Campaign Dashboard")

# --- Upload Files ---
st.sidebar.header("📁 Upload Required Files")
inf_file = st.sidebar.file_uploader("Upload influencers.csv", type=["csv"])
posts_file = st.sidebar.file_uploader("Upload posts.csv", type=["csv"])
track_file = st.sidebar.file_uploader("Upload tracking_data.csv", type=["csv"])
payout_file = st.sidebar.file_uploader("Upload payouts.csv", type=["csv"])

if not all([inf_file, posts_file, track_file, payout_file]):
    st.warning("⚠️ Please upload all 4 required CSV files to proceed.")
    st.stop()

# --- Read & Clean Data ---
def load_and_clean(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

df_inf = load_and_clean(inf_file)
df_posts = load_and_clean(posts_file)
df_track = load_and_clean(track_file)
df_payout = load_and_clean(payout_file)

# --- Fix duplicate 'orders' column from payouts ---
df_payout = df_payout.rename(columns={'orders': 'payout_orders'})

# --- Merge datasets ---
df = df_track.merge(df_inf, on="influencer_id", how="left")
df = df.merge(df_payout, on="influencer_id", how="left")

# --- Sidebar Filters ---
platforms = st.sidebar.multiselect("Platform", options=df['platform'].dropna().unique())
brands = st.sidebar.multiselect("Brand/Product", options=df['product'].dropna().unique())
categories = st.sidebar.multiselect("Influencer Category", options=df_inf['category'].dropna().unique())
genders = st.sidebar.multiselect("Gender", options=df_inf['gender'].dropna().unique())

if platforms:
    df = df[df['platform'].isin(platforms)]
if brands:
    df = df[df['product'].isin(brands)]
if categories:
    df = df[df['category'].isin(categories)]
if genders:
    df = df[df['gender'].isin(genders)]

# --- KPIs ---
total_orders = df['orders'].sum()
total_revenue = df['revenue'].sum()
total_payout = df['total_payout'].sum()
roas = total_revenue / total_payout if total_payout else 0
roi = (total_revenue - total_payout) / total_payout if total_payout else 0

col1, col2, col3 = st.columns(3)
col1.metric("🛒 Orders", f"{total_orders:,}")
col2.metric("💰 Revenue", f"₹{total_revenue:,.0f}")
col3.metric("📊 ROAS / ROI", f"ROAS: {roas:.2f} | ROI: {roi:.2f}")

# --- Influencer Performance ---
top_inf = df.groupby(['influencer_id', 'name'])[['orders', 'revenue', 'total_payout']].sum().reset_index()
top_inf['ROAS'] = top_inf['revenue'] / top_inf['total_payout']
top_inf = top_inf.sort_values(by='revenue', ascending=False).reset_index(drop=True)
top_inf.index += 1  # Start index at 1 for ranking
top_inf.index.name = "Rank"
st.dataframe(top_inf.round(2), use_container_width=True)

# --- Engagement Analysis ---
st.subheader("📸 Post Engagement")
df_posts = df_posts.merge(df_inf[['influencer_id', 'name']], on='influencer_id', how='left')

df_posts['engagement'] = df_posts['likes'] + df_posts['comments']
top_posts = df_posts.sort_values(by='engagement', ascending=False).head(10)
fig = px.bar(top_posts, x='name', y='engagement', color='platform', title="Top Posts by Engagement")
st.plotly_chart(fig, use_container_width=True)

# --- Poor ROI Detection ---
st.subheader("❌ Influencers with Poor ROI")
poor_roi = top_inf[top_inf['ROAS'] < 1]
if not poor_roi.empty:
    st.dataframe(poor_roi[['name', 'revenue', 'total_payout', 'ROAS']].round(2), use_container_width=True)
else:
    st.info("✅ No influencers with ROAS < 1")

# --- Export Options ---
st.subheader("📤 Export Insights")
export_df = top_inf[['name', 'orders', 'revenue', 'total_payout', 'ROAS']].round(2)

col_csv, col_pdf = st.columns(2)

with col_csv:
    csv = export_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "insights.csv", "text/csv")

with col_pdf:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="HealthKart Campaign Summary", ln=True, align="C")

    for index, row in export_df.head(20).iterrows():
        line = f"{row['name']}: Revenue Rs.{row['revenue']}, ROAS {row['ROAS']:.2f}"

        pdf.cell(200, 10, txt=line, ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("⬇️ Download PDF", pdf_bytes, file_name="summary.pdf")

st.success("✅ Dashboard loaded successfully with all features.")
