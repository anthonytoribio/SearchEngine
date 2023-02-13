import os
import Document
from nltk.stem import SnowballStemmer

#GLOBAL Vars:
SNOWBALL = SnowballStemmer(language="english")

def parse(file, id: int) -> Document:
    #weightDict = loop through all the {key:word : val: int}
    totalWords = 0
    weightDict = {}
    #create tfFreqDict
    #tfFreqDict = loop through keys of weightDict and create dict {key:stemWord : val: (freq:float, weight:int)}
    tfFreqDict = {}
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
    # iterate over files in
    # that directory
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            file = os.path.join(subdir, file)
            # print(file)
            # with open(file, 'r') as opened:
            #     pass

            document = parse(file, id)
            documentDict[id] = document
            id += 1

    for index, doc in documentDict.items():
        for stem, score in doc.doc_tf_dict.items():
            indexer[stem].append(index)


if __name__ == "__main__":
    main()

