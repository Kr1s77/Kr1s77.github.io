# _*_ coding: utf-8 _*_
import os
import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


if __name__ == '__main__':
    print os.popen('curl http://httpbin.org/ip').read()
    app.run(host='0.0.0.0', port=8080)
