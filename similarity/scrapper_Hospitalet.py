import time
import json
import requests

import pandas as pd 
from bs4 import BeautifulSoup

"""
Scrapper for the Hospitalet open data webiste:
    https://opendata.l-h.cat/

Retrieves all available datasets with title and description.
There's an API, but it's only possible to retrieve data for individual datasets

It retrieves around 100 datasets

To Do:
    - Also retrieve creation time and other data
"""

def main():

    baseUrl = "https://opendata.l-h.cat/"
    numberPages = 11   # Number of pages of datasets
    pageCount = 0
    retrievedData = []

    for i in range(1,11):

        url = baseUrl + f"browse?&page={i}"
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        for dataset_soup in soup.find_all("div", class_="browse2-result"):
            title_soup = dataset_soup.find_all("h2")[0]
            title = title_soup.get_text().strip()
            link = title_soup.find_all("a")[0].get("href")

            try:
                description = dataset_soup.find_all("div", class_="browse2-result-description collapsible-content")[0].get_text().strip()
            except:
                description = "-"
                
            try:
                category = dataset_soup.find_all("a", class_="browse2-result-category browse2-result-header-section")[0].get_text()
            except:
                category = "-"
                
            retrievedData.append([title, link, description, category])

        pageCount += 1
        print("Pages scrapped: ", pageCount)

        # Stop to avoid web overload
        time.sleep(1.5)

    catalog_columns = ["title", "web_url", "description", "category"]
    catalog = pd.DataFrame(retrievedData, columns = catalog_columns)
    catalog.to_csv("../data/catalog_hospitalet.csv", index=False)



if __name__ == "__main__":
    main()
