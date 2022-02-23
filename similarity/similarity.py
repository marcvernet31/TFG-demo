import pickle
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

from stopwords_ca import batch
from sklearn.feature_extraction.text import TfidfVectorizer

"""
Similarity between arrays of textes based on TF-IDF
Creates a matrix of similarities for titles and for descriptions


!!! Packet instalation problem, Run:
    %> conda run -n sklearn-env python3 similarity.py
"""

# Punctiation chars to be removed
punctuations = "!”#$%&'()*+,-./:;?@[\]^_`{|}~’"
# Added words to stopwords
batch += ["l", "d", "\\n"]



# Clean a text for NLP
def preprocess(text):

    # remove possible nan
    if type(text) == float: text = "-"
        
    # remove \n
    text = text.strip()
    
    # remove puntuations
    for p in punctuations:
        try:
            text = text.replace(p, ' ')
        except:
            print(text)
        
    # lower text
    text = text.lower()

    # remove stopwords
    text_split = text.split(' ')
    text = ' '.join([x for x in text_split if x not in batch])
    
    return text



# Preprocess a list of texts
def preprocess_text_list(text_list):
    return [(lambda x: preprocess(x))(x) for x in text_list]



# Genereate pairwaise similarity matrix from an array of texts
def gen_pairwise_similarity(text):
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(text)  

    pairwise_similarity = tfidf * tfidf.T 
    return(pairwise_similarity)



def main():

    barcelona = pd.read_csv("../data/catalegBCN_2022-02-19_11-16.csv")
    try:
        del barcelona["Unnamed: 0"]
    except:
        pass

    hospitalet = pd.read_csv("../data/catalog_Hospitalet.csv")
    try:
        del hospitalet["Unnamed: 0"]
    except:
        pass



    ## Unify catalogs into a single one

    append_hospitalet = hospitalet[["title", "description", "web_url", "category"]]
    append_hospitalet["origen"] = ["hospitalet"] * len(append_hospitalet)

    #catalog = catalog[["title_ca", "notes_ca", "organization_parent_name_ca", "organization_name_ca", "date_published", "fuente", "url_busqueda_ca"]]
    append_barcelona = barcelona[["title_ca", "notes_ca", "url_busqueda_ca", "organization_parent_name_ca"]]
    append_barcelona = append_barcelona.rename(columns={"title_ca":"title", "description":"description", "link_web":"web_url", "parent_class":"category"})
    append_barcelona["origen"] = ["barcelona"] * len(append_barcelona)

    catalog_unified = pd.concat([append_hospitalet, append_barcelona])
    catalog_unified.to_csv("../data/catalog_unified.csv")



    ## Calculate similarity matrices

    titles = list(catalog_unified["title"])
    descriptions = list(catalog_unified["description"])

    titles_clean = preprocess_text_list(titles)
    descriptions_clean = preprocess_text_list(descriptions)

    pairwise_similarity_titles = gen_pairwise_similarity(titles_clean)
    pairwise_similarity_descriptions = gen_pairwise_similarity(descriptions_clean)



    ## Save similarity matrices

    pairwise_similarity_titles_list = pairwise_similarity_titles.toarray().tolist()
    pairwise_similarity_descriptions_list = pairwise_similarity_descriptions.toarray().tolist()

    with open('../data/pairwise_similarity_titles.pkl', 'wb') as f:
        pickle.dump(pairwise_similarity_titles_list, f)
    
    with open('../data/pairwise_similarity_descriptions.pkl', 'wb') as f:
        pickle.dump(pairwise_similarity_descriptions_list, f)



if __name__ == "__main__":
    main()