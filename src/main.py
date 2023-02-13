import os
import Document

def parse(file, id: int) -> Document:
    #weightDict = loop through all the {key:word : val: int}
    #tfFreqDict = loop through keys of weightDict and create dict {key:stemWord : val: (freq:float, weight:int)}
    # instantiate Document -> Document(id, tfFreqDict)
    # return Document 
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

