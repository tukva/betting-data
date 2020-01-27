from http import HTTPStatus

from sanic.views import HTTPMethodView
from sanic.response import json
from common.utils.decorators import filter_data

from models import tb_link
from services.utils import get_data
from services.forms import LinkResponseSchema


class LinksView(HTTPMethodView):

    @filter_data(tb_link)
    async def get(self, request):
        sql_expr = request.get("sql_expr")
        links = await get_data(sql_expr)
        resp = LinkResponseSchema().dump(links, many=True if isinstance(links, list) else False)
        return json(resp, HTTPStatus.OK)


class LinkDetails(HTTPMethodView):

    @filter_data(tb_link)
    async def get(self, request, link_id):
        sql_expr = request.get("sql_expr")
        links = await get_data(sql_expr)
        resp = LinkResponseSchema().dump(links)
        return json(resp, HTTPStatus.OK)
