# from nltk.stem import SnowballStemmer
# SNOWBALL = SnowballStemmer(language="english")

# print(SNOWBALL.stem("i'm"))

import json
import os

import json
    
# Data to be written
dictionary ={
    "name" : "sathiyajith",
    "rollno" : 56,
    "cgpa" : 8.6,
    "phonenumber" : "9976770500"
}
    

    
parent_dir = os.path.dirname(os.path.realpath(__file__))

indexer_json_file = open(os.path.join(parent_dir, "data/indexer.json"), 'w')

# with open(os.path.join(parent_dir, "data/indexer.json"), "w") as outfile:
json.dump(dictionary, indexer_json_file)
    