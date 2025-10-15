import re

def clean_keywords(keyword_list):
    cleaned = []

    for kw in keyword_list:
        if not isinstance(kw, str):
            continue  # skip if not string

        kw = kw.strip()

        # skip header if detected
        if kw.lower() == "keyword":
            continue

        # remove unwanted special characters but keep hyphens/underscores
        kw = re.sub(r'[^a-zA-Z0-9\s\-_]', '', kw)

        # normalize multiple spaces
        kw = re.sub(r'\s+', ' ', kw)

        # avoid empty and duplicates
        if kw and kw not in cleaned:
            cleaned.append(kw)

    return cleaned
