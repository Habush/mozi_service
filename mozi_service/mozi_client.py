__author__ = 'Xabush Semrie'

import pathlib
import grpc
from service_specs.moses_service_pb2 import AnalysisParameters, CrossValOptions
from service_specs.moses_service_pb2_grpc import MosesServiceStub
import os

moses_opts = "-j8 --balance=1 -m 1000 -W1 --output-cscore=1 --result-count 100 --reduct-knob-building-effort=1 --hc-widen-search=1 --enable-fs=1 --fs-algo=simple --fs-target-size=4 --hc-crossover-min-neighbors=5000 --fs-focus=all --fs-seed=init --complexity-ratio=3 --hc-fraction-of-nn=.3 --hc-crossover-pop-size=1000"

cross_val_opts = {"testSize": 0.3, "folds": 2, "randomSeeds": 2}

def send_data():

    yield AnalysisParameters(mosesOpts=moses_opts)

    crossVal = CrossValOptions(testSize=cross_val_opts["testSize"], folds=cross_val_opts["folds"], randomSeed=cross_val_opts["randomSeeds"])

    yield AnalysisParameters(crossValOpts=crossVal)

    yield AnalysisParameters(category="older-than")

    data_dir = os.path.join(pathlib.Path(__file__).absolute().parent.parent, 'data')

    os.chdir(data_dir)

    with open('bin_truncated.csv', 'rb') as f:
        while True:
            buffer = f.read()

            if buffer:
                yield AnalysisParameters(dataset=buffer)

            else:
                return




def start_analysis(stub):
    iterator = send_data()
    result = stub.StartAnalysis(iterator)

    return result


if __name__ == "__main__":
    channel = grpc.insecure_channel("localhost:8000")
    stub = MosesServiceStub(channel)

    result = start_analysis(stub)

    print(result)

