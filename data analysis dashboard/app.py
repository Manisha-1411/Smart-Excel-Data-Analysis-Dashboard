import os
import base64
import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Apex Financial Analytics | Smart Enterprise Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# Custom Aesthetic (Abstract Blue Gradient Theme)
# ==============================================================================
def load_background_base64(image_filename="background.jpg"):
    """
    Safely load a local background image and convert it to base64.
    Smoothly catches FileNotFoundError and returns None so the application
    can gracefully fallback to a high-fidelity CSS gradient.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(current_dir, image_filename)

    try:
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"'{image_filename}' not found at {target_path}")
        with open(target_path, "rb") as img_file:
            encoded_bytes = base64.b64encode(img_file.read()).decode("utf-8")
            return encoded_bytes, None
    except FileNotFoundError as fnf_err:
        return None, str(fnf_err)
    except Exception as exc:
        return None, f"Unexpected error reading image: {exc}"


def apply_theme():
    """
    Inject custom enterprise CSS. Enforces crisp white typography (#ffffff)
    for maximum contrast against the abstract blue background imagery.
    """
    bg_base64, bg_error = load_background_base64("background.jpg")

    if bg_base64:
        bg_style = f"""
            background-image: 
                linear-gradient(135deg, rgba(8, 16, 38, 0.82) 0%, rgba(4, 9, 24, 0.90) 100%),
                url("data:image/jpeg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        """
    else:
        # Fallback multi-stop luxury blue gradient if image is absent
        bg_style = """
            background: radial-gradient(circle at 15% 20%, #0d244f 0%, #071530 45%, #020713 100%);
            background-attachment: fixed;
        """

    css = f"""
    <style>
        /* Global Background & Root Typography */
        .stApp {{
            {bg_style}
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}

        /* Structural Text explicit crisp white contrast */
        h1, h2, h3, h4, h5, h6, p, span, label, div, .stMarkdown {{
            color: #ffffff !important;
        }}

        /* Header typography enhancement */
        h1 {{
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
        }}

        h2, h3 {{
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(10, 20, 48, 0.92) 0%, rgba(5, 12, 28, 0.96) 100%) !important;
            border-right: 1px solid rgba(56, 189, 248, 0.18) !important;
            backdrop-filter: blur(14px) !important;
        }}

        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {{
            color: #ffffff !important;
            font-weight: 600 !important;
        }}

        /* Glassmorphism Cards & Containers */
        .metric-card {{
            background: rgba(14, 28, 64, 0.65);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 12px;
            padding: 18px 22px;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .metric-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(56, 189, 248, 0.55);
            box-shadow: 0 12px 30px rgba(14, 165, 233, 0.22);
        }}

        .metric-title {{
            color: #94a3b8 !important;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
        }}

        .metric-value {{
            color: #ffffff !important;
            font-size: 1.75rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }}

        .chart-card {{
            background: rgba(11, 23, 54, 0.60);
            border: 1px solid rgba(56, 189, 248, 0.20);
            border-radius: 14px;
            padding: 16px;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.38);
            margin-bottom: 20px;
        }}

        /* Widget inputs restyling */
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {{
            background-color: rgba(15, 23, 42, 0.75) !important;
            border-color: rgba(56, 189, 248, 0.3) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }}

        .stSelectbox svg, .stMultiSelect svg {{
            fill: #38bdf8 !important;
        }}

        /* Tag / pill styles in multi-select */
        span[data-baseweb="tag"] {{
            background-color: rgba(14, 165, 233, 0.25) !important;
            border: 1px solid rgba(56, 189, 248, 0.5) !important;
            color: #ffffff !important;
        }}

        /* Streamlit Banner / Alert customization */
        .stAlert {{
            background-color: rgba(15, 23, 42, 0.82) !important;
            border: 1px solid rgba(56, 189, 248, 0.35) !important;
            color: #ffffff !important;
            border-radius: 10px !important;
        }}

        /* File Uploader Container */
        [data-testid="stFileUploader"] {{
            background: rgba(15, 23, 42, 0.45);
            border: 1px dashed rgba(56, 189, 248, 0.4);
            border-radius: 10px;
            padding: 10px;
        }}

        /* Radio Options */
        .stRadio div[role="radiogroup"] > label {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(56, 189, 248, 0.2);
            padding: 6px 14px;
            border-radius: 8px;
            margin-right: 8px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    return bg_error


# Initialize Theme and capture any background file notice
bg_warning_msg = apply_theme()

# ==============================================================================
# Helper Functions: Column Auto-Detection & Smart Inference
# ==============================================================================
def find_best_column_match(columns, candidates):
    """Return the first column in columns that contains any candidate substring (case-insensitive)."""
    cols_lower = [str(c).strip().lower() for c in columns]
    for cand in candidates:
        for idx, col in enumerate(cols_lower):
            if cand in col:
                return columns[idx]
    return None


def get_column_recommendations(df):
    """
    Dynamically detect categorical and numeric columns.
    Identifies best candidates for Payment Methods, Receiving Methods, and Values.
    """
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "string", "bool"]).columns.tolist()

    # Fallback if categorical list is empty
    if not cat_cols:
        cat_cols = [c for c in df.columns if c not in num_cols]
    if not cat_cols:
        cat_cols = df.columns.tolist()

    # Heuristic matching for Payment Methods
    payment_candidates = ["payment_method", "payment", "pay_method", "pay", "source", "gateway", "channel", "method"]
    payment_col = find_best_column_match(cat_cols, payment_candidates) or (cat_cols[0] if cat_cols else None)

    # Heuristic matching for Receiving Methods
    receiving_candidates = ["receiving_method", "receiving", "receive", "destination", "recipient", "category", "type", "target"]
    remaining_cats = [c for c in cat_cols if c != payment_col]
    receiving_col = find_best_column_match(remaining_cats if remaining_cats else cat_cols, receiving_candidates)
    if not receiving_col:
        receiving_col = remaining_cats[0] if remaining_cats else (cat_cols[0] if cat_cols else None)

    # Heuristic matching for Metric / Amount Values
    value_candidates = ["amount", "value", "total", "balance", "net_worth", "sum", "price", "volume"]
    value_col = find_best_column_match(num_cols, value_candidates) or (num_cols[0] if num_cols else None)

    return cat_cols, num_cols, payment_col, receiving_col, value_col


# ==============================================================================
# Left Sidebar Controls (Strict Specifications)
# ==============================================================================
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
    <span style="font-size: 26px;">💎</span>
    <div>
        <h2 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #ffffff;">APEX ANALYTICS</h2>
        <span style="font-size: 0.75rem; color: #38bdf8; letter-spacing: 0.05em;">ENTERPRISE INTELLIGENCE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 1. Multi-select box pre-populated with standard tracking metrics
default_accounts = ["net_worth", "crypto", "growth", "binance", "kraken"]
selected_accounts = st.sidebar.multiselect(
    "Select accounts to display:",
    options=default_accounts,
    default=default_accounts,
    help="Filter data streams across core financial accounts and holdings"
)

# 2. Radio button component toggling temporal intervals
temporal_interval = st.sidebar.radio(
    "Temporal Interval",
    options=["Monthly", "Weekly", "Daily"],
    index=0,
    horizontal=True,
    help="Aggregate and analyze financial metrics across standard time intervals"
)

st.sidebar.markdown("<hr style='border: 0; border-top: 1px solid rgba(56, 189, 248, 0.2); margin: 20px 0;'>", unsafe_allow_html=True)

# 3. CSV File Uploader targeted exclusively at .csv files
uploaded_file = st.sidebar.file_uploader(
    "Upload Financial Data (CSV):",
    type=["csv"],
    help="Upload your enterprise CSV file for automated visualization"
)

# Optional Demo Data Toggle to facilitate zero-setup evaluation
st.sidebar.markdown("<br>", unsafe_allow_html=True)
use_sample_data = st.sidebar.checkbox(
    "Load Sample Enterprise CSV",
    value=False,
    help="Quickly preview dashboard capabilities with high-fidelity mock enterprise records"
)

# Background file notice handler (graceful visual reminder if background.jpg was absent)
if bg_warning_msg:
    st.sidebar.warning(
        f"⚠️ **Visual Asset Reminder:**\n{bg_warning_msg}\n\n"
        "Active fallback: Modern deep-blue radial gradient."
    )
else:
    st.sidebar.caption("🎨 **Theme Active:** Custom Blue Gradient from local `background.jpg`.")

st.sidebar.markdown("""
<div style='margin-top: 35px; padding: 12px; background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px;'>
    <div style='font-size: 0.75rem; color: #94a3b8;'>SYSTEM STATUS</div>
    <div style='font-size: 0.85rem; color: #38bdf8; font-weight: 700;'>● LIVE OPERATIONAL</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# Header & Navigation
# ==============================================================================
st.markdown("""
<div style="margin-bottom: 25px;">
    <h1 style="margin: 0; font-size: 2.2rem; color: #ffffff;">Executive Financial Analytics</h1>
    <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 1.05rem;">
        Intelligent multi-account reconciliation, payment flow diagnostics, and capital distribution.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# Data Loading & Ingestion
# ==============================================================================
df = None
data_source_label = ""

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        data_source_label = f"Uploaded File: {uploaded_file.name}"
    except Exception as e:
        st.error(f"❌ Error parsing uploaded CSV: {e}")
elif use_sample_data or st.session_state.get("use_sample", False):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_path = os.path.join(current_dir, "sample_transactions.csv")
    if os.path.exists(sample_path):
        df = pd.read_csv(sample_path)
        data_source_label = "Active Dataset: Enterprise Sample Data (sample_transactions.csv)"
    else:
        st.error(f"Sample data file not found at {sample_path}.")

# ==============================================================================
# Dynamic Data Handling & Fallbacks
# ==============================================================================
if df is None:
    # Graceful Informative Banner when no file is uploaded
    st.markdown("""
    <div class="metric-card" style="border-left: 5px solid #38bdf8; padding: 30px; margin-top: 15px;">
        <div style="display: flex; align-items: flex-start; gap: 20px;">
            <div style="font-size: 40px; line-height: 1;">📂</div>
            <div>
                <h3 style="margin: 0 0 8px 0; font-size: 1.4rem; color: #ffffff;">Awaiting CSV Data Source</h3>
                <p style="margin: 0 0 16px 0; color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                    To initiate automated analytics, please upload a corporate transaction or reconciliation 
                    file using the <strong>sidebar file uploader</strong> (restricted exclusively to <code>.csv</code>).
                </p>
                <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                    <span style="background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; color: #e0f2fe;">
                        ✓ Auto-Column Mapping
                    </span>
                    <span style="background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; color: #e0f2fe;">
                        ✓ Interactive Dual-Column Visualizer
                    </span>
                    <span style="background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; color: #e0f2fe;">
                        ✓ Plotly Dark High-Performance Engine
                    </span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Prompt user with an immediate shortcut button
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, _ = st.columns([1.5, 1.5, 3])
    with c1:
        if st.button("🚀 Load Sample Enterprise Dataset", type="primary"):
            st.session_state["use_sample"] = True
            st.rerun()

    st.stop()

# ==============================================================================
# Process and Filter Dataset
# ==============================================================================
# If the dataset contains an 'account' column, filter by user sidebar selection
if "account" in [c.lower() for c in df.columns]:
    account_col_name = [c for c in df.columns if c.lower() == "account"][0]
    if selected_accounts:
        # Match case-insensitively
        active_df = df[df[account_col_name].astype(str).str.lower().isin([a.lower() for a in selected_accounts])].copy()
        if active_df.empty:
            st.warning("⚠️ No records match the selected accounts. Showing full dataset.")
            active_df = df.copy()
    else:
        active_df = df.copy()
else:
    active_df = df.copy()

# Auto-detect columns dynamically
cat_cols, num_cols, default_pay_col, default_recv_col, default_val_col = get_column_recommendations(active_df)

# ==============================================================================
# Executive KPI Row
# ==============================================================================
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

total_records = len(active_df)
total_volume = (
    active_df[default_val_col].sum() if (default_val_col and default_val_col in active_df.columns) else 0.0
)
top_pay_method = (
    active_df[default_pay_col].mode().iloc[0] 
    if (default_pay_col and not active_df[default_pay_col].empty) else "N/A"
)
top_recv_method = (
    active_df[default_recv_col].mode().iloc[0] 
    if (default_recv_col and not active_df[default_recv_col].empty) else "N/A"
)

with kpi_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TOTAL RECONCILED VOLUME</div>
        <div class="metric-value">${total_volume:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TOTAL TRANSACTIONS</div>
        <div class="metric-value">{total_records:,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">PRIMARY PAYMENT METHOD</div>
        <div class="metric-value" style="font-size: 1.3rem;">{top_pay_method}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">CADENCE & INTERVAL</div>
        <div class="metric-value" style="font-size: 1.35rem; color: #38bdf8 !important;">{temporal_interval}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# Responsive Grid Layout (Dual Columns)
# ==============================================================================
left_col, right_col = st.columns(2)

# Custom enterprise color palettes matching the abstract blue/cyan gradient aesthetic
custom_bar_colors = ["#00f0ff", "#38bdf8", "#0284c7", "#2563eb", "#6366f1", "#8b5cf6", "#a855f7", "#ec4899"]
custom_pie_colors = ["#38bdf8", "#0ea5e9", "#2563eb", "#6366f1", "#818cf8", "#34d399", "#2dd4bf", "#f43f5e"]

# ------------------------------------------------------------------------------
# Left Column: Interactive Bar Chart ("Payment Methods")
# ------------------------------------------------------------------------------
with left_col:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <h3 style="margin: 0; font-size: 1.25rem; color: #ffffff;">💳 Payment Methods</h3>
        <span style="font-size: 0.8rem; color: #38bdf8; background: rgba(56, 189, 248, 0.15); padding: 3px 8px; border-radius: 4px;">
            Interactive Bar Chart
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Dynamic Column Bindings with smart fallbacks
    with st.expander("⚙️ Customize Axis & Aggregations", expanded=False):
        c_pay1, c_pay2, c_pay3 = st.columns(3)
        with c_pay1:
            selected_pay_col = st.selectbox(
                "Category (X-Axis):",
                options=cat_cols if cat_cols else active_df.columns.tolist(),
                index=cat_cols.index(default_pay_col) if default_pay_col in cat_cols else 0,
                key="sb_pay_cat"
            )
        with c_pay2:
            val_options = ["Transaction Count"] + num_cols
            default_val_idx = (val_options.index(default_val_col)) if default_val_col in val_options else 0
            selected_pay_val = st.selectbox(
                "Metric (Y-Axis):",
                options=val_options,
                index=default_val_idx,
                key="sb_pay_val"
            )
        with c_pay3:
            pay_agg_mode = st.selectbox(
                "Aggregation:",
                options=["Sum", "Average", "Count"] if selected_pay_val != "Transaction Count" else ["Count"],
                index=0,
                key="sb_pay_agg"
            )

    # Compute aggregation
    if selected_pay_val == "Transaction Count" or pay_agg_mode == "Count":
        bar_df = (
            active_df.groupby(selected_pay_col, as_index=False)
            .size()
            .rename(columns={"size": "Count"})
        )
        y_axis_name = "Count"
        y_title = "Total Transactions"
    else:
        if pay_agg_mode == "Average":
            bar_df = (
                active_df.groupby(selected_pay_col, as_index=False)[selected_pay_val]
                .mean()
                .rename(columns={selected_pay_val: "Average Amount"})
            )
            y_axis_name = "Average Amount"
            y_title = f"Avg {selected_pay_val}"
        else:
            bar_df = (
                active_df.groupby(selected_pay_col, as_index=False)[selected_pay_val]
                .sum()
                .rename(columns={selected_pay_val: "Total Amount"})
            )
            y_axis_name = "Total Amount"
            y_title = f"Sum of {selected_pay_val}"

    # Sort descending for clean visual hierarchy
    bar_df = bar_df.sort_values(by=y_axis_name, ascending=False)

    # Render Plotly Bar Chart with plotly_dark template
    fig_bar = px.bar(
        bar_df,
        x=selected_pay_col,
        y=y_axis_name,
        color=selected_pay_col,
        color_discrete_sequence=custom_bar_colors,
        template="plotly_dark",
        labels={selected_pay_col: "Payment Method", y_axis_name: y_title}
    )

    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=25, b=10),
        font=dict(color="#ffffff", family="Inter, sans-serif"),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="rgba(15, 23, 42, 0.95)",
            bordercolor="#38bdf8",
            font_size=13,
            font_color="#ffffff"
        ),
        xaxis=dict(
            showgrid=False,
            color="#ffffff",
            tickangle=-25,
            title=dict(font=dict(color="#94a3b8", size=12))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.08)",
            color="#ffffff",
            title=dict(font=dict(color="#94a3b8", size=12))
        )
    )
    fig_bar.update_traces(
        marker=dict(line=dict(width=1, color="rgba(255, 255, 255, 0.2)")),
        hovertemplate="<b>%{x}</b><br>" + y_title + ": %{y:,.2f}<extra></extra>"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------------------------------------------------------------
# Right Column: Interactive Pie/Donut Chart ("Receiving Methods")
# ------------------------------------------------------------------------------
with right_col:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <h3 style="margin: 0; font-size: 1.25rem; color: #ffffff;">📥 Receiving Methods</h3>
        <span style="font-size: 0.8rem; color: #38bdf8; background: rgba(56, 189, 248, 0.15); padding: 3px 8px; border-radius: 4px;">
            Interactive Donut Chart
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Dynamic Column Bindings with smart fallbacks
    with st.expander("⚙️ Customize Slices & Metric", expanded=False):
        c_recv1, c_recv2, c_recv3 = st.columns(3)
        with c_recv1:
            selected_recv_col = st.selectbox(
                "Category (Slices):",
                options=cat_cols if cat_cols else active_df.columns.tolist(),
                index=cat_cols.index(default_recv_col) if default_recv_col in cat_cols else 0,
                key="sb_recv_cat"
            )
        with c_recv2:
            recv_val_options = ["Transaction Count"] + num_cols
            default_recv_idx = (recv_val_options.index(default_val_col)) if default_val_col in recv_val_options else 0
            selected_recv_val = st.selectbox(
                "Metric (Values):",
                options=recv_val_options,
                index=default_recv_idx,
                key="sb_recv_val"
            )
        with c_recv3:
            chart_style = st.selectbox(
                "Style:",
                options=["Donut (Modern)", "Classic Pie"],
                index=0,
                key="sb_pie_style"
            )

    hole_ratio = 0.55 if chart_style == "Donut (Modern)" else 0.0

    # Compute aggregation for Pie/Donut
    if selected_recv_val == "Transaction Count":
        pie_df = (
            active_df.groupby(selected_recv_col, as_index=False)
            .size()
            .rename(columns={"size": "Volume"})
        )
        val_label = "Transactions"
    else:
        pie_df = (
            active_df.groupby(selected_recv_col, as_index=False)[selected_recv_val]
            .sum()
            .rename(columns={selected_recv_val: "Volume"})
        )
        val_label = selected_recv_val

    # Render Plotly Pie/Donut with plotly_dark template
    fig_pie = px.pie(
        pie_df,
        names=selected_recv_col,
        values="Volume",
        hole=hole_ratio,
        color_discrete_sequence=custom_pie_colors,
        template="plotly_dark"
    )

    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=25, b=10),
        font=dict(color="#ffffff", family="Inter, sans-serif"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color="#ffffff", size=11)
        ),
        hoverlabel=dict(
            bgcolor="rgba(15, 23, 42, 0.95)",
            bordercolor="#38bdf8",
            font_size=13,
            font_color="#ffffff"
        )
    )
    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        insidetextfont=dict(color="#ffffff", size=11),
        marker=dict(line=dict(color="rgba(10, 20, 48, 0.8)", width=2)),
        hovertemplate="<b>%{label}</b><br>" + val_label + ": %{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# ==============================================================================
# Enterprise Data Explorer & Audit Records
# ==============================================================================
with st.expander("📋 Interactive Data Explorer & Audit Log", expanded=False):
    st.markdown(f"**Data Stream:** `{data_source_label}` &nbsp;|&nbsp; **Active Rows:** `{len(active_df)}`")
    st.dataframe(active_df, use_container_width=True)
    
    # Quick CSV Download of currently filtered records
    csv_bytes = active_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Export Filtered Dataset (CSV)",
        data=csv_bytes,
        file_name="reconciled_analytics_export.csv",
        mime="text/csv"
    )
