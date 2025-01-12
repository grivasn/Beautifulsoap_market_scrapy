from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def scrape_products(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    category = url.split("/")[-1].replace("-", " ").title()
    all_products = soup.find_all("div", class_="productName detailUrl")
    all_prices = soup.find_all("div", class_="discountPrice")
    current_date = datetime.now().strftime("%Y-%m-%d")
    product_list = []

    for product, price in zip(all_products, all_prices):
        product_name = product.text.strip()
        raw_price = price.find("span", class_="discountPriceSpan").text.strip()
        product_price = raw_price.replace("₺", "").replace(",", ".")
        product_list.append({
            "Tarih": current_date,
            "Kategori": category,
            "Ürün": product_name,
            "Fiyat": product_price
        })

    return product_list

urls = [
    "https://www.onurmarket.com/meyve-sebze",
    "https://www.onurmarket.com/et-balik-pilic",
    "https://www.onurmarket.com/kahvaltilik",
    "https://www.onurmarket.com/sut-ve-yogurt-urunleri",
    "https://www.onurmarket.com/temel-gida",
    "https://www.onurmarket.com/cay-kahve",
    "https://www.onurmarket.com/icecekler",
    "https://www.onurmarket.com/firin-pastane",
    "https://www.onurmarket.com/atistirmalik",
    "https://www.onurmarket.com/dondurma",
    "https://www.onurmarket.com/meze-hazir-yemek-dondurulmus",
    "https://www.onurmarket.com/deterjan-temizlik",
    "https://www.onurmarket.com/kisisel-bakim-kozmetik",
    "https://www.onurmarket.com/anne-bebek",
    "https://www.onurmarket.com/ev-yasam",
    "https://www.onurmarket.com/kitap-kirtasiye-oyuncak",
    "https://www.onurmarket.com/pet-shop",
    "https://www.onurmarket.com/elektronik",
    "https://www.onurmarket.com/vegan-vejetaryen-urunler"
]

all_data = []

for url in urls:
    print(f"\nURL: {url}")
    all_data.extend(scrape_products(url))

df = pd.DataFrame(all_data)

output_file = "onurmarket_urunler.xlsx"
df.to_excel(output_file, index=False, sheet_name="Ürünler")

print(f"Veriler başarıyla '{output_file}' dosyasına kaydedildi.")
