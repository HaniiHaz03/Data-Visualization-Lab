
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Lab 10 | Framing the Data Story",
    page_icon="📊",
    layout="wide"
)

st.title("Framing the Data Story")
st.caption("Understanding students' data visualization skills")

# ==================================================
# 2. ORIGINAL DATA
# ==================================================

skills = [
    "Data storytelling",
    "Python",
    "Chart selection",
    "Color and labels",
    "Data cleaning"
]

ratings = [2.4, 3.0, 3.2, 3.7, 4.1]

df = pd.DataFrame({
    "Skill": skills,
    "Average rating": ratings
})

# ==================================================
# 3. AUDIENCE SELECTION
# ==================================================

st.sidebar.header("Dashboard Settings")

audience = st.sidebar.selectbox(
    "Select target audience",
    [
        "Students",
        "Workshop Instructor",
        "Department Manager"
    ]
)

# ==================================================
# 4. CHANGE ONE RATING
# ==================================================

st.sidebar.subheader("Adjust the Data")

new_rating = st.sidebar.slider(
    "Change Data Storytelling rating",
    min_value=1.0,
    max_value=5.0,
    value=2.4,
    step=0.1
)

df.loc[
    df["Skill"] == "Data storytelling",
    "Average rating"
] = new_rating

# ==================================================
# 5. IDENTIFY THE LOWEST-RATED SKILL
# ==================================================

lowest_row = df.loc[df["Average rating"].idxmin()]

lowest_skill = lowest_row["Skill"]
lowest_rating = lowest_row["Average rating"]

# ==================================================
# 6. FRAME THE STORY FOR EACH AUDIENCE
# ==================================================

if audience == "Students":
    title = f"Students Need More Support in {lowest_skill}"
    purpose = (
        "Help students identify which data visualization skill "
        "they should improve."
    )
    takeaway = (
        f"{lowest_skill} received the lowest average self-rating "
        f"of {lowest_rating:.1f} out of 5. Students should focus "
        "on improving this skill."
    )

elif audience == "Workshop Instructor":
    title = f"Prioritize {lowest_skill} in the Next Workshop"
    purpose = (
        "Help the instructor decide which topic deserves more "
        "attention during workshop planning."
    )
    takeaway = (
        f"{lowest_skill} has the lowest average rating "
        f"({lowest_rating:.1f}/5). Allocate more workshop time "
        "to this area."
    )

else:
    title = f"Students Need Support in {lowest_skill}"
    purpose = (
        "Help the department manager identify areas where "
        "additional learning support may be needed."
    )
    takeaway = (
        f"{lowest_skill} has the lowest average rating "
        f"({lowest_rating:.1f}/5). Consider providing targeted "
        "learning resources or training."
    )

# ==================================================
# 7. DISPLAY THE DATA STORY
# ==================================================

st.subheader(title)

st.write(f"**Audience:** {audience}")
st.write(f"**Purpose:** {purpose}")
st.info(f"**Key takeaway:** {takeaway}")

# ==================================================
# 8. CREATE THE HORIZONTAL BAR CHART
# ==================================================

fig, ax = plt.subplots(figsize=(9, 5))

bar_colors = [
    "#E07A3F" if skill == lowest_skill else "#4C78A8"
    for skill in df["Skill"]
]

bars = ax.barh(
    df["Skill"],
    df["Average rating"],
    color=bar_colors
)

ax.set_xlim(0, 5)
ax.set_xticks(range(0, 6))

ax.set_xlabel(
    "Average self-rating (1 = beginner, 5 = confident)"
)

ax.set_title(
    f"{lowest_skill} received the lowest average rating",
    fontsize=13,
    pad=15
)

ax.invert_yaxis()

# Add value labels
for bar, value in zip(bars, df["Average rating"]):
    ax.text(
        value + 0.05,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.1f}",
        va="center"
    )

# Reduce unnecessary visual elements
ax.grid(
    axis="x",
    color="#DDDDDD",
    linewidth=0.7
)

ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()

st.pyplot(fig, clear_figure=True)

st.caption(
    "Fictional practice values. Ratings are averages on a "
    "1–5 scale. The orange bar highlights the lowest-rated skill."
)

# ==================================================
# 9. DISPLAY THE DATA TABLE
# ==================================================

with st.expander("View the rating data"):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# ==================================================
# 10. EXPLAIN THE GRAPH
# ==================================================

st.subheader("How to Read This Chart")

st.write(
    "- The vertical axis lists the five data visualization skills."
)

st.write(
    "- The horizontal axis shows average self-ratings from 1 to 5."
)

st.write(
    "- Each bar represents the average rating for one skill."
)

st.write(
    "- The orange bar highlights the skill with the lowest average rating."
)

st.write(
    "- The values are fictional averages, not individual student scores."
)

st.caption(
    "The results are intended for chart-design practice and "
    "should not be interpreted as findings from a real survey."
)
