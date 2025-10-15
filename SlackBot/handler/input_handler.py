import pandas as pd
import io
import requests
from utils.cleaning import clean_keywords
from backend.outline import generate_outline_for_group
from backend.post_idea import generate_post_idea_for_group
from utils.grouping import group_keywords

# --- Process manual text input ---
def process_text_input(text):
    if not text.strip():
        return [], "❌ No keywords detected. Please provide some keywords."

    # Split by comma or newline
    keywords = [kw.strip() for kw in text.replace(",", "\n").split("\n") if kw.strip()]
    if not keywords:
        return [], "❌ No valid keywords found in your input."

    cleaned_keywords = clean_keywords(keywords)
    if not cleaned_keywords:
        return [], "❌ No valid keywords after cleaning. Try different keywords."

    return cleaned_keywords, None


# --- Process CSV file uploaded via Slack ---
def process_csv_file(file_url, slack_token):
    headers = {"Authorization": f"Bearer {slack_token}"}
    try:
        r = requests.get(file_url, headers=headers)
        if r.status_code != 200:
            return [], "❌ Failed to download the CSV file."

        df = pd.read_csv(io.StringIO(r.text))
        if df.empty:
            return [], "❌ CSV file is empty."

        # Automatically take first column as keywords
        col_name = df.columns[0]
        keywords = df[col_name].dropna().astype(str).tolist()

        cleaned_keywords = clean_keywords(keywords)
        if not cleaned_keywords:
            return [], "❌ No valid keywords found in CSV after cleaning."

        return cleaned_keywords, None

    except Exception as e:
        return [], f"❌ Failed to process CSV file: {e}"


# --- Generate results (keywords → groups → outline → post ideas) ---


def generate_results(keywords):
    if not keywords:
        return "❌ No keywords to process."

    groups = group_keywords(keywords)
    if not groups:
        return "❌ Failed to group keywords. Try with more diverse keywords."

    results = []
    for i, (group_id, kw_list) in enumerate(groups.items(), 1):
        outline = generate_outline_for_group(kw_list)
        post_idea = generate_post_idea_for_group(kw_list, outline)

        results.append({
            "group": i,
            "keywords": kw_list,
            "outline": outline,
            "post_idea": post_idea
        })

    return results
