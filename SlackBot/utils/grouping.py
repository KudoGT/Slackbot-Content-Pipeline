import ollama

def group_keywords(keywords):
    if not keywords:
        return {}


    # Create a prompt for semantically grouping similar keywords
    prompt = f"""
        You are an expert in semantic keyword analysis.

        Given the following list of keywords:
        {keywords}

        Group them based on semantic similarity (i.e., meaning and context). 
        Each group must contain at least 2 closely related keywords (mandatory).

        Format your response like this:
        Group 1: [keyword1, keyword2, ...]  
        Group 2: [keyword3, keyword4, ...]  
        ...

        If any keywords do not belong to any group, place them under:
        Noise: [keywordX, keywordY, ...]

        The Noise group must also contain at least 2 keywords.

        Only return the grouped keywords in the format above. No explanations.
    """



    # Ask the LLM to create groups
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text_output = response.message.content.strip()

    # Parse LLM output into dict
    groups = {}
    for line in text_output.split("\n"):
        line = line.strip()
        if not line:
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip().lower().replace(" ", "_")
        # Convert string list to actual list
        try:
            val_list = eval(val.strip())
            if isinstance(val_list, list):
                groups[key] = val_list
        except:
            continue

    return groups
