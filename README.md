# TrendPulse — Task 1: Data Collection

## Project Overview

**TrendPulse** is a 4-part data pipeline project designed to identify and analyze what is currently trending on Hacker News.

The project is completed step by step:

| Task | Description |
|---|---|
| Task 1 | Fetch JSON data from Hacker News API |
| Task 2 | Clean and prepare the data |
| Task 3 | Analyze data using NumPy and Pandas |
| Task 4 | Visualize the trends |

This repository contains **Task 1 — Fetch Data from API**.

---

## Task 1 Objective

The objective of Task 1 is to:

- Fetch the top 500 story IDs from Hacker News.
- Fetch the details of each story using the Hacker News API.
- Categorize stories into 5 categories based on keywords in their titles.
- Collect up to 25 stories per category.
- Extract the required fields.
- Save the collected data as a JSON file inside the `data/` folder.

### Categories

The following five categories are used:

1. Technology
2. World News
3. Sports
4. Science
5. Entertainment

---

## Hacker News API

Hacker News provides a free and open API. No API key, login, or registration is required.

### Top Stories API

```text
https://hacker-news.firebaseio.com/v0/topstories.json
```

This endpoint returns a list of Hacker News story IDs.

The first **500 story IDs** are used for this task.

### Story Details API

For each story ID, the following endpoint is used:

```text
https://hacker-news.firebaseio.com/v0/item/{id}.json
```

Example:

```text
https://hacker-news.firebaseio.com/v0/item/8863.json
```

### Request Header

The script sends the following User-Agent header:

```python
headers = {
    "User-Agent": "TrendPulse/1.0"
}
```

---

## Category Keywords

Each story is assigned to a category by checking whether its title contains one of the specified keywords.

Matching is **case-insensitive**.

| Category | Keywords |
|---|---|
| technology | AI, software, tech, code, computer, data, cloud, API, GPU, LLM |
| worldnews | war, government, country, president, election, climate, attack, global |
| sports | NFL, NBA, FIFA, sport, game, team, player, league, championship |
| science | research, study, space, physics, biology, discovery, NASA, genome |
| entertainment | movie, film, music, Netflix, game, book, show, award, streaming |

> Note: The keyword `game` appears in both **sports** and **entertainment**. The script checks categories in the defined order, so a title matching `game` will be assigned to the first matching category.

---

## Data Fields

Each collected story contains the following 7 fields:

| Field | Hacker News Source | Description |
|---|---|---|
| `post_id` | `id` | Unique Hacker News story ID |
| `title` | `title` | Story title |
| `category` | Custom | Category assigned using title keywords |
| `score` | `score` | Number of upvotes |
| `num_comments` | `descendants` | Number of comments |
| `author` | `by` | Hacker News username |
| `collected_at` | Custom | Date and time when the story was collected |

Example record:

```json
{
    "post_id": 12345678,
    "title": "Example technology story",
    "category": "technology",
    "score": 250,
    "num_comments": 75,
    "author": "example_user",
    "collected_at": "2026-09-15T12:30:00"
}
```

---

## Project Structure

```text
trendpulse-yourname/
│
├── task1_data_collection.py
├── data/
│   └── trends_YYYYMMDD.json
│
└── README.md
```

### Files

**`task1_data_collection.py`**

Contains the Python program used to fetch, categorize, and save Hacker News stories.

**`data/trends_YYYYMMDD.json`**

Contains the collected Hacker News stories in JSON format.

**`README.md`**

Contains project documentation and instructions.

---

## Technologies Used

- Python 3
- Requests
- JSON
- datetime
- os
- time
- Hacker News API

---

## Python Libraries

The main external library used is:

```text
requests
```

The following modules are from Python's standard library:

```python
time
json
os
datetime
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<username>/trendpulse-<name>.git
```

Move into the project directory:

```bash
cd trendpulse-<name>
```

### 2. Install Requests

```bash
pip install requests
```

If you are using a specific Python installation:

```bash
python -m pip install requests
```

---

## How to Run

Run the Python script from the project root:

```bash
python task1_data_collection.py
```

On some Windows systems, you may need:

```bash
py task1_data_collection.py
```

---

## How the Script Works

### Step 1 — Fetch Top Story IDs

The script calls:

```text
https://hacker-news.firebaseio.com/v0/topstories.json
```

and retrieves the first 500 story IDs.

