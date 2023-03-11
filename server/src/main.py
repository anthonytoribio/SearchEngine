import os
from Document import Document
import pickle
from nltk.stem import SnowballStemmer
from bs4 import BeautifulSoup
import json
from collections import defaultdict
from helper import *
import platform
import statistics
import copy

 
#GLOBAL Vars:
SNOWBALL = SnowballStemmer(language="english")
CAP = 10000000 #LIMIT of pickle 
FILE = "FinalIndexer.txt" #String name of the text file that holds the combined indexer
NUM_DOCS = 0

def parse(file: str, id: int) -> Document:
    #weightDict = loop through all the {key:word : val: int}
    weightDict = {}
    #create tfFreqDict
    #tfFreqDict = loop through keys of weightDict and create dict {key:stemWord : val: (freq:float, weight:int)}
    tfFreqDict = {}
    f = open(file, 'r')
    f = json.load(f)
    soup = BeautifulSoup(f["content"], features="html.parser")
    title = "Doc: " + str(id)
    
    #get all the urls we see in this document
    hrefs = [a.get('href') for a in soup.find_all('a')]
    
    freqDict = defaultdict(int)
    #totalWords = len(soup.get_text().split())
    # Assigning a weight of 4 for all words in the title tag
    if soup.title != None:
        weightDict = {SNOWBALL.stem(word.strip()) : 4 for word in tokenize(soup.find("title").text.split())}
        titleWords = [SNOWBALL.stem(word.strip()) for word in tokenize(soup.find("title").text.split())]
        for titleWord in titleWords:
            freqDict[titleWord] += 1
        title = soup.find("title").text

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

    if (len(all_words) > 0 and len(title.split()) != 0 and title.split()[0] != "Doc:"):
        title = " ".join(all_words[0:4])

    all_words = tokenize(all_words)
    # Assigning a weight of 1 for all other words in the document 
    # if not already in weightDict
    weightDict = Dict_Update(weightDict, all_words, 1)
    for word in all_words:
        freqDict[word] += 1

    for key in weightDict.keys():
        #stem the key as you're storing into the tfFreqDict
        #the first value is the weighted frequency of the word and the second value is the frequency of the word
        tfFreqDict[key] = (weightDict[key], freqDict[key])
    # instantiate Document -> Document(id, tfFreqDict, url)
    doc = Document(id, tfFreqDict, f["url"], hrefs, title, " ".join(all_words[:10]), len(all_words))
    return doc 


def buildUrlDict():
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(parent_dir, "data/doc_dict"), 'rb') 
    documentDict = pickle.load(file)
    
    urlDict = defaultdict(str)
    for docid, doc in documentDict.items():
        urlDict[doc.docUrl] = docid
    
    return urlDict


def pageRank(urlDict):
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(parent_dir, "data/doc_dict"), 'rb') 
    documentDict = pickle.load(file)

    build_children_and_parents(urlDict, documentDict)

    #loop through 10 iterations
    for _ in range(10):
        #Go through each doc
        prevDoc = copy.deepcopy(documentDict)
        for docid in urlDict.values():
            documentDict[docid].update_pagerank(0.05, len(documentDict), prevDoc)
    
    doc_dict_file = open(os.path.join(parent_dir, "data/doc_dict"), 'wb')
    pickle.dump(documentDict, doc_dict_file)
    doc_dict_file.close() 


def resetRank():
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(parent_dir, "data/doc_dict"), 'rb') 
    documentDict = pickle.load(file) 

    for doc in documentDict.values():
        doc.pagerank = 1
        doc.parents = []
        doc.children = []
    
    doc_dict_file = open(os.path.join(parent_dir, "data/doc_dict"), 'wb')
    pickle.dump(documentDict, doc_dict_file)
    doc_dict_file.close() 
    


