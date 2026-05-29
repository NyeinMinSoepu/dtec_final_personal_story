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
