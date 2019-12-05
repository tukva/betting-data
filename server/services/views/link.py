from sanic.views import HTTPMethodView
from engine import Connection

from services.decorators import mapp_func


class LinkView(HTTPMethodView):
    decorators = [mapp_func()]

    async def get(self, request, link_id, cls):
        async with Connection() as conn:
            return await cls.get(conn, link_id)

    async def put(self, request, link_id, cls):
        async with Connection() as conn:
            return await cls.put(conn, link_id)


class AllLinksView(HTTPMethodView):
    decorators = [mapp_func()]

    async def get(self, request, cls):
        async with Connection() as conn:
            return await cls.get(conn)

    async def put(self, request, cls):
        async with Connection() as conn:
            return await cls.put(conn)
