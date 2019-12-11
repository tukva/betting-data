from http import HTTPStatus

from sanic.views import HTTPMethodView
from sanic.response import json
from common.utils.camunda import Camunda, CamundaException

from settings import StatusTeam, TypeLink
from engine import Connection
from services.forms import TeamResponseSchema
from services.utils import get_teams, get_team_by_id, get_teams_by_link_id, moderate_team, approve_team, \
    get_link_by_id, get_links, put_teams_by_link
from services.decorators import validate_change_status_team


class TeamsView(HTTPMethodView):

    async def get(self, request):
        if request.args.get("link_id"):
            link_id = request.args.get("link_id")
            teams = await get_teams_by_link_id(link_id)
        else:
            teams = await get_teams()
        resp = TeamResponseSchema().dump(teams, many=True)
        return json(resp, HTTPStatus.OK)

    async def put(self, request):
        try:
            process_definition_id = await Camunda.get_process_definition_id("BetAggr")
        except CamundaException as e:
            return json(e, HTTPStatus.UNPROCESSABLE_ENTITY)
        if request.args.get("link_id"):
            link_id = request.args.get("link_id")
            link = await get_link_by_id(link_id, TypeLink.TEAM)
            async with Connection() as conn:
                await put_teams_by_link(conn, link, process_definition_id)
        else:
            links = await get_links("team")
            async with Connection() as conn:
                for link in links:
                    await put_teams_by_link(conn, link, process_definition_id)
        return json("OK", HTTPStatus.OK)


class TeamDetailsView(HTTPMethodView):

    @validate_change_status_team()
    async def patch(self, request, team_id):
        team = await get_team_by_id(team_id)
        if request.json.get("status") == StatusTeam.MODERATED:
            try:
                await Camunda.task_complete(team.team_id, StatusTeam.NEW, True)
            except CamundaException as e:
                return json(e, HTTPStatus.UNPROCESSABLE_ENTITY)
            await moderate_team(team.team_id, request.json.get("real_team_id"), StatusTeam.MODERATED)
        else:
            try:
                await Camunda.task_complete(team.team_id, StatusTeam.MODERATED, True)
            except CamundaException as e:
                return json(e, HTTPStatus.UNPROCESSABLE_ENTITY)
            await approve_team(team.team_id, StatusTeam.APPROVED)
        return json("OK", HTTPStatus.OK)
