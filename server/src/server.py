from flask import Flask, request, redirect, url_for
from main import FILE, main
import json
import pickle, os
import time
from helper import ranked_retrieval

app = Flask(__name__)
parent_dir = os.path.dirname(os.path.realpath(__file__))
outdexer_file = open(os.path.join(parent_dir, "data/outdexer"), 'rb')
outdexer = pickle.load(outdexer_file)
doc_dict_file = open(os.path.join(parent_dir, "data/doc_dict"), 'rb') 
documentDict = pickle.load(doc_dict_file)
K = 200
@app.route("/")
def start():
    return 'works'

@app.route("/test")
def test():
    return {
        "name":"h",
        "bro":"nothing"
    }

@app.route("/test/help", methods=["POST", "GET"])
def get_query():
    if request.method == "POST":
        start = time.time()
        return_lst = []
        query = request.json["state"]
        doc_ids = ranked_retrieval(query.split(), FILE, outdexer, documentDict, K)
        for id in doc_ids:
            doc = documentDict[int(id)]
            return_lst.append({"title":doc.title, "url":doc.docUrl, "description":doc.desc})
        return_lst.append(time.time()-start)
        return return_lst
    else:
        return


if __name__=='__main__':
    app.run(debug=True, port=4999)