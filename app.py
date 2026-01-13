import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import numpy as np
from scipy import stats

st.set_page_config(page_title="SupplySyncAI – MLOps UI", layout="wide")

st.markdown("""
    <div style="
        background-color:#2E86C1;
        padding:20px;
        text-align:center;
        color:white;
        border-radius:6px;
        font-size:28px;
        font-weight:600;">
        SupplySyncAI 
        <div style="font-size:14px; font-weight:normal; margin-top:4px;">
            Autonomous Inventory Intelligence Platform
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data
def load_data():
    """Load CSV data"""
    try:
        return pd.read_csv("fact_consolidated.csv")
    except FileNotFoundError:
        st.error(" File 'fact_consolidated.csv' not found in the current directory")
        return None
    except Exception as e:
        st.error(f" Error loading file: {str(e)}")
        return None

def show_small_plot(fig):
    """Display centered small plot"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.image(buf, width=480)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# STEP 1: LOAD DATA
# ============================================================

st.markdown("# 📥 STEP 1: LOAD DATA")
st.info("Upload your CSV file or load from existing data")

if "df" not in st.session_state:
    st.session_state.df = None
if "processed_df" not in st.session_state:
    st.session_state.processed_df = None

# File upload section
uploaded_file = st.file_uploader("📤 Upload CSV File", type=["csv"])

col1, col2 = st.columns(2)

with col1:
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.processed_df = st.session_state.df.copy()
            st.success(f"✔ File '{uploaded_file.name}' loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.session_state.df = None
            st.session_state.processed_df = None

with col2:
    if st.button("📂 Load Default Data", key="load_btn", use_container_width=True):
        data = load_data()
        if data is not None:
            st.session_state.df = data
            st.session_state.processed_df = st.session_state.df.copy()
            st.success("✔ Default dataset loaded successfully!")
        else:
            st.session_state.df = None
            st.session_state.processed_df = None

# Show metrics if data is loaded
if st.session_state.df is not None:
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("📊 Rows Loaded", f"{st.session_state.df.shape[0]:,}")
    with metric_col2:
        st.metric("📋 Columns Loaded", st.session_state.df.shape[1])

if st.session_state.df is not None:
    with st.expander("📋 Data Preview", expanded=True):
        st.dataframe(st.session_state.df.head(20), use_container_width=True)
        st.info(f"**Shape:** {st.session_state.df.shape[0]:,} rows × {st.session_state.df.shape[1]} columns")
else:
    st.warning("⚠️ Click 'Load Data' button to proceed")
    st.stop()

# ============================================================
# STEP 2: DATA PREPROCESSING
# ============================================================

st.markdown("# 🧹 STEP 2: DATA PREPROCESSING")
st.info("Clean and prepare data for analysis")

df = st.session_state.df
if df is None or st.session_state.processed_df is None:
    st.warning("⚠️ Please load data first in Step 1")
    st.stop()

processed_df = st.session_state.processed_df.copy()

preprocessing_cols = st.columns(4)
remove_duplicates = preprocessing_cols[0].checkbox("🔄 Remove Duplicates", value=False)
remove_nulls = preprocessing_cols[1].checkbox("🚫 Remove NULL Rows", value=False)
replace_nulls = preprocessing_cols[2].checkbox("📝 Replace NULL Values", value=False)
convert_numeric = preprocessing_cols[3].checkbox("🔢 Convert to Numeric", value=False)

status_logs = []

# Remove duplicates
if remove_duplicates:
    before = processed_df.shape[0]
    processed_df = processed_df.drop_duplicates()
    removed = before - processed_df.shape[0]
    status_logs.append(f"✔ Removed **{removed} duplicate rows**")

# Remove NULL rows
if remove_nulls:
    before = processed_df.shape[0]
    processed_df = processed_df.dropna()
    removed = before - processed_df.shape[0]
    status_logs.append(f"✔ Removed **{removed} rows with NULL values**")

# Replace NULL with Unknown
if replace_nulls:
    null_count = processed_df.isnull().sum().sum()
    processed_df = processed_df.fillna("Unknown")
    status_logs.append(f"✔ Replaced **{null_count} NULL values** with 'Unknown'")

# Convert numeric safely
if convert_numeric:
    safe_cols = processed_df.select_dtypes(include=["object"]).columns
    exclude = [
        "transaction_id","product_id","store_id","customer_id",
        "sales_channel_id","promo_id","event_id","customer_time_id",
        "promo_time_id","reorder_time_id","stock_time_id",
        "forecast_time_id","returns_return_id"
    ]
    safe_cols = [c for c in safe_cols if c not in exclude]
    
    converted = 0
    for col in safe_cols:
        before = processed_df[col].dtype
        processed_df[col] = pd.to_numeric(processed_df[col], errors="ignore")
        after = processed_df[col].dtype
        if before != after:
            converted += 1
    status_logs.append(f"✔ Converted **{converted} columns** to numeric")

st.session_state.processed_df = processed_df

# Show preprocessing results
with st.expander("✅ Preprocessing Summary", expanded=True):
    ppc1, ppc2, ppc3, ppc4 = st.columns(4)
    with ppc1:
        st.metric("Total Rows", f"{processed_df.shape[0]:,}")
    with ppc2:
        st.metric("Total Columns", processed_df.shape[1])
    with ppc3:
        st.metric("NULL Values", f"{processed_df.isnull().sum().sum():,}")
    with ppc4:
        st.metric("Duplicates", f"{processed_df.duplicated().sum():,}")
    
    if status_logs:
        st.success("**Changes Made:**")
        for s in status_logs:
            st.markdown(f"  {s}")
    
    st.dataframe(processed_df.head(15), use_container_width=True)

# ============================================================
# STEP 3: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================

st.markdown("# 📊 STEP 3: EXPLORATORY DATA ANALYSIS (EDA)")
st.info("Analyze dataset characteristics, distributions, and relationships")

df = st.session_state.processed_df

# Column Mapping
def map_col(candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

col_rev = map_col(["total_sales_amount"])
col_qty = map_col(["quantity_sold"])
col_price = map_col(["unit_price"])
col_date = map_col(["date"])
col_product = map_col(["product_id"])
col_store = map_col(["store_id"])
col_channel = map_col(["sales_channel_id"])
col_event = map_col(["event_id"])
col_promo = map_col(["promo_id"])

num_df = df.select_dtypes(include=np.number)

# ============================================================
# 3.1 DATA QUALITY ANALYSIS
# ============================================================

with st.expander("🔍 3.1: Data Quality Overview", expanded=True):
    st.subheader("Dataset Structure")
    dq_col1, dq_col2, dq_col3 = st.columns(3)
    with dq_col1:
        st.metric("📊 Total Rows", f"{df.shape[0]:,}")
    with dq_col2:
        st.metric("📋 Total Columns", f"{df.shape[1]}")
    with dq_col3:
        st.metric("🔢 Numeric Columns", f"{num_df.shape[1]}")
    
    st.subheader("Data Types Distribution")
    dtype_dist = df.dtypes.value_counts()
    st.dataframe(dtype_dist.to_frame("Count"), use_container_width=True)
    
    st.subheader("Missing Values Analysis")
    missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    missing_data = missing_pct[missing_pct > 0]
    
    if len(missing_data) > 0:
        st.dataframe(missing_data.to_frame("Missing %"), use_container_width=True)
    else:
        st.success("✔ No missing values found!")
    
    st.subheader("Duplicate Rows Analysis")
    dup_count = df.duplicated().sum()
    st.metric("Duplicate Rows", f"{dup_count:,}")

# ============================================================
# 3.2 NUMERICAL COLUMNS ANALYSIS
# ============================================================

with st.expander("📈 3.2: Numerical Columns Analysis", expanded=True):
    
    if num_df.shape[1] > 0:
        st.subheader("Summary Statistics")
        st.dataframe(df[num_df.columns].describe().T, use_container_width=True)
        
        st.subheader("Skewness & Kurtosis Analysis")
        skew_kurt = pd.DataFrame({
            'Skewness': df[num_df.columns].skew(),
            'Kurtosis': df[num_df.columns].kurtosis()
        })
        st.dataframe(skew_kurt, use_container_width=True)
        
        st.subheader("Distribution Visualization")
        selected_num_col = st.selectbox("Select numeric column to visualize:", num_df.columns, key="num_dist")
        
        if selected_num_col:
            fig, axes = plt.subplots(1, 2, figsize=(14, 4))
            
            # Histogram
            axes[0].hist(df[selected_num_col].dropna(), bins=40, color='skyblue', edgecolor='black')
            axes[0].set_title(f'Distribution of {selected_num_col}', fontweight='bold')
            axes[0].set_xlabel(selected_num_col)
            axes[0].set_ylabel('Frequency')
            axes[0].grid(alpha=0.3)
            
            # Box plot
            axes[1].boxplot(df[selected_num_col].dropna())
            axes[1].set_title(f'Box Plot of {selected_num_col}', fontweight='bold')
            axes[1].set_ylabel(selected_num_col)
            axes[1].grid(alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
    else:
        st.warning("No numeric columns available for analysis")

# ============================================================
# 3.3 CATEGORICAL COLUMNS ANALYSIS
# ============================================================

with st.expander("📂 3.3: Categorical Columns Analysis", expanded=False):
    cat_cols = df.select_dtypes(include=['object']).columns
    
    if len(cat_cols) > 0:
        selected_cat = st.selectbox("Select categorical column to analyze:", cat_cols, key="cat_analysis")
        
        st.subheader(f"Value Counts: {selected_cat}")
        value_counts = df[selected_cat].value_counts().head(15)
        st.dataframe(value_counts.to_frame('Count'), use_container_width=True)
        
        if len(value_counts) <= 20:
            fig, ax = plt.subplots(figsize=(10, 5))
            value_counts.plot(kind='barh', ax=ax, color='steelblue')
            ax.set_title(f'Top Values in {selected_cat}', fontweight='bold')
            ax.set_xlabel('Count')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
    else:
        st.info("No categorical columns found")

# ============================================================
# 3.4 CORRELATION ANALYSIS
# ============================================================

with st.expander("🔗 3.4: Correlation Analysis", expanded=True):
    
    if num_df.shape[1] >= 2:
        st.subheader("Feature Correlation Matrix")
        corr_matrix = num_df.corr()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
        ax.set_title('Correlation Matrix - All Numeric Features', fontweight='bold', fontsize=14)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        st.subheader("Top Correlated Feature Pairs")
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.3:
                    corr_pairs.append({
                        'Feature 1': corr_matrix.columns[i],
                        'Feature 2': corr_matrix.columns[j],
                        'Correlation': corr_value
                    })
        
        if corr_pairs:
            corr_df = pd.DataFrame(corr_pairs)
            corr_df['Abs_Correlation'] = corr_df['Correlation'].abs()
            corr_df = corr_df.sort_values('Abs_Correlation', ascending=False)
            corr_df['Correlation'] = corr_df['Correlation'].apply(lambda x: f'{x:.4f}')
            st.dataframe(corr_df[['Feature 1', 'Feature 2', 'Correlation']], use_container_width=True)
        else:
            st.info("No strong correlations found (|corr| > 0.3)")
    else:
        st.info("Not enough numeric columns for correlation analysis")

# ============================================================
# 3.5 BUSINESS METRICS ANALYSIS
# ============================================================

with st.expander("💰 3.5: Business Metrics Analysis", expanded=True):
    
    st.subheader("Key Business Metrics")
    bm_col1, bm_col2, bm_col3 = st.columns(3)
    
    if col_rev:
        with bm_col1:
            st.metric("💵 Total Revenue", f"${df[col_rev].sum():,.2f}")
        with bm_col2:
            st.metric("📊 Avg Transaction Value", f"${df[col_rev].mean():,.2f}")
        with bm_col3:
            st.metric("📈 Max Transaction Value", f"${df[col_rev].max():,.2f}")
    
    if col_qty:
        bm_col1, bm_col2 = st.columns(2)
        with bm_col1:
            st.metric("📦 Total Units Sold", f"{df[col_qty].sum():,.0f}")
        with bm_col2:
            st.metric("🎯 Avg Units per Transaction", f"{df[col_qty].mean():.2f}")
    
    st.subheader("Top Performers Analysis")
    
    if col_product:
        st.markdown("**Top 10 Products by Transaction Count**")
        top_products = df[col_product].value_counts().head(10)
        st.dataframe(top_products.to_frame('Transactions'), use_container_width=True)
    
    if col_store:
        st.markdown("**Top 10 Stores by Transaction Count**")
        top_stores = df[col_store].value_counts().head(10)
        st.dataframe(top_stores.to_frame('Transactions'), use_container_width=True)
    
    if col_channel:
        st.markdown("**Sales by Channel**")
        channel_dist = df[col_channel].value_counts()
        st.dataframe(channel_dist.to_frame('Transactions'), use_container_width=True)

# ============================================================
# 3.6 TIME SERIES ANALYSIS (if date column exists)
# ============================================================

if col_date:
    with st.expander("📅 3.6: Time Series Analysis", expanded=False):
        st.subheader("Date Range")
        try:
            df_date = pd.to_datetime(df[col_date], errors='coerce')
            st.metric("Start Date", str(df_date.min()))
            st.metric("End Date", str(df_date.max()))
            st.metric("Days Span", str((df_date.max() - df_date.min()).days))
        except:
            st.warning("Could not parse date column")

# ============================================================
# 3.7 OUTLIER DETECTION
# ============================================================

with st.expander("⚠️ 3.7: Outlier Detection", expanded=False):
    st.subheader("Identify Outliers using IQR Method")
    
    if num_df.shape[1] > 0:
        selected_outlier_col = st.selectbox("Select column for outlier detection:", num_df.columns, key="outlier")
        
        Q1 = df[selected_outlier_col].quantile(0.25)
        Q3 = df[selected_outlier_col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[selected_outlier_col] < lower_bound) | (df[selected_outlier_col] > upper_bound)]
        
        st.metric("Total Outliers", len(outliers))
        st.metric("Outlier Percentage", f"{len(outliers)/len(df)*100:.2f}%")
        
        st.info(f"**IQR Bounds:** Lower = {lower_bound:.2f}, Upper = {upper_bound:.2f}")
        
        if len(outliers) > 0:
            st.dataframe(outliers[[selected_outlier_col]].head(20), use_container_width=True)

# ============================================================
# STEP 4: FEATURE ENGINEERING & ADVANCED ANALYSIS
# ============================================================

st.markdown("# ⚙️ STEP 4: FEATURE ENGINEERING & ADVANCED ANALYSIS")
st.info("Create new features and derive actionable insights")

with st.expander("🛠️ 4.1: Feature Creation", expanded=True):
    st.subheader("Create New Features")
    
    feature_options = []
    
    # Revenue per unit
    if col_rev and col_qty:
        if st.checkbox("Create: Revenue per Unit", value=False):
            processed_df['revenue_per_unit'] = processed_df[col_rev] / processed_df[col_qty]
            processed_df['revenue_per_unit'] = processed_df['revenue_per_unit'].fillna(0)
            st.success("✔ Created 'revenue_per_unit' feature")
            feature_options.append('revenue_per_unit')
    
    # Price brackets (if price exists)
    if col_price:
        if st.checkbox("Create: Price Brackets", value=False):
            processed_df['price_bracket'] = pd.cut(processed_df[col_price], 
                                                   bins=5, 
                                                   labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
            st.success("✔ Created 'price_bracket' feature")
            feature_options.append('price_bracket')
    
    # High-value transactions
    if col_rev:
        if st.checkbox("Create: High-Value Transaction Flag", value=False):
            threshold = processed_df[col_rev].quantile(0.75)
            processed_df['is_high_value'] = (processed_df[col_rev] > threshold).astype(int)
            st.success(f"✔ Created 'is_high_value' feature (threshold: ${threshold:,.2f})")
            feature_options.append('is_high_value')
    
    st.session_state.processed_df = processed_df

with st.expander("📊 4.2: Advanced Insights", expanded=True):
    st.subheader("Segment Performance Analysis")
    
    if 'price_bracket' in processed_df.columns and col_rev:
        bracket_perf = processed_df.groupby('price_bracket')[col_rev].agg(['count', 'sum', 'mean'])
        bracket_perf.columns = ['Transactions', 'Total Revenue', 'Avg Value']
        st.dataframe(bracket_perf, use_container_width=True)
    
    if 'is_high_value' in processed_df.columns and col_rev:
        value_segment = processed_df.groupby('is_high_value')[col_rev].agg(['count', 'sum', 'mean', 'std'])
        value_segment.columns = ['Transactions', 'Total Revenue', 'Avg Value', 'Std Dev']
        st.dataframe(value_segment, use_container_width=True)

# ============================================================
# STEP 5: SUMMARY & FINAL REPORT
# ============================================================

st.markdown("# 📋 STEP 5: COMPREHENSIVE SUMMARY REPORT")
st.success("Analysis Pipeline Completed!")

with st.expander("📄 Final Summary Report", expanded=True):
    
    report_data = {
        "📊 Dataset Overview": {
            "Total Rows": f"{processed_df.shape[0]:,}",
            "Total Columns": processed_df.shape[1],
            "Numeric Features": num_df.shape[1],
            "Categorical Features": processed_df.select_dtypes(include='object').shape[1],
        },
        "🧹 Data Quality": {
            "Missing Values": f"{processed_df.isnull().sum().sum():,}",
            "Duplicate Rows": f"{processed_df.duplicated().sum():,}",
            "Completeness": f"{(1 - processed_df.isnull().sum().sum() / (processed_df.shape[0] * processed_df.shape[1])) * 100:.2f}%",
        },
        "💰 Business Metrics": {
            "Total Revenue": f"${processed_df[col_rev].sum():,.2f}" if col_rev else "N/A",
            "Avg Transaction": f"${processed_df[col_rev].mean():,.2f}" if col_rev else "N/A",
            "Total Units": f"{int(processed_df[col_qty].sum()):,}" if col_qty else "N/A",
        },
    }
    
    for section, metrics in report_data.items():
        st.subheader(section)
        for key, value in metrics.items():
            st.metric(key, value)
    
    st.markdown("---")
    st.subheader("🎯 Key Insights & Recommendations")
    
    insights = []
    
    # Insight 1: Data Quality
    null_pct = (processed_df.isnull().sum().sum() / (processed_df.shape[0] * processed_df.shape[1])) * 100
    if null_pct == 0:
        insights.append("✔ **Data Quality:** Dataset is clean with no missing values")
    else:
        insights.append(f"⚠️ **Data Quality:** {null_pct:.2f}% of data contains missing values - consider imputation")
    
    # Insight 2: Duplicates
    dup_pct = (processed_df.duplicated().sum() / len(processed_df)) * 100
    if dup_pct == 0:
        insights.append("✔ **Duplication:** No duplicate records found")
    else:
        insights.append(f"⚠️ **Duplication:** {dup_pct:.2f}% duplicate records detected")
    
    # Insight 3: Distribution
    if num_df.shape[1] > 0:
        skewed_cols = df[num_df.columns].skew()
        highly_skewed = len(skewed_cols[skewed_cols.abs() > 1])
        if highly_skewed > 0:
            insights.append(f"📊 **Distribution:** {highly_skewed} highly skewed numeric features detected - consider transformation")
        else:
            insights.append("📊 **Distribution:** Features show reasonable distributions")
    
    # Insight 4: Correlations
    if num_df.shape[1] >= 2:
        corr_matrix = num_df.corr()
        high_corr = ((corr_matrix.abs() > 0.8) & (corr_matrix.abs() < 1)).sum().sum() / 2
        if high_corr > 0:
            insights.append(f"🔗 **Multicollinearity:** {int(high_corr)} pairs of highly correlated features found")
    
    for insight in insights:
        st.markdown(f"• {insight}")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
    <br><br>
    <div style="
        background-color:#2E86C1;
        padding:12px;
        text-align:center;
        color:white;
        border-radius:6px;
        font-size:14px;">
        © 2025 SupplySyncAI – Inventory Intelligence & Analytics Platform | 
        Complete Data Analysis Pipeline: Load → Preprocess → EDA → Feature Engineering → Summary
    </div>
""", unsafe_allow_html=True)
