
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Lab 9 - Chart Design",
    layout="wide"
)

# Dataset with six fictional branches
data = pd.DataFrame({
    "Branch": [
        "Kuala Lumpur",
        "Penang",
        "Johor",
        "Perak",
        "Sabah",
        "Sarawak"
    ],
    "Sales": [96, 99, 98, 100, 97, 99]
})

# Application title
st.title("Improving Data Visualization")
st.write(
    "Comparison of cluttered and improved bar charts "
    "using fictional branch sales data."
)

# Select chart style
version = st.radio(
    "Select Chart Version:",
    ["Cluttered", "Improved"],
    horizontal=True
)

# Create chart
fig, ax = plt.subplots(figsize=(10, 5))

if version == "Cluttered":

    bars = ax.bar(
        data["Branch"],
        data["Sales"],
        color=[
            "#8FB9A8", "#D8B365", "#B2ABD2",
            "#5E3C99", "#E07A3F", "#80A6C2"
        ]
    )

    ax.set_ylim(95, 101)
    ax.set_facecolor("#E8E8E8")
    ax.grid(True, color="white", linewidth=2)
    ax.set_title("BRANCH SALES PERFORMANCE!!!")

else:

    bars = ax.bar(
        data["Branch"],
        data["Sales"],
        color="#4C78A8"
    )

    # Highlight the highest sales value
    highest_index = data["Sales"].idxmax()
    bars[highest_index].set_color("#E07A3F")

    # Start the vertical axis at zero
    ax.set_ylim(0, 105)
    ax.set_yticks(range(0, 101, 20))

    # Display sales values
    ax.bar_label(bars, fmt="%.0f", padding=3)

    # Descriptive title
    ax.set_title("Perak Branch Records the Highest Sales")

    # Simple horizontal gridlines
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.7)
    ax.set_axisbelow(True)

    # Remove unnecessary borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# Axis labels
ax.set_xlabel("Branch")
ax.set_ylabel("Sales (units)")

# Keep branch names readable
plt.xticks(rotation=0)

# Source and author note
fig.text(
    0.5, 0.01,
    "Data: fictional practice values (2026) | Chart: Nurul Haniizati",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.05, 1, 1])

# Display chart
st.pyplot(fig, clear_figure=True)

# Explanation
st.caption(
    "The improved chart uses a zero baseline, clear labels "
    "and minimal decoration to support accurate comparison."
)

plt.close(fig)
