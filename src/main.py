import os
from Document import Document
import pickle
from nltk.stem import SnowballStemmer
from bs4 import BeautifulSoup
import json


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
    # Assigning a weight of 3 for all words in the title tag
    weightDict = {word.strip() : [3, 1] for word in soup.find("title").text.split()}

    # Getting all words in h1, h2, h3 tags
    h_tags = soup.find_all('h1') + soup.find_all('h2') + soup.find_all('h3')
    h_words = [word for h in h_tags for word in h.text.split()]

    # Assigning a weight of 2 if word in h_words not already in weightDict
    for word in h_words:
        if word not in weightDict:
            weightDict[word] = [2, 1]
        else:
            weightDict[word][1] += 1

    # Getting all words in the document
    all_text = [word for word in soup.stripped_strings]
    all_words = [word for text in all_text for word in text.split()]

    # Assigning a weight of 1 for all other words in the document 
    # if not already in weightDict
    for word in all_words:
        if word not in weightDict:
            weightDict[word] = [1, 1]
        else:
            weightDict[word][1] += 1

    for key in weightDict.keys():
        #stem the key as you're storing into the tfFreqDict
        tfFreqDict[SNOWBALL.stem(key)] = (weightDict[key][1]/totalWords, weightDict[key][0])
    # instantiate Document -> Document(id, tfFreqDict)
    doc = Document(id, tfFreqDict)
    return doc 
    



def main():

    id = 0
    indexer = dict()
    documentDict = dict()

    # assign directory
    directory = 'DEV/'
    directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), directory)
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    # iterate over files in
    # that directory
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            file = os.path.join(subdir, file)
            # print(file)
            # with open(file, 'r') as opened:
            #     pass

            document = parse(file, id)
            exit()
            documentDict[id] = document
            id += 1

    for index, doc in documentDict.items():
        for stem, score in doc.doc_tf_dict.items():
            indexer[stem].append(index)



    #this is to stor the indexer and doc_dict
    indexer_file = open(os.path.join(parent_dir, "data/indexer"), 'wb')
    pickle.dump(indexer, indexer_file)
    indexer_file.close()
    
    doc_dict_file = open(os.path.join(parent_dir, "data/doc_dict"), 'wb')
    pickle.dump(indexer, doc_dict_file)
    doc_dict_file.close()
    
    



if __name__ == "__main__":
    main()

