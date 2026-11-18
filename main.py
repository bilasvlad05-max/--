
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

RATINGS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def get_soup(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_genres():
    soup = get_soup(BASE_URL)
    genres = {}

    category_list = soup.select(
        ".side_categories ul ul li a"
    )

    for category in category_list:
        name = category.text.strip()
        link = urljoin(BASE_URL, category["href"])
        genres[name] = link

    return genres


def parse_books(url):
    books = []

    while url:
        soup = get_soup(url)

        for item in soup.select("article.product_pod"):
            title = item.h3.a["title"]

            price_text = item.select_one(
                ".price_color"
            ).text.strip()

            price = float(
                price_text.replace("Â£", "").replace("£", "")
            )

            rating_class = item.select_one(
                ".star-rating"
            )["class"][1]

            rating = RATINGS.get(rating_class, 0)

            availability = item.select_one(
                ".availability"
            ).text.strip()

            books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability
            })

        next_page = soup.select_one("li.next a")

        if next_page:
            url = urljoin(url, next_page["href"])
        else:
            url = None

    return books


def display_books(books):
    if not books:
        print("\nКниг не знайдено!")
        return

    print(f"\nЗнайдено книг: {len(books)}")
    print("-" * 65)

    for number, book in enumerate(books, 1):
        print(f"\n{number}. {book['title']}")
        print(f"   Ціна: £{book['price']:.2f}")
        print(f"   Рейтинг: {'★' * book['rating']}{'☆' * (5 - book['rating'])}")
        print(f"   Наявність: {book['availability']}")

    print("\n" + "-" * 65)


def sort_books(books):
    print("\n=== СОРТУВАННЯ ===")
    print("1. Ціна: від дешевих до дорогих")
    print("2. Ціна: від дорогих до дешевих")
    print("3. Рейтинг: від найвищого до найнижчого")
    print("4. Рейтинг: від найнижчого до найвищого")

    choice = input("\nВаш вибір: ")

    if choice == "1":
        books.sort(key=lambda x: x["price"])
    elif choice == "2":
        books.sort(key=lambda x: x["price"], reverse=True)
    elif choice == "3":
        books.sort(key=lambda x: x["rating"], reverse=True)
    elif choice == "4":
        books.sort(key=lambda x: x["rating"])
    else:
        print("Неправильний вибір!")
        return

    display_books(books)


def main():
    print("=" * 45)
    print("         BOOK SCRAPER")
    print("=" * 45)

    print("\nЗавантаження жанрів...")

    try:
        genres = get_genres()

        if not genres:
            print("Не вдалося знайти жанри!")
            return

        genre_names = list(genres.keys())

        print("\n=== ДОСТУПНІ ЖАНРИ ===")

        for number, genre in enumerate(genre_names, 1):
            print(f"{number}. {genre}")

        print("\n0. Усі книги")

        choice = input("\nОберіть жанр: ")

        if choice == "0":
            url = BASE_URL
            selected_genre = "Усі книги"
        elif choice.isdigit() and 1 <= int(choice) <= len(genre_names):
            selected_genre = genre_names[int(choice) - 1]
            url = genres[selected_genre]
        else:
            print("Неправильний вибір!")
            return

        print(f"\nЗавантаження книг: {selected_genre}...")

        books = parse_books(url)

        if not books:
            print("Книг не знайдено!")
            return

        print(f"Завантажено книг: {len(books)}")

        while True:
            print("\n=== МЕНЮ ===")
            print("1. Показати всі книги")
            print("2. Сортувати книги")
            print("3. Вийти")

            action = input("\nВаш вибір: ")

            if action == "1":
                display_books(books)
            elif action == "2":
                sort_books(books)
            elif action == "3":
                print("\nДякую за використання Book Scraper!")
                break
            else:
                print("Неправильний вибір!")

    except requests.RequestException as error:
        print(f"\nПомилка підключення: {error}")

    except Exception as error:
        print(f"\nСталася помилка: {error}")


if __name__ == "__main__":
    main()


