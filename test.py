import requests
from bs4 import BeautifulSoup
import urllib.parse

url = "http://books.toscrape.com/index.html"


def parse_page(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    return soup
    


def scrap_categories(home_url):
    soup = parse_page(home_url)
    for web in (
        soup.find("ul", class_="nav nav-list").find("li").find("ul").find_all("li")
    ):
        href = web.a.get("href")
        books_url = urllib.parse.urljoin(home_url, href)

        next_pages_categories(books_url)


def next_pages_categories(url):
    scrap_books_infos(url)
    while True:
        soup = parse_page(url)
        next_page = soup.select_one("li.next>a")
        if next_page:
            next_url = next_page.get("href")
            url = urllib.parse.urljoin(url, next_url)
            scrap_books_infos(url)
        else:
            break


def scrap_books_infos(books_url):
    soup = parse_page(books_url)
    for h3 in soup.find_all("h3"):
        href = h3.a.get("href")
        book_url = urllib.parse.urljoin(books_url, href)
        scrap_one_book(book_url)


def scrap_one_book(one_book_url):
    soup = parse_page(one_book_url)
    rows = soup.find_all("td")
    universal_product_code = rows[0].get_text()
    title = soup.find("h1").get_text()
    price_including_tax = rows[2].get_text()
    price_excluding_tax = rows[3].get_text()
    number_available = rows[5].get_text()
    product_description = soup.find_all("p")[3].get_text()
    category = soup.find_all("a")[3].get_text()
    review_rating = rows[6].get_text()
    image_url = soup.find_all("img")[0]
    print(title)
    print(category)

    # print(universal_product_code)
    # print(price_including_tax)
    # print(price_excluding_tax)
    # print(number_available)
    # print(product_description)
    # print(review_rating)
    # print(image_url["src"])


scrap_categories(url)
