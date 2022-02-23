import pickle

import numpy as np 
import pandas as pd



def retrieveItem(itemId):
    catalog = pd.read_csv("../data/catalog_unified.csv")

    title = catalog.iloc[[itemId]]["title"].item()
    description = catalog.iloc[[itemId]]["description"].item()
    origen = catalog.iloc[[itemId]]["origen"].item()
    web_url = catalog.iloc[[itemId]]["web_url"].item()
    category = catalog.iloc[[itemId]]["category"].item()


    return {
        "title": title,
        "description": description,
        "origen": origen,
        "web_url": web_url,
        "category": category
    }

def catalog():
    catalog = pd.read_csv("../data/catalog_unified.csv")
    catalog =  catalog.fillna('')

    title = list(catalog["title"])
    description = list(catalog["description"])
    origen = list(catalog["origen"])
    web_url = list(catalog["web_url"])
    category = list(catalog["category"])


    catalog_list = []
    for i in range(len(catalog)):
        obj = {
            "title": title[i],
            "description": description[i],
            "origen": origen[i],
            "web_url": web_url[i],
            "category": category[i]
        }
        catalog_list.append(obj)

    return catalog_list


def similar(itemId):
    itemId = int(itemId)
    with open("pairwise_similarity_title.pkl", "rb") as input_file:
        pairwise_similarity_title = pickle.load(input_file)
        pairwise_similarity_title = np.array(pairwise_similarity_title)
    with open("pairwise_similarity_desc.pkl", "rb") as input_file:
        pairwise_similarity_desc = pickle.load(input_file)
        pairwise_similarity_desc = np.array(pairwise_similarity_desc)

    pairwise_similarity = np.add(pairwise_similarity_title, pairwise_similarity_desc)
    pairwise_similarity = pairwise_similarity / 2

    similarity_vector = pairwise_similarity[itemId] #.toarray()
    similarity_vector = list(similarity_vector)

    similarity_vector_sorted = sorted(similarity_vector, reverse=True)
    sorted_ind = [similarity_vector.index(i) for i in similarity_vector_sorted]

    return sorted_ind