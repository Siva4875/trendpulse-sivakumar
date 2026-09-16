"""
TrendPulse - Task 4: Visualizations

This script:
1. Loads the analysed CSV from Task 3.
2. Creates an outputs folder if it does not exist.
3. Creates 3 visualizations using Matplotlib:
   - Top 10 stories by score
   - Stories per category
   - Score vs comments
4. Saves each chart as a PNG file.
5. Creates a combined TrendPulse dashboard.
6. Saves the dashboard as a PNG file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration


INPUT_FILE = "data/trends_analysed.csv"
OUTPUT_FOLDER = "outputs"

# Step 1: Check input file


if not os.path.exists(INPUT_FILE):

    print(f"Error: {INPUT_FILE} not found.")
    print("Please run task3_analysis.py first.")
    exit()


# Step 2: Create outputs folder

os.makedirs(OUTPUT_FOLDER, exist_ok=True)



# Step 3: Load analysed CSV


try:

    df = pd.read_csv(INPUT_FILE)

except Exception as error:

    print(f"Error loading CSV file: {error}")
    exit()


print(f"Loaded {len(df)} stories from {INPUT_FILE}")


# Prepare is_popular column


# CSV files can sometimes store Boolean values as strings.
# Convert the column safely to Boolean.

if df["is_popular"].dtype == "object":

    df["is_popular"] = (
        df["is_popular"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "true": True,
            "false": False
        })
    )


# CHART 1
# Top 10 Stories by Score


# Sort stories by score in descending order
# and select the top 10.

top_10 = (
    df.sort_values(
        by="score",
        ascending=False
    )
    .head(10)
    .copy()
)


# Shorten titles longer than 50 characters.

def shorten_title(title):
    """Shorten a title to a maximum of 50 characters."""

    title = str(title)

    if len(title) > 50:
        return title[:47] + "..."

    return title


top_10["short_title"] = (
    top_10["title"]
    .apply(shorten_title)
)



# Create the chart.

plt.figure(figsize=(12, 7))

plt.barh(
    top_10["short_title"],
    top_10["score"]
)

# Reverse the y-axis so the highest score appears at the top.

plt.gca().invert_yaxis()

plt.title(
    "Top 10 Hacker News Stories by Score"
)

plt.xlabel(
    "Score"
)

plt.ylabel(
    "Story Title"
)

plt.tight_layout()


# Save BEFORE show as required.

chart1_file = os.path.join(
    OUTPUT_FOLDER,
    "chart1_top_stories.png"
)

plt.savefig(
    chart1_file,
    dpi=300,
    bbox_inches="tight"
)

print(f"Saved: {chart1_file}")

plt.show()

plt.close()

# CHART 2
# Stories per Category


# Count the number of stories in each category.

category_counts = (
    df["category"]
    .value_counts()
)


# Create the chart.

plt.figure(figsize=(10, 6))

# Use a different colour for each bar.
plt.bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ][:len(category_counts)]
)

plt.title(
    "Number of Stories per Category"
)

plt.xlabel(
    "Category"
)

plt.ylabel(
    "Number of Stories"
)

plt.xticks(
    rotation=30
)

plt.tight_layout()


# Save BEFORE show.

chart2_file = os.path.join(
    OUTPUT_FOLDER,
    "chart2_categories.png"
)

plt.savefig(
    chart2_file,
    dpi=300,
    bbox_inches="tight"
)

print(f"Saved: {chart2_file}")

plt.show()

plt.close()


# CHART 3
# Score vs Comments



plt.figure(figsize=(10, 7))


# Separate popular and non-popular stories.

popular = df[
    df["is_popular"] == True
]

not_popular = df[
    df["is_popular"] == False
]


# Plot non-popular stories.

plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)


# Plot popular stories.

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)


plt.title(
    "Score vs Number of Comments"
)

plt.xlabel(
    "Score"
)

plt.ylabel(
    "Number of Comments"
)

plt.legend()

plt.tight_layout()


# Save BEFORE show.

chart3_file = os.path.join(
    OUTPUT_FOLDER,
    "chart3_scatter.png"
)

plt.savefig(
    chart3_file,
    dpi=300,
    bbox_inches="tight"
)

print(f"Saved: {chart3_file}")

plt.show()

plt.close()


# BONUS — TREND PULSE DASHBOARD

# Create a 2x2 dashboard layout.

fig, axes = plt.subplots(
    2,
    2,
    figsize=(18, 12)
)

# Dashboard Chart 1


axes[0, 0].barh(
    top_10["short_title"],
    top_10["score"]
)

axes[0, 0].invert_yaxis()

axes[0, 0].set_title(
    "Top 10 Stories by Score"
)

axes[0, 0].set_xlabel(
    "Score"
)

axes[0, 0].set_ylabel(
    "Story Title"
)

# Dashboard Chart 2


axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ][:len(category_counts)]
)

axes[0, 1].set_title(
    "Stories per Category"
)

axes[0, 1].set_xlabel(
    "Category"
)

axes[0, 1].set_ylabel(
    "Number of Stories"
)

axes[0, 1].tick_params(
    axis="x",
    rotation=30
)



# Dashboard Chart 3


axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)

axes[1, 0].set_title(
    "Score vs Comments"
)

axes[1, 0].set_xlabel(
    "Score"
)

axes[1, 0].set_ylabel(
    "Number of Comments"
)

axes[1, 0].legend()


# Dashboard 4 — Information Panel


axes[1, 1].axis("off")

axes[1, 1].text(
    0.5,
    0.75,
    "TrendPulse Summary",
    fontsize=20,
    ha="center"
)

axes[1, 1].text(
    0.5,
    0.60,
    f"Total Stories: {len(df)}",
    fontsize=14,
    ha="center"
)

axes[1, 1].text(
    0.5,
    0.50,
    f"Average Score: {df['score'].mean():,.2f}",
    fontsize=14,
    ha="center"
)

axes[1, 1].text(
    0.5,
    0.40,
    f"Average Comments: {df['num_comments'].mean():,.2f}",
    fontsize=14,
    ha="center"
)

axes[1, 1].text(
    0.5,
    0.30,
    f"Popular Stories: {popular.shape[0]}",
    fontsize=14,
    ha="center"
)


# Overall Dashboard Title


fig.suptitle(
    "TrendPulse Dashboard",
    fontsize=24
)

fig.tight_layout(
    rect=[0, 0, 1, 0.95]
)


# Save dashboard BEFORE show.

dashboard_file = os.path.join(
    OUTPUT_FOLDER,
    "dashboard.png"
)

fig.savefig(
    dashboard_file,
    dpi=300,
    bbox_inches="tight"
)

print(f"Saved: {dashboard_file}")

plt.show()

plt.close(fig)

# Final message


print("\n" + "=" * 50)
print("TrendPulse Task 4 Completed Successfully!")
print("=" * 50)

print("\nOutput files:")

print(f"1. {chart1_file}")
print(f"2. {chart2_file}")
print(f"3. {chart3_file}")
print(f"4. {dashboard_file}")

