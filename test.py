import csv
import urllib.parse
from csv import DictWriter
import requests
from bs4 import BeautifulSoup
import os

url = "http://books.toscrape.com/index.html"


def parse_page(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    return soup


def scrap_all_books(home_url):
    for web in (
        parse_page(home_url).find("ul", class_="nav nav-list").find("li").find("ul").find_all("li")
    ):
        name = web.a.text.strip()
    csv_name = ((name + ".csv").replace(" ", "_"))

    cat = "./folder_csv_file"
    os.makedirs("folder_csv_file", exist_ok=True)

    csv_name = f"{cat}/{csv_name}"
    with open(csv_name, "w", newline="", encoding="utf-8") as fichier:
        thewriter = DictWriter(
            fichier,
            fieldnames=[
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
        csv_writer
        thewriter.writeheader()
        for book_info in get_categories(home_url):
            thewriter.writerow(book_info)


def get_categories(home_url):
    soup = parse_page(home_url)
    for web in (
        soup.find("ul", class_="nav nav-list").find("li").find("ul").find_all("li")
    ):
        href = web.a.get("href")
        name = web.a.text.strip()
        print(name)
        books_url = urllib.parse.urljoin(home_url, href)
        # img = "./cat"
        # os.makedirs(img, exist_ok=True)
        # response = requests.get(books_url, allow_redirects=True)
        # pictures_name = ''.join(filter(str.isalnum, name))
        # pictures_name = f"{img}/{pictures_name}"
        # with open(pictures_name + ".csv", "w") as file:
        #     file.write(response.content)
        for book_info in get_next_pages_categories(books_url):
            yield book_info


def get_next_pages_categories(url):
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
    image_url = "https://books.toscrape.com/" + soup.find_all("img")[0].get("src")
    # img = "./folder_image_of_book"
    # os.makedirs(img, exist_ok=True)
    # response = requests.get(image_url, allow_redirects=True)
    # pictures_name = ''.join(filter(str.isalnum, title))
    # pictures_name = f"{img}/{pictures_name}"
    # with open(pictures_name + ".jpg", "wb") as file:
    #     file.write(response.content)
    return {
        "title": title,
        "universal_product_code": universal_product_code,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url,
    }


scrap_all_books(url)
