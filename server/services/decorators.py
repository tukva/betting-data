from functools import wraps
from http import HTTPStatus

from sanic.response import json
from marshmallow.exceptions import ValidationError

from models import tb_team, tb_real_team
from settings import StatusTeam
from engine import Connection
from services.forms import ChangeStatusTeam


def validate_change_status_team():
    def decorator(f):
        @wraps(f)
        async def decorated_function(self, request, team_id, *args, **kwargs):
            try:
                ChangeStatusTeam().load(request.json)
            except ValidationError as e:
                return json(e.messages, HTTPStatus.UNPROCESSABLE_ENTITY)

            async with Connection() as conn:
                select_team = await conn.execute(tb_team.select().where(
                    tb_team.c.team_id == team_id))

                if not select_team.rowcount:
                    return json("Not Found", HTTPStatus.NOT_FOUND)

                if request.json.get("status") == StatusTeam.APPROVED:
                    select_real_team = await conn.execute(tb_real_team.select().where(
                        tb_real_team.c.real_team_id == request.json.get("real_team_id")))

                    if not select_real_team.rowcount:
                        return json("real_id does not exist", HTTPStatus.UNPROCESSABLE_ENTITY)

            return await f(self, request, team_id, *args, **kwargs)
        return decorated_function
    return decorator
