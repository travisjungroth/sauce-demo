from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    with open('index.html') as f:
        return f.read()


@app.route('/success')
def success():
    with open('success.html') as f:
        return f.read()


if __name__ == '__main__':
    app.run()
