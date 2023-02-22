from nltk.stem import SnowballStemmer
SNOWBALL = SnowballStemmer(language="english")

print(SNOWBALL.stem("statistics112"))
print(SNOWBALL.stem("produce"))
print(SNOWBALL.stem("produces"))


# import pickle, os

# parent_dir = os.path.dirname(os.path.realpath(__file__))


# indexer = {"Hello":2}
# indexer_file = open(os.path.join(parent_dir, "data/indexer"), 'wb')
# pickle.dump(indexer, indexer_file)
# indexer_file.close()

# import os

# import json

# with open('src/data/indexer.json') as json_file:
#     data = json.load(json_file)
    
# print(len(data))