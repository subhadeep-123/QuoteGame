import requests
from bs4 import BeautifulSoup
import time
from random import choice
from csv import DictWriter

BASE_URL = "http://quotes.toscrape.com"


def scrape_quotes():
    all_quotes = []
    url = "/page/1"
    while url:
        res = requests.get(f"{BASE_URL}{url}")
        print(f"Now Scraping {BASE_URL}{url}...")
        soup = BeautifulSoup(res.text, 'html.parser')
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            all_quotes.append({
                "Text": quote.find(class_="text").get_text(),
                "Author": quote.find(class_="author").get_text(),
                "Bio-Link": quote.find("a")["href"]
            })
        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        time.sleep(2)
    return all_quotes


# Write quotes to CSV FILE
def write_quotes(quotes):
    with open('quotes.csv', 'w', encoding='utf-8') as file:
        headers = ["Text", "Author", "Bio-Link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)


quotes = scrape_quotes()
write_quotes(quotes)
