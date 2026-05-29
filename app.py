import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

# 1. STREAMLIT PAGE CONFIGURATION
st.set_page_config(
    page_title="Productivity",
    page_icon="",
    layout="wide"
)

# 2. CACHED DATA PIPELINE 
@st.cache_data
def load_data():
    df = pd.read_csv("learningexperience.csv")
    
    df = df.drop(columns=["id","tasks", "total"])
    
    df['date'] = pd.to_datetime(df['date'], format='%m-%d-%Y', errors='coerce')

    # Decimal Duration Calculation (Hours spent)
    start_dt = pd.to_datetime(df['start'], format='%H:%M', errors='coerce')
    end_dt = pd.to_datetime(df['end'], format='%H:%M', errors='coerce')
    df['duration'] = end_dt - start_dt
    
    # Map explicit string/categorical component tags back if needed
    df['start'] = start_dt.dt.time
    df['end'] = end_dt.dt.time
    df['duration'] = (pd.to_timedelta(df['duration']).dt.total_seconds() / 3600).abs()
    return df

# Initialize Data Setup Runtime
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading your raw file data: {e}")
    st.stop()


# 3. SIDEBAR: PERSONAL DESCRIPTION & RESPONSIVE TIMELINE CONTROLS
with st.sidebar:
    st.title("👤 About Me")
    st.markdown("""
    **Name:** Nyein Min Soe  
    **Project:** Productivity Tracking  
    
    This dashboard shows the works I have done at an Internship position, and the major accomplishments that I have achieved during that time.
    """)
    st.write("---")
    
    st.header("⚙️ Time-Series Settings")
    time_granularity = st.radio(
        "Choose Trends Granularity:",
        options=["Days", "Weeks"],
        help="This setting directly updates the visual plotting structure inside the 'Time-Series Trends' tab."
    )


# 4. MAIN CONTAINER ENGINE: TAB SEPARATION CONTROL
st.title(" Productivity Dashboard")

tab1, tab2 = st.tabs(["Task Analysis", "Time-Series Trends"])


