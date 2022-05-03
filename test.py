import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
if page.ok:
    soup = BeautifulSoup(page.text)
    title = soup.find("h1")
    universal_product_code = soup.find("td")
    price_including_tax = soup.findAll("td")
    print(len(price_including_tax))
    print(title.text, universal_product_code.text, price_including_tax.text)