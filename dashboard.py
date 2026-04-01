"""
dashboard.py — IT Job Market Analysis — Streamlit Dashboard
============================================================
Interactive web dashboard for Gujarat IT Job Market Analysis.

Run locally:
    pip install streamlit
    streamlit run dashboard/dashboard.py

Features:
  - Sidebar filters (City, Domain, Portal, Job Type)
  - KPI metric cards
  - 10 interactive charts
  - Raw data table with search
  - Download filtered data

Upload final_merged_jobs.csv to same folder or
update FILE_PATH below.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
matplotlib.use("Agg")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG — must be first Streamlit command
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title  = "IT Job Market — Gujarat",
    page_icon   = "🔍",
    layout      = "wide",
    initial_sidebar_state = "expanded",
)

# ─────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────
CITY_COLORS   = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2"]
PORTAL_COLORS = ["#FF5733", "#0A66C2", "#E8423F", "#0CAA41", "#003A9B"]
TYPE_COLORS   = ["#4E79A7", "#F28E2B", "#E15759", "#59A14F"]
BG            = "#F7F9FC"
ACCENT        = "#2C3E50"

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and preprocess dataset. Cached for performance."""
    # Try multiple paths
    for path in [
        "final_merged_jobs.csv",
        "data/final_merged_jobs.csv",
        "../data/final_merged_jobs.csv",
        os.path.join(os.path.dirname(__file__), "..", "data", "final_merged_jobs.csv"),
    ]:
        if os.path.exists(path):
            df = pd.read_csv(path, encoding="utf-8-sig")
            df["date_posted"]      = pd.to_datetime(df["date_posted"], errors="coerce")
            df["salary_lpa"]       = df["salary_annual_inr"] / 100_000
            df["experience_years"] = pd.to_numeric(
                df["experience_years"], errors="coerce"
            ).fillna(0)
            return df
    return None


# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .main { background-color: #F7F9FC; }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #E0E6ED;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    div[data-testid="metric-container"] label {
        font-size: 13px !important;
        color: #6B7280 !important;
        font-weight: 600 !important;
    }
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #2C3E50 !important;
    }

    /* Section headers */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #2C3E50;
        padding: 8px 0 4px 0;
        border-bottom: 2px solid #4E79A7;
        margin-bottom: 16px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #2C3E50;
        color: white;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] p {
        color: white !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9CA3AF;
        font-size: 13px;
        padding: 20px;
        border-top: 1px solid #E5E7EB;
        margin-top: 40px;
    }

    /* Chart containers */
    .chart-box {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #E0E6ED;
    }

    /* Warning/info box */
    .edu-notice {
        background: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 13px;
        color: #92400E;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER — save matplotlib fig to streamlit
# ─────────────────────────────────────────────────────────────
def show_fig(fig):
    """Display a matplotlib figure in Streamlit."""
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────
def main():

    # ── Load data ─────────────────────────────────────────────
    df_raw = load_data()

    if df_raw is None:
        st.error("❌ Could not find `final_merged_jobs.csv`")
        st.info("""
        **To fix this:**
        1. Make sure `final_merged_jobs.csv` is in the same folder as `dashboard.py`
        2. Or update the path in the `load_data()` function
        """)
        st.stop()

    # ── SIDEBAR ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 🔍 IT Job Market")
        st.markdown("### Gujarat, India")
        st.markdown("---")

        st.markdown("### 🎛️ Filters")

        # City filter
        all_cities  = sorted(df_raw["city"].dropna().unique().tolist())
        sel_cities  = st.multiselect(
            "🏙️ City",
            options=all_cities,
            default=all_cities,
        )

        # Portal filter
        all_portals = sorted(df_raw["source_portal"].dropna().unique().tolist())
        sel_portals = st.multiselect(
            "🌐 Portal",
            options=all_portals,
            default=all_portals,
        )

        # Job type filter
        all_types  = sorted(df_raw["job_type"].dropna().unique().tolist())
        sel_types  = st.multiselect(
            "💼 Job Type",
            options=all_types,
            default=all_types,
        )

        # Domain filter
        all_domains  = sorted(df_raw["job_domain"].dropna().unique().tolist())
        sel_domains  = st.multiselect(
            "🏷️ IT Domain",
            options=all_domains,
            default=all_domains,
        )

        st.markdown("---")
        st.markdown("### 📊 Dataset Info")
        st.markdown(f"**Total Records:** {len(df_raw):,}")
        st.markdown(f"**Portals:** {df_raw['source_portal'].nunique()}")
        st.markdown(f"**Domains:** {df_raw['job_domain'].nunique()}")
        st.markdown(f"**Cities:** {df_raw['city'].nunique()}")
        st.markdown("---")
        st.markdown("""
        <div style='color:#94A3B8; font-size:12px;'>
        ⚠️ Educational Purpose Only<br>
        Data is synthetically simulated.<br>
        Final Year Internship Project
        </div>
        """, unsafe_allow_html=True)

    # ── Apply filters ─────────────────────────────────────────
    df = df_raw.copy()
    if sel_cities:
        df = df[df["city"].isin(sel_cities)]
    if sel_portals:
        df = df[df["source_portal"].isin(sel_portals)]
    if sel_types:
        df = df[df["job_type"].isin(sel_types)]
    if sel_domains:
        df = df[df["job_domain"].isin(sel_domains)]

    if len(df) == 0:
        st.warning("⚠️ No records match your filters. Please adjust the selections.")
        st.stop()

    sal_df = df[df["salary_lpa"] > 0.5].copy()

    # ── HEADER ────────────────────────────────────────────────
    st.markdown("""
    <h1 style='color:#2C3E50; margin-bottom:4px;'>
        🔍 IT Job Market Analysis — Gujarat, India
    </h1>
    <p style='color:#6B7280; font-size:15px; margin-bottom:8px;'>
        Final Year Engineering Internship Project &nbsp;|&nbsp;
        5 Portals &nbsp;|&nbsp; 4 Cities &nbsp;|&nbsp; 20 IT Domains
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='edu-notice'>
    ⚠️ <b>Educational Purpose Only</b> — All data is synthetically simulated.
    Built as part of a Data Analytics Internship to learn end-to-end data pipeline development.
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────
    # KPI METRIC CARDS
    # ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>📊 Overview</div>",
                unsafe_allow_html=True)

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    k1.metric("📋 Total Jobs",       f"{len(df):,}")
    k2.metric("🏙️ Cities",           f"{df['city'].nunique()}")
    k3.metric("🌐 Portals",          f"{df['source_portal'].nunique()}")
    k4.metric("🏷️ Domains",          f"{df['job_domain'].nunique()}")
    k5.metric("🎓 Internships",      f"{df[df['job_type']=='Internship'].shape[0]:,}")
    k6.metric("💰 Median Salary",
              f"₹{sal_df['salary_lpa'].median():.1f}L" if len(sal_df) > 0 else "N/A")

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────
    # ROW 1 — City Distribution + Portal Distribution
    # ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🏙️ City & Portal Distribution</div>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        city_counts = df["city"].value_counts()
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        colors_c = CITY_COLORS[:len(city_counts)]
        bars = ax.bar(city_counts.index, city_counts.values,
                      color=colors_c, edgecolor="white", width=0.6)
        for bar, val in zip(bars, city_counts.values):
            ax.text(bar.get_x()+bar.get_width()/2,
                    bar.get_height()+5, f"{int(val):,}",
                    ha="center", fontweight="bold", fontsize=10)
        ax.set_title("Jobs per City", fontweight="bold", fontsize=13)
        ax.set_ylabel("Job Listings")
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        show_fig(fig)

    with col2:
        portal_counts = df["source_portal"].value_counts()
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        colors_p = PORTAL_COLORS[:len(portal_counts)]
        bars = ax.bar(portal_counts.index, portal_counts.values,
                      color=colors_p, edgecolor="white", width=0.6)
        for bar, val in zip(bars, portal_counts.values):
            ax.text(bar.get_x()+bar.get_width()/2,
                    bar.get_height()+5, f"{int(val):,}",
                    ha="center", fontweight="bold", fontsize=10)
        ax.set_title("Jobs per Portal", fontweight="bold", fontsize=13)
        ax.set_ylabel("Job Listings")
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        plt.xticks(rotation=15, ha="right", fontsize=9)
        plt.tight_layout()
        show_fig(fig)

    # ─────────────────────────────────────────────────────────
    # ROW 2 — Domain Trends
    # ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🏷️ IT Domain Hiring Trends</div>",
                unsafe_allow_html=True)

    domain_counts = df["job_domain"].value_counts().head(15)
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    colors_d = sns.color_palette("Spectral", len(domain_counts))
    bars = ax.barh(domain_counts.index[::-1],
                   domain_counts.values[::-1],
                   color=colors_d[::-1], edgecolor="white", height=0.7)
    for bar, val in zip(bars, domain_counts.values[::-1]):
        ax.text(bar.get_width()+2,
                bar.get_y()+bar.get_height()/2,
                str(int(val)), va="center",
                fontsize=9, fontweight="bold")
    ax.set_title("Top 15 IT Domains by Job Demand",
                 fontweight="bold", fontsize=13)
    ax.set_xlabel("Number of Listings")
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    show_fig(fig)

    # ─────────────────────────────────────────────────────────
    # ROW 3 — City × Domain Heatmap + Job Type
    # ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🔥 Heatmap & Job Types</div>",
                unsafe_allow_html=True)

    col3, col4 = st.columns([2, 1])

    with col3:
        pivot = df.pivot_table(
            index="job_domain", columns="city",
            values="job_title", aggfunc="count", fill_value=0
        )
        pivot = pivot.loc[
            pivot.sum(axis=1).sort_values(ascending=False).head(12).index
        ]
        fig, ax = plt.subplots(figsize=(9, 7))
        fig.patch.set_facecolor("white")
        sns.heatmap(pivot, ax=ax, annot=True, fmt="d",
                    cmap="YlOrRd", linewidths=0.5,
                    linecolor="white",
                    cbar_kws={"label":"Jobs","shrink":0.8},
                    annot_kws={"size":9, "weight":"bold"})
        ax.set_title("City × IT Domain Heatmap",
                     fontweight="bold", fontsize=13)
        ax.set_xlabel("City")
        ax.set_ylabel("Domain")
        ax.tick_params(axis="x", rotation=0)
        ax.tick_params(axis="y", rotation=0, labelsize=8)
        plt.tight_layout()
        show_fig(fig)

    with col4:
        jt_counts = df["job_type"].value_counts()
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor("white")
        wedges, _, autotexts = ax.pie(
            jt_counts.values,
            labels=jt_counts.index,
            colors=TYPE_COLORS[:len(jt_counts)],
            autopct="%1.1f%%", startangle=90,
            wedgeprops=dict(width=0.55,
                           edgecolor="white",
                           linewidth=2),
        )
        for at in autotexts:
            at.set_fontsize(9)
            at.set_fontweight("bold")
        ax.set_title("Job Type Split",
                     fontweight="bold", fontsize=13)
        plt.tight_layout()
        show_fig(fig)

    # ─────────────────────────────────────────────────────────
    # ROW 4 — Top Skills
    # ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🔥 Top In-Demand Tech Skills</div>",
                unsafe_allow_html=True)

    all_skills = (
        df["skills"].dropna()
          .str.split(", ").explode()
          .str.strip().str.title()
          .value_counts().head(25)
    )
    fig, ax = plt.subplots(figsize=(14, 5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    colors_s = sns.color_palette("coolwarm_r", 25)
    bars = ax.bar(range(25), all_skills.values,
                  color=colors_s, edgecolor="white")
    ax.set_xticks(range(25))
    ax.set_xticklabels(all_skills.index,
                       rotation=45, ha="right", fontsize=8.5)
    for bar, val in zip(bars, all_skills.values):
        ax.text(bar.get_x()+bar.get_width()/2,
                bar.get_height()+2, str(int(val)),
                ha="center", fontsize=7)
    ax.set_title("Top 25 Most In-Demand Tech Skills",
                 fontweight="bold", fontsize=13)
    ax.set_ylabel("Job Mentions")
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    show_fig(fig)

    # ─────────────────────────────────────────────────────────
    # ROW 5 — Salary Analysis
    # ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>💰 Salary Analysis</div>",
                unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:
        if len(sal_df) > 0:
            cities_available = [
                c for c in ["Surat","Ahmedabad","Vadodara","Gandhinagar"]
                if c in sal_df["city"].values
            ]
            data_city = [
                sal_df[sal_df["city"]==c]["salary_lpa"].dropna().values
                for c in cities_available
            ]
            fig, ax = plt.subplots(figsize=(7, 4.5))
            fig.patch.set_facecolor("white")
            ax.set_facecolor("white")
            bp = ax.boxplot(data_city, patch_artist=True,
                            notch=False, widths=0.55)
            for patch, color in zip(bp["boxes"],
                                    CITY_COLORS[:len(cities_available)]):
                patch.set_facecolor(color)
                patch.set_alpha(0.8)
            for med in bp["medians"]:
                med.set_color("white")
                med.set_linewidth(2.5)
            ax.set_xticklabels(cities_available, fontsize=10)
            ax.set_title("Salary Distribution by City (LPA)",
                         fontweight="bold", fontsize=12)
            ax.set_ylabel("Annual Salary (LPA)")
            ax.spines[["top","right"]].set_visible(False)
            ax.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            show_fig(fig)
        else:
            st.info("No salary data available for selected filters.")

    with col6:
        if len(sal_df) > 0:
            top8 = sal_df.groupby("job_domain")["salary_lpa"] \
                         .median().nlargest(8)
            fig, ax = plt.subplots(figsize=(7, 4.5))
            fig.patch.set_facecolor("white")
            ax.set_facecolor("white")
            colors_8 = sns.color_palette("RdYlGn", 8)
            bars = ax.barh(top8.index[::-1], top8.values[::-1],
                           color=colors_8[::-1], edgecolor="white")
            for bar, val in zip(bars, top8.values[::-1]):
                ax.text(bar.get_width()+0.1,
                        bar.get_y()+bar.get_height()/2,
                        f"₹{val:.1f}L", va="center",
                        fontsize=9, fontweight="bold")
            ax.set_title("Median Salary by Domain (Top 8)",
                         fontweight="bold", fontsize=12)
            ax.set_xlabel("Median Salary (LPA)")
            ax.spines[["top","right"]].set_visible(False)
            ax.grid(axis="x", alpha=0.3)
            plt.tight_layout()
            show_fig(fig)

    # ─────────────────────────────────────────────────────────
    # ROW 6 — Experience + Top Companies
    # ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>📅 Experience & Companies</div>",
                unsafe_allow_html=True)

    col7, col8 = st.columns(2)

    with col7:
        exp_numeric = df["experience_years"].dropna()
        bins        = [0, 1, 3, 5, 8, 12, 20]
        labels_exp  = ["Fresher\n(0-1yr)", "Junior\n(1-3yr)",
                       "Mid\n(3-5yr)", "Senior\n(5-8yr)",
                       "Lead\n(8-12yr)", "Principal\n(12+yr)"]
        exp_binned     = pd.cut(exp_numeric, bins=bins,
                                labels=labels_exp, right=False)
        exp_bin_counts = exp_binned.value_counts().reindex(labels_exp)

        fig, ax = plt.subplots(figsize=(7, 4.5))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        colors_exp = sns.color_palette("Blues_d", 6)
        bars = ax.bar(range(6), exp_bin_counts.values,
                      color=colors_exp, edgecolor="white", width=0.65)
        ax.set_xticks(range(6))
        ax.set_xticklabels(labels_exp, fontsize=9)
        for bar, val in zip(bars, exp_bin_counts.values):
            ax.text(bar.get_x()+bar.get_width()/2,
                    bar.get_height()+5, f"{int(val):,}",
                    ha="center", fontweight="bold", fontsize=9)
        ax.set_title("Experience Level Distribution",
                     fontweight="bold", fontsize=12)
        ax.set_ylabel("Job Count")
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        show_fig(fig)

    with col8:
        top15_co = df["company_name"].value_counts().head(15)
        fig, ax  = plt.subplots(figsize=(7, 4.5))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        colors_co = sns.color_palette("tab20", 15)
        bars = ax.barh(top15_co.index[::-1],
                       top15_co.values[::-1],
                       color=colors_co[::-1],
                       edgecolor="white", height=0.7)
        for bar, val in zip(bars, top15_co.values[::-1]):
            ax.text(bar.get_width()+0.2,
                    bar.get_y()+bar.get_height()/2,
                    str(int(val)), va="center",
                    fontsize=8.5, fontweight="bold")
        ax.set_title("Top 15 Hiring Companies",
                     fontweight="bold", fontsize=12)
        ax.set_xlabel("Listings")
        ax.tick_params(axis="y", labelsize=8)
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        show_fig(fig)

    # ─────────────────────────────────────────────────────────
    # ROW 7 — Jobs Over Time
    # ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>📈 Job Postings Over Time</div>",
                unsafe_allow_html=True)

    daily = (df.groupby("date_posted").size()
               .reset_index(name="count"))
    daily["7d_avg"] = daily["count"].rolling(7, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(14, 4))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.fill_between(daily["date_posted"], daily["count"],
                    alpha=0.15, color="#4E79A7")
    ax.plot(daily["date_posted"], daily["count"],
            color="#4E79A7", linewidth=1.2,
            alpha=0.6, label="Daily Count")
    ax.plot(daily["date_posted"], daily["7d_avg"],
            color="#E15759", linewidth=2.5,
            label="7-Day Avg")
    ax.set_title("IT Job Postings Over Time — All 5 Portals",
                 fontweight="bold", fontsize=13)
    ax.set_xlabel("Date")
    ax.set_ylabel("Jobs Posted")
    ax.legend(fontsize=10)
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    show_fig(fig)

    # ─────────────────────────────────────────────────────────
    # ROW 8 — KEY INSIGHTS
    # ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>💡 Key Insights</div>",
                unsafe_allow_html=True)

    city_leader  = df["city"].value_counts().idxmax()
    top_domain   = df["job_domain"].value_counts().idxmax()
    top_skill    = all_skills.idxmax()
    top_company  = df["company_name"].value_counts().idxmax()
    top_portal   = df["source_portal"].value_counts().idxmax()
    median_sal   = sal_df["salary_lpa"].median() if len(sal_df) > 0 else 0
    total_intern = df[df["job_type"]=="Internship"].shape[0]

    i1, i2, i3, i4 = st.columns(4)
    with i1:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:16px;
                    border:1px solid #E0E6ED; box-shadow:0 2px 8px rgba(0,0,0,0.06);'>
        <div style='font-size:24px;'>🏙️</div>
        <div style='font-size:13px; color:#6B7280; font-weight:600;'>Leading City</div>
        <div style='font-size:20px; font-weight:700; color:#2C3E50;'>{city_leader}</div>
        <div style='font-size:12px; color:#9CA3AF;'>Most IT job listings</div>
        </div>
        """, unsafe_allow_html=True)

    with i2:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:16px;
                    border:1px solid #E0E6ED; box-shadow:0 2px 8px rgba(0,0,0,0.06);'>
        <div style='font-size:24px;'>💼</div>
        <div style='font-size:13px; color:#6B7280; font-weight:600;'>Top Domain</div>
        <div style='font-size:16px; font-weight:700; color:#2C3E50;'>{top_domain[:22]}</div>
        <div style='font-size:12px; color:#9CA3AF;'>Most in-demand</div>
        </div>
        """, unsafe_allow_html=True)

    with i3:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:16px;
                    border:1px solid #E0E6ED; box-shadow:0 2px 8px rgba(0,0,0,0.06);'>
        <div style='font-size:24px;'>🔥</div>
        <div style='font-size:13px; color:#6B7280; font-weight:600;'>Trending Skill</div>
        <div style='font-size:20px; font-weight:700; color:#2C3E50;'>{top_skill}</div>
        <div style='font-size:12px; color:#9CA3AF;'>#1 skill overall</div>
        </div>
        """, unsafe_allow_html=True)

    with i4:
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:16px;
                    border:1px solid #E0E6ED; box-shadow:0 2px 8px rgba(0,0,0,0.06);'>
        <div style='font-size:24px;'>🎓</div>
        <div style='font-size:13px; color:#6B7280; font-weight:600;'>Internships</div>
        <div style='font-size:20px; font-weight:700; color:#2C3E50;'>{total_intern:,}</div>
        <div style='font-size:12px; color:#9CA3AF;'>Available listings</div>
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────
    # ROW 9 — RAW DATA TABLE
    # ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🗃️ Browse Data</div>",
                unsafe_allow_html=True)

    show_cols = ["job_title", "company_name", "city",
                 "job_domain", "job_type", "experience",
                 "salary", "skills", "source_portal"]
    search = st.text_input("🔎 Search job title or company",
                           placeholder="e.g. Python, Data Analyst, TCS...")

    display_df = df[show_cols].copy()
    if search:
        mask = (
            display_df["job_title"].str.contains(search, case=False, na=False) |
            display_df["company_name"].str.contains(search, case=False, na=False) |
            display_df["skills"].str.contains(search, case=False, na=False)
        )
        display_df = display_df[mask]

    st.dataframe(
        display_df.head(100),
        use_container_width=True,
        height=350,
    )
    st.caption(f"Showing {min(100, len(display_df)):,} of {len(display_df):,} records")

    # ─────────────────────────────────────────────────────────
    # DOWNLOAD BUTTON
    # ─────────────────────────────────────────────────────────
    col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 4])
    with col_dl1:
        st.download_button(
            label     = "⬇️ Download Filtered CSV",
            data      = df[show_cols].to_csv(index=False).encode("utf-8"),
            file_name = "filtered_jobs.csv",
            mime      = "text/csv",
        )
    with col_dl2:
        st.download_button(
            label     = "⬇️ Download Full CSV",
            data      = df_raw[show_cols].to_csv(index=False).encode("utf-8"),
            file_name = "all_jobs.csv",
            mime      = "text/csv",
        )

    # ─────────────────────────────────────────────────────────
    # FOOTER
    # ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class='footer'>
        🔍 IT Job Market Analysis — Gujarat, India &nbsp;|&nbsp;
        Final Year Engineering Internship Project &nbsp;|&nbsp;
        ⚠️ Educational Purpose Only — Data is Synthetically Simulated<br>
        Built with Python · Pandas · Matplotlib · Seaborn · Streamlit
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
