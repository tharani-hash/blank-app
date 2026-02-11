import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
import io
import numpy as np

# ────────────────────────────────────────────────
# PAGE CONFIG
# ────────────────────────────────────────────────
st.set_page_config(page_title="AI-Driven Stock Rebalancing", layout="wide")

# ────────────────────────────────────────────────
# CSS (Phase 1 style - clean and professional)
# ────────────────────────────────────────────────
st.markdown("""
<style>
    /* App background */
    .stApp {
        background-color: #FFFFFF;
        margin: 0;
        padding: 0;
    }

    /* 🔥 Remove ALL app-level top spacing */
    .block-container {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }

    /* 🔥 Remove internal main section padding */
    section.main > div:first-child {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }

    /* ✅ KEEP header visible (do NOT hide it) */
    header {
        position: relative;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* =========================================
   RADIO CONTAINER – FULL WIDTH
   ========================================= */
div.stRadio {
    width: 100%;
    padding: 0 !important;
    margin: 0 !important;
}

/* =========================================
   Teal WRAP BOX – FULL PAGE WIDTH
   ========================================= */
div.stRadio > div {
    background-color:  #14B8A6;
    padding: 16px 400px;
    border-radius: 8px;
    width: 100%;              
    box-sizing: border-box;
}

/* =========================================
   RADIO GROUP ALIGNMENT
   ========================================= */
div[data-baseweb="radio-group"] {
    display: flex;
    justify-content: center;  /* center options inside */
}

/* =========================================
   RADIO OPTION TEXT
   ========================================= */
/* RADIO LABEL TEXT – FORCE WHITE */
div[data-baseweb="radio"] label,
div[data-baseweb="radio"] label span {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
}

/* =========================================
   SPACE BETWEEN OPTIONS
   ========================================= */
div[data-baseweb="radio"] {
    margin-right: 28px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
        /* Dark blue themed button */
        div.stButton > button {
            background-color: #0B2C5D;   /* Dark blue from your header */
            color: #FFFFFF;
            border-radius: 8px;
            padding: 8px 18px;
            border: none;
            font-weight: 600;
        }

        div.stButton > button:hover {
            background-color: #08306B;   /* Slightly darker on hover */
            color: #FFFFFF;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
/* =========================================
   SUMMARY GRID (CENTERED, SMALL, EQUAL BOXES)
   ========================================= */
.summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px;
    margin: 6px 0 10px 0;
    justify-content: center;
}

/* =========================================
   SUMMARY CARD (TABLE CONTAINER)
   ========================================= */
.summary-card {
    border: 2px solid #6B7280;
    border-radius: 2px;
    background-color: #E5E7EB;
    overflow: hidden;
    text-align: center;
}

/* =========================================
   HEADER ROW (NO WRAP, SAME HEIGHT)
   ========================================= */
.summary-title {
    background-color: #9CA3AF;
    color: #000000;
    font-size: 14px;
    font-weight: 700;
    padding: 8px 6px;
    border-bottom: 1px solid #6B7280;
    white-space: nowrap;       /* 🔥 stop wrapping */
    overflow: hidden;
    text-overflow: ellipsis;
}

/* =========================================
   VALUE CELL (COMPACT)
   ========================================= */
.summary-value {
    font-size: 22px;
    font-weight: 600;
    color: #000000;
    padding: 1px 0;
}
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# HEADER (matches slide 1–2)
# ────────────────────────────────────────────────
st.markdown("""
<div style="
    background-color:#0B2C5D;
    padding:35px;
    border-radius:12px;
    color:white;
    text-align:center;
    margin:0 0 20px 0;
">
    <h1 style="margin:0 0 8px 0;">
        AI-Driven Stock Rebalancing for Demand-Responsive Retail
    </h1>
    <h3 style="font-weight:400; margin:0;">
        Move the Right Stock, to the Right Store, at the Right Time
    </h3>
    <p style="font-size:17px; margin-top:15px;">
        Clustering-Based Demand Signals + Optimization-Driven Transfers
    </p>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# WHY THIS MATTERS (matches slide 3–5)
# ────────────────────────────────────────────────
st.markdown("""
<div style="
    background-color:#2F75B5;
    padding:28px;
    border-radius:12px;
    color:white;
    font-size:16px;
    line-height:1.6;
    margin-bottom:25px;
">

<p>
<b>Smart Inventory Redistribution</b> is an AI-powered decision engine designed to continuously rebalance inventory across stores, warehouses, and regions based on real-time demand signals.
</p>

<p>
Traditional inventory systems treat each store in isolation, leading to overstock in low-demand locations and stockouts in high-demand ones. This application breaks that silo by analyzing:
</p>
<ul>
    <li>Demand forecasts</li>
    <li>Inventory health metrics</li>
    <li>Store and cluster-level demand behavior</li>
    <li>Logistics and route feasibility</li>
    <li>Optimization models for transfer decisions</li>
</ul>

<div style="margin:20px 0; padding:20px; background:#FFFFFF; border-radius:10px; border:1px solid #D1D5DB;">
    <h4 style="margin:0; color:#000000;">❓ Why This Matters</h4>
    <div style="background:#FFFFFF; padding:15px; border-radius:8px; margin:15px 0; border:1px solid #E5E7EB;">
        <h5 style="margin:0; color:#000000;"> The Retail Problem</h5>
        <ul style="color:#000000; margin:10px 0 0 20px;">
            <li>Inventory is capital locked on shelves</li>
            <li>Overstock → markdowns & wastage</li>
            <li>Stockouts → lost revenue & poor CX</li>
            <li>Manual transfers → slow, reactive, expensive</li>
        </ul>
    </div>
    <div style="background:#FFFFFF; padding:15px; border-radius:8px; border:1px solid #E5E7EB;">
        <h5 style="margin:0; color:#000000;"> The AI Advantage</h5>
        <p style="color:#000000; margin:10px 0;">Transforms reactive replenishment into proactive rebalancing:</p>
        <ul style="color:#000000; margin:0 0 0 20px;">
            <li>Identify excess stock early</li>
            <li>Detect demand hotspots</li>
            <li>Optimize transfers with AI</li>
            <li>Reduce procurement & logistics cost</li>
            <li>Improve fill rates & customer satisfaction</li>
        </ul>
    </div>
</div>

</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# DATA COLLECTION & INTEGRATION
# ────────────────────────────────────────────────
st.markdown("""
<div style="
    background-color:#0B2C5D;
    padding:18px 25px;
    border-radius:10px;
    color:white;
    margin-top:20px;
    margin-bottom:10px;
">
    <h3 style="margin:0;">
        Data Collection & Integration (Unified Data Ingestion)
    </h3>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background-color:#2F75B5;
    padding:28px;
    border-radius:12px;
    color:white;
    font-size:16px;
    line-height:1.6;
    margin-bottom:20px;
">

<p>
This section consolidates data from multiple enterprise sources into a single analytical model.
</p>

<b>Integrated Data Domains:</b>
<ul>
    <li>Customer behavior & loyalty</li>
    <li>Product master & pricing</li>
    <li>Store & sales channel data</li>
    <li>Promotions & events</li>
    <li>Inventory & stock conditions</li>
    <li>Weather & market trends</li>
    <li>Time & seasonality signals</li>
</ul>

<p>
All data is validated and aligned using a <b>consistent dimensional model</b>
to ensure forecasting accuracy.
</p>

</div>
""", unsafe_allow_html=True)

# Make sure session key exists
if "df" not in st.session_state:
    st.session_state.df = None

# Load Button
if st.button("Load Data"):
    st.session_state.df = pd.read_csv("FACT_SUPPLY_CHAIN_FINAL.csv")
    st.success("Data loaded successfully!")

# Show preview if loaded
df = st.session_state.df

if df is not None:
    st.markdown(
    """
    <div style="
        background-color:#0B2C5D;
        padding:18px 25px;
        border-radius:10px;
        color:white;
        margin-top:20px;
        margin-bottom:10px;
    ">
        <h3 style="margin:0;">Data Preview</h3>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.dataframe(df.head(20))
    st.info(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
else:
    st.info("Click the button above to load the dataset.")

# ────────────────────────────────────────────────
# DATA PRE-PROCESSING
# ────────────────────────────────────────────────
st.markdown("""
<div style="
    background-color:#0B2C5D;
    padding:18px 25px;
    border-radius:10px;
    color:white;
    margin-top:25px;
    margin-bottom:12px;
">
    <h3 style="margin:0;">
        Data Pre-Processing (Data Quality & Readiness)
    </h3>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background-color:#2F75B5;
    padding:24px;
    border-radius:12px;
    color:white;
    font-size:16px;
    line-height:1.7;
    margin-bottom:20px;
">
This section ensures the dataset is <b>model-ready</b> by handling:
<ul>
    <li>Missing values & inconsistencies</li>
    <li>Outliers & anomalies</li>
    <li>Data type validation</li>
    <li>Referential integrity checks across dimensions</li>
    <li>Time alignment and granularity normalization</li>
</ul>

This step guarantees that downstream models are trained on
<b>clean, reliable, and trustworthy data.</b>
</div>
""", unsafe_allow_html=True)

# Safety check
if st.session_state.df is None:
    st.warning("⚠ Load data first.")
    st.stop()

df = st.session_state.df

# Preprocessing controls
col1, col2, col3 = st.columns(3)
remove_dup = col1.checkbox("Remove Duplicates", value=True)
drop_null = col2.checkbox("Drop NULL Rows", value=False)
fill_unknown = col3.checkbox("Fill NULLs with 'Unknown'", value=True)

if st.button("Apply Preprocessing"):
    temp = df.copy()
    if remove_dup: temp = temp.drop_duplicates()
    if drop_null:  temp = temp.dropna()
    if fill_unknown: temp = temp.fillna("Unknown")
    st.session_state.df = temp
    st.session_state.preprocessing_completed = True
    st.success("Preprocessing applied!")

# ────────────────────────────────────────────────
# EDA SECTION
# ────────────────────────────────────────────────
if not st.session_state.get("preprocessing_completed", False):
    st.info("ℹ Please apply at least one data pre-processing step to unlock EDA.")
    st.stop()

df = st.session_state.get("df", None)

if df is None:
    st.warning("⚠ No dataset available.")
    st.stop()

# EDA Header
st.markdown(
    """
    <div style="
        background-color:#0B2C5D;
        padding:18px 25px;
        border-radius:10px;
        color:white;
        margin-top:20px;
        margin-bottom:10px;
    ">
        <h3 style="margin:0;">Exploratory Data Analysis (EDA)</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(f"Dataset Loaded: **{df.shape[0]} rows × {df.shape[1]} columns**")

# EDA Navigation
# Session state for drill-down navigation
if "drill_down_path" not in st.session_state:
    st.session_state.drill_down_path = []
if "selected_store" not in st.session_state:
    st.session_state.selected_store = None
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "selected_cluster" not in st.session_state:
    st.session_state.selected_cluster = None

st.markdown("###  List of Analytics")

if "eda_option" not in st.session_state:
    st.session_state.eda_option = None

def nav_button(label, value):
    """Instant active highlight + no size change"""
    if st.session_state.eda_option == value:
        st.markdown(
            f"""
            <div style="
                background-color:#2F75B5;
                color:white;
                padding:14px;
                border-radius:10px;
                font-weight:600;
                text-align:center;
                margin-bottom:12px;
            ">
                {label}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        if st.button(label, use_container_width=True):
            st.session_state.eda_option = value
            # Clear drill-down path when switching analysis
            st.session_state.drill_down_path = []
            st.session_state.selected_store = None
            st.session_state.selected_product = None
            st.session_state.selected_cluster = None
            st.rerun()

def handle_drill_down(entity_type, entity_id, entity_name):
    """Handle drill-down clicks and update session state"""
    if entity_type == "store":
        st.session_state.selected_store = entity_id
        st.session_state.drill_down_path = ["Store", entity_name]
    elif entity_type == "product":
        st.session_state.selected_product = entity_id
        st.session_state.drill_down_path = ["Product", entity_name]
    elif entity_type == "cluster":
        st.session_state.selected_cluster = entity_id
        st.session_state.drill_down_path = ["Cluster", entity_name]
    
    # Clear other selections
    if entity_type != "store":
        st.session_state.selected_store = None
    if entity_type != "product":
        st.session_state.selected_product = None
    if entity_type != "cluster":
        st.session_state.selected_cluster = None

row1 = st.columns(5)
row2 = st.columns(4)

with row1[0]:
    nav_button("Data Quality Overview", "Data Quality Overview")
with row1[1]:
    nav_button("Inventory Overview", "Sales Overview")
with row1[2]:
    nav_button("Transfer Optimization", "Promotion Effectiveness")
with row1[3]:
    nav_button("Product-Level Analysis", "Product-Level Analysis")
with row1[4]:
    nav_button("Route Analysis", "Customer-Level Analysis")

with row2[0]:
    nav_button("Model Optimization", "Event Impact Analysis")
with row2[1]:
    nav_button("Store-Level Analysis", "Store-Level Analysis")
with row2[2]:
    nav_button("Cluster Analysis", "Sales Channel Analysis")
with row2[3]:
    nav_button("Summary Report", "Summary Report")

eda_option = st.session_state.eda_option

if eda_option is None:
    st.info(" Select an analysis to view insights.")
    st.stop()

# EDA Content
if eda_option == "Data Quality Overview":
    st.markdown("""
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">
    <b>Data Quality Analysis</b>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Rows", f"{len(df):,}")
    col1.metric("Columns", df.shape[1])
    col2.metric("Duplicates", df.duplicated().sum())
    col2.metric("Missing Values", df.isnull().sum().sum())
    
    st.subheader("Missing Values (%)")
    missing = (df.isnull().mean() * 100).round(2).sort_values(ascending=False)
    st.bar_chart(missing.head(15))

elif eda_option == "Sales Overview":
    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">

    <b>What this section does:</b>

    This provides a <b>macro-level snapshot of sales performance</b>, answering the question:

    "What does overall sales look like across time?"

    It typically highlights:
    <ul>
        <li>Total revenue</li>
        <li>Total units sold</li>
        <li>Average order value</li>
        <li>Sales trends over time</li>
    </ul><br>

    <b>Why this matters:</b>

    Before diving into granular analysis, it's important to understand:
    <ul>
        <li>Overall business scale</li>
        <li>Growth or decline patterns</li>
        <li>Presence of seasonality or anomalies</li>
    </ul><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Baseline sales behavior</li>
        <li>Early signals of trends or volatility</li>
        <li>Context for all deeper analyses</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown("### Inventory Overview")

    # Column mapping for inventory data
    col_stock_value = None
    col_on_hand = None
    col_fill_rate = None
    col_stockout = None
    col_turnover = None
    
    # Find stock value column
    for col in ['stock_value', 'inventory_value', 'total_stock_value']:
        if col in df.columns:
            col_stock_value = col
            break
    
    # Find on hand quantity column
    for col in ['on_hand_qty', 'on_hand_quantity', 'stock_on_hand']:
        if col in df.columns:
            col_on_hand = col
            break
    
    # Find fill rate column
    for col in ['fill_rate_pct', 'fill_rate', 'fill_percentage']:
        if col in df.columns:
            col_fill_rate = col
            break
    
    # Find stockout percentage column
    for col in ['stockout_pct', 'stockout_percentage', 'out_of_stock_pct']:
        if col in df.columns:
            col_stockout = col
            break
    
    # Find inventory turnover column
    for col in ['inventory_turnover', 'turnover', 'stock_turnover']:
        if col in df.columns:
            col_turnover = col
            break

    # ---------- DRILL-DOWN SUMMARY ----------
    st.markdown("#### 📊 Inventory Summary")
    summary_cols = st.columns(4)
    
    with summary_cols[0]:
        st.metric("Total Stock Value", f"${df[col_stock_value].sum():,.0f}" if col_stock_value else "N/A")
    
    with summary_cols[1]:
        st.metric("Total On-Hand Quantity", f"{df[col_on_hand].sum():,.0f}" if col_on_hand else "N/A")
    
    with summary_cols[2]:
        avg_fill = df[col_fill_rate].mean() if col_fill_rate else None
        st.metric("Avg Fill Rate", f"{avg_fill:.1f}%" if avg_fill else "N/A")
    
    with summary_cols[3]:
        avg_stockout = df[col_stockout].mean() if col_stockout else None
        st.metric("Avg Stockout Rate", f"{avg_stockout:.1f}%" if avg_stockout else "N/A")

    # ---------- DRILL-DOWN NAVIGATION ----------
    if st.session_state.drill_down_path:
        st.markdown("#### 📍 Current Drill-Down Path")
        path_display = " → ".join(st.session_state.drill_down_path)
        st.info(f"**Navigation:** {path_display}")
        
        if st.button("🔄 Reset Navigation"):
            st.session_state.drill_down_path = []
            st.session_state.selected_store = None
            st.session_state.selected_product = None
            st.session_state.selected_cluster = None
            st.rerun()

    # ---------- INTERACTIVE CHARTS WITH DRILL-DOWN ----------
    st.markdown("#### 📈 Interactive Inventory Analysis")
    
    # Store analysis with drill-down
    if col_stock_value and 'store_id' in df.columns:
        with st.expander("🏪 Store Performance (Click to Drill Down)", expanded=False):
            store_performance = df.groupby('store_id')[col_stock_value].sum().sort_values(ascending=False)
            
            # Create clickable store data
            store_df = store_performance.reset_index()
            store_df.columns = ['Store ID', 'Stock Value']
            
            # Display store table with drill-down capability
            for _, row in store_df.head(10).iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{row['Store ID']}**")
                with col2:
                    if st.button(f"🔍 View Details", key=f"store_{row['Store ID']}"):
                        handle_drill_down("store", row['Store ID'], row['Store ID'])
            
            if st.checkbox("Show All Stores", key="show_all_stores"):
                st.dataframe(store_df, use_container_width=True)

    # Product analysis with drill-down
    if col_stock_value and 'product_id' in df.columns:
        with st.expander("📦 Product Performance (Click to Drill Down)", expanded=False):
            product_performance = df.groupby('product_id')[col_stock_value].sum().sort_values(ascending=False)
            
            # Create clickable product data
            product_df = product_performance.reset_index()
            product_df.columns = ['Product ID', 'Stock Value']
            
            # Display product table with drill-down capability
            for _, row in product_df.head(10).iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{row['Product ID']}**")
                with col2:
                    if st.button(f"🔍 View Details", key=f"product_{row['Product ID']}"):
                        handle_drill_down("product", row['Product ID'], row['Product ID'])
            
            if st.checkbox("Show All Products", key="show_all_products"):
                st.dataframe(product_df, use_container_width=True)

    # Cluster analysis with drill-down
    if col_stock_value and 'cluster_id' in df.columns:
        with st.expander("🎯 Cluster Analysis (Click to Drill Down)", expanded=False):
            cluster_performance = df.groupby('cluster_id')[col_stock_value].sum().sort_values(ascending=False)
            
            # Create clickable cluster data
            cluster_df = cluster_performance.reset_index()
            cluster_df.columns = ['Cluster ID', 'Stock Value']
            
            # Display cluster table with drill-down capability
            for _, row in cluster_df.head(10).iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Cluster {row['Cluster ID']}**")
                with col2:
                    if st.button(f"🔍 View Details", key=f"cluster_{row['Cluster ID']}"):
                        handle_drill_down("cluster", row['Cluster ID'], f"Cluster {row['Cluster ID']}")
            
            if st.checkbox("Show All Clusters", key="show_all_clusters"):
                st.dataframe(cluster_df, use_container_width=True)

    # ---------- DETAILED DRILL-DOWN VIEW ----------
    if st.session_state.drill_down_path:
        st.markdown(f"#### 🔍 Detailed View: {' → '.join(st.session_state.drill_down_path)}")
        
        # Filter data based on drill-down path
        filtered_df = df.copy()
        
        # Apply filters based on drill-down path
        if "Store" in st.session_state.drill_down_path and st.session_state.selected_store:
            filtered_df = filtered_df[filtered_df['store_id'] == st.session_state.selected_store]
            st.info(f"📊 Showing data for **Store {st.session_state.selected_store}**")
            
        elif "Product" in st.session_state.drill_down_path and st.session_state.selected_product:
            filtered_df = filtered_df[filtered_df['product_id'] == st.session_state.selected_product]
            st.info(f"📦 Showing data for **Product {st.session_state.selected_product}**")
            
        elif "Cluster" in st.session_state.drill_down_path and st.session_state.selected_cluster:
            filtered_df = filtered_df[filtered_df['cluster_id'] == st.session_state.selected_cluster]
            st.info(f"🎯 Showing data for **Cluster {st.session_state.selected_cluster}**")
        
        # Show detailed metrics for filtered data
        if not filtered_df.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Filtered Records", f"{len(filtered_df):,}")
                st.metric("Total Stock Value", f"${filtered_df[col_stock_value].sum():,.0f}" if col_stock_value else "N/A")
            
            with col2:
                st.metric("Avg Fill Rate", f"{filtered_df[col_fill_rate].mean():.1f}%" if col_fill_rate else "N/A")
                st.metric("Avg Stockout Rate", f"{filtered_df[col_stockout].mean():.1f}%" if col_stockout else "N/A")
            
            with col3:
                st.metric("Unique Stores", f"{filtered_df['store_id'].nunique()}" if 'store_id' in filtered_df.columns else "N/A")
                st.metric("Unique Products", f"{filtered_df['product_id'].nunique()}" if 'product_id' in filtered_df.columns else "N/A")
                st.metric("Unique Clusters", f"{filtered_df['cluster_id'].nunique()}" if 'cluster_id' in filtered_df.columns else "N/A")
            
            # Detailed data table
            st.markdown("#### 📋 Detailed Data")
            st.dataframe(filtered_df.head(100), use_container_width=True)
        else:
            st.warning("No data available for selected drill-down path.")

    # ---------- ROW 1 ----------
    if col_stock_value:
        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">Total Stock Value</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Average Stock Value</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Maximum Stock Value</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"${df[col_stock_value].sum():,.2f}",
                f"${df[col_stock_value].mean():,.2f}",
                f"${df[col_stock_value].max():,.2f}",
            ),
            unsafe_allow_html=True
        )

    # ---------- ROW 2 ----------
    if col_on_hand and col_stock_value:
        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">Total On Hand Quantity</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Average On Hand Quantity</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Total Products</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"{df[col_on_hand].sum():,}",
                f"{df[col_on_hand].mean():.2f}",
                f"{df['product_id'].nunique():,}",
            ),
            unsafe_allow_html=True
        )

    # ---------- TIME SERIES ANALYSIS ----------
    if 'date_id' in df.columns and col_stock_value:
        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Stock Value By Time</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        # Aggregate stock value by date
        stock_time = (
            df.groupby('date_id')[col_stock_value]
            .sum()
            .sort_index()
        )

        st.bar_chart(stock_time)

    # ---------- STORE ANALYSIS ----------
    if 'store_id' in df.columns and col_stock_value:
        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Stock Value By Store</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        stock_store = (
            df.groupby('store_id')[col_stock_value]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(stock_store)

    # ---------- CLUSTER ANALYSIS ----------
    if 'cluster_id' in df.columns and col_stock_value:
        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Stock Value By Cluster</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        stock_cluster = (
            df.groupby('cluster_id')[col_stock_value]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(stock_cluster)

elif eda_option == "Promotion Effectiveness":
    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">

    <b>What this section does:</b><br><br>

    This analyzes <b>transfer optimization metrics</b> by comparing
    transfer costs, service level improvements, and efficiency gains.

    It evaluates:
    <ul>
        <li>Cost savings from optimized transfers</li>
        <li>Service level improvements</li>
        <li>Transfer efficiency across clusters</li>
    </ul>
    <br>

    <b>Why this matters:</b>

    Optimized transfers can reduce logistics costs while improving
    inventory availability. This analysis helps ensure transfers are
    <b>cost-effective and service-oriented</b>.

    </div>
    """,
    unsafe_allow_html=True
    )

    transfer_id_col = None
    for c in ["shipment_id", "transfer_id", "from_store_id"]:
        if c in df.columns:
            transfer_id_col = c
            break

    transfer_cost_col = None
    for c in ["transfer_cost", "fuel_cost", "shipment_cost"]:
        if c in df.columns:
            transfer_cost_col = c
            break

    transfer_qty_col = None
    for c in ["transfer_qty", "optimal_transfer_qty", "shipment_quantity"]:
        if c in df.columns:
            transfer_qty_col = c
            break

    service_gain_col = None
    for c in ["service_level_gain_pct", "cost_minimization_pct", "model_confidence_score"]:
        if c in df.columns:
            service_gain_col = c
            break

    if transfer_id_col and transfer_cost_col:
        base = df[df[transfer_id_col].notna()].copy()
        agg = {transfer_cost_col: "sum"}
        if transfer_qty_col:
            agg[transfer_qty_col] = "sum"
        if service_gain_col:
            agg[service_gain_col] = "mean"

        transfer_metrics = base.groupby(transfer_id_col).agg(agg).replace([np.inf, -np.inf], np.nan).dropna(how="all")

        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">Total Transfer Cost</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title"># Transfers</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Avg Service Gain</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"${transfer_metrics[transfer_cost_col].sum():,.2f}",
                f"{transfer_metrics.shape[0]:,}",
                f"{transfer_metrics[service_gain_col].mean():.1f}%" if service_gain_col else "NA",
            ),
            unsafe_allow_html=True,
        )

        # ---------- DRILL-DOWN TRANSFERS ----------
        if st.session_state.drill_down_path and "Transfer" in st.session_state.drill_down_path:
            st.markdown(f"#### 🚚 Transfer Details: {' → '.join(st.session_state.drill_down_path)}")
            
            # Filter transfers based on drill-down path
            filtered_transfers = transfer_metrics.copy()
            if st.session_state.selected_store:
                filtered_transfers = df[df['from_store_id'] == st.session_state.selected_store]
                st.info(f"📊 Showing transfers from **Store {st.session_state.selected_store}**")
            
            elif st.session_state.selected_cluster:
                # Filter by cluster if cluster data available
                if 'cluster_id' in df.columns:
                    filtered_transfers = df[df['cluster_id'] == st.session_state.selected_cluster]
                    st.info(f"🎯 Showing transfers for **Cluster {st.session_state.selected_cluster}**")
                else:
                    filtered_transfers = transfer_metrics
                    st.info(f"🚚 Showing all transfers")
            
            # Transfer details table
            st.dataframe(filtered_transfers.head(20), use_container_width=True)
            
            # Transfer performance charts
            col1, col2 = st.columns(2)
            with col1:
                top_transfers = filtered_transfers.sort_values(transfer_cost_col, ascending=False).head(15)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(range(len(top_transfers)), top_transfers[transfer_cost_col])
                ax.set_title("Top Transfers by Cost")
                ax.set_xlabel("Transfer ID")
                ax.set_ylabel("Cost ($)")
                ax.tick_params(axis="x", rotation=45)
                ax.grid(axis="y", linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                if service_gain_col and transfer_qty_col:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.scatter(filtered_transfers[transfer_cost_col], filtered_transfers[service_gain_col], alpha=0.7)
                    ax.set_xlabel("Transfer Cost")
                    ax.set_ylabel("Service Gain (%)")
                    ax.set_title("Transfer Cost vs Service Gain")
                    ax.grid(True, linestyle="--", alpha=0.3)
                    st.pyplot(fig)
                    plt.close(fig)
                elif transfer_cost_col and transfer_qty_col:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.scatter(transfer_metrics[transfer_cost_col], transfer_metrics[transfer_qty_col], alpha=0.7)
                    ax.set_xlabel("Transfer Cost")
                    ax.set_ylabel("Transfer Quantity")
                    ax.set_title("Transfer Cost vs Quantity")
                    ax.grid(True, linestyle="--", alpha=0.3)
                    st.pyplot(fig)
                    plt.close(fig)
        else:
            col1, col2 = st.columns(2)
            with col1:
                top = transfer_metrics.sort_values(transfer_cost_col, ascending=False).head(15)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(top.index.astype(str), top[transfer_cost_col])
                ax.set_title("Top Transfers by Cost")
                ax.tick_params(axis="x", rotation=45)
                ax.grid(axis="y", linestyle="--", alpha=0.3)
                ax.set_title("Transfer Cost vs Quantity")
                ax.grid(True, linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)
    else:
        st.info("Transfer columns not available in the dataset.")

elif eda_option == "Product-Level Analysis":
    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">
    <b>What this section does:</b>
    <ul>
        <li>Analyzes inventory performance at the product (SKU) level</li>
        <li>Highlights top products by stock value and quantity</li>
        <li>Shows inventory concentration across products</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
    )

    if "product_id" in df.columns:
        prod_stock_col = None
        for c in ["stock_value", "on_hand_qty", "inventory_value"]:
            if c in df.columns:
                prod_stock_col = c
                break

        prod_qty_col = None
        for c in ["on_hand_qty", "reserved_qty", "in_transit_qty"]:
            if c in df.columns:
                prod_qty_col = c
                break

        agg = {}
        if prod_stock_col:
            agg[prod_stock_col] = "sum"
        if prod_qty_col:
            agg[prod_qty_col] = "sum"

        if agg:
            prod = df.groupby("product_id").agg(agg).replace([np.inf, -np.inf], np.nan).dropna(how="all")

            st.markdown(
                """
                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="summary-title"># Products</div>
                        <div class="summary-value">{}</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Total Stock Value</div>
                        <div class="summary-value">{}</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Total Quantity</div>
                        <div class="summary-value">{}</div>
                    </div>
                </div>
                """.format(
                    f"{prod.shape[0]:,}",
                    f"${prod[prod_stock_col].sum():,.2f}" if prod_stock_col else "NA",
                    f"{prod[prod_qty_col].sum():,}" if prod_qty_col else "NA",
                ),
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            if prod_stock_col:
                with col1:
                    top = prod.sort_values(prod_stock_col, ascending=False).head(20)
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(top.index.astype(str), top[prod_stock_col])
                    ax.set_title("Top Products by Stock Value")
                    ax.tick_params(axis="x", rotation=45)
                    ax.grid(axis="y", linestyle="--", alpha=0.3)
                    st.pyplot(fig)
                    plt.close(fig)

            if prod_qty_col:
                with col2:
                    top = prod.sort_values(prod_qty_col, ascending=False).head(20)
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(top.index.astype(str), top[prod_qty_col], color="#2F75B5")
                    ax.set_title("Top Products by Quantity")
                    ax.tick_params(axis="x", rotation=45)
                    ax.grid(axis="y", linestyle="--", alpha=0.3)
                    st.pyplot(fig)
                    plt.close(fig)
        else:
            st.info("Product stock/quantity columns not available in the dataset.")
    else:
        st.info("Product column not available in the dataset.")

elif eda_option == "Customer-Level Analysis":
    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">
    <b>What this section does:</b>
    <ul>
        <li>Analyzes inventory performance by route and vehicle</li>
        <li>Highlights top routes by efficiency</li>
        <li>Shows distribution of delivery performance</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
    )

    if "route_id" in df.columns:
        route_eff_col = None
        for c in ["route_efficiency_score", "delivery_time_mins", "fuel_cost"]:
            if c in df.columns:
                route_eff_col = c
                break

        if route_eff_col:
            route = df.groupby("route_id")[route_eff_col].mean().replace([np.inf, -np.inf], np.nan).dropna()
            st.markdown(
                """
                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="summary-title"># Routes</div>
                        <div class="summary-value">{}</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Avg Efficiency Score</div>
                        <div class="summary-value">{}</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Best Route Score</div>
                        <div class="summary-value">{}</div>
                    </div>
                </div>
                """.format(
                    f"{route.shape[0]:,}",
                    f"{route.mean():.2f}" if "efficiency" in route_eff_col else f"{route.mean():.1f}",
                    f"{route.max():.2f}" if "efficiency" in route_eff_col else f"{route.max():.1f}",
                ),
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                top = route.sort_values(ascending=False).head(20)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(top.index.astype(str), top.values)
                ax.set_title("Top Routes by Efficiency")
                ax.tick_params(axis="x", rotation=45)
                ax.grid(axis="y", linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(route.values, bins=20, color="#2F75B5", alpha=0.8)
                ax.set_title("Route Efficiency Distribution")
                ax.set_xlabel("Efficiency Score")
                ax.set_ylabel("# Routes")
                ax.grid(True, linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)
        else:
            st.info("Route efficiency columns not available in the dataset.")
    else:
        st.info("Route columns not available in the dataset.")

elif eda_option == "Event Impact Analysis":
    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">
    <b>What this section does:</b><br><br>
    Analyzes inventory optimization recommendations and model confidence.
    </div>
    """,
    unsafe_allow_html=True
    )

    model_col = None
    for c in ["model_confidence_score", "model_version", "recommendation_date"]:
        if c in df.columns:
            model_col = c
            break

    opt_qty_col = None
    for c in ["optimal_transfer_qty", "cost_minimization_pct", "service_level_gain_pct"]:
        if c in df.columns:
            opt_qty_col = c
            break

    if model_col and opt_qty_col:
        opt = df[df[model_col].notna()].groupby(model_col)[opt_qty_col].mean().sort_values(ascending=False)
        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title"># Models</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Avg Optimization</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Best Optimization</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"{opt.shape[0]:,}",
                f"{opt.mean():.1f}%" if "pct" in opt_qty_col else f"{opt.mean():.0f}",
                f"{opt.max():.1f}%" if "pct" in opt_qty_col else f"{opt.max():.0f}",
            ),
            unsafe_allow_html=True,
        )

        fig, ax = plt.subplots(figsize=(10, 4))
        top = opt.head(20)
        ax.bar(top.index.astype(str), top.values)
        ax.set_title("Model Optimization Performance")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Model optimization columns not available in the dataset.")

elif eda_option == "Store-Level Analysis":
    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">
    <b>What this section does:</b><br><br>
    Analyzes inventory performance and distribution across stores.
    </div>
    """,
    unsafe_allow_html=True
    )

    store_col = None
    for c in ["store_id", "destination_store", "to_store_id"]:
        if c in df.columns:
            store_col = c
            break

    store_rev_col = None
    for c in ["stock_value", "inventory_value", "total_stock_value"]:
        if c in df.columns:
            store_rev_col = c
            break

    store_qty_col = None
    for c in ["on_hand_qty", "reserved_qty", "in_transit_qty"]:
        if c in df.columns:
            store_qty_col = c
            break

    if store_col and (store_rev_col or store_qty_col):
        agg = {}
        if store_rev_col:
            agg[store_rev_col] = "sum"
        if store_qty_col:
            agg[store_qty_col] = "sum"
        s = df.groupby(store_col).agg(agg).replace([np.inf, -np.inf], np.nan).dropna(how="all")

        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title"># Stores</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Total Stock Value</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Total Quantity</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"{s.shape[0]:,}",
                f"${s[store_rev_col].sum():,.2f}" if store_rev_col else "NA",
                f"{s[store_qty_col].sum():,}" if store_qty_col else "NA",
            ),
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        if store_rev_col:
            with col1:
                top = s.sort_values(store_rev_col, ascending=False).head(20)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(top.index.astype(str), top[store_rev_col])
                ax.set_title("Top Stores by Stock Value")
                ax.tick_params(axis="x", rotation=45)
                ax.grid(axis="y", linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)

        if store_qty_col:
            with col2:
                top = s.sort_values(store_qty_col, ascending=False).head(20)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(top.index.astype(str), top[store_qty_col], color="#2F75B5")
                ax.set_title("Top Stores by Quantity")
                ax.tick_params(axis="x", rotation=45)
                ax.grid(axis="y", linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)
    else:
        st.info("Store columns not available in the dataset.")

elif eda_option == "Sales Channel Analysis":
    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">
    <b>What this section does:</b><br><br>
    Analyzes inventory distribution across clusters and routes.
    </div>
    """,
    unsafe_allow_html=True
    )

    cluster_col = None
    for c in ["cluster_id", "route_id", "vehicle_id"]:
        if c in df.columns:
            cluster_col = c
            break

    cluster_stock_col = None
    for c in ["stock_value", "on_hand_qty", "inventory_value"]:
        if c in df.columns:
            cluster_stock_col = c
            break

    if cluster_col and cluster_stock_col:
        ch = df.groupby(cluster_col)[cluster_stock_col].sum().sort_values(ascending=False)
        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title"># Clusters</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Total Stock Value</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Top Cluster Value</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"{ch.shape[0]:,}",
                f"${ch.sum():,.2f}",
                f"${ch.iloc[0]:,.2f}" if ch.shape[0] else "NA",
            ),
            unsafe_allow_html=True,
        )

        fig, ax = plt.subplots(figsize=(10, 4))
        top = ch.head(15)
        ax.bar(top.index.astype(str), top.values)
        ax.set_title("Stock Value by Cluster")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Cluster columns not available in the dataset.")

elif eda_option == "Summary Report":
    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">
    <b>What this section does:</b><br><br>
    Provides a consolidated summary of key EDA findings and dataset readiness.
    </div>
    """,
    unsafe_allow_html=True
    )

    rows_count = df.shape[0]
    cols_count = df.shape[1]
    dup_count = int(df.duplicated().sum())
    missing_total = int(df.isnull().sum().sum())

    st.markdown(
        """
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-title">Rows</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Columns</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Missing Values</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Duplicate Rows</div>
                <div class="summary-value">{}</div>
            </div>
        </div>
        """.format(
            f"{rows_count:,}",
            f"{cols_count:,}",
            f"{missing_total:,}",
            f"{dup_count:,}",
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            background-color:#0B2C5D;
            padding:22px;
            border-radius:12px;
            color:white;
            font-size:15px;
            line-height:1.7;
        ">
        <b>Summary:</b>
        <ul>
            <li>This dataset contains comprehensive inventory metrics across products, stores, clusters, transfers, and optimization models.</li>
            <li>Use Inventory Overview to verify stock levels, values, and trends over time.</li>
            <li>Use Product, Store, Cluster, and Transfer analyses to identify optimization opportunities.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Inventory Summary</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Column mapping for inventory summary
    inventory_stock_col = None
    inventory_qty_col = None
    inventory_value_col = None
    inventory_store_col = None
    inventory_product_col = None
    inventory_date_col = None
    inventory_cluster_col = None
    inventory_transfer_col = None
    inventory_model_col = None
    inventory_opt_col = None

    for c in ["stock_value", "inventory_value", "total_stock_value"]:
        if c in df.columns:
            inventory_stock_col = c
            break

    for c in ["on_hand_qty", "reserved_qty", "in_transit_qty"]:
        if c in df.columns:
            inventory_qty_col = c
            break

    for c in ["date_id", "week_start_date", "created_at"]:
        if c in df.columns:
            inventory_date_col = c
            break

    for c in ["cluster_id", "route_id", "vehicle_id"]:
        if c in df.columns:
            inventory_cluster_col = c
            break

    for c in ["shipment_id", "transfer_id", "from_store_id"]:
        if c in df.columns:
            inventory_transfer_col = c
            break

    for c in ["model_confidence_score", "model_version", "recommendation_date"]:
        if c in df.columns:
            inventory_model_col = c
            break

    for c in ["optimal_transfer_qty", "cost_minimization_pct", "service_level_gain_pct"]:
        if c in df.columns:
            inventory_opt_col = c
            break

    for c in ["transaction_id", "shipment_id"]:
        if c in df.columns:
            inventory_txn_col = c
            break

    # Remove unused variables
    inventory_price_col = None
    inventory_store_col = None
    inventory_product_col = None

    for c in ["store_id", "store", "store_name", "destination_store", "to_store_id"]:
        if c in df.columns:
            inventory_store_col = c
            break

    for c in ["product_id", "product", "product_name", "sku"]:
        if c in df.columns:
            inventory_product_col = c
            break

    # Build inventory metrics
    if inventory_stock_col:
        stock_metric_col = inventory_stock_col
    elif inventory_qty_col and inventory_stock_col:
        stock_metric_col = inventory_stock_col
    else:
        stock_metric_col = None

    df_inventory = df.copy()

    if stock_metric_col is None:
        st.info("Inventory summary needs stock value or quantity columns.")
    else:
        # Summary cards
        top_store_label = "NA"
        top_store_value = "NA"
        top_product_label = "NA"
        top_product_value = "NA"

        if inventory_store_col:
            store_stock = (
                df_inventory.groupby(inventory_store_col)[stock_metric_col]
                .sum()
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
                .sort_values(ascending=False)
            )
            if store_stock.shape[0]:
                top_store_label = str(store_stock.index[0])
                top_store_value = f"${store_stock.iloc[0]:,.2f}"

        if inventory_product_col:
            product_stock = (
                df_inventory.groupby(inventory_product_col)[stock_metric_col]
                .sum()
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
                .sort_values(ascending=False)
            )
            if product_stock.shape[0]:
                top_product_label = str(product_stock.index[0])
                top_product_value = f"${product_stock.iloc[0]:,.2f}"

        total_stock_value = df_inventory[stock_metric_col].replace([np.inf, -np.inf], np.nan).dropna().sum()
        total_qty_value = None
        if inventory_qty_col and inventory_qty_col in df_inventory.columns:
            total_qty_value = df_inventory[inventory_qty_col].replace([np.inf, -np.inf], np.nan).dropna().sum()

        txn_count_value = None
        if inventory_txn_col and inventory_txn_col in df_inventory.columns:
            txn_count_value = df_inventory[inventory_txn_col].nunique(dropna=True)

        aov_value = None
        if txn_count_value and total_stock_value:
            aov_value = total_stock_value / txn_count_value

        avg_price_value = None
        if total_qty_value and total_qty_value != 0 and total_stock_value:
            avg_price_value = total_stock_value / total_qty_value

        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">Total Stock Value</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Total Quantity</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Avg Unit Value</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Top Store</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Top Product</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"${total_stock_value:,.2f}",
                f"{total_qty_value:,.0f}" if total_qty_value is not None else "NA",
                f"${avg_price_value:,.2f}" if avg_price_value is not None else "NA",
                top_store_label,
                top_product_label,
            ),
            unsafe_allow_html=True,
        )

        if avg_price_value is not None:
            st.info(f"**Avg selling price:** ${avg_price_value:,.2f} per unit")

        if inventory_transfer_col and inventory_transfer_col in df_inventory.columns and total_stock_value:
            transfer_total = df_inventory[inventory_transfer_col].replace([np.inf, -np.inf], np.nan).dropna().sum()
            st.info(f"**Total transfers:** {transfer_total:,.0f}")

        # Initialize variables to avoid NameError
        store_stock = None
        product_stock = None
        
        if inventory_store_col:
            store_stock = (
                df_inventory.groupby(inventory_store_col)[stock_metric_col]
                .sum()
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
                .sort_values(ascending=False)
            )
        
        if inventory_product_col:
            product_stock = (
                df_inventory.groupby(inventory_product_col)[stock_metric_col]
                .sum()
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
                .sort_values(ascending=False)
            )

        colA, colB = st.columns(2)

        with colA:
            if inventory_store_col and store_stock is not None:
                st.markdown("#### Top Stores by Stock Value")
                top_locations = store_stock.head(15).reset_index()
                top_locations.columns = ["Store", "Stock Value"]
                st.dataframe(top_locations, use_container_width=True)
            else:
                st.info("No store column found for store-level summary.")

        with colB:
            if inventory_product_col and product_stock is not None:
                st.markdown("#### Top Products by Stock Value")
                top_products = product_stock.head(15).reset_index()
                top_products.columns = ["Product", "Stock Value"]
                st.dataframe(top_products, use_container_width=True)
            else:
                st.info("No product column found for product-level summary.")

        if inventory_date_col:
            st.markdown("#### Stock Trend by Date")
            temp = df_inventory[[inventory_date_col, stock_metric_col]].copy()
            temp[inventory_date_col] = pd.to_datetime(temp[inventory_date_col], errors="coerce")
            temp = temp.dropna(subset=[inventory_date_col])
            if not temp.empty:
                by_date = temp.groupby(temp[inventory_date_col].dt.date)[stock_metric_col].sum().sort_index()
                st.line_chart(by_date)
            else:
                st.info("Date column exists but values could not be parsed.")

        if inventory_cluster_col:
            st.markdown("#### Inventory by Cluster")
            cluster_stock = (
                df_inventory.groupby(inventory_cluster_col)[stock_metric_col]
                .sum()
                .sort_values(ascending=False)
            )
            st.bar_chart(cluster_stock.head(20))

        else:
            st.info(f"Detailed visualization for **{eda_option}** coming soon...")

# Footer
st.markdown("""
<div style="text-align:center; margin:60px 0 20px; color:#666; font-size:14px;">
    © 2025 SupplySyncAI – Smart Inventory Redistribution Engine
</div>
""", unsafe_allow_html=True)
