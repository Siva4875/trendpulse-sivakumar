"""
TrendPulse - Task 3: Analysis with Pandas & NumPy

This script:
1. Loads the cleaned CSV file from Task 2.
2. Explores the data using Pandas.
3. Calculates statistics using NumPy.
4. Finds the category with the most stories.
5. Finds the most commented story.
6. Adds engagement and is_popular columns.
7. Saves the analysed data for Task 4.
"""

import pandas as pd
import numpy as np
import os

# Configuration


INPUT_FILE = "data/trends_clean.csv"
OUTPUT_FILE = "data/trends_analysed.csv"


# Step 1: Check if input file exists

if not os.path.exists(INPUT_FILE):

    print(f"Error: {INPUT_FILE} not found.")
    print("Please run task2_data_processing.py first.")
    exit()


# Step 2: Load CSV using Pandas

try:

    df = pd.read_csv(INPUT_FILE)

except Exception as error:

    print(f"Error loading CSV file: {error}")
    exit()


print(f"Loaded data: {df.shape}")



# Step 3: Display first 5 rows

print("\nFirst 5 rows:")

print(df.head())



# Step 4: Print DataFrame shape

print("\nDataFrame Shape:")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# Step 5: Calculate average score and comments

average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print("\nAverage Score   :", round(average_score, 2))
print("Average Comments:", round(average_comments, 2))



# Step 6: NumPy Statistics


# Convert score column into a NumPy array.
scores = df["score"].to_numpy()


# Mean score
mean_score = np.mean(scores)


# Median score
median_score = np.median(scores)


# Standard deviation
std_score = np.std(scores)


# Highest score
max_score = np.max(scores)


# Lowest score
min_score = np.min(scores)


print("\n--- NumPy Stats ---")

print(f"Mean score   : {mean_score:,.2f}")
print(f"Median score : {median_score:,.2f}")
print(f"Std deviation: {std_score:,.2f}")
print(f"Max score    : {max_score:,}")
print(f"Min score    : {min_score:,}")


# Step 7: Find category with the most stories

category_counts = df["category"].value_counts()

most_common_category = category_counts.idxmax()
most_common_category_count = category_counts.max()


print(
    f"\nMost stories in: "
    f"{most_common_category} "
    f"({most_common_category_count} stories)"
)



# Step 8: Find the story with the most comments

most_commented_index = df["num_comments"].idxmax()

most_commented_story = df.loc[
    most_commented_index,
    "title"
]

most_commented_count = df.loc[
    most_commented_index,
    "num_comments"
]


print(
    f'\nMost commented story: '
    f'"{most_commented_story}" '
    f"— {most_commented_count:,} comments"
)


# Step 9: Add engagement column

# Formula:
#
# engagement = num_comments / (score + 1)
#
# +1 prevents division by zero if score is 0.

df["engagement"] = (
    df["num_comments"] /
    (df["score"] + 1)
)


# Step 10: Add is_popular column

# A story is considered popular when its score
# is greater than the average score.

df["is_popular"] = (
    df["score"] > average_score
)


# Step 11: Save analysed DataFrame

try:

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

except Exception as error:

    print(f"Error saving analysed CSV: {error}")
    exit()


print(
    f"\nSaved {len(df)} rows to {OUTPUT_FILE}"
)



# Step 12: Display new columns


print("\nNew columns added:")

print("  engagement")
print("  is_popular")

# Final message


print("\nTask 3 completed successfully!")




