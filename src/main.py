import os
import Document
import pickle   

def parse(file, id: int) -> Document:
    #weightDict = loop through all the {key:word : val: int}
    #tfFreqDict = loop through keys of weightDict and create dict {key:stemWord : val: (freq:float, weight:int)}
    # instantiate Document -> Document(id, tfFreqDict)
    # return Document 
    pass



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

