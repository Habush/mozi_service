__author__ = 'Abdulrahman Semrie'

import pathlib
from flask import Flask, request, Response
from jsonrpcserver import methods
import threading
import os
import base64
from cross_val.moses_cross_val import CrossValidation
from config import MONGODB_URI
import uuid
from pymongo import MongoClient
from models import Task, Result
import time
from itertools import groupby
import jsonpickle
import shutil

app = Flask(__name__)

db = MongoClient(MONGODB_URI)["mozi_service"]


def run_cross_validation(**kwargs):

    id = kwargs["id"]
    opts = kwargs["opts"]
    cwd = kwargs["cwd"]

    cross_val = CrossValidation(db, id, opts, cwd=cwd)

    cross_val.run_cross_val()


@methods.add
def handle(**kwargs):
    content = base64.b64decode(kwargs['file'])
    opts = kwargs['options']

    task_id = str(uuid.uuid4())

    data_dir = os.path.join(pathlib.Path(__file__).absolute().parent, 'data')

    os.chdir(data_dir)
    if (not os.path.exists(task_id)):
        os.mkdir(task_id)

    file_path = "{0}/{0}.csv".format(task_id)

    with open(file_path, 'wb') as f:
        f.write(content)

    task = Task(db, task_id, time.time(), 1)
    task.save()
    params = {"id": task_id, "opts": opts, "cwd": data_dir+ "/" + task_id}

    thread = threading.Thread(target=run_cross_validation, kwargs=params, daemon=True)
    thread.start()

    return task_id


def clean_up(task_id):
    task_dir = os.path.join(pathlib.Path(__file__).absolute().parent, 'data/'+task_id)
    if os.path.exists(task_dir):
        shutil.rmtree(task_dir)

@app.route('/', methods=['POST'])
def index():
    req = request.get_data().decode()
    response = methods.dispatch(req)
    return Response(str(response), response.http_status, mimetype='application/json')

@app.route("/status/<id>", methods=['GET'])
def status(id):

    task_status = Task.get_task_status(db, id)

    if task_status == 0:
        clean_up(id)
        results = Result.get_result(id, db)

        tree = []
        if results is not None:

            for fold, result in groupby(sorted(results, key=lambda k: k.fold), lambda k: k.fold):
                temp = {"fold": fold}
                for r in result:
                    result_model = {"id": r.id, "task": r.task, "fold": r.fold, "precision": r.precision,
                                    "recall": r.recall, "accuracy": r.accuracy, "data": r.data}
                    temp["result"] = jsonpickle.encode(result_model, unpicklable=False)

                tree.append(temp)

            return jsonpickle.encode(tree, unpicklable=False), 200

    elif task_status == 1:
        return "Moses still running"

    elif task_status == -2:
        return "Task not found"

    elif task_status == -1:
        return "Task run into error"




if __name__ == '__main__':
    app.run()
