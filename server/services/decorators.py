from functools import wraps
from http import HTTPStatus

from sanic.response import json
from marshmallow.exceptions import ValidationError

from constants import StatusTeam
from services.forms import ChangeStatusTeam
from services.utils import real_team_exists, link_exists


def validate_change_status_team():
    def decorator(f):
        @wraps(f)
        async def decorated_function(self, request, *args, **kwargs):
            try:
                ChangeStatusTeam().load(request.json)
            except ValidationError as e:
                return json(e.messages, HTTPStatus.UNPROCESSABLE_ENTITY)

            if request.json.get("status") == StatusTeam.MODERATED:
                real_team_id = request.json.get("real_team_id")
                if not await real_team_exists(real_team_id):
                    return json("real_id does not exist", HTTPStatus.UNPROCESSABLE_ENTITY)

            return await f(self, request, *args, **kwargs)
        return decorated_function
    return decorator


def validate_create_team():
    def decorator(f):
        @wraps(f)
        async def decorated_function(self, request, *args, **kwargs):
            link_id = request.json.get("link_id")
            if not await link_exists(link_id):
                return json("link_id does not exist", HTTPStatus.UNPROCESSABLE_ENTITY)

            return await f(self, request, *args, **kwargs)
        return decorated_function

    return decorator
