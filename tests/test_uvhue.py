from nose.tools import *
from uvhttp.utils import http_server
from uvhttp.dns import Resolver
from uvspotify.uvhue import Hue
from uvspotify.utils import HueServer

@http_server(HueServer)
async def test_hue_link(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'hue', 80, server.host.encode(), 60, port=server.port)

    hue = Hue(loop, 'http://hue/', resolver=resolver)
    await hue.link()

