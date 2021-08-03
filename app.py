from flask import Flask, app
from flask.helpers import url_for,send_file

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> SSL certificado </h1>'
    
if __name__ == '__main__':
    app.run(debug=False)
