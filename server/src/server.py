from flask import Flask, request, redirect, url_for
from main import FILE, main
import json
app = Flask(__name__)
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
        return_lst = []
        query = request.json["state"]
        # results = main(query)
        results = ["hamburger.uci.ics.edu", "example.com", query+".com"]
        for result in results:
            return_lst.append({"url":result,"description":"NULL"})
        return return_lst
    else:
        return
    
if __name__=='__main__':
    app.run(debug=True, port=4999)