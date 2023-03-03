from flask import Flask

app = Flask(__name__)
@app.route("/")
def poop():
    return 'anthony'

@app.route("/test")
def test():
    return {
        "name":"hey",
        "bro":"nothing"
    }

if __name__=='__main__':
    app.run(debug=True, port=4999)