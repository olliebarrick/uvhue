from uvhttp.http import Session

class Hue(Session):
    """
    Hue client for :mod:`uvhttp`.
    """
    def __init__(self, loop, hue_api, **kwargs):
        self.hue_api = hue_api
        super().__init__(10, loop, **kwargs)

    def set_hue_id(self, hue_id):
        """
        Set the hue id for the API to use.
        """
        pass

    async def link(self):
        """
        Link with a hue bridge. Return a user id that can be used.
        """
        user = await self.post(self.hue_api, data=json.dumps({
            "devicetype": "uvhue#device"
        }).encode())

    async def api(self, method, path, *args, **kwargs):
        """
        Make an API request to hue with the given path.

        The path should be everything except for the common part of the URL.

        For example, ``https://hue/api/1209310239/lights`` becomes
        ``/lights``.
        """
        return await self.request(method, self.hue_api + path, *args, **kwargs)
