__author__ = 'Abdulrahman Semrie'

from jsonrpcclient import request as rpcrequest
import base64
import pathlib

import os


data_dir = os.path.join(pathlib.Path(__file__).absolute().parent, 'data')

os.chdir(data_dir)

with open('bin_truncated.csv', 'rb') as f:
    content = f.read()


encoded = base64.b64encode(content).decode()

opts = {'numberOfThreads':8, 'maximumEvals': 1000, 'balance': 1, 'outputCscore': 1, 'reductKnobBuildingEffort': 1, 'fsAlgo':'smd', 'fsTargetSize':4, 'inputCategory': 'older-than'}

if __name__ == '__main__':
    response = rpcrequest('http://localhost:5000/', 'handle', file=encoded, options={"mosesOptions": opts, "crossValidationOptions": {"testSize": 0.3, "folds": 2, "randomSeed": 2}})

    print(response)