def buildIndex():
    id = 0 #id for docs (updates for each new doc)
    indexer = defaultdict(list) #maps stem words to doc ids
    documentDict = dict() #maps docids to Document Objects

    # assign directory
    directory = 'DEV/'
    directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), directory)
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    # iterate over files in that directory
    for subdir, dirs, files in os.walk(directory):
        #Parse the file into a Document Object and add to documentDict
        for file in files:
            file = os.path.join(subdir, file)
            document = parse(file, id)
            documentDict[id] = document
            id += 1

    NUM_DOCS = id #save the number of documents in global var
    
    #This is used for the partial indexer file name
    partialIndexCounter = 1

    #Loop through each document and add the stem words to the indexer dictionary
    for id, doc in documentDict.items():
        for stem, score in doc.doc_tf_dict.items():
            if stem == '':
                continue
            indexer[stem].append(id)
        #Check the size of the partial indexer if over CAP then write the partial index into 
        # disk and then clear the indexer for the documents that follow
        if (len(pickle.dumps(indexer, -1)) >= CAP):
                #sort the indexer by alpha (lexico) and then write to file
                sortedKeys = sorted(indexer)
                partialIndexerFile = open(os.path.join(parent_dir, "data/PI" + str(partialIndexCounter)+".txt"), 'w')
                partialIndexCounter += 1
                for key in sortedKeys:
                    partialIndexerFile.write(key + " ")
                    for docId in indexer[key]:
                        partialIndexerFile.write(str(docId) + " ")
                    partialIndexerFile.write("\n")
                partialIndexerFile.close()
                indexer = defaultdict(list)

    if len(indexer) != 0:
        sortedKeys = sorted(indexer)
        partialIndexerFile = open(os.path.join(parent_dir, "data/PI" + str(partialIndexCounter)+".txt"), 'w')
        partialIndexCounter += 1
        for key in sortedKeys:
            partialIndexerFile.write(key + " ")
            for docId in indexer[key]:
                partialIndexerFile.write(str(docId) + " ")
            partialIndexerFile.write("\n")
        partialIndexerFile.close()

    # Merge all the partial indexes
    partialIndexes = partialIndexCounter - 1 #3

    if partialIndexes > 1:
        currFile = open(os.path.join(parent_dir, "data/PI" + str(partialIndexes) +".txt"), 'r')
        prevFile = open(os.path.join(parent_dir, "data/PI" + str(partialIndexes-1) +".txt"), 'r')

        file, idx = merge(prevFile, currFile, partialIndexes)

        for i in range(1, partialIndexes - 1):
            currFile = open(os.path.join(parent_dir, "data/PI" + str(i) +".txt"), 'r')
            #Check if this is the final partial indexer to merge
            if (i == partialIndexes - 2):
                file, idx = merge(currFile, file, idx, final=True)
            else:
               file, idx = merge(currFile, file, idx, final=False) 
        
        # file variable holds our combined index
        # idx holds the number of the PI file that has the combined index
    else:
        #rename the PI1 to the FILE global var
        os.rename(os.path.join(parent_dir, "data/PI1.txt"), FILE)
        file = open(os.path.join(parent_dir, FILE), 'r')
          
    #Create the indexer of the indexer
    outdexer = {} #maps stem words to the byte in the new combined indexer file
    start = 0
    line = file.readline()
    while line != '':
        lineList = line.split()
        outdexer[lineList[0]] = [start, len(lineList)-1, calculate_log_idf_factor(len(lineList)-1, NUM_DOCS)]
        start += len(line)
        if platform.system() == 'Windows':
            start += 1
        line = file.readline()

    file.close()

    #store outdexer in a pickle file
    outdexer_file = open(os.path.join(parent_dir, "data/outdexer"), 'wb')
    pickle.dump(outdexer, outdexer_file)
    outdexer_file.close()

    #store the documentDict in a pickle file
    doc_dict_file = open(os.path.join(parent_dir, "data/doc_dict"), 'wb')
    pickle.dump(documentDict, doc_dict_file)
    doc_dict_file.close() 

    #Store the outdexer for debugging purposes
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    outdexer_json_file = open(os.path.join(parent_dir, "data/outdexer.json"), 'w')
    json.dump(outdexer, outdexer_json_file, indent=4, separators=(":", ",")) 


def main():
    parent_dir = os.path.dirname(os.path.realpath(__file__))

    #check if the indexer is already created if not then create
    if (not os.path.isfile(os.path.join(parent_dir, "data/" + FILE))):
        print("CREATING INDEXER......")
        buildIndex()
        print("INDEX HAS BEEN CREATED \n")
        print("BUILDING PAGE RANK...")
        urlDict = buildUrlDict()
        pageRank(urlDict)
        print("PAGE RANK CREATED \n")
        
    #This code is to collect and store data for all document's page rank values
    #Load the documentDict
    file = open(os.path.join(parent_dir, "data/doc_dict"), 'rb') 
    documentDict = pickle.load(file)
    
    pageRank_list = []
    for docid, doc in documentDict.items():
        if doc.pagerank != 0:
            pageRank_list.append(doc.pagerank)
    pagerank_file = open(os.path.join(parent_dir, "data/pagerank_file"), 'wb')
    pickle.dump(pageRank_list, pagerank_file)
    pagerank_file.close() 
    rankMode = statistics.mean(pageRank_list)
    

    #load the outdexer and documentdict
    file = open(os.path.join(parent_dir, "data/outdexer"), 'rb')
    outdexer = pickle.load(file)

    #Load the documentDict
    file = open(os.path.join(parent_dir, "data/doc_dict"), 'rb') 
    documentDict = pickle.load(file)
    

    while 1:
        query = input("Type in a query:\n")
        if query.lower().strip() == "exit":
            return
        query = query.split()
        s = ranked_retrieval(query, FILE, outdexer, documentDict, 30, rankMode)

        print("Here are your search results: ")
        for doc_id in s:
            print(documentDict[int(doc_id)].docUrl)


if __name__ == "__main__":
    main()