import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re

load_dotenv()
URL = os.environ.get("URL")
API_URL = os.environ.get("API_URL")

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None

def get_data_from_api(api_url, number):
    try:
        response = requests.get(f"{api_url}/{number}/0")
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None

def get_product_7_status(data):
    if not isinstance(data, dict):
        return None
    
    products = data.get("oResultado")
    if not isinstance(products, list):
        return None
    
    for product in products:
        if isinstance(product, dict) and product.get("id_producto_bsa") == 7:
            balance = product.get("saldo_bsa", 0)
            
            if balance <= 0:
                return "zero balance", "red"
            elif balance < 2000:
                return "low balance", "yellow"
            else:
                return "complete balance", "green"
    return None

def get_setmark_numbers_and_names_from_tables(html):
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    for link in soup.find_all('a', onclick=True):
        match = re.search(r"setMark\((\d+),\s*\d+,\s*'([^']+)'\)", link['onclick'])
        if match:
            number, name = match.groups()
            api_data = get_data_from_api(API_URL, number)
            status = get_product_7_status(api_data)
            
            if status:
                results.append({
                    "name": name,
                    "number": number,
                    "status": status[0],
                    "color": status[1]
                })
    
    return results

if __name__ == "__main__":
    print(get_setmark_numbers_and_names_from_tables(fetch_html(URL)))