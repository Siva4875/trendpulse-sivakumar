""" TrendPulse - Task 1: Fetch Data from Hacker News API This script: 
1. Fetches the top 500 Hacker News story IDs. 
2. Fetches details for each story. 
3. Categorizes stories based on title keywords. 
4. Collects up to 25 stories per category. 
5. Saves the collected stories as a JSON file. 

Categories: 
- technology 
- worldnews 
- sports 
- science 
- entertainment """

import requests
import time
import json
import os
from datetime import datetime

# configuration
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json" 
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

HEADERS = { "User-Agent": "TrendPulse/1.0" }

MAX_STORIES = 500 
MAX_PER_CATEGORY = 25


# Category Keywords

CATEGORY_KEYWORDS = { 
    "technology": [ 
        "AI", 
        "software", 
        "tech", 
        "code", 
        "computer", 
        "data", 
        "cloud", 
        "API", 
        "GPU", 
        "LLM" 
    ], 

    "worldnews": [ 
        "war", 
        "government", 
        "country", 
        "president", 
        "election", 
        "climate", 
        "attack", 
        "global"
    ], 

    "sports": [ 
        "NFL", 
        "NBA", 
        "FIFA", 
        "sport", 
        "game", 
        "team", 
        "player", 
        "league", 
        "championship" 
    ], 

    "science": [ 
        "research", 
        "study", 
        "space", 
        "physics", 
        "biology", 
        "discovery", 
        "NASA", 
        "genome" 
    ], 

    "entertainment": [ 
        "movie", 
        "film", 
        "music", 
        "Netflix", 
        "game", 
        "book", 
        "show", 
        "award", 
        "streaming" 
    ] 
}


# Function: Fetch Top Story IDs

def fetch_top_story_ids(): 
    """Fetch the top 500 Hacker News story IDs.""" 

    try: 
        response = requests.get( 
            TOP_STORIES_URL, 
            headers=HEADERS, 
            timeout=10 
            ) 
        response.raise_for_status() 
        story_ids = response.json() 

    # Fetch only the first 500 IDs 
        return story_ids[:MAX_STORIES] 
    except requests.RequestException as error: 
        print(f"Failed to fetch top story IDs: {error}") 
    return []

# Function: Fetch Story Details

def fetch_story(story_id): 
    """Fetch details for a single Hacker News story."""

    try:
        response = requests.get( 
            ITEM_URL.format(story_id), 
            headers=HEADERS, 
            timeout=10 
            ) 

        response.raise_for_status() 

        story = response.json() 

        return story

    except requests.RequestException as error: 
        print(f"Failed to fetch story {story_id}: {error}") 
        return None

# Function: Categorize Story

def categorize_story(title): 
    """ 
    Assign a category based on keywords found in the title. 
    Matching is case-insensitive. 
    """

    title_lower = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in title_lower: 
                return category

    return None

# Function: Create Story Record

def create_story_record(story, category): 
    """Extract the required fields from a Hacker News story.""" 

    return { 
        "post_id": story.get("id"), 
        "title": story.get("title"), 
        "category": category, 
        "score": story.get("score", 0), 
        "num_comments": story.get("descendants", 0), 
        "author": story.get("by"), 
        "collected_at": datetime.now().isoformat() 
        }

# Main Program


def main(): 

    print("Starting TrendPulse data collection...") 

    # Step 1: Fetch top story IDs 
    story_ids = fetch_top_story_ids() 

    if not story_ids: 
        print("No story IDs were retrieved. Exiting.") 
        return 

    print(f"Fetched {len(story_ids)} top story IDs.") 

    # Store collected stories 
    collected_stories = [] 

    # Track number of stories collected per category 
    category_counts = { 
        category: 0 
        for category in CATEGORY_KEYWORDS 
    }


    # ----------------------------------------------------- 
    # Process each category 
    # ----------------------------------------------------- 
    # 
    # We fetch stories from the top 500 list and assign them 
    # to categories based on title keywords. 
    # 
    # A story is added to the first matching category. 
    # 
    # Maximum 25 stories are collected per category. 
    # ----------------------------------------------------- 

    for category in CATEGORY_KEYWORDS: 

        print(f"\nCollecting category: {category}") 

        for story_id in story_ids: 

            # Stop when this category has 25 stories 
            if category_counts[category] >= MAX_PER_CATEGORY: 
                break 

            # Fetch story details 
            story = fetch_story(story_id) 

            # If request failed, move to the next story 
            if story is None: 
                continue 

            # Ignore deleted/dead stories 
            if story.get("type") != "story": 
                continue 

            if story.get("deleted") or story.get("dead"): 
                continue 

            # Get title 
            title = story.get("title", "") 

            if not title: 
                continue 

            # Determine category based on title keywords 
            detected_category = categorize_story(title) 

            # Add story only if it belongs to current category 
            if detected_category == category: 

                record = create_story_record( 
                story, 
                category 

            ) 

                collected_stories.append(record) 

                category_counts[category] += 1 

                print( 
                    f" Collected {category_counts[category]}/" 
                    f"{MAX_PER_CATEGORY}: {title}" 
                ) 

        # Wait 2 seconds between category loops 
        if category != list(CATEGORY_KEYWORDS.keys())[-1]: 
            print("Waiting 2 seconds before next category...") 
            time.sleep(2)

    # --------------------------------------------------------- 
    # Create data directory 
    # --------------------------------------------------------- 

    os.makedirs("data", exist_ok=True) 

    # --------------------------------------------------------- 
    # Create output filename 
    # --------------------------------------------------------- 

    date_string = datetime.now().strftime("%Y%m%d") 
    output_file = f"data/trends_{date_string}.json"



    # --------------------------------------------------------- 
    # Save data to JSON 
    # --------------------------------------------------------- 

    try: 
        with open( 
            output_file, 
            "w", 
            encoding="utf-8" 
        ) as file: 

            json.dump( 
                collected_stories, 
                file, 
                indent=4, 
                ensure_ascii=False 
            ) 
    except OSError as error: 

        print(f"Failed to save JSON file: {error}")


    # --------------------------------------------------------- 
    # # Print summary 
    # # --------------------------------------------------------- 
    
    print("\n" + "=" * 50) 
    print("TrendPulse Data Collection Completed") 
    print("=" * 50) 

    print(f"Collected {len(collected_stories)} stories.") 
    print(f"Saved to {output_file}") 

    print("\nCategory Summary:") 

    for category, count in category_counts.items(): 
        print(f"{category}: {count}")

# --------------------------------------------------------- 
# Run the program 
#  --------------------------------------------------------- 

if __name__ == "__main__": 
    main()


    