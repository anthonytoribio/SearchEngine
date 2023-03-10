import os
from nltk.stem import SnowballStemmer
import math
from collections import defaultdict
import time


PARENTDIRECTORY = os.path.dirname(os.path.realpath(__file__))
FILE = "FinalIndexer.txt" #String name of the text file that holds the combined indexer
SNOWBALL = SnowballStemmer(language="english")

ALPHANUMERIC = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1",
    "2", "3", "4", "5", "6", "7", "8", "9", "0"}

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def tokenize(wordList: '[str]') -> '[str]':
    """
    The function returns a list of strings (tokens) from the original file
    that are seperated by non alphanumeric characters. If an error occured
    then the function will return -1.

    Time Complexity: O(n)
    """
    if len(wordList) < 1:
        return wordList
    try:
        tokens = []
        data = " ".join(wordList)
        data = data.lower()
        start = 0
        for index in range(len(data)):
            #print(f"data char is: {data[index]}")
            #print(f"start data is: {data[start]}")
            #print()
            if not (data[start] in ALPHANUMERIC) and data[index] in ALPHANUMERIC:
                #DEBUG print("Setting start")
                start = index
            elif data[start] in ALPHANUMERIC and not (data[index] in ALPHANUMERIC):
                #DEBUG print("Adding token\n")
                tokens.append(data[start:index])
                start = index
    except UnicodeDecodeError:
        print("ERROR: Program can only tokenize a text file (.txt).")
        return -1
    index+= 1

    if (len(tokens) < 1 or tokens[-1] != data[start:index]) and data[start] in ALPHANUMERIC:
        tokens.append(data[start:index])
    #DEBUG print(tokens)
    return tokens   


def Dict_Update(dictionary, words, weight):
    for word in words:
        if word not in dictionary:
            dictionary[word] = weight
        else:
            dictionary[word] += weight
    return dictionary


def ourSort(thefile, list1, list2) -> None:
    """
    The function sorts 2 lists of doc ids and writes the sorted doc ids
    to the given open file (theFile). 

    Time Complexity: O(n)
    """
    #2 Pointers to keep track position in list (for merge)
    p1 = 0
    p2 = 0

    while p1 < len(list1) and p2 < len(list2):
        val1 = int(list1[p1])
        val2 = int(list2[p2])
        if val1 < val2:
            thefile.write(list1[p1] + ' ')
            p1 += 1
        elif val2 < val1:
            thefile.write(list2[p2] + ' ')
            p2 += 1
        else:
            thefile.write(list1[p1] + ' ')
            p1 += 1
            p2 += 1
    
    if p1 < len(list1):
        while p1 < len(list1):
            thefile.write(list1[p1] + ' ')
            p1 += 1
    
    if p2 < len(list2):
        while p2 < len(list2):
            thefile.write(list2[p2] + ' ')
            p2 += 1
    
    thefile.write('\n')


def merge(file1, file2, index:int, final = False):
    """
    The function merges 2 given files (partial indexes). While merging
    the function will write these merged stems and doc ids into 
    a new PI{N}.txt file. The new text file will be denoted by the index arg.
    The fuction will return an open file object to the new partial index and 
    the next file number.

    Time Complexity: O(n)
    """
    if (final):
        returnedFile = open(os.path.join(PARENTDIRECTORY, "data/" + FILE), 'w')
    else:
        returnedFile = open(os.path.join(PARENTDIRECTORY, "data/PI" + str(index + 1) +".txt"), 'w')
    line1 = file1.readline()
    line2 = file2.readline()
    while (line1 != '' and line2 != ''):
        ln1 = line1.rstrip().split()
        ln2 = line2.rstrip().split()

        if (ln1[0] < ln2[0]):
            returnedFile.write(ln1[0] + ' ')
            for doc in ln1[1:]:
                returnedFile.write(doc + ' ')
            returnedFile.write('\n')
            line1 = file1.readline()
        elif (ln1[0] > ln2[0]):
            returnedFile.write(ln2[0] + ' ')
            for doc in ln2[1:]:
                returnedFile.write(doc + ' ')
            returnedFile.write('\n')
            line2 = file2.readline()
        else:
            # Case where the two stems are the same
            returnedFile.write(ln1[0] + ' ')
            ourSort(returnedFile, ln1[1:], ln2[1:])
            line1 = file1.readline()
            line2 = file2.readline()
    
    if line1 != '':
        while line1 != '':
            ln1 = line1.rstrip().split()
            returnedFile.write(ln1[0] + ' ')
            for doc in ln1[1:]:
                returnedFile.write(doc + ' ')
            returnedFile.write('\n')  
            line1 = file1.readline()  

    if line2 != '':
        while line2 != '':
            ln2 = line2.rstrip().split()
            returnedFile.write(ln2[0] + ' ')
            for doc in ln2[1:]:
                returnedFile.write(doc + ' ')
            returnedFile.write('\n')  
            line2 = file2.readline()    

    file1.close()
    file2.close()
    returnedFile.close()
    if (final):
        returnedFile = open(os.path.join(PARENTDIRECTORY, "data/" + FILE), 'r')
    else:
        returnedFile = open(os.path.join(PARENTDIRECTORY, "data/PI" + str(index + 1) +".txt"), 'r')

    return [returnedFile, index + 1]     


