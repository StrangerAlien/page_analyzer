from bs4 import BeautifulSoup


def parse_html(page_content):
    result = {}
    soup = BeautifulSoup(page_content, 'html.parser')

    h1 = soup.find('h1')
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})

    result['h1'] = h1.get_text().strip() if h1 else ''
    result['title'] = title.get_text().strip() if title else ''
    result['description'] = (
        description.get('content', '').strip()) if description else ''
    return result
