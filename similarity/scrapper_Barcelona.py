import time
import json
import requests

import pandas as pd 
from bs4 import BeautifulSoup

"""
Scrapper for the Barcelona OpenData webiste:
    https://opendata-ajuntament.barcelona.cat/data/ca/dataset/

Retrieves all available datasets with title and description, it uses an original dataset
with a catalog of all available datasets provided by OpenData
There's an API, but it's only possible to retrieve data for individual datasets

It retreives around 520 datasets, it's very slow

To Do:
    - Also retrieve creation time and other data
"""

# Number of datasets to retrieve
# To generete test datasets fast
retrieveLim = 20

def main():
    # Catalog provided by the OpenData plataform with information of all the
    # available datasets. Allows for a faster scrapping of missing data
    catalog = pd.read_csv("../data/catalegBCN_2022-02-19_11-16.csv")

    baseUrl_web = "https://opendata-ajuntament.barcelona.cat/data/ca/dataset/"
    
    # List of the name of all available datasets
    # Name that vcan be used inb the url
    names = list(catalog["name"])

    description_list = []
    parent_class_list = []
    child_class_list = []

    datasetIndex = 1
    for name in names:
        start = time.time()

        if(retrieveLim < datasetIndex): break

        url = baseUrl_web + name
        try:
            html = requests.get(url).text
        except:
            print(f'Connection for {datasetIndex} failed')
            continue

        
        soup = BeautifulSoup(html, 'html.parser')
    
        # Extract dataset description
        description = soup.find_all("div", class_="notes embedded-content")[0].get_text()
        description_list.append(description)

        # Extract area with category definition    
        icons = soup.find_all("ul", class_="dataset-groups")[0]
    
        # Main Category
        parent_class = icons.find_all("li", class_="parent")[0].get_text().strip()
        parent_class_list.append(parent_class)
        
        # Sub Category
        child_class = icons.find_all("li", class_="child")[0].get_text().strip()
        child_class_list.append(child_class)


        print("Dataset:", datasetIndex)
        datasetIndex += 1
        print(f"{round(time.time() - start, 2)}s")
        print("--------")

    catalog["description"] = description_list
    catalog["parent_class"] = parent_class_list
    catalog["child_class"] = child_class_list

    link_list = [baseUrl_web+x for x in list(catalog["name"])]
    catalog["link_web"] = link_list

    catalog.to_csv("../data/cataleg_barcelona.csv")



if __name__ == "__main__":
    main()
