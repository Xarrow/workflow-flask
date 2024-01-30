# -*- coding: utf-8 -*-
from flask import Flask
from flask import request

from singlefile import SingleFile

app = Flask(__name__)
singleFile = SingleFile(chrome_cwd="/usr/bin/google-chrome-stable", single_file_cwd="/workspaces/single-file-cli")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/singleFile", methods=['GET', 'POST'])
def single_file():
    if request.method == 'POST':
        url = request.get_json()['url']
    else:
        url = request.args.get("url")
    return singleFile.execute(url)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8089, debug=True)
