from googlesearch import search
import requests
import time

def search_top_urls(key_groups, num=3):
    
    query = ' '.join(key_groups)
    urls = []

    # googlesearch-python uses 'num_results=' not 'stop='
    for url in search(query, num_results=num):
        urls.append(url)

    return urls

def fetch_page_content(url):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/115.0.0.0 Safari/537.36'
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

    return None

def fetch_url_content(key_groups, num=3):
    urls = search_top_urls(key_groups, num=num)
    pages = []

    for url in urls:
        html = fetch_page_content(url)
        if html:
            pages.append({'url': url, 'html': html})
        time.sleep(1)

    return pages
