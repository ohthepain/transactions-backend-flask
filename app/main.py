from flask import Flask, render_template

app = Flask(__name__)


@app.route('/ping')
def hello_world():
    return 'pong'

if __name__ == '__main__':
    app.run()