#This function takes a filename and an offset representing the statring byte to read from, it returns a set of words 
# that are read from the given line  
def read_set_from_line( filename, offset)  -> set:    
    with open(os.path.join(PARENTDIRECTORY, "data/" + filename), "r") as file:
        file.seek(offset)
        line = file.readline()
        return set(line.split()[1:])


#this function is bone of boolean retrieval, it takes a query of words, the name of the file to ream from, and an indexer object
#and it returns a set of doc_ids
def boolean_retrieval(query, filename, indexer)->set:
    #print(tokenize(query))
    #query = [SNOWBALL.stem(word) for word in tokenize(query)]
    #print(query)
    query = sorted(query, key = lambda x: indexer[x][1])
    s = read_set_from_line(filename, indexer[query[0]][0])

    for string in query[1:]:
        offset = indexer[string][0]
        next_set = read_set_from_line(filename, offset)
        temp = set()
        for word in s:
            if word in next_set:
                temp.add(word)
        s = temp
        
    return s

def buildDocLenDict(documentDict):
    length_dict = defaultdict(int)
    for doc_id, document in documentDict.items():
        tf_dict = document.doc_tf_dict
        document_length = sum([ x[1] for x in tf_dict.values()])
        length_dict[int(doc_id)] = document_length
    print()
    return length_dict
        



def calculate_log_idf_factor(term_occur, doc_len):
    quotient = doc_len / term_occur
    return float(math.log(quotient, 10))

def calculate_log_tf(weighted_freq):
    return float(1+ math.log(weighted_freq, 10 ))



def ranked_retrieval(query, filename, outdexer, documentDict, top_k)->set:
    start = time.time()
    processed_query = [SNOWBALL.stem(word) for word in tokenize(query)]
    
    sorted_query = sorted(processed_query, key=lambda x: outdexer[x][2], reverse=True)
    query_len = len(processed_query)
    
    #This part is to perform heuristics to shrink the number of urls we need to compare
    retrival_sets = set()
    for i in range(query_len):
        retrival_sets = boolean_retrieval(sorted_query[:i+1], filename, outdexer)
        if len(retrival_sets) > top_k:
            break
    
    score_dict = defaultdict(float)

    #compute the score for each document
    for doc_id in retrival_sets:
        document = documentDict[int(doc_id)]
        tf_dict = document.doc_tf_dict
        term_score_dict = defaultdict(float)
        for term in sorted_query:
            #the formula is weighted_freq * idf_score / length of the document
            if term in term_score_dict:
                score_dict[int(doc_id)] += term_score_dict[term]
                continue
            if term not in tf_dict:
                continue
            else:                
                #score = tf_dict[term][0] * outdexer[term][2] / tf_dict[term][1]
                #print(term[0])
                score = calculate_log_tf(tf_dict[term][0]) * outdexer[term][2]
                score_dict[int(doc_id)] += score
                term_score_dict[term] = score

        score_dict[int(doc_id)] =  (score_dict[int(doc_id)] / (query_len * documentDict[int(doc_id)].length)) + (documentDict[int(doc_id)].pagerank)
        #print(documentDict[int(doc_id)].pagerank)
    
    retrival_list = list(retrival_sets)
    #DEBUG
    res = sorted(retrival_list[:top_k], key= lambda x:score_dict[x], reverse=True) 
    print(time.time() - start)
    return res
        

def build_children_and_parents(url_dict, doc_dict):
    for doc_id, doc in doc_dict.items():
        for url in doc.out_urls:
            if url in url_dict:
                cur_url_doc_id = url_dict[url]
                doc_dict[cur_url_doc_id].parents.append(doc_id)
                doc.children.append(cur_url_doc_id)



if __name__=="__main__":
    # test1 = open(os.path.join(PARENTDIRECTORY, "data/test1.txt"), 'r')
    # test2 = open(os.path.join(PARENTDIRECTORY, "data/test2.txt"), 'r')
    # merge(test1, test2, 15)
    #file = open(os.path.join(PARENTDIRECTORY, "data/PI13.txt"), 'r')
    # outdexer = {}
    # start = 0
    # stop = 0
    # line = file.readline()
    # while line != '':
    #     outdexer[line.split()[0]] = start
    #     start += len(line) + 1
    #     stop += 1
    #     line = file.readline()
    #     if stop == 2:
    #         break
    # print(outdexer)
    # file.seek(36398)
    # print(file.readline())
    a = ["hello"]
    print("FINAL:", tokenize(a))

    