
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Lab 8 | Sentiment Analysis",
    page_icon="💬",
    layout="wide"
)

st.title("Product Feedback: Qualitative Data and Sentiment Analysis")
st.caption(
    "Practice data only. Automated sentiment labels are estimates "
    "and should be reviewed by humans."
)

# ==================================================
# 2. SAMPLE PRODUCT REVIEWS
# ==================================================

reviews = [
    "The bottle keeps my water cold all day.",
    "Great size and easy to carry to class.",
    "I love the simple design and sturdy lid.",
    "It leaks in my bag. Very disappointing.",
    "The cap is hard to open and the bottle feels heavy.",
    "Good value, but cleaning the narrow opening is difficult.",
    "Keeps drinks cold, though the paint scratches easily.",
    "The bottle is fine. Nothing special either way.",
    "I expected better insulation for this price.",
    "Lightweight, useful, and easy to wash.",
    "Not bad, but I would prefer a larger capacity.",
    "Excellent bottle. I use it every day.",
    "The lid broke after one week. Poor quality.",
    "It works as described and arrived on time.",
    "Nice color, but it does not keep drinks cold.",
    "Affordable and practical for carrying water.",
    "The bottle is okay; the handle is uncomfortable.",
    "Very happy with the purchase and the quality."
]

df = pd.DataFrame({
    "id": [f"R{i:02}" for i in range(1, 19)],
    "text": reviews
})

# ==================================================
# 3. SENTIMENT ANALYSIS USING VADER
# ==================================================

analyzer = SentimentIntensityAnalyzer()

def label_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "Positive", score

    elif score <= -0.05:
        return "Negative", score

    else:
        return "Neutral", score

df[["sentiment", "compound"]] = df["text"].apply(
    lambda text: pd.Series(label_sentiment(text))
)

# ==================================================
# 4. ASSIGN A MAIN TOPIC TO EACH COMMENT
# ==================================================

topic_mapping = {
    "R01": "Insulation",
    "R02": "Portability",
    "R03": "Lid and Design",
    "R04": "Lid and Design",
    "R05": "Lid and Design",
    "R06": "Cleaning",
    "R07": "Durability",
    "R08": "Overall Experience",
    "R09": "Insulation",
    "R10": "Cleaning",
    "R11": "Capacity",
    "R12": "Quality",
    "R13": "Durability",
    "R14": "Delivery",
    "R15": "Insulation",
    "R16": "Price and Value",
    "R17": "Comfort",
    "R18": "Quality"
}

df["topic"] = df["id"].map(topic_mapping)

# ==================================================
# 5. SIDEBAR
# ==================================================

st.sidebar.title("Dashboard Controls")

selected_sentiment = st.sidebar.multiselect(
    "Filter by sentiment",
    options=["Positive", "Neutral", "Negative"],
    default=["Positive", "Neutral", "Negative"]
)

filtered_df = df[df["sentiment"].isin(selected_sentiment)]

# ==================================================
# 6. SUMMARY METRICS
# ==================================================

st.subheader("Overall Feedback Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Comments", len(df))
col2.metric(
    "Positive",
    (df["sentiment"] == "Positive").sum()
)
col3.metric(
    "Neutral",
    (df["sentiment"] == "Neutral").sum()
)
col4.metric(
    "Negative",
    (df["sentiment"] == "Negative").sum()
)

# ==================================================
# 7. SENTIMENT COUNT CHART
# ==================================================

st.subheader("Comment Counts by Sentiment")

order = ["Positive", "Neutral", "Negative"]

counts = (
    filtered_df["sentiment"]
    .value_counts()
    .reindex(order, fill_value=0)
)

st.bar_chart(counts, horizontal=True)

# ==================================================
# 8. WORD CLOUD
# ==================================================

st.subheader("Words Used in the Comments")

# Improvement:
# Removed "bottle" from the original custom stop-word list.
# This allows readers to see the product name in the word cloud.
#
# "lid" is retained as a useful term because it highlights
# an important product feature mentioned by customers.

stop_words = set(STOPWORDS) | {
    "drinks",
    "drink"
}

cloud = WordCloud(
    width=1000,
    height=500,
    background_color="white",
    colormap="viridis",
    stopwords=stop_words,
    collocations=False
).generate(" ".join(filtered_df["text"]))

fig, ax = plt.subplots(figsize=(12, 5))
ax.imshow(cloud, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig, clear_figure=True)

st.caption(
    "Word size represents how frequently a word appears after "
    "stop words are removed. Larger words do not necessarily "
    "indicate stronger opinions or greater customer satisfaction."
)

# ==================================================
# 9. TOPIC ANALYSIS
# ==================================================

st.subheader("Sentiment by Product Topic")

topic_counts = pd.crosstab(
    filtered_df["topic"],
    filtered_df["sentiment"]
)

topic_counts = topic_counts.reindex(
    columns=["Positive", "Neutral", "Negative"],
    fill_value=0
)

st.bar_chart(topic_counts)

st.caption(
    "Each comment is assigned one main topic. The sample is small, "
    "so topic comparisons should be treated as exploratory."
)

# ==================================================
# 10. ORIGINAL COMMENTS
# ==================================================

st.subheader("Review the Original Comments")

st.dataframe(
    filtered_df[
        ["id", "text", "topic", "sentiment", "compound"]
    ],
    use_container_width=True,
    hide_index=True
)

st.caption(
    "The compound score is a sentiment model output, "
    "not a confidence rating."
)

# ==================================================
# 11. MANUAL SENTIMENT AUDIT
# ==================================================

st.subheader("Manual Review of Six Comments")

audit_ids = ["R01", "R02", "R08", "R15", "R04", "R13"]

audit_df = df[df["id"].isin(audit_ids)].copy()

audit_df["manual_assessment"] = [
    "Reasonable",
    "Reasonable",
    "Reasonable",
    "Borderline",
    "Reasonable",
    "Reasonable"
]

audit_df["review_explanation"] = [
    "The comment clearly describes good insulation performance.",
    "The comment expresses positive opinions about size and portability.",
    "The customer describes an ordinary experience without strong emotion.",
    "The comment contains both positive and negative opinions.",
    "The customer clearly expresses disappointment about leakage.",
    "The comment clearly expresses dissatisfaction with product durability."
]

st.dataframe(
    audit_df[
        [
            "id",
            "text",
            "sentiment",
            "manual_assessment",
            "review_explanation"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Manual assessments are examples for this exercise. "
    "Compare them with the actual VADER labels and revise them "
    "if your own review gives a different conclusion."
)

# ==================================================
# 12. NEGATION TEST
# ==================================================

st.subheader("Testing Negation in Sentiment Analysis")

test_comment = "The bottle is not easy to clean."

test_sentiment, test_score = label_sentiment(test_comment)

st.write("Test comment:", test_comment)
st.write("Predicted sentiment:", test_sentiment)
st.write("Compound score:", round(test_score, 4))

st.caption(
    "Negation can change the meaning of a sentence. "
    "However, automated sentiment tools may not always interpret "
    "the full context correctly."
)

# ==================================================
# 13. CONCLUSION
# ==================================================

st.subheader("Dashboard Interpretation")

st.write(
    "This dashboard summarizes customer feedback using sentiment "
    "classification, word frequency, and product topics. "
    "The visualizations help identify common experiences and "
    "possible areas for product improvement. However, the results "
    "should be interpreted carefully because automated sentiment "
    "analysis may not fully understand mixed opinions, sarcasm, "
    "or sentence context."
)

st.caption("TFB3133/TEB3133 Data Visualization | Lab 8")
