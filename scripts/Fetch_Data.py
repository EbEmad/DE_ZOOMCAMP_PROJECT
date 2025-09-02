import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
def fetch_data(**kwargs):
    try:
        url = "https://www.worldometers.info/world-population/population-by-country/"
        requested_result = requests.get(url).text
        doc = BeautifulSoup(requested_result, 'html.parser')
        print("Connection to the website established.")
        return doc
    except Exception as e:
        raise Exception("CONNECTION ERROR: Can't connect to the website to fetch the data!") from e