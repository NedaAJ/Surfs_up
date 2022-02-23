from flask import Flask

#creating a new Flask App Instance
app = Flask(__name__)

@app.route('/')

def hello_world():
    return 'Hello World'

# http://127.0.0.1:5000/
