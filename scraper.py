import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
BASE_SITE = "https://books.toscrape.com/"
books = []

def extract_rating(star_string):
    rating_map = {
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    }
    return rating_map.get(star_string, 0)

page = 1
while True:
    res = requests.get(BASE_URL.format(page))
    if res.status_code == 404:
        print(f"✅ Reached end of pages at page {page}.")
        break

    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.select('article.product_pod')

    for article in articles:
        title = article.h3.a['title']
        price = article.select_one('.price_color').text[2:]
        availability = article.select_one('.instock.availability').text.strip()
        rating = extract_rating(article.p['class'][1])

        # Get detail page URL
        relative_url = article.h3.a['href']
        detail_url = urljoin(BASE_SITE + 'catalogue/', relative_url)

        # Visit detail page for description & genre
        detail_res = requests.get(detail_url)
        detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
        desc_tag = detail_soup.select_one('#product_description + p')
        description = desc_tag.text.strip() if desc_tag else ''
        breadcrumb_links=detail_soup.select("ul.breadcrumb li a")
        genre=breadcrumb_links[-1].text.strip() if len(breadcrumb_links)>2 else "Unknown"

        books.append({
            'title': title,
            'price': float(price),
            'availability': availability,
            'rating': rating,
            'description': description,
            'genre': genre
        })

        print(f"Scraped: {title}")

        # Optional: be polite
        time.sleep(0.5)

    print(f"✅ Finished page {page}")
    page += 1

df = pd.DataFrame(books)
df.to_csv('src/data/books_with_descriptions.csv', index=False)
print("✅ Saved books_with_descriptions.csv")
