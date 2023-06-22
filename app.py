from flask import Flask, render_template
from 

app = Flask(__name__)

@app.route('/')
def display_data():
    data = {
        'accountId': {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3'
        }
    }
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
