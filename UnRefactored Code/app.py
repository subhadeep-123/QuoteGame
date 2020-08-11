import requests
from bs4 import BeautifulSoup
import time
from random import choice

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
        # time.sleep(1)
    return all_quotes


def start_game(quotes):
    quote = choice(quotes)
    print("Here's a quote: ")
    print(quote['Text'])
    # print(quote['Author'])
    remaining_guess = 4
    guess = ' '
    while guess.lower() != quote["Author"].lower() and remaining_guess > 0:
        guess = input(
            f"Who said this quote? Guesses Reamining: {remaining_guess} ")
        if guess.lower() == quote["Author"].lower():
            print("YOU GOT IT RIGHT!!")
            break
        remaining_guess -= 1
        if remaining_guess == 3:
            res = requests.get(f"{BASE_URL}{quote['Bio-Link']}")
            soup = BeautifulSoup(res.text, 'html.parser')
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(
                f"Here's a hint: The Author was born on {birth_date} {birth_place}")
        elif remaining_guess == 2:
            print(
                f"Here's a hint: The Author First Name starts with {quote['Author'][0]}")
        elif remaining_guess == 1:
            last_str = quote['Author'].split(" ")[1][0]
            print(
                f"Here's a hint: The Author Last Name starts with {last_str}")
        else:
            print(
                f"Ooops!! YOU HAVE RUN OUT OF CHANCES\nThe answer was {quote['Author']}")

    again = ''
    while again.lower() not in ('yes', 'y', 'n', 'no'):
        again = input("\nWould you like to play again (y/n)? ")
    if again.lower() in ('yes', 'y'):
        return start_game(quotes)
    else:
        print("OK, GOODBYE")


if __name__ == "__main__":
    quotes = scrape_quotes()
    start_game(quotes)
