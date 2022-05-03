import requests
from bs4 import BeautifulSoup
import urllib.parse
url = "http://books.toscrape.com/index.html"


def parse_page(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    return soup


def get_book_data(book_url):
    soup = parse_page(book_url)
    rows = soup.find_all("td")
    universal_product_code = rows[0].get_text()
    print(universal_product_code)
    title = soup.find("h1").get_text()
    price_including_tax = rows[2].get_text()
    price_excluding_tax = rows[3].get_text()
    number_available = rows[5].get_text()
    product_description = soup.find_all("p")[3].get_text()
    category = rows[3].get_text()
    review_rating = rows[6].get_text()
    image_url = soup.find_all("img")[0]
    print(universal_product_code)
    print(title)
    print(price_including_tax)
    print(price_excluding_tax)
    print(number_available)
    print(product_description)
    print(category)
    print(review_rating)
    print(image_url["src"])
    
url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

def get_category_data(category_url):
    soup = parse_page(category_url)
    for web in soup.find_all("h3"):
        relative_url = web.a.get("href")
        absolute_url = urllib.parse.urljoin(category_url, relative_url)
        get_book_data(absolute_url)
