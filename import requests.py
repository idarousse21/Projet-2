import requests
from bs4 import BeautifulSoup
import urllib.parse

url = "http://books.toscrape.com/index.html"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, "html.parser")

for web in soup.find_all("h3"):
    href = web.a.get("href")
    reponse = requests.get(urllib.parse.urljoin(url, href))
    soup = BeautifulSoup(reponse.text, "html.parser")
    universal_product_code = soup.find_all("td")[0].get_text()
    title = soup.find("h1").get_text()
    price_including_tax = soup.find_all("td")[2].get_text()
    price_excluding_tax = soup.find_all("td")[3].get_text()
    number_available = soup.find_all("td")[5].get_text()
    product_description = soup.find_all("p")[3].get_text()
    category = soup.find_all("a")[3].get_text()
    review_rating = soup.find_all("td")[6].get_text()
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
