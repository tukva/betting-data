from sanic.response import json
from marshmallow.exceptions import ValidationError

from engine import Connection
from services.utils import set_real_team
from services.forms import ChangeStatusTeam


async def change_status_team(request, team_id):
    try:
        data = ChangeStatusTeam().load(request.json)
    except ValidationError as e:
        return json(e.messages, 422)
    async with Connection() as conn:
        return await set_real_team(conn, team_id, data)
