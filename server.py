__author__ = 'Abdulrahman Semrie'

import pathlib
from flask import Flask, request, Response
from jsonrpcserver import methods
import os
from config import MOZI_URI
import shutil
import requests

app = Flask(__name__)


@methods.add
def handle(**kwargs):
    content = kwargs["file"]
    opts = kwargs["options"]

    params = {"file": content, "options": opts}

    response = requests.post(MOZI_URI, json=params)

    if response.status_code == 201:
        return str(response.content, "utf-8")

    else:
        return "Error occurred Please try again"


def clean_up(task_id):
    task_dir = os.path.join(pathlib.Path(__file__).absolute().parent, 'data/'+task_id)
    if os.path.exists(task_dir):
        shutil.rmtree(task_dir)

@app.route('/', methods=['POST'])
def index():
    req = request.get_data().decode()
    response = methods.dispatch(req)
    return Response(str(response), response.http_status, mimetype='application/json')





if __name__ == '__main__':
    app.run(port=5001)
