from bs4 import BeautifulSoup


# Extract info from a single page
def extract_single_page_info(page):
    
    url = page['url']
    html = page['html']

    soup = BeautifulSoup(html, 'html.parser')

    # Title
    title = soup.title.string.strip() if soup.title and soup.title.string else ''

    # Meta description
    meta_tag = (
        soup.find('meta', attrs={'name': 'description'}) or
        soup.find('meta', attrs={'property': 'og:description'})
    )
    meta = meta_tag.get('content', '').strip() if meta_tag else ''

    # Headings
    headings = [
        h.get_text().strip()
        for h in soup.find_all(['h1', 'h2', 'h3'])
        if h.get_text().strip()
    ]

    # Paragraph text
    text = ' '.join([
        p.get_text().strip()
        for p in soup.find_all('p')
        if p.get_text().strip()
    ])

    return {
        'url': url,
        'title': title,
        'meta': meta,
        'headings': headings,
        'text': text
    }


# Extract info from multiple pages
def extract_pages_info(pages):
    extracted = []

    for page in pages:
        info = extract_single_page_info(page)
        extracted.append(info)

    return extracted
