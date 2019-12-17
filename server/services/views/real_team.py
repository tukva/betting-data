from http import HTTPStatus

from sanic.views import HTTPMethodView
from sanic.response import json
from common.utils.decorators import filter_data

from models import tb_real_team
from services.forms import TeamResponseSchema, CreateRealTeamSchema
from services.utils import get_data, create_update_real_team


class RealTeamsView(HTTPMethodView):

    @filter_data(tb_real_team)
    async def get(self, request):
        sql_expr = request.get("sql_expr")
        real_teams = await get_data(sql_expr)
        resp = TeamResponseSchema().dump(real_teams, many=True if isinstance(real_teams, list) else False)
        return json(resp, HTTPStatus.OK)

    async def post(self, request):
        data = CreateRealTeamSchema().load(request.json)
        await create_update_real_team(data)
        return json("Created", HTTPStatus.OK)
