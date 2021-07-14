# _*_ coding: utf-8 _*_
import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