# ==========================================
# TAB 1: ORIGINAL CATEGORIZATION BAR PLOTS
# ==========================================
with tab1:
    st.subheader("Micro-Return on Investment by Category")
    "My service learning internship journey begins at the End of July 2025 and lasts till the end of the year."
    "During those times, I have been abled to work on different aspects such as learning new skills by attending new courses, improving academic writing, and research paper developments."
    "This is mainly due to the the opportunities given by Parami, and the mentors and people that I have met there."
    "Please, take a look at what I have done to understand my journey through this learning."
    sns.set_theme(style="whitegrid")
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(32, 12))

    # Plot A: Total Categorical Hours Weight
    time_spent = df.groupby('task_cat')['duration'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(x='duration', y='task_cat', data=time_spent, ax=ax1, palette="Blues_r", hue='task_cat', legend=False)
    ax1.set_title("The Time Investment (Total Hours)", fontsize=14, fontweight='bold', pad=50)
    ax1.set_xlabel("Total Hours Spent", fontsize=12)
    ax1.set_ylabel("", fontsize=12)
    
    for p in ax1.patches:
        ax1.annotate(f"{p.get_width():.1f} hrs", (p.get_width() + 0.1, p.get_y() + p.get_height()/2), va='center', fontweight='bold')

    # Plot B: Emotional ROI Breakdown Metrics
    roi = df.groupby('task_cat')[['personal_enjoyment', 'stress_level']].mean().reset_index()
    melted_roi = roi.melt(id_vars='task_cat', var_name='Metric', value_name='Score')
    melted_roi['Metric'] = melted_roi['Metric'].replace({'personal_enjoyment': 'Enjoyment', 'stress_level': 'Stress Level'})

    sns.barplot(x='Score', y='task_cat', hue='Metric', data=melted_roi, ax=ax2, palette={'Enjoyment': '#2ecc71', 'Stress Level': '#e74c3c'}
    )
    ax2.set_title("The Emotional Return on Investment (ROI)", fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel("Average Score (1 - 10)", fontsize=12)
    ax2.set_xlim(0, 10)
    ax2.set_ylabel("")
    ax2.set_yticklabels([]) 
    ax2.legend(loc='lower right', frameon=True, facecolor='white')

    plt.tight_layout()
    st.pyplot(fig1)
    
    # 📝 TYPE YOUR TAB 1 EXPLANATION INSIDE THE TRIPLE QUOTES BELOW:
    st.markdown("#### Task Analysis Insights & Accomplishments")
    st.markdown("""
    The overall metrics for my accomplishments are as follows:
    - **Accomplishments :** Successfully completed 4 academic courses, read 2 books, and done 3 posts, during that time. Also, assisted in 3 expert interviews, and make contact with others to understand the relationship.
    - **Insight:** I personally believe that the highest form of enjoyment doesn't neceressily depends on how much I hae done but what I am doing for the process and do I feel statisfy or not. 
    - **Takeaway:** My key take away was that it is essential to do more work on what you enjoy and this will allow you to cope with the work.
    """)


# ==========================================
# TAB 2: TIME-SERIES RESPONSIVE GRAPH ENGINE
# ==========================================
with tab2:
    if time_granularity == "Days":
        st.subheader("Daily Productivity, Stress and Enjoyment Over Days")
        "The figures below showcase the stress, working time, and enjoyment over the period 180+ days"
        # Aggregate daily tracking metrics safely
        daily = df.groupby('date').agg({'duration': 'sum', 'personal_enjoyment': 'mean', 'stress_level': 'mean'}).reset_index()
        
        fig2, (ax_t1, ax_t2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        # Sub-Graph A: Workload Flow
        ax_t1.plot(daily['date'], daily['duration'], color='#8e44ad', marker='o', linewidth=2, label='Total Hours')
        ax_t1.fill_between(daily['date'], daily['duration'], color='#8e44ad', alpha=0.1)
        ax_t1.set_title("The Chronological Journey: Daily Workload & Well-being Trends", fontsize=14, fontweight='bold', pad=10)
        ax_t1.set_ylabel("Hours Worked / Day", fontsize=11)
        ax_t1.grid(True, linestyle='--', alpha=0.5)
        
        # Sub-Graph B: Sanity Fluctuation Tracker 
        ax_t2.plot(daily['date'], daily['personal_enjoyment'], color='#2ecc71', marker='o', linewidth=2, label='Average Enjoyment')
        ax_t2.plot(daily['date'], daily['stress_level'], color='#e74c3c', marker='x', linestyle='--', linewidth=2, label='Average Stress')
        ax_t2.set_ylabel("Metric Score (1 - 10)", fontsize=11)
        ax_t2.set_xlabel("Date", fontsize=11)
        ax_t2.set_ylim(1, 10)
        ax_t2.grid(True, linestyle='--', alpha=0.5)
        ax_t2.legend(loc='upper left', frameon=True, facecolor='white')
        
        fig2.autofmt_xdate()
        plt.tight_layout()
        st.pyplot(fig2)
        
        # 📝 TYPE YOUR DAILY PLOT EXPLANATION INSIDE THE TRIPLE QUOTES BELOW:
        st.markdown("#### Daily Timeline Insights")
        st.markdown("""
        Following is the daily trend of the total working Hours, average Stress, and Enjoyment of life:
        - I can see that the working time tends to flactuate a little bit in the early days of August, Ater Sep, Early Oct, and later Dec.
        - For the enjoyment the relationship is that the later end of Sep, the middle periods of October, and November are least stressful times. 
        - I personally feel that the stress and the conditions and working hours have a bit of connection as it sometimes longer working hours cause burnouts, but it is more of a separate issue than the direct relationship.
        """)

    else:
        st.subheader("Daily Productivity, Stress and Enjoyment Over Weeks")
        "The picures below shows the sum for each week of stress, daily working time, and enjoyment over the period of six months."
        # Keep internal grouping layout sequence matching chronological pipeline dates
        weekly = df.groupby('week', sort=True).agg({'duration': 'sum', 'personal_enjoyment': 'mean', 'stress_level': 'mean'}).reset_index()
        
        fig3, (ax_w1, ax_w2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Weekly Plot A: Workload Weight
        ax_w1.plot(weekly['week'], weekly['duration'], color='#8e44ad', marker='o', linewidth=2.5)
        ax_w1.set_title("Total Workload by Week", fontsize=13, fontweight='bold')
        ax_w1.set_xlabel("Week Number", fontsize=11)
        ax_w1.set_ylabel("Total Hours Logged", fontsize=11)
        ax_w1.grid(axis='y', linestyle='--', alpha=0.6)
        
        # Weekly Plot B: Subjective Exhaustion Analysis
        ax_w2.plot(weekly['week'], weekly['personal_enjoyment'], color='#2ecc71', marker='o', linewidth=2.5, label='Avg Enjoyment')
        ax_w2.plot(weekly['week'], weekly['stress_level'], color='#e74c3c', marker='s', linewidth=2.5, label='Avg Stress')
        ax_w2.set_title("Mental Trends by Week", fontsize=13, fontweight='bold')
        ax_w2.set_xlabel("Week Number", fontsize=11)
        ax_w2.set_ylabel("Score (1 - 10)", fontsize=11)
        ax_w2.set_ylim(1, 10)
        ax_w2.grid(axis='y', linestyle='--', alpha=0.6)
        ax_w2.legend(loc='best', frameon=True, facecolor='white')
        
        plt.tight_layout()
        st.pyplot(fig3)
        
        # 📝 TYPE YOUR WEEKLY PLOT EXPLANATION INSIDE THE TRIPLE QUOTES BELOW:
        st.markdown("####  Weekly Timeline Insights")
        st.markdown("""
        Following is the weekly trend of the total working Hours, average Stress, and Enjoyment of life:
        - I can see that I have worked more during week 4, 5 and 6. That times are in summerbreak, and the most contributions comes during that time.
        - For the enjoyment the relationship is stress and enjoyment rhymes, but enjoyment is at higher pace than stress, and stress fluctuates. 
        - I can see that I personally felt enjoyabe overall, but the stress comes during busy weeks, but those weeks are what is worth of learning.
        """)
