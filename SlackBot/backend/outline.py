import ollama
from utils.fetcher import fetch_url_content
from utils.extractor import extract_pages_info 


# generating outline using LLM
def generate_outline(key_groups, pages_info, max_tokens=300):

    page_summaries = ''

    if not pages_info:
        page_summaries = "No top-ranking web pages found. Generate outline using keywords only."

    for p in pages_info:
        page_summaries += f"Title: {p['title']}\nMeta: {p['meta']}\nHeadings: {p['headings']}\nText: {p['text'][:600]}\n\n"

    prompt = f"""
        Generate a clean blog post outline using the following keywords: {', '.join(key_groups)} and using the following page data: {page_summaries}.

        - Use plain text formatting that looks good in Slack.
        - Format section headers with all caps (e.g., "SECTION 1: INTRODUCTION").
        - Use hyphens (-) for bullet points, no asterisks or Markdown symbols.
        - Keep output readable and minimal in formatting.
        - Include a final section titled "CONCLUSION" (mandatory).
        keep it under 200 words.
    """

    try:
        response = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
        )

        outline = response.message.content.strip()
    except Exception as e:
        print(f'[Error generating outline]: {e}')
        outline = 'Outline generation failed !'
        
    return outline 
    


def generate_outline_for_group(key_groups):
    
    pages = fetch_url_content(key_groups)
    pages_info = extract_pages_info(pages) 
    outline = generate_outline(key_groups, pages_info)
    return outline
