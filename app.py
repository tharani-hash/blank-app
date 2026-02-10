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

    # Column mapping (adjust to your actual CSV headers)
    COLUMN_MAP = {
        "sales_value": "revenue",
        "shop_id": "store_id",
        "cust_id": "customer_id",
        "promo_code": "promo_id",
        "channel_code": "sales_channel_id",
        "txn_date": "date"
    }
    st.session_state.df.rename(columns=COLUMN_MAP, inplace=True)

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

# Safety check - show warning but DON'T stop
if st.session_state.df is None:
    st.warning(" Load data first.")
else:
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
        st.rerun()  # Refresh to show EDA section

# ────────────────────────────────────────────────
# EDA SECTION - ONLY SHOW IF PREPROCESSING DONE
# ────────────────────────────────────────────────
if not st.session_state.get("preprocessing_completed", False):
    st.info("ℹ Please apply at least one data pre-processing step to unlock EDA.")
else:
    df = st.session_state.get("df", None)

    if df is None:
        st.warning("⚠ No dataset available.")
    else:
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

        # ... rest of your EDA code continues here ...
        # [Keep all your existing EDA code inside this else block]
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

# EDA readiness check
EDA_REQUIREMENTS = {
    "Data Quality Overview": {
        "required_any": [],
        "required_all": [],
    },
    "Sales Overview": {
        "required_any": [["total_sales_amount", "revenue", "sales_amount", "product_revenue"]],
        "required_all": [],
    },
    "Promotion Effectiveness": {
        "required_any": [
            ["promo_id", "promo_transaction_id", "promotion_id", "promotion_transaction_id"],
            [
                "promo_total_sales_amount",
                "promo_sales_amount",
                "promo_sales",
                "promo_revenue",
                "total_sales_amount",
                "revenue",
            ],
        ],
        "required_all": [],
    },
    "Product-Level Analysis": {
        "required_any": [["product_id"]],
        "required_all": [],
    },
    "Customer-Level Analysis": {
        "required_any": [["customer_id"], ["total_sales_amount", "revenue", "sales_amount"]],
        "required_all": [],
    },
    "Event Impact Analysis": {
        "required_any": [["event_id", "event_category", "event_name"], ["total_sales_amount", "revenue", "sales_amount"]],
        "required_all": [],
    },
    "Store-Level Analysis": {
        "required_any": [
            ["store_id", "destination_store", "to_store_id"],
            ["total_sales_amount", "store_revenue", "revenue", "sales_amount", "quantity_sold", "quantity", "sales_quantity"],
        ],
        "required_all": [],
    },
    "Sales Channel Analysis": {
        "required_any": [["sales_channel_id", "channel_id", "sales_channel"], ["total_sales_amount", "revenue", "sales_amount"]],
        "required_all": [],
    },
    "Summary Report": {
        "required_any": [],
        "required_all": [],
    },
}

def _check_eda_requirements(df_check: pd.DataFrame):
    cols = set(df_check.columns)
    rows = []
    for option, req in EDA_REQUIREMENTS.items():
        missing_groups = []
        # required_all: every column must exist
        for c in req.get("required_all", []):
            if c not in cols:
                missing_groups.append(f"Missing: {c}")

        # required_any: for each group, at least one must exist
        for group in req.get("required_any", []):
            if not any(c in cols for c in group):
                missing_groups.append("Any of: " + ", ".join(group))

        ready = len(missing_groups) == 0
        rows.append(
            {
                "Analysis": option,
                "Status": "Ready" if ready else "Missing columns",
                "Details": "-" if ready else "; ".join(missing_groups),
            }
        )
    return pd.DataFrame(rows)

