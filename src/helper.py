ALPHANUMERIC = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1",
    "2", "3", "4", "5", "6", "7", "8", "9", "0"}

def tokenize(wordList: '[str]') -> '[str]':
    """
    The function returns a list of strings (tokens) from the original file
    that are seperated by non alphanumeric characters. If an error occured
    then the function will return -1.
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


def read_set_from_line( filename, offset)  -> set:    
    with open(filename, 'r') as file:
        file.seek(offset)
        line = file.readline()
        return set(line.split()[1:])

    



def boolean_retrieval(query, filename, indexer)->set:
    query = sorted(query, key = lambda x: indexer[x][2])
    s = read_set_from_line(filename, indexer[query[0]][1])



    for string in query[1:]:
        offset = indexer[string][1]
        next_set = read_set_from_line(filename, offset)
        temp = set()
        for word in s:
            if word in next_set:
                temp.add(word)
        s = temp
            
        
    return s

{1,2,3,4,5,6,7,8,9,10}
{1,2,3}

# if __name__=="__main__":
#     exWords = ["Pineapple", "pizza", "spider-man", "UCI", "don't", "Eric", "would",
#         "order", "pineapple", "pizza", "(apple)"]

#     print(tokenize(exWords))