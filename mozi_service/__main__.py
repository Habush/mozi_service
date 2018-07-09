__author__ = 'Abdulrahman Semrie'

from flask import Flask, request, Response
from jsonrpcserver import methods
import requests
from config import MOZI_URI, SERVER_PORT, DEBUG_MODE

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


@app.route('/', methods=['POST'])
def index():
    req = request.get_data().decode()
    response = methods.dispatch(req)
    return Response(str(response), response.http_status, mimetype='application/json')





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=SERVER_PORT, debug=DEBUG_MODE)
