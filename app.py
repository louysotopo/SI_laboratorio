from flask import Flask, app

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> SSL certificado </h1>'
    

if __name__ == '__main__':
    app.run(debug=True)
