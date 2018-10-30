import base64
import time

__author__ = 'Xabush Semrie'

from service_specs.moses_service_pb2_grpc import MosesServiceServicer, add_MosesServiceServicer_to_server
from service_specs.moses_service_pb2 import Result
from mozi_service.config import MOZI_URI
import requests
import grpc
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class MoziSerivcer(MosesServiceServicer):

    def StartAnalysis(self, request_iterator, context):

        moses_opts, cross_val_opts, category, data_bytes = None, {}, "", bytearray()

        for i, data in enumerate(request_iterator):
            if i == 0:
                if data.HasField("mosesOpts"):
                    moses_opts = data.mosesOpts
                    continue
                else:
                    raise Exception("Moses options not found")
            elif i == 1:
                if data.HasField("crossValOpts"):
                    cross_val_opts['folds'] = data.crossValOpts.folds
                    cross_val_opts['testSize'] = data.crossValOpts.testSize
                    cross_val_opts['randomSeed'] = data.crossValOpts.randomSeed
                    continue
                else:
                    raise Exception("Cross-validation options not found")

            elif i == 2:
                if data.HasField("category"):
                    category = data.category
                    continue
                else:
                    raise Exception("Category option not found")


            else:
                if data.HasField("dataset"):
                    data_bytes.extend(bytes(data.dataset))

        b_string = data_bytes.decode('utf-8').replace("'", '"')
        req_json = {"mosesOpts": moses_opts, "crossValOpts": cross_val_opts, "category": category ,"file": b_string}

        response = requests.post(MOZI_URI, json=req_json)

        if response.ok:
            result_url = response.json()["url"]
            return Result(resultUrl=result_url, description="")

        return Result(result_url="", description="Error occurred")


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    add_MosesServiceServicer_to_server(MoziSerivcer(), server)
    server.add_insecure_port('[::]:8000')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
