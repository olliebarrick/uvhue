from nose.tools import *
from uvhttp.utils import http_server
from uvhttp.dns import Resolver
from uvhue.uvhue import Hue, HueException
from uvhue.utils import HueServer

@http_server(HueServer)
async def test_hue_link(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'hue', 80, server.host.encode(), 60, port=server.port)

    server.press_button()

    hue = Hue(loop, b'http://hue/', resolver=resolver)
    assert_equal(await hue.link(), hue.hue_id)
    assert_equal(len(hue.hue_id), 32)

@http_server(HueServer)
async def test_hue_link_unauthorized(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'hue', 80, server.host.encode(), 60, port=server.port)

    hue = Hue(loop, b'http://hue/', resolver=resolver)

    try:
        await hue.link()
    except HueException:
        pass
    else:
        raise AssertionError('Should have raised a HueException.')

@http_server(HueServer)
async def test_hue_api(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'hue', 80, server.host.encode(), 60, port=server.port)

    server.press_button()

    hue = Hue(loop, b'http://hue/', resolver=resolver)
    await hue.link()

    response = await hue.api(b'GET', b'lights')

    lights = response.json()
    assert_equal(len(lights), 2)

@http_server(HueServer)
async def test_hue_list_lights(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'hue', 80, server.host.encode(), 60, port=server.port)

    server.press_button()

    hue = Hue(loop, b'http://hue/', resolver=resolver)
    await hue.link()

    lights = await hue.lights()
    assert_equal(len(lights), 2)

@http_server(HueServer)
async def test_hue_set_state(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'hue', 80, server.host.encode(), 60, port=server.port)

    server.press_button()

    hue = Hue(loop, b'http://hue/', resolver=resolver)
    await hue.link()

    lights = await hue.lights()

    xy = { "xy": [1, 2]}

    assert_equal(await hue.set_state("1", xy), True)

    # cached
    lights = await hue.lights()
    assert_not_equal(lights["1"]["state"]["xy"], xy["xy"])
    
    lights = await hue.lights(refresh=True)
    assert_equal(lights["1"]["state"]["xy"], xy["xy"])

@http_server(HueServer)
async def test_hue_set_all_states(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'hue', 80, server.host.encode(), 60, port=server.port)

    server.press_button()

    hue = Hue(loop, b'http://hue/', resolver=resolver)
    await hue.link()

    xy = { "xy": [1, 2]}

    assert_equal(await hue.set_states(xy), True)

    # cached
    lights = await hue.lights()
    assert_not_equal(lights["1"]["state"]["xy"], xy["xy"])
    assert_not_equal(lights["2"]["state"]["xy"], xy["xy"])
    
    lights = await hue.lights(refresh=True)
    assert_equal(lights["1"]["state"]["xy"], xy["xy"])
    assert_equal(lights["2"]["state"]["xy"], xy["xy"])
