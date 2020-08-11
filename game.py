import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

BASE_URL = "http://quotes.toscrape.com"


def read_quotes(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(quotes):
    quote = choice(quotes)
    print("Here's a quote: ")
    print(quote['Text'])
    # print(quote['Author'])
    remaining_guess = 4
    guess = ' '
    while guess.lower() != quote["Author"].lower() and remaining_guess > 0:
        guess = input(
            f"Who said this quote? Guesses Reamining {remaining_guess}: ")
        if guess.lower() == quote["Author"].lower():
            print("YOU GOT IT RIGHT!!")
            break
        remaining_guess -= 1
        hint(quote, remaining_guess)

    again = ''
    while again.lower() not in ('yes', 'y', 'n', 'no'):
        again = input("\nWould you like to play again (y/n)? ")
    if again.lower() in ('yes', 'y'):
        return start_game(quotes)
    else:
        print("OK, GOODBYE")


def hint(quote, remaining_guess):
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
        print(f"Here's a hint: The Author Last Name starts with {last_str}")
    else:
        print(
            f"Ooops!! YOU HAVE RUN OUT OF CHANCES\nThe answer was {quote['Author']}")


if __name__ == "__main__":
    quotes = read_quotes('quotes.csv')
    start_game(quotes)
