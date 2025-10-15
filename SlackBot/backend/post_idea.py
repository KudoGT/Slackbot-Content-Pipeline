import ollama

def generate_post_idea_for_group(keywords, outline_text=""):

    # Limit outline length to avoid LLM overload
    outline_text = outline_text[:1000]


    # Prepare keyword string
    keyword_str = ", ".join(keywords)

    # prompt
    prompt = f"""
        Given the keyword group: {keyword_str}

        Use the outline below as reference:
        {outline_text}

        Generate one catchy, creative post idea or title that:
        - Aligns with the theme
        - Is simple, structured, and easy to read
        - Looks good visually (clean and clear)
        - Is under 15 words

        Only return the title as a single line — no commentary or explanations.
    """

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        post_idea = response.message.content.strip()
    except Exception as e:
        print(f"[Error generating post idea]: {e}")
        post_idea = "Could not generate post idea."

    return post_idea
























# import ollama

# def generate_post_idea_for_group(key_group, outline):
#     prompt = f"""
# Based on the following outline for the keyword group {key_group}:

# {outline}

# Suggest a concise, catchy post idea (15 words max).
# """
#     response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
#     post_idea = response.message.content.strip().split("\n")[0]  # Keep first line only
#     return post_idea
