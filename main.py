import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

books = []

for book in soup.select("article.product_pod"):
    title = book.h3.a["title"]

    price_text = book.select_one("p.price_color").text
    price = float(price_text.replace("Â£", "").replace("£", ""))

    rating_text = book.select_one("p.star-rating")["class"]
    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    rating = ratings[rating_text[1]]

    availability = book.select_one("p.instock").get_text(strip=True)

    books.append({
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability
    })

# 5 найдешевших книжок
cheapest_books = sorted(books, key=lambda book: book["price"])[:5]

print("5 найдешевших книжок:")
for book in cheapest_books:
    print(f'{book["title"]} — £{book["price"]}, рейтинг: {book["rating"]}')

# Кількість книжок з рейтингом 5
five_star_books = [book for book in books if book["rating"] == 5]

print("\nКількість книжок з рейтингом 5:", len(five_star_books))
