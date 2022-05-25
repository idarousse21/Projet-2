import urllib.parse
from csv import DictWriter
import requests
from bs4 import BeautifulSoup
import os


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def scrap_all_books(home_url):
    os.makedirs("book_to_scrap_categories", exist_ok=True)
    soup = parse_page(home_url)
    for list_category in (
        soup.find("ul", class_="nav nav-list").find("li").find("ul").find_all("li")
    ):
        category_urls = list_category.a.get("href")
        category_urls_absolu = urllib.parse.urljoin(home_url, category_urls)
        name_category = list_category.a.text.strip()
        print(name_category)
        csv_name = (name_category + ".csv").replace(" ", "_")

        dossier_categories = "./book_to_scrap_categories"
        csv_name = f"{dossier_categories}/{csv_name}"
        with open(csv_name, "w", newline="", encoding="utf8") as csv_files:
            writer = DictWriter(
                csv_files,
                fieldnames=[
                    "product_page_url",
                    "title",
                    "universal_product_code",
                    "price_including_tax",
                    "price_excluding_tax",
                    "number_available",
                    "product_description",
                    "category",
                    "review_rating",
                    "image_url",
                ],
            )
            writer.writeheader()
            for books_info in get_books_for_category(category_urls_absolu):
                writer.writerow(books_info)


def get_books_for_category(url_parse):
    for book_info in get_books_page(url_parse):
        yield book_info
    while True:
        soup = parse_page(url_parse)
        next_page = soup.select_one("li.next>a")
        if next_page:
            next_url = next_page.get("href")
            url_parse = urllib.parse.urljoin(url_parse, next_url)
            for book_info in get_books_page(url_parse):
                yield book_info
        else:
            break


def get_books_page(books_url):
    soup = parse_page(books_url)
    for url_parse in soup.find_all("h3"):
        urls_books = url_parse.a.get("href")
        book_url_absolu = urllib.parse.urljoin(books_url, urls_books)
        print(book_url_absolu)
        yield scrap_infos_book(book_url_absolu)


def scrap_infos_book(book_url):
    soup = parse_page(book_url)
    product_page = soup.find_all("td")
    universal_product_code = product_page[0].get_text()
    title = soup.find("h1").get_text()
    price_including_tax = product_page[2].get_text()
    price_excluding_tax = product_page[3].get_text()
    number_available = product_page[5].get_text()
    product_description = soup.find_all("p")[3].get_text()
    category = soup.find_all("a")[3].get_text()
    review_rating = product_page[6].get_text()
    image_url = soup.find("img").get("src")
    urls_image_absolu = urllib.parse.urljoin(book_url, image_url)
    dossier_image = "./image_book_to_scrap"
    os.makedirs(dossier_image, exist_ok=True)
    response = requests.get(urls_image_absolu, allow_redirects=True)

    pictures_name = "".join(filter(str.isalnum, title))
    pictures_name = f"{dossier_image}/{pictures_name}"
    with open(pictures_name + ".jpg", "wb") as file:
        file.write(response.content)

    return {
        "product_page_url": book_url,
        "universal_product_code": universal_product_code,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": urls_image_absolu,
    }


url = "https://books.toscrape.com/index.html"

scrap_all_books(url)
