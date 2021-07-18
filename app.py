from flask import Flask, app
from flask.helpers import url_for,send_file

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> SSL certificado </h1>'
    
@app.route('/.well-known/pki-validation/2B629DA0F08747ECBE5DA8DC53E1D04D.txt')
def hello():
    return send_file(path_or_file='2B629DA0F08747ECBE5DA8DC53E1D04D.txt')

if __name__ == '__main__':
    app.run(debug=False)
