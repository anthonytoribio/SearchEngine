import os
import Document
from bs4 import BeautifulSoup
import json
def parse(file, id: int) -> Document:
    f = json.loads(file)
    soup = BeautifulSoup(file["content"])
    WeightDict = {word : 1 for word in soup.title.string}
    #tfFreqDict = loop through keys of weightDict and create dict {key:stemWord : val: (freq:float, weight:int)}
    # instantiate Document -> Document(id, tfFreqDict)
    # return Document 
    print(WeightDict)
    pass



def main():
    # assign directory
    directory = 'DEV/'
    directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), directory)
    # iterate over files in
    # that directory
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            file =os.path.join(subdir, file)
            with open(file, 'r') as opened:
                pass



if __name__ == "__main__":
    main()

