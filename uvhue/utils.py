from nose.tools import *
from uvhttp.utils import HttpServer
from sanic.response import json

class HueServer(HttpServer):
    def add_routes(self):
        super().add_routes()

        self.app.add_route(self.link, '/api', methods=['POST'])

    def link(self):
        pass
