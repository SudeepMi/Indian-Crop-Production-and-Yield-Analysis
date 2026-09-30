import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Config
st.set_page_config(
    page_title="Indian Crop Production & Yield Analytics",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        margin-bottom: 10px;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #38bdf8;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 5px;
    }
    .metric-sub {
        color: #4ade80;
        font-size: 0.85rem;
        margin-top: 4px;
    }
    .header-box {
        background: linear-gradient(90deg, #064e3b 0%, #047857 50%, #065f46 100%);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    paths = ['data/cleaned_crop_production.csv', 'data/crop_production.csv', '../data/cleaned_crop_production.csv']
    path_to_use = None
    for p in paths:
        if os.path.exists(p):
            path_to_use = p
            break
    
    if path_to_use is None:
        st.error("Data file not found! Please run data pipeline first.")
        st.stop()
        
    df = pd.read_csv(path_to_use)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    if 'yield' not in df.columns:
        df['yield'] = np.where((df['area'] > 0) & (df['production'].notna()), df['production'] / df['area'], np.nan)
    return df

df = load_data()

# Header Banner
st.markdown("""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.2rem; font-weight:800;">🌾 Indian Crop Production & Yield Analytics</h1>
    <p style="margin:5px 0 0 0; font-size:1.1rem; opacity:0.9;">
        Interactive Data Analytics Platform | Special Focus Case Study on Gujarat State (1997 - 2015)
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.image("https://img.icons8.com/color/96/wheat.png", width=70)
st.sidebar.title("🔍 Analytics Controls")

focus_option = st.sidebar.radio("Analysis Mode Focus:", ["All India (National)", "Gujarat Case Study Focus 🏛️"])

all_years = sorted([int(y) for y in df['crop_year'].dropna().unique()])
min_year, max_year = min(all_years), max(all_years)

selected_years = st.sidebar.slider(
    "Select Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_df = df[(df['crop_year'] >= selected_years[0]) & (df['crop_year'] <= selected_years[1])]

if focus_option == "Gujarat Case Study Focus 🏛️":
    filtered_df = filtered_df[filtered_df['state_name'].str.lower() == 'gujarat']
    available_districts = sorted(filtered_df['district_name'].dropna().unique())
    selected_districts = st.sidebar.multiselect("Select Gujarat Districts:", available_districts, default=[])
    if selected_districts:
        filtered_df = filtered_df[filtered_df['district_name'].isin(selected_districts)]
else:
    available_states = sorted(filtered_df['state_name'].dropna().unique())
    selected_states = st.sidebar.multiselect("Filter by State:", available_states, default=[])
    if selected_states:
        filtered_df = filtered_df[filtered_df['state_name'].isin(selected_states)]

available_crops = sorted(filtered_df['crop'].dropna().unique())
selected_crops = st.sidebar.multiselect("Filter by Crop:", available_crops, default=[])
if selected_crops:
    filtered_df = filtered_df[filtered_df['crop'].isin(selected_crops)]

available_seasons = sorted(filtered_df['season'].dropna().unique())
selected_seasons = st.sidebar.multiselect("Filter by Season:", available_seasons, default=[])
if selected_seasons:
    filtered_df = filtered_df[filtered_df['season'].isin(selected_seasons)]

# KPI Metrics Cards
tot_prod = filtered_df['production'].sum()
tot_area = filtered_df['area'].sum()
avg_yield = tot_prod / tot_area if tot_area > 0 else 0
tot_records = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Production</div>
        <div class="metric-value">{tot_prod/1e6:,.2f} M</div>
        <div class="metric-sub">Tonnes ({tot_prod:,.0f} T)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Cultivated Area</div>
        <div class="metric-value">{tot_area/1e6:,.2f} M</div>
        <div class="metric-sub">Hectares ({tot_area:,.0f} Ha)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Yield</div>
        <div class="metric-value">{avg_yield:.2f}</div>
        <div class="metric-sub">Tonnes / Hectare ({avg_yield*1000:,.1f} Kg/Ha)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Data Records</div>
        <div class="metric-value">{tot_records:,}</div>
        <div class="metric-sub">Matching Rows ({tot_records/len(df)*100:.1f}% of total)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Tabs Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Production & Area Trends",
    "🏛️ Gujarat Deep-Dive",
    "📊 Yield & Statistical Correlation",
    "🔥 State × Crop Matrix",
    "📋 Raw Dataset Explorer"
])

with tab1:
    st.subheader("National & State Production Trajectories")
    
    t_col1, t_col2 = st.columns(2)
    
    with t_col1:
        yearly_p = filtered_df.groupby('crop_year')['production'].sum() / 1e6
        fig_p = px.line(
            x=yearly_p.index, y=yearly_p.values,
            labels={'x': 'Year', 'y': 'Production (Million Tonnes)'},
            title="Annual Production Trend",
            markers=True, template="plotly_dark"
        )
        fig_p.update_traces(line_color="#38bdf8", line_width=3)
        st.plotly_chart(fig_p, use_container_width=True)

    with t_col2:
        yearly_a = filtered_df.groupby('crop_year')['area'].sum() / 1e6
        fig_a = px.line(
            x=yearly_a.index, y=yearly_a.values,
            labels={'x': 'Year', 'y': 'Cultivated Area (Million Hectares)'},
            title="Annual Cultivated Area Trend",
            markers=True, template="plotly_dark"
        )
        fig_a.update_traces(line_color="#4ade80", line_width=3)
        st.plotly_chart(fig_a, use_container_width=True)

    st.subheader("Top Major Crops & States")
    b_col1, b_col2 = st.columns(2)
    
    with b_col1:
        top_c = filtered_df.groupby('crop')['production'].sum().nlargest(10).reset_index()
        top_c['production_m'] = top_c['production'] / 1e6
        fig_c = px.bar(
            top_c, x='production_m', y='crop', orientation='h',
            title="Top 10 Major Crops by Production (Million Tonnes)",
            labels={'production_m': 'Production (M Tonnes)', 'crop': 'Crop'},
            color='production_m', color_continuous_scale='Viridis', template="plotly_dark"
        )
        fig_c.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_c, use_container_width=True)

    with b_col2:
        top_s = filtered_df.groupby('state_name')['production'].sum().nlargest(10).reset_index()
        top_s['production_m'] = top_s['production'] / 1e6
        fig_s = px.bar(
            top_s, x='production_m', y='state_name', orientation='h',
            title="Top 10 Agricultural States by Production (Million Tonnes)",
            labels={'production_m': 'Production (M Tonnes)', 'state_name': 'State'},
            color='production_m', color_continuous_scale='Tealgrn', template="plotly_dark"
        )
        fig_s.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_s, use_container_width=True)

with tab2:
    st.subheader("🏛️ Gujarat Agricultural Case Study")
    guj_df = df[df['state_name'].str.lower() == 'gujarat']
    
    g_m1, g_m2, g_m3 = st.columns(3)
    g_m1.metric("Gujarat Production", f"{guj_df['production'].sum()/1e6:,.2f} M Tonnes")
    g_m2.metric("Gujarat Cultivated Area", f"{guj_df['area'].sum()/1e6:,.2f} M Hectares")
    g_m3.metric("Gujarat District Count", f"{guj_df['district_name'].nunique()} Districts")

    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        guj_top_crops = guj_df.groupby('crop')['production'].sum().nlargest(10).reset_index()
        guj_top_crops['production_m'] = guj_top_crops['production'] / 1e6
        fig_g_c = px.bar(
            guj_top_crops, x='production_m', y='crop', orientation='h',
            title="Top 10 Major Crops in Gujarat",
            labels={'production_m': 'Production (M Tonnes)', 'crop': 'Crop'},
            color='production_m', color_continuous_scale='Magma', template="plotly_dark"
        )
        fig_g_c.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_g_c, use_container_width=True)

    with g_col2:
        guj_yearly = guj_df.groupby('crop_year')['production'].sum() / 1e6
        fig_g_y = px.area(
            x=guj_yearly.index, y=guj_yearly.values,
            labels={'x': 'Year', 'y': 'Production (M Tonnes)'},
            title="Gujarat Production Trajectory (1997 - Present)",
            template="plotly_dark"
        )
        fig_g_y.update_traces(fillcolor="rgba(244, 63, 94, 0.3)", line_color="#f43f5e")
        st.plotly_chart(fig_g_y, use_container_width=True)

with tab3:
    st.subheader("📊 Yield Analytics & Scatter Correlation")
    
    s_col1, s_col2 = st.columns(2)
    
    with s_col1:
        sample_df = filtered_df[(filtered_df['area'] > 0) & (filtered_df['production'] > 0)].sample(min(3000, len(filtered_df)), random_state=42)
        fig_scat = px.scatter(
            sample_df, x='area', y='production', color='season', log_x=True, log_y=True,
            title="Cultivated Area vs Production (Log Scale)",
            labels={'area': 'Area (Hectares)', 'production': 'Production (Tonnes)'},
            template="plotly_dark", opacity=0.6
        )
        st.plotly_chart(fig_scat, use_container_width=True)

    with s_col2:
        selected_box_crops = ['Rice', 'Wheat', 'Maize', 'Groundnut', 'Cotton(lint)', 'Sugarcane', 'Bajra']
        box_df = filtered_df[(filtered_df['crop'].isin(selected_box_crops)) & (filtered_df['yield'] > 0) & (filtered_df['yield'] < 100)]
        fig_box = px.box(
            box_df, x='crop', y='yield', color='crop',
            title="Crop Yield Distribution & Variability (Tonnes / Hectare)",
            labels={'yield': 'Yield (t/ha)', 'crop': 'Crop'},
            template="plotly_dark"
        )
        st.plotly_chart(fig_box, use_container_width=True)

with tab4:
    st.subheader("🔥 State × Crop Matrix Heatmap")
    
    top_st = filtered_df.groupby('state_name')['production'].sum().nlargest(10).index
    top_cr = filtered_df.groupby('crop')['production'].sum().nlargest(10).index
    
    heat_df = filtered_df[(filtered_df['state_name'].isin(top_st)) & (filtered_df['crop'].isin(top_cr))]
    pivot_matrix = heat_df.pivot_table(index='state_name', columns='crop', values='production', aggfunc='sum', fill_value=0) / 1e6
    
    fig_heat = px.imshow(
        pivot_matrix,
        labels=dict(x="Crop", y="State", color="Production (M Tonnes)"),
        title="Production Intensity Matrix across Top States and Crops",
        color_continuous_scale="YlGnBu",
        aspect="auto", template="plotly_dark"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with tab5:
    st.subheader("📋 Dataset Filtered Table Explorer")
    st.dataframe(filtered_df.head(500), use_container_width=True)
    
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_crop_production.csv",
        mime="text/csv"
    )
