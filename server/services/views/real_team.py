from http import HTTPStatus

from sanic.views import HTTPMethodView
from sanic.response import json

from engine import Connection
from settings import TypeLink
from services.forms import TeamResponseSchema
from services.utils import get_real_teams, get_links, put_real_teams_by_link


class RealTeamsView(HTTPMethodView):

    async def get(self, request):
        real_teams = await get_real_teams()
        resp = TeamResponseSchema().dump(real_teams, many=True)
        return json(resp, HTTPStatus.OK)

    async def put(self, request):
        links = await get_links(TypeLink.REAL_TEAM)
        async with Connection() as conn:
            for link in links:
                await put_real_teams_by_link(conn, link)
        return json("OK", HTTPStatus.OK)
