import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="Embracing AI in Education Analysis", 
    page_icon="🎓", 
    layout="wide"
)

# 2. Nexus Pro CSS (DEBESMSCAT Research Themed)
st.markdown("""
<style>
    .stApp { background-color: #f1f4f9; }
    .header {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
        color: white; padding: 2.5rem; border-radius: 15px; margin-bottom: 25px;
        border-bottom: 5px solid #17d427;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important; border-radius: 12px !important;
        border: 1px solid #d1d5db !important; padding: 0px !important;
    }
    .title-box {
        background-color: #0d3b66; color: white; padding: 12px 20px;
        font-weight: 700; font-size: 1.15rem; border-radius: 12px 12px 0 0;
    }
    .stMetricValue { color: #007cbb !important; font-weight: 900 !important; }
</style>
""", unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("data.csv")
        data.columns = data.columns.str.strip()
        if "AI Adoption Rate (%)" in data.columns:
            data.rename(columns={"AI Adoption Rate (%)": "Rate"}, inplace=True)
        return data
    except Exception as e:
        st.error(f"⚠️ Error loading 'data.csv': {e}")
        return pd.DataFrame()

df = load_data()

# 4. Official Research Header
st.markdown("""
<div class="header">
    <div style="font-size: 32px; font-weight: 800; line-height: 1.2;">EMBRACING AI IN EDUCATION:<br>How Students and Teachers are Adapting (2024–2026)</div>
    <div style="font-size: 14px; margin-top: 10px; color: #cfd8e3;">DEBESMSCAT | College of Computing and Information Technology</div>
</div>
""", unsafe_allow_html=True)

if not df.empty:
    latest_year = df['Year'].max()
    initial_year = df['Year'].min()
    
    # Current Peak Values
    s_val = df[(df['Year']==latest_year) & (df['User Type']=='Student')]['Rate'].values[0]
    t_val = df[(df['Year']==latest_year) & (df['User Type']=='Teacher')]['Rate'].values[0]
    
    # Growth & Averages
    s_growth = s_val - df[(df['Year']==initial_year) & (df['User Type']=='Student')]['Rate'].values[0]
    t_growth = t_val - df[(df['Year']==initial_year) & (df['User Type']=='Teacher')]['Rate'].values[0]
    avg_student = df[df['User Type']=='Student']['Rate'].mean()
    avg_teacher = df[df['User Type']=='Teacher']['Rate'].mean()

    # 5. Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        with st.container(border=True):
            st.markdown('<div class="title-box">Total Student Growth</div>', unsafe_allow_html=True)
            st.metric("", f"+{s_growth}%", "Overall Trend")
    with m2:
        with st.container(border=True):
            st.markdown('<div class="title-box">Total Teacher Growth</div>', unsafe_allow_html=True)
            st.metric("", f"+{t_growth}%", "Overall Trend")
    with m3:
        with st.container(border=True):
            st.markdown('<div class="title-box">Avg. Historical Gap</div>', unsafe_allow_html=True)
            st.metric("", f"{round(avg_student - avg_teacher, 1)}%", "3-Year Avg.")

    # 6. Visualizations Row
    c_left, c_right = st.columns(2)

    with c_left:
        with st.container(border=True):
            st.markdown('<div class="title-box">📈 Fig 1: 3-Year Growth Trajectory</div>', unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            for user, color in zip(["Student", "Teacher"], ["#17d427", "#3b6978"]):
                subset = df[df["User Type"] == user].sort_values("Year")
                ax1.plot(subset["Year"], subset["Rate"], marker='o', label=user, color=color, lw=3, zorder=3)
            ax1.grid(True, linestyle='--', alpha=0.6, zorder=0) 
            ax1.set_ylim(0, 100)
            ax1.set_xticks(df['Year'].unique())
            ax1.set_ylabel("Adoption Rate (%)")
            ax1.legend(frameon=True)
            st.pyplot(fig1)

    with c_right:
        with st.container(border=True):
            st.markdown('<div class="title-box">📊 Fig 2: Comparative Yearly View</div>', unsafe_allow_html=True)
            years = sorted(df['Year'].unique())
            x = np.arange(len(years))
            width = 0.35
            fig2, ax2 = plt.subplots(figsize=(8, 5.2))
            s_rates = df[df['User Type'] == 'Student'].sort_values('Year')['Rate'].values
            t_rates = df[df['User Type'] == 'Teacher'].sort_values('Year')['Rate'].values
            
            ax2.bar(x - width/2, s_rates, width, label='Student', color='#17d427', zorder=3)
            ax2.bar(x + width/2, t_rates, width, label='Teacher', color='#3b6978', zorder=3)
            ax2.grid(True, axis='y', linestyle='--', alpha=0.6, zorder=0) 
            ax2.set_xticks(x)
            ax2.set_xticklabels(years)
            ax2.set_ylim(0, 100)
            ax2.set_ylabel("Adoption Rate (%)")
            ax2.legend(frameon=True)
            st.pyplot(fig2)

    # 7. Strategic Overall Insights
    with st.container(border=True):
        st.markdown('<div class="title-box">💡 Key Research Insights (2024–2026)</div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            1. **Adoption Velocity:** Student AI usage grew from **55%** to **82%** — a total increase of **{s_growth}%**, driven largely by research and data analysis needs.
            2. **The Teacher Pivot:** Faculty adoption reached **63%** by 2026. While slower than students, the shift from *Lesson Planning* to *Curriculum Design* shows a deepening of AI integration.
            """)
        with col_b:
            st.markdown(f"""
            3. **The Implementation Gap:** The adoption delta between students and teachers remains significant at **{s_val - t_val}%**. This suggests a need for targeted institutional policy adjustments.
            4. **Efficiency vs. Adoption:** While student usage is nearing a plateau, teacher growth remains linear, indicating a "catch-up" phase as ethical frameworks and training become standardized.
            """)

    # 8. Data Explorer & References
    with st.container(border=True):
        st.markdown('<div class="title-box">🔍 Full Dataset Explorer & References</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **References**
        * UNESCO Institute for Statistics (2025). AI and education.
        * OECD (2026). Digital Education Outlook.
        * Stanford University (2025). AI Index Report.
        """)
else:
    st.warning("⚠️ 'data.csv' is empty or missing.")