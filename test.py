from urllib import response
import requests
from bs4 import BeautifulSoup
import urllib.parse

url = "http://books.toscrape.com/index.html"


def parse_page(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    return soup


for i in range(51):
    url_1 = "https://books.toscrape.com/catalogue/page" + str(i) + ".html"
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    for web in soup.find_all("h3"):
        href = web.a.get("href")
        reponse = requests.get(urllib.parse.urljoin(url, href))
        soup = BeautifulSoup(reponse.text, "html.parser")
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
        print(universal_product_code)
        print(title)
        print(price_including_tax)
        print(price_excluding_tax)
        print(number_available)
        print(product_description)
        print(category)
        print(review_rating)
        print(image_url["src"])

"""
def url_categorie(categorie):
    soup = parse_page(categorie)
    for web in (
        soup.find("ul", class_="nav nav-list").find("li").find("ul").find_all("li")
    ):
        href = web.a.get("href")
        print(href)


def get_info_book(book_info):
    soup = url_categorie(book_info)
    for web in soup.find_all("h3"):
        href = web.a.get("href")
        reponse = requests.get(urllib.parse.urljoin(url, href))
        soup = BeautifulSoup(reponse.text, "html.parser")
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
        print(universal_product_code)
        print(title)
        print(price_including_tax)
        print(price_excluding_tax)
        print(number_available)
        print(product_description)
        print(category)
        print(review_rating)
        print(image_url["src"])

"""
