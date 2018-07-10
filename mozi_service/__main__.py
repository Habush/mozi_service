__author__ = 'Abdulrahman Semrie'

from jsonrpcserver import methods
import requests
from aiohttp import web
from config import MOZI_URI, SERVER_PORT

app = web.Application()


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



async def index(request):
    req = await request.text()
    response = methods.dispatch(req)
    return web.json_response(response, status=response.http_status)





if __name__ == '__main__':
    app.router.add_post('/', index)
    web.run_app(app, host='127.0.0.1', port=SERVER_PORT)
