from flask import Flask

app = Flask(__name__)
# @app.route("/")
# def poop():
#     return 'anthony'

@app.route("/test")
def test():
    return [
        {
            "url": "hamburger.ics.com",
            "description": "hamburger"
        },
        {
            "url": "poop.ics.uci.edu",
            "description": "this is the poop website"
        }
    ]

if __name__=='__main__':
    app.run(debug=True, port=4999)