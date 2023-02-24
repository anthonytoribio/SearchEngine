import os
from Document import Document
import pickle
from nltk.stem import SnowballStemmer
from bs4 import BeautifulSoup
import json
from collections import defaultdict
from helper import *


#GLOBAL Vars:
SNOWBALL = SnowballStemmer(language="english")


def parse(file, id: int) -> Document:
    #weightDict = loop through all the {key:word : val: int}
    weightDict = {}
    #create tfFreqDict
    #tfFreqDict = loop through keys of weightDict and create dict {key:stemWord : val: (freq:float, weight:int)}
    tfFreqDict = {}
    f = open(file, 'r')
    f = json.load(f)
    soup = BeautifulSoup(f["content"], features="html.parser")
    totalWords = len(soup.get_text().split())
    # Assigning a weight of 4 for all words in the title tag
    if soup.title != None:
        weightDict = {SNOWBALL.stem(word.strip()) : 4 for word in tokenize(soup.find("title").text.split())}

    # Getting all words in h1, h2, h3 tags
    h_tags = soup.find_all('h1') + soup.find_all('h2') + soup.find_all('h3')
    h_words = [SNOWBALL.stem(word) for h in h_tags for word in h.text.split()]

    h_words = tokenize(h_words)
    # Assigning a weight of 3 if word in h_words not already in weightDict
    weightDict = Dict_Update(weightDict, h_words, 3)

    # Getting all words in bold
    bold_tags = soup.find_all('b') + soup.find_all('strong')
    bold_words = [SNOWBALL.stem(word) for b in bold_tags for word in b.text.split()]

    bold_words = tokenize(bold_words)
    #Assigning a weight of 2 if word in bold_words not already in weightDict
    weightDict = Dict_Update(weightDict, bold_words, 2)

    # Getting all words in the document
    all_text = [word for word in soup.stripped_strings]
    all_words = [SNOWBALL.stem(word) for text in all_text for word in text.split()]

    all_words = tokenize(all_words)
    # Assigning a weight of 1 for all other words in the document 
    # if not already in weightDict
    weightDict = Dict_Update(weightDict, all_words, 1)
    freqDict = defaultdict(int)
    for word in all_words:
        freqDict[word] += 1

    for key in weightDict.keys():
        #stem the key as you're storing into the tfFreqDict
        tfFreqDict[key] = (weightDict[key]/totalWords, freqDict[key])
    # instantiate Document -> Document(id, tfFreqDict, url)
    doc = Document(id, tfFreqDict, f["url"])
    return doc 
    



def main():

    id = 0
    indexer = defaultdict(list)
    documentDict = dict()

    # assign directory
    directory = 'DEV/'
    directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), directory)
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    # iterate over files in
    # that directory
    for subdir, dirs, files in os.walk(directory):
        break
        for file in files:
            file = os.path.join(subdir, file)
            # print(file)
            # with open(file, 'r') as opened:
            #     pass
            document = parse(file, id)
            documentDict[id] = document
            id += 1

    for index, doc in documentDict.items():
        #print(index, " |", doc) #DEBUG
        for stem, score in doc.doc_tf_dict.items():
            #print(stem, "\n") DEBUG
            indexer[stem].append(index)
    print("NUMBER OF DOCUMENTS IS: ", id + 1)



    #this is to stor the indexer and doc_dict
    print("THE # OF UNIQUE STEMMED WORDS ARE: ", len(indexer))
    indexer_file = open(os.path.join(parent_dir, "data/indexer"), 'wb')
    pickle.dump(indexer, indexer_file)
    indexer_file.close()
    
    doc_dict_file = open(os.path.join(parent_dir, "data/doc_dict"), 'wb')
    pickle.dump(indexer, doc_dict_file)
    doc_dict_file.close()
    
    
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    indexer_json_file = open(os.path.join(parent_dir, "data/indexer.json"), 'w')
    json.dump(indexer, indexer_json_file, indent=4, separators=(":", ","))
    
    while 1:
        query = input("Type in a query:\n")
        if query.lower().strip() == "exit":
            return
        query = query.split()
        s = boolean_retrieval(query)
        print("Here are your search results: ")
        for doc_id in s:
            print(documentDict[doc_id].docUrl)

if __name__ == "__main__":
    main()

