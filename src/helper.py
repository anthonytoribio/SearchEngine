import os

PARENTDIRECTORY = os.path.dirname(os.path.realpath(__file__))
FILE = "FinalIndexer.txt" #String name of the text file that holds the combined indexer

ALPHANUMERIC = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1",
    "2", "3", "4", "5", "6", "7", "8", "9", "0"}

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
            #DEBUG print(f"data char is: {data[index]}")
            #DEBUG print(f"start data is: {data[start]}")
            if not (data[start] in ALPHANUMERIC) and data[index] in ALPHANUMERIC:
                #DEBUG print("Setting start")
                start = index
            elif data[start] in ALPHANUMERIC and not data[index] in ALPHANUMERIC:
                #DEBUG print("Adding token\n")
                tokens.append(data[start:index])
                start = index
    except UnicodeDecodeError:
        print("ERROR: Program can only tokenize a text file (.txt).")
        return -1
    if (len(tokens) < 1 or not tokens[-1] != data[start:index]) and data[start] in ALPHANUMERIC:
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
        returnedFile = open(os.path.join(PARENTDIRECTORY, FILE), 'w')
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
    returnedFile = open(os.path.join(PARENTDIRECTORY, "data/PI" + str(index + 1) +".txt"), 'r')

    return [returnedFile, index + 1]     



#This function takes a filename and an offset representing the statring byte to read from, it returns a set of words 
# that are read from the given line  
def read_set_from_line( filename, offset)  -> set:    
    with open(filename, 'r') as file:
        file.seek(offset)
        line = file.readline()
        return set(line.split()[1:])


#this function is bone of boolean retrieval, it takes a query of words, the name of the file to ream from, and an indexer object
def boolean_retrieval(query, filename, indexer)->set:
    query = sorted(query, key = lambda x: indexer[x][1])
    s = read_set_from_line(filename, indexer[query[0]][0])

    for string in query[1:]:
        offset = indexer[string][1]
        next_set = read_set_from_line(filename, offset)
        temp = set()
        for word in s:
            if word in next_set:
                temp.add(word)
        s = temp
        
    return s


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
    pass

    