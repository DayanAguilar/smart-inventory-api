import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()

URL = os.environ.get("URL")
API_URL = os.environ.get("API_URL")

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
