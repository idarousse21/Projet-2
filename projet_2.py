import urllib.parse
from csv import DictWriter
import requests
from bs4 import BeautifulSoup
import os


def parse_page(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.content, "html.parser")
    return soup


def scrap_all_books(home_url):
    os.makedirs("book_to_scrap_categories", exist_ok=True)
    soup = parse_page(home_url)
    for web in (
        soup.find("ul", class_="nav nav-list").find("li").find("ul").find_all("li")
    ):
        href = web.a.get("href")
        category_urls = urllib.parse.urljoin(home_url, href)
        name = web.a.text.strip()
        print(name)
        csv_name = (name + ".csv").replace(" ", "_")

        categories = "./book_to_scrap_categories"
        csv_name = f"{categories}/{csv_name}"
        with open(csv_name, "w", newline="", encoding="utf8") as csv_files:
            # csv_writer = csv.writer(csv_files)
            thewriter = DictWriter(
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
            thewriter.writeheader()
            for book_info in get_books_for_category(category_urls):
                thewriter.writerow(book_info)


def get_books_for_category(url):
    for book_info in get_books_page(url):
        yield book_info
    while True:
        soup = parse_page(url)
        next_page = soup.select_one("li.next>a")
        if next_page:
            next_url = next_page.get("href")
            url = urllib.parse.urljoin(url, next_url)
            for book_info in get_books_page(url):
                yield book_info
        else:
            break


def get_books_page(books_url):
    soup = parse_page(books_url)
    for h3 in soup.find_all("h3"):
        href = h3.a.get("href")
        book_url = urllib.parse.urljoin(books_url, href)
        print(book_url)
        yield scrap_infos_book(book_url)


def scrap_infos_book(book_url):
    soup = parse_page(book_url)
    rows = soup.find_all("td")
    universal_product_code = rows[0].get_text()
    title = soup.find("h1").get_text()
    price_including_tax = rows[2].get_text()
    price_excluding_tax = rows[3].get_text()
    number_available = rows[5].get_text()
    product_description = soup.find_all("p")[3].get_text()
    category = soup.find_all("a")[3].get_text()
    review_rating = rows[6].get_text()
    image_url = soup.find("img").get("src")
    image_url = urllib.parse.urljoin(book_url, image_url)
    dossier_image = "./image_book_to_scrap"
    os.makedirs(dossier_image, exist_ok=True)
    response = requests.get(image_url, allow_redirects=True)

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
        "image_url": image_url,
    }


url = "https://books.toscrape.com/index.html"

scrap_all_books(url)
