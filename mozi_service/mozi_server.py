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

    def StartAnalysis(self, request, context):

        moses_opts, cross_val_opts = request.mosesOpts, request.crossValOpts
        category, dataset = request.category, request.dataset

        req_json = {"mosesOpts": moses_opts, "crossValOpts": cross_val_opts, "category": category, "file": dataset}

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
