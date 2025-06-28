from flask import Flask, render_template
import os

app = Flask(__name__)

def listdir_without_hidden(path):
    for file in os.listdir(path):
        if not file.startswith('.'):
            yield file
            
@app.route('/')
@app.route('/<path:path>')
def index(path=None):
    if path is None:
        path = '/'
    elif path =="/":
        pass
    else:
        path="/"+path
    data = list(listdir_without_hidden(path))
    
    return render_template('index.html', data_array=data)


if __name__ == '__main__':
    app.run(debug=True)