with st.expander("EDA readiness check (required columns)", expanded=False):
    try:
        req_df = _check_eda_requirements(df)
        st.dataframe(req_df, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not compute EDA readiness check: {e}")

# EDA Navigation
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
            st.rerun()

row1 = st.columns(5)
row2 = st.columns(4)

with row1[0]:
    nav_button("Data Quality Overview", "Data Quality Overview")
with row1[1]:
    nav_button("Sales Overview", "Sales Overview")
with row1[2]:
    nav_button("Promotion Effectiveness", "Promotion Effectiveness")
with row1[3]:
    nav_button("Product-Level Analysis", "Product-Level Analysis")
with row1[4]:
    nav_button("Customer-Level Analysis", "Customer-Level Analysis")

with row2[0]:
    nav_button("Event Impact Analysis", "Event Impact Analysis")
with row2[1]:
    nav_button("Store-Level Analysis", "Store-Level Analysis")
with row2[2]:
    nav_button("Sales Channel Analysis", "Sales Channel Analysis")
with row2[3]:
    nav_button("Summary Report", "Summary Report")

eda_option = st.session_state.eda_option

if eda_option is None:
    st.info(" Select an analysis to view insights.")
    st.stop()

# EDA Content
if eda_option == "Data Quality Overview":
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

    This checks whether your dataset is <b>clean, usable, and reliable</b> before any deeper analysis.

    It typically highlights:
    <ul>
        <li>Row/column counts</li>
        <li>Duplicate records</li>
        <li>Missing values (overall and by column)</li>
    </ul><br>

    <b>Why this matters:</b>

    Poor data quality can distort trends and produce misleading insights.
    This step helps you catch issues early and understand what needs cleaning.
    <br><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Which columns have the most missing data</li>
        <li>How much missing/duplicate data exists overall</li>
        <li>Whether the dataset is ready for analysis/modeling</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
    )
    
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
    st.markdown("###  Sales Overview")

    # Column mapping for sales data
    col_rev = None
    col_qty = None
    col_price = None
    col_date = None
    
    # Find revenue column
    for col in ['total_sales_amount', 'revenue', 'sales_amount', 'product_revenue']:
        if col in df.columns:
            col_rev = col
            break
    
    # Find quantity column
    for col in ['quantity_sold', 'quantity', 'sales_quantity']:
        if col in df.columns:
            col_qty = col
            break
    
    # Find price column
    for col in ['unit_price', 'price']:
        if col in df.columns:
            col_price = col
            break
    
    # Find date column
    for col in ['date', 'created_at', 'sales_date', 'transaction_date']:
        if col in df.columns:
            col_date = col
            break

    # ---------- ROW 1 ----------
    if col_rev:
        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">Total Revenue</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Average Order Value</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Maximum Order Value</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"${df[col_rev].sum():,.2f}",
                f"${df[col_rev].mean():,.2f}",
                f"${df[col_rev].max():,.2f}",
            ),
            unsafe_allow_html=True
        )

    # ---------- ROW 2 ----------
    if col_qty and col_price:
        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">Total Sales</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Total Units Sold</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Average Units / Transaction</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"${(df[col_qty] * df[col_price]).sum():,.2f}",
                f"{df[col_qty].sum():,}",
                f"{df[col_qty].mean():.2f}",
            ),
            unsafe_allow_html=True
        )

    # ---------- TIME SERIES ANALYSIS ----------
    if col_date and col_rev:
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
            <b>Sales By Time</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        # Convert to datetime safely
        df_temp = df.copy()
        df_temp[col_date] = pd.to_datetime(df_temp[col_date], errors='coerce')

        # Aggregate sales by date
        sales_time = (
            df_temp.groupby(df_temp[col_date].dt.date)[col_rev]
            .sum()
            .sort_index()
        )

        st.bar_chart(sales_time)

    # ---------- STORE ANALYSIS ----------
    if 'store_id' in df.columns and col_rev:
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
            <b>Sales By Store</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        sales_store = (
            df.groupby('store_id')[col_rev]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(sales_store)

    # ---------- SALES CHANNEL ANALYSIS ----------
    if 'sales_channel_id' in df.columns and col_rev:
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
            <b>Sales By Sales Channels</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        sales_channel = (
            df.groupby('sales_channel_id')[col_rev]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(sales_channel)

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

    <b>What this section does:</b>

    This analyzes how <b>promotions impact sales performance</b> by comparing promotion cost, sales uplift, and revenue contribution.

    It typically highlights:
    <ul>
        <li>Revenue uplift generated by promotions</li>
        <li>Promotion cost vs sales impact</li>
        <li>Effectiveness of individual promotions</li>
    </ul>

    <b>Why this matters:</b>

    Promotions can increase sales but may also reduce margins.
    This helps ensure promotions are <b>cost-effective and profitable</b>.
    <br><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Which promotions drive the most revenue</li>
        <li>Whether higher promo spend correlates with higher uplift</li>
        <li>Which promotions may be inefficient and need redesign</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
    )

    promo_id_col = None
    for c in ["promo_id", "promo_transaction_id", "promotion_id", "promotion_transaction_id"]:
        if c in df.columns:
            promo_id_col = c
            break

    promo_sales_col = None
    for c in ["promo_total_sales_amount", "promo_sales_amount", "promo_sales", "promo_revenue", "total_sales_amount", "revenue"]:
        if c in df.columns:
            promo_sales_col = c
            break

    promo_cost_col = None
    for c in ["promo_promo_cost", "promo_cost", "promotion_cost"]:
        if c in df.columns:
            promo_cost_col = c
            break

    promo_uplift_col = None
    for c in ["promo_promo_uplift_revenue", "promo_uplift_revenue", "uplift_revenue"]:
        if c in df.columns:
            promo_uplift_col = c
            break

    if promo_id_col and promo_sales_col:
        base = df[df[promo_id_col].notna()].copy()
        agg = {promo_sales_col: "sum"}
        if promo_cost_col:
            agg[promo_cost_col] = "sum"
        if promo_uplift_col:
            agg[promo_uplift_col] = "sum"

        promo_metrics = base.groupby(promo_id_col).agg(agg).replace([np.inf, -np.inf], np.nan).dropna(how="all")

        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">Total Promo Revenue</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title"># Promotions</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Avg Promo Revenue</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"${promo_metrics[promo_sales_col].sum():,.2f}",
                f"{promo_metrics.shape[0]:,}",
                f"${promo_metrics[promo_sales_col].mean():,.2f}",
            ),
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            top = promo_metrics.sort_values(promo_sales_col, ascending=False).head(15)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(top.index.astype(str), top[promo_sales_col])
            ax.set_title("Top Promotions by Revenue")
            ax.tick_params(axis="x", rotation=45)
            ax.grid(axis="y", linestyle="--", alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            if promo_cost_col and promo_uplift_col:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.scatter(promo_metrics[promo_cost_col], promo_metrics[promo_uplift_col], alpha=0.7)
                ax.set_xlabel("Promotion Cost")
                ax.set_ylabel("Revenue Uplift")
                ax.set_title("Promotion Cost vs Revenue Uplift")
                ax.grid(True, linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)
            elif promo_cost_col:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.scatter(promo_metrics[promo_cost_col], promo_metrics[promo_sales_col], alpha=0.7)
                ax.set_xlabel("Promotion Cost")
                ax.set_ylabel("Promotion Revenue")
                ax.set_title("Promotion Cost vs Promotion Revenue")
                ax.grid(True, linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)
    else:
        st.info("Promotion columns not available in the dataset.")

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

    This breaks down performance at the <b>product (SKU) level</b> to identify your top and bottom performers.

    It typically highlights:
    <ul>
        <li>Top products by revenue</li>
        <li>Top products by units sold</li>
        <li>How concentrated sales are across products</li>
    </ul><br>

    <b>Why this matters:</b>

    Product-level insights help with assortment planning, replenishment priorities, and identifying over-dependence on a few SKUs.
    <br><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Which SKUs contribute most to revenue and volume</li>
        <li>Whether sales are driven by a small set of products</li>
        <li>Early signals of potential inventory or pricing opportunities</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
    )

    if "product_id" in df.columns:
        prod_rev_col = None
        for c in ["total_sales_amount", "product_revenue", "revenue", "sales_amount"]:
            if c in df.columns:
                prod_rev_col = c
                break

        prod_qty_col = None
        for c in ["quantity_sold", "quantity", "sales_quantity"]:
            if c in df.columns:
                prod_qty_col = c
                break

        agg = {}
        if prod_rev_col:
            agg[prod_rev_col] = "sum"
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
                        <div class="summary-title">Total Product Revenue</div>
                        <div class="summary-value">{}</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Total Units Sold</div>
                        <div class="summary-value">{}</div>
                    </div>
                </div>
                """.format(
                    f"{prod.shape[0]:,}",
                    f"${prod[prod_rev_col].sum():,.2f}" if prod_rev_col else "NA",
                    f"{prod[prod_qty_col].sum():,}" if prod_qty_col else "NA",
                ),
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            if prod_rev_col:
                with col1:
                    top = prod.sort_values(prod_rev_col, ascending=False).head(20)
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(top.index.astype(str), top[prod_rev_col])
                    ax.set_title("Top Products by Revenue")
                    ax.tick_params(axis="x", rotation=45)
                    ax.grid(axis="y", linestyle="--", alpha=0.3)
                    st.pyplot(fig)
                    plt.close(fig)

            if prod_qty_col:
                with col2:
                    top = prod.sort_values(prod_qty_col, ascending=False).head(20)
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(top.index.astype(str), top[prod_qty_col], color="#2F75B5")
                    ax.set_title("Top Products by Units Sold")
                    ax.tick_params(axis="x", rotation=45)
                    ax.grid(axis="y", linestyle="--", alpha=0.3)
                    st.pyplot(fig)
                    plt.close(fig)
        else:
            st.info("Product revenue/quantity columns not available in the dataset.")
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

    This evaluates <b>customer value and purchase behavior</b> to understand who drives revenue.

    It typically highlights:
    <ul>
        <li>Top customers by revenue</li>
        <li>Revenue distribution across customers</li>
        <li>How concentrated customer revenue is</li>
    </ul><br>

    <b>Why this matters:</b>

    Knowing your highest-value customers helps with retention strategy, targeting, and forecasting (especially when revenue is concentrated).
    <br><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Whether a few customers drive most of the business</li>
        <li>How revenue varies across customers</li>
        <li>Which customers may be key accounts</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
    )

    if "customer_id" in df.columns:
        cust_rev_col = None
        for c in ["total_sales_amount", "revenue", "sales_amount"]:
            if c in df.columns:
                cust_rev_col = c
                break

        if cust_rev_col:
            cust = df.groupby("customer_id")[cust_rev_col].sum().replace([np.inf, -np.inf], np.nan).dropna()
            st.markdown(
                """
                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="summary-title"># Customers</div>
                        <div class="summary-value">{}</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Total Customer Revenue</div>
                        <div class="summary-value">{}</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Avg Revenue / Customer</div>
                        <div class="summary-value">{}</div>
                    </div>
                </div>
                """.format(
                    f"{cust.shape[0]:,}",
                    f"${cust.sum():,.2f}",
                    f"${cust.mean():,.2f}",
                ),
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                top = cust.sort_values(ascending=False).head(20)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(top.index.astype(str), top.values)
                ax.set_title("Top Customers by Revenue")
                ax.tick_params(axis="x", rotation=45)
                ax.grid(axis="y", linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(cust.values, bins=20, color="#2F75B5", alpha=0.8)
                ax.set_title("Customer Revenue Distribution")
                ax.set_xlabel("Revenue")
                ax.set_ylabel("# Customers")
                ax.grid(True, linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)
        else:
            st.info("Customer revenue column not available in the dataset.")
    else:
        st.info("Customer column not available in the dataset.")

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

    <b>What this section does:</b>

    This measures how <b>events</b> (holidays, campaigns, special days) influence sales by comparing revenue across event categories.
    <br><br>

    <b>Why this matters:</b>

    Events can create demand spikes or dips. Understanding their impact improves planning for inventory, staffing, and promotion timing.
    <br><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Which events correlate with the highest sales</li>
        <li>Whether event-driven sales are significant vs baseline</li>
        <li>Prioritization of events for future planning</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
    )

    event_col = None
    for c in ["event_id", "event_category", "event_name"]:
        if c in df.columns:
            event_col = c
            break

    event_rev_col = None
    for c in ["total_sales_amount", "revenue", "sales_amount"]:
        if c in df.columns:
            event_rev_col = c
            break

    if event_col and event_rev_col:
        ev = df[df[event_col].notna()].groupby(event_col)[event_rev_col].sum().sort_values(ascending=False)
        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title"># Events</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Event Revenue</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Top Event Revenue</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"{ev.shape[0]:,}",
                f"${ev.sum():,.2f}",
                f"${ev.iloc[0]:,.2f}" if ev.shape[0] else "NA",
            ),
            unsafe_allow_html=True,
        )

        fig, ax = plt.subplots(figsize=(10, 4))
        top = ev.head(20)
        ax.bar(top.index.astype(str), top.values)
        ax.set_title("Top Events by Revenue")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Event columns not available in the dataset.")

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

    <b>What this section does:</b>

    This compares performance across <b>stores/locations</b> to see where sales are strongest (and weakest).

    It typically highlights:
    <ul>
        <li>Top stores by revenue</li>
        <li>Top stores by units sold</li>
        <li>Differences in performance across locations</li>
    </ul><br>

    <b>Why this matters:</b>

    Store-level differences drive allocation and replenishment decisions. This helps you match inventory and strategy to local demand.
    <br><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Which locations are key revenue drivers</li>
        <li>Whether certain stores consistently underperform</li>
        <li>Where to focus operational improvements</li>
    </ul>

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
    for c in ["total_sales_amount", "store_revenue", "revenue", "sales_amount"]:
        if c in df.columns:
            store_rev_col = c
            break

    store_qty_col = None
    for c in ["quantity_sold", "quantity", "sales_quantity"]:
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
                    <div class="summary-title">Total Store Revenue</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Total Units Sold</div>
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
                ax.set_title("Top Stores by Revenue")
                ax.tick_params(axis="x", rotation=45)
                ax.grid(axis="y", linestyle="--", alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)

        if store_qty_col:
            with col2:
                top = s.sort_values(store_qty_col, ascending=False).head(20)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(top.index.astype(str), top[store_qty_col], color="#2F75B5")
                ax.set_title("Top Stores by Units Sold")
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

    <b>What this section does:</b>

    This compares performance across <b>sales channels</b> (e.g., online vs in-store, marketplace vs direct).

    It typically highlights:
    <ul>
        <li>Top channels by revenue</li>
        <li>Revenue distribution across channels</li>
        <li>Channel concentration risk</li>
    </ul><br>

    <b>Why this matters:</b>

    Channel mix influences strategy, pricing, and marketing spend. Understanding which channels drive revenue helps optimize investments.
    <br><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Which channels generate the most revenue</li>
        <li>Whether you rely heavily on one channel</li>
        <li>Opportunities to grow underutilized channels</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
    )

    channel_col = None
    for c in ["sales_channel_id", "channel_id", "sales_channel"]:
        if c in df.columns:
            channel_col = c
            break

    channel_rev_col = None
    for c in ["total_sales_amount", "revenue", "sales_amount"]:
        if c in df.columns:
            channel_rev_col = c
            break

    if channel_col and channel_rev_col:
        ch = df.groupby(channel_col)[channel_rev_col].sum().sort_values(ascending=False)
        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title"># Channels</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Channel Revenue</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Top Channel Revenue</div>
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
        ax.set_title("Revenue by Sales Channel")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Sales channel columns not available in the dataset.")

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

    <b>What this section does:</b>

    This provides a <b>consolidated summary</b> of key EDA outputs and overall dataset readiness.

    It typically highlights:
    <ul>
        <li>High-level dataset stats (rows, columns, missing values, duplicates)</li>
        <li>Key takeaways from earlier EDA sections</li>
        <li>A quick “what to do next” checklist</li>
    </ul><br>

    <b>Why this matters:</b>

    It helps stakeholders quickly understand the dataset quality and the most important signals before moving into forecasting/modeling.
    <br><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Whether the data looks ready for downstream use</li>
        <li>Which EDA sections to focus on based on findings</li>
        <li>A single place to review the most important summary metrics</li>
    </ul>

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
            <li>This dataset contains a rich mix of numeric and categorical features across products, customers, stores, channels, promotions, and events.</li>
            <li>Use the Sales Overview to verify seasonality/trends and baseline demand.</li>
            <li>Use Promotion, Product, Customer, Store and Channel analyses to identify concentration and key drivers.</li>
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
            <b>Retail Summary</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Column mapping for retail summary
    retail_rev_col = None
    retail_qty_col = None
    retail_price_col = None
    retail_store_col = None
    retail_product_col = None
    retail_date_col = None
    retail_channel_col = None
    retail_event_col = None
    retail_customer_col = None
    retail_txn_col = None
    retail_promo_rev_col = None
    retail_stock_sold_col = None
    retail_stock_damaged_col = None
    retail_returns_col = None

    for c in ["total_sales_amount", "revenue", "sales_amount", "product_revenue", "store_revenue", "promo_total_sales_amount"]:
        if c in df.columns:
            retail_rev_col = c
            break

    for c in ["quantity_sold", "quantity", "sales_quantity"]:
        if c in df.columns:
            retail_qty_col = c
            break

    for c in ["unit_price", "price"]:
        if c in df.columns:
            retail_price_col = c
            break

    for c in ["created_at", "date", "sales_date", "transaction_date"]:
        if c in df.columns:
            retail_date_col = c
            break

    for c in ["sales_channel_id", "channel_id", "sales_channel"]:
        if c in df.columns:
            retail_channel_col = c
            break

    for c in ["event_id", "event_category", "event_name"]:
        if c in df.columns:
            retail_event_col = c
            break

    for c in ["customer_id"]:
        if c in df.columns:
            retail_customer_col = c
            break

    for c in ["transaction_id", "order_id"]:
        if c in df.columns:
            retail_txn_col = c
            break

    for c in ["promo_total_sales_amount", "promo_sales_amount", "promo_revenue"]:
        if c in df.columns:
            retail_promo_rev_col = c
            break

    for c in ["stock_sold_qty"]:
        if c in df.columns:
            retail_stock_sold_col = c
            break

    for c in ["stock_damaged_qty"]:
        if c in df.columns:
            retail_stock_damaged_col = c
            break

    for c in ["returns_quantity_returned", "returns_qty", "return_qty"]:
        if c in df.columns:
            retail_returns_col = c
            break

    for c in ["store_id", "store", "store_name", "destination_store", "to_store_id", "city", "region", "location"]:
        if c in df.columns:
            retail_store_col = c
            break

    for c in ["product_id", "product", "product_name", "sku", "item_name"]:
        if c in df.columns:
            retail_product_col = c
            break

    # Build a unified sales metric
    sales_metric_col = None
    df_retail = df.copy()
    if retail_rev_col:
        sales_metric_col = retail_rev_col
    elif retail_qty_col and retail_price_col:
        df_retail["_computed_sales_amount"] = df_retail[retail_qty_col] * df_retail[retail_price_col]
        sales_metric_col = "_computed_sales_amount"

    if sales_metric_col is None:
        st.info("Retail summary needs a revenue column (e.g. total_sales_amount) or both quantity and price columns.")
    else:
        # Summary cards
        top_store_label = "NA"
        top_store_value = "NA"
        top_product_label = "NA"
        top_product_value = "NA"

        if retail_store_col:
            store_sales = (
                df_retail.groupby(retail_store_col)[sales_metric_col]
                .sum()
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
                .sort_values(ascending=False)
            )
            if store_sales.shape[0]:
                top_store_label = str(store_sales.index[0])
                top_store_value = f"${store_sales.iloc[0]:,.2f}"

        if retail_product_col:
            product_sales = (
                df_retail.groupby(retail_product_col)[sales_metric_col]
                .sum()
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
                .sort_values(ascending=False)
            )
            if product_sales.shape[0]:
                top_product_label = str(product_sales.index[0])
                top_product_value = f"${product_sales.iloc[0]:,.2f}"

        total_sales_value = df_retail[sales_metric_col].replace([np.inf, -np.inf], np.nan).dropna().sum()
        total_units_value = None
        if retail_qty_col and retail_qty_col in df_retail.columns:
            total_units_value = df_retail[retail_qty_col].replace([np.inf, -np.inf], np.nan).dropna().sum()

        txn_count_value = None
        if retail_txn_col and retail_txn_col in df_retail.columns:
            txn_count_value = df_retail[retail_txn_col].nunique(dropna=True)

        aov_value = None
        if txn_count_value:
            aov_value = total_sales_value / txn_count_value

        avg_price_value = None
        if total_units_value and total_units_value != 0:
            avg_price_value = total_sales_value / total_units_value

        st.markdown(
            """
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">Total Retail Sales</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Total Units Sold</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Avg Order Value</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Top Sales Location</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Best-Selling Product</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"${total_sales_value:,.2f}",
                f"{total_units_value:,.0f}" if total_units_value is not None else "NA",
                f"${aov_value:,.2f}" if aov_value is not None else "NA",
                top_store_label,
                top_product_label,
            ),
            unsafe_allow_html=True,
        )

        if avg_price_value is not None:
            st.info(f"**Avg selling price:** ${avg_price_value:,.2f} per unit")

        if retail_promo_rev_col and retail_promo_rev_col in df_retail.columns and total_sales_value:
            promo_total = df_retail[retail_promo_rev_col].replace([np.inf, -np.inf], np.nan).dropna().sum()
            promo_share = (promo_total / total_sales_value) * 100
            st.info(f"**Promo revenue share:** ${promo_total:,.2f} ({promo_share:.1f}%)")

        colA, colB = st.columns(2)

        with colA:
            if retail_store_col:
                st.markdown("#### Top Locations by Sales")
                top_locations = store_sales.head(15).reset_index()
                top_locations.columns = ["Location", "Sales"]
                st.dataframe(top_locations, use_container_width=True)
            else:
                st.info("No location/store column found for location-level summary.")

        with colB:
            if retail_product_col:
                st.markdown("#### Top Products by Sales")
                top_products = product_sales.head(15).reset_index()
                top_products.columns = ["Product", "Sales"]
                st.dataframe(top_products, use_container_width=True)
            else:
                st.info("No product column found for product-level summary.")

        if retail_date_col:
            st.markdown("#### Sales Trend by Date")
            temp = df_retail[[retail_date_col, sales_metric_col]].copy()
            temp[retail_date_col] = pd.to_datetime(temp[retail_date_col], errors="coerce")
            temp = temp.dropna(subset=[retail_date_col])
            if not temp.empty:
                by_date = temp.groupby(temp[retail_date_col].dt.date)[sales_metric_col].sum().sort_index()
                st.line_chart(by_date)
            else:
                st.info("Date column exists but values could not be parsed.")

        if retail_channel_col:
            st.markdown("#### Sales by Channel")
            channel_sales = (
                df_retail.groupby(retail_channel_col)[sales_metric_col]
                .sum()
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
                .sort_values(ascending=False)
            )
            if channel_sales.shape[0]:
                st.bar_chart(channel_sales.head(15))

        if retail_event_col:
            st.markdown("#### Top Events by Sales")
            event_sales = (
                df_retail.groupby(retail_event_col)[sales_metric_col]
                .sum()
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
                .sort_values(ascending=False)
            )
            if event_sales.shape[0]:
                top_events = event_sales.head(15).reset_index()
                top_events.columns = ["Event", "Sales"]
                st.dataframe(top_events, use_container_width=True)

        if retail_customer_col:
            st.markdown("#### Top Customers by Sales")
            cust_sales = (
                df_retail.groupby(retail_customer_col)[sales_metric_col]
                .sum()
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
                .sort_values(ascending=False)
            )
            if cust_sales.shape[0]:
                top_customers = cust_sales.head(15).reset_index()
                top_customers.columns = ["Customer", "Sales"]
                st.dataframe(top_customers, use_container_width=True)

                top10_share = (cust_sales.head(10).sum() / cust_sales.sum()) * 100 if cust_sales.sum() else 0
                st.info(f"**Revenue concentration:** Top 10 customers contribute {top10_share:.1f}% of customer revenue")

        if retail_store_col and retail_product_col:
            st.markdown("#### Best-Selling Product in Each Location")
            per_loc = (
                df_retail.groupby([retail_store_col, retail_product_col])[sales_metric_col]
                .sum()
                .reset_index()
                .replace([np.inf, -np.inf], np.nan)
                .dropna(subset=[sales_metric_col])
            )

            idx = per_loc.groupby(retail_store_col)[sales_metric_col].idxmax()
            best_by_loc = per_loc.loc[idx].sort_values(sales_metric_col, ascending=False)
            best_by_loc.columns = ["Location", "Best Product", "Sales"]
            st.dataframe(best_by_loc.head(30), use_container_width=True)

        if retail_stock_sold_col or retail_stock_damaged_col or retail_returns_col:
            st.markdown("#### Inventory & Returns Summary")
            inv_cols = []
            if retail_stock_sold_col:
                inv_cols.append(retail_stock_sold_col)
            if retail_stock_damaged_col:
                inv_cols.append(retail_stock_damaged_col)
            if retail_returns_col:
                inv_cols.append(retail_returns_col)

            inv_vals = {}
            if retail_stock_sold_col:
                inv_vals["Stock Sold Qty"] = df_retail[retail_stock_sold_col].replace([np.inf, -np.inf], np.nan).dropna().sum()
            if retail_stock_damaged_col:
                inv_vals["Stock Damaged Qty"] = df_retail[retail_stock_damaged_col].replace([np.inf, -np.inf], np.nan).dropna().sum()
            if retail_returns_col:
                inv_vals["Returns Qty"] = df_retail[retail_returns_col].replace([np.inf, -np.inf], np.nan).dropna().sum()

            inv_df = pd.DataFrame({"Metric": list(inv_vals.keys()), "Value": list(inv_vals.values())})
            st.dataframe(inv_df, use_container_width=True)

            if retail_returns_col and retail_stock_sold_col and inv_vals.get("Stock Sold Qty"):
                rr = (inv_vals.get("Returns Qty", 0) / inv_vals.get("Stock Sold Qty")) * 100
                st.info(f"**Return rate:** {rr:.2f}%")

else:
    st.info(f"Detailed visualization for **{eda_option}** coming soon...")

# Footer
st.markdown("""
<div style="text-align:center; margin:60px 0 20px; color:#666; font-size:14px;">
    © 2025 SupplySyncAI – Smart Inventory Redistribution Engine
</div>
""", unsafe_allow_html=True)
