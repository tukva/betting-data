from collections import namedtuple
from functools import wraps

from sanic.response import json

from services.utils import TeamsByLink, TeamsByAllLinks, RealTeamsByAllLinks

Data = namedtuple('Data', ['name', 'cls_data_by_link', 'cls_data_by_all_links'])
teams = Data("teams", TeamsByLink, TeamsByAllLinks)
real_teams = Data("real_teams", None, RealTeamsByAllLinks)

VALID_DATA = [teams, real_teams]


def mapp_func():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            data = request.args.get("data")

            if not data:
                return json("Type the data parameter if you want to get something", 200)

            data_by = None
            for field in VALID_DATA:
                if field.name == data:
                    data_by = field

            if not data_by:
                return json(f"Тo such data '{data}'. "
                            f"Valid data: {[field.name for field in VALID_DATA]}", 422)

            if kwargs.get("link_id"):
                if not data_by.cls_data_by_link:
                    return json("Can not to use link", 422)

                cls = data_by.cls_data_by_link
                return await f(request=request, cls=cls, *args, **kwargs)

            if not data_by.cls_data_by_all_links:
                return json("Can not to use all links", 422)

            cls = data_by.cls_data_by_all_links

            return await f(request, cls=cls, *args, **kwargs)
        return decorated_function
    return decorator
