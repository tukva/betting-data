from http import HTTPStatus

from sanic.views import HTTPMethodView
from sanic.response import json
from common.utils.camunda import Camunda, CamundaException
from common.utils.decorators import filter_data

from constants import StatusTeam
from services.forms import CreateTeamSchema
from services.forms import TeamResponseSchema
from services.decorators import validate_change_status_team
from services.utils import get_data, update_team, create_or_update_team
from models import tb_team


class TeamsView(HTTPMethodView):

    @filter_data(tb_team)
    async def get(self, request):
        sql_expr = request.get("sql_expr")
        teams = await get_data(sql_expr)
        resp = TeamResponseSchema().dump(teams, many=True if isinstance(teams, list) else False)
        return json(resp, HTTPStatus.OK)

    async def post(self, request):
        try:
            process_definition_id = await Camunda.get_process_definition_id("BetAggr")
        except CamundaException as e:
            return json(e, HTTPStatus.UNPROCESSABLE_ENTITY)

        data = CreateTeamSchema().load(request.json)
        await create_or_update_team(process_definition_id, data)

        return json("OK", HTTPStatus.OK)


class TeamDetailsView(HTTPMethodView):

    @validate_change_status_team()
    @filter_data(tb_team)
    async def patch(self, request, team_id):
        sql_expr = request.get("sql_expr")
        team = await get_data(sql_expr)

        if not team:
            return json("Not Found", HTTPStatus.NOT_FOUND)

        new_status = request.json.get("status")
        complete_status = StatusTeam.NEW if new_status == StatusTeam.MODERATED else StatusTeam.MODERATED

        try:
            await Camunda.task_complete(team.team_id, complete_status, True)
        except CamundaException as e:
            return json(e, HTTPStatus.UNPROCESSABLE_ENTITY)

        update_data = {"status": StatusTeam.MODERATED}
        if new_status == StatusTeam.MODERATED:
            update_data["real_team_id"] = request.json.get("real_team_id")

        await update_team(team_id, **update_data)

        return json("OK", HTTPStatus.OK)
