from flask import Flask
app = Flask(__name__)
@app.route("/")
def test():
    return 'anthony'

if __name__=='__main__':
    app.run(debug=True, port=4999)