### Step 2 — Fetch Story Details

For each story ID, the script calls:

```text
https://hacker-news.firebaseio.com/v0/item/{id}.json
```

The required story information is extracted from the API response.

### Step 3 — Categorize Stories

The title is converted to lowercase and compared against the category keywords.

For example:

```text
"New AI software released for developers"
```

contains `AI` and `software`, so it can be classified as:

```text
technology
```

### Step 4 — Limit Stories Per Category

The script collects a maximum of:

```text
25 stories per category
```

Therefore, the theoretical maximum is:

```text
5 categories × 25 stories = 125 stories
```

### Step 5 — Handle Failed Requests

If an API request fails, the script prints an error message and continues processing the next story.

This prevents a single failed request from stopping the entire program.

### Step 6 — Wait Between Categories

The assignment requires a 2-second delay between category loops.

The script uses:

```python
time.sleep(2)
```

between categories.

The delay is **not** applied after every individual API request.

### Step 7 — Create the Data Folder

If the `data/` folder does not already exist, the script creates it automatically:

```python
os.makedirs("data", exist_ok=True)
```

### Step 8 — Save JSON

The output filename is generated using the current date:

```text
data/trends_YYYYMMDD.json
```

For example:

```text
data/trends_20260915.json
```

---

## Expected Output

After successful execution, the console will display information similar to:

```text
Starting TrendPulse data collection...
Fetched 500 top story IDs.

Collecting category: technology
  Collected 1/25: ...
  Collected 2/25: ...
  ...

Waiting 2 seconds before next category...

Collecting category: worldnews
  Collected 1/25: ...
  ...

==================================================
TrendPulse Data Collection Completed
==================================================
Collected 120 stories.
Saved to data/trends_20260915.json

Category Summary:
technology: 25
worldnews: 20
sports: 25
science: 25
entertainment: 25
```

The exact number of stories may vary because the Hacker News top stories change over time and not every story title will match the required keywords.

---

## Error Handling

The script uses exception handling for API failures.

Example:

```python
try:
    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )
    response.raise_for_status()

except requests.RequestException as error:
    print(f"Failed to fetch story: {error}")
```

If an individual story cannot be retrieved, the script skips that story and continues.

---

## Assignment Requirements Checklist

| Requirement | Status |
|---|---|
| Fetch Hacker News top stories | ✅ |
| Fetch first 500 story IDs | ✅ |
| Fetch story details | ✅ |
| Use `requests` library | ✅ |
| Use `TrendPulse/1.0` User-Agent | ✅ |
| Handle failed requests | ✅ |
| Categorize stories using keywords | ✅ |
| Case-insensitive keyword matching | ✅ |
| 5 required categories | ✅ |
| Maximum 25 stories per category | ✅ |
| Extract all 7 required fields | ✅ |
| Add collection date/time | ✅ |
| Create `data/` folder | ✅ |
| Save JSON output | ✅ |
| Wait 2 seconds between categories | ✅ |
| Print total number collected | ✅ |
| Code comments included | ✅ |

---

## Output File

The generated file will be stored at:

```text
data/trends_YYYYMMDD.json
```

Example:

```text
data/trends_20260915.json
```

The JSON file contains an array of story objects.

---

## GitHub Submission

After testing the script, commit and push the project to a **public GitHub repository**.

### Initialize Git

```bash
git init
```

### Add files

```bash
git add task1_data_collection.py README.md data/
```

### Commit

```bash
git commit -m "Complete TrendPulse Task 1 data collection"
```

### Add GitHub repository

```bash
git remote add origin https://github.com/<username>/trendpulse-<name>.git
```

### Push

```bash
git branch -M main
git push -u origin main
```

### Submission Link

Replace `<username>` and `<name>` with your GitHub details.

```text
https://github.com/<username>/trendpulse-<name>/blob/main/task1_data_collection.py
```

---

## Future Tasks

TrendPulse will continue with the following tasks:

### Task 2 — Clean CSV

The JSON data collected in Task 1 will be cleaned and converted into a CSV dataset.

### Task 3 — NumPy & Pandas

The cleaned data will be analyzed using NumPy and Pandas to identify trends and statistics.

### Task 4 — Visualization

The final data will be visualized using charts and graphs to understand the trending categories.

---

## Author

**Siva Kumar D**

TrendPulse — Task 1: Data Collection
