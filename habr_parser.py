import requests
from bs4 import BeautifulSoup
import time

KEYWORDS = ['дизайн', 'фото', 'python', 'web', 'разработка']

def get_full_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text_element = soup.find('div', class_='article-formatted-body')
    return text_element.get_text().lower() if text_element else ''

def parse_habr():
    response = requests.get('https://habr.com/ru/all/')
    soup = BeautifulSoup(response.text, 'html.parser')

    for article in soup.find_all('article'):
        title = article.find('h2').text.strip()
        link = article.find('h2').find('a').get('href')

        if not link or ('/articles/' not in link and '/post/' not in link):
            continue

        full_link = f"https://habr.com{link}" if link.startswith('/') else link
        date = article.find('time').get('title')

        # Проверяем превью
        preview = article.find(['div', 'p'], class_=lambda x: x and 'article-formatted-body' in str(x))
        preview_text = preview.get_text().lower() if preview else ''

        # Проверяем ключевые слова в превью и заголовке
        if any(keyword in preview_text or keyword in title.lower() for keyword in KEYWORDS):
            print(f"{date} – {title} – {full_link}")
        else:
            # Проверяем полный текст статьи
            full_text = get_full_text(full_link)
            time.sleep(0.5)

            if any(keyword in full_text for keyword in KEYWORDS):
                print(f"{date} – {title} – {full_link}")

if __name__ == "__main__":
    parse_habr()