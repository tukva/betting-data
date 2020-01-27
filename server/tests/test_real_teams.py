from http import HTTPStatus
from unittest import mock

import pytest

from common.rest_client.base_client_parser import BaseClientParser


@pytest.mark.real_teams
async def test_get_real_teams(test_cli, add_real_team):
    response_json = {'created_on': '2019-11-07T14:13:44.041152', 'real_team_id': 1, 'name': 'Chelsea'}

    resp = await test_cli.get('/real-teams')
    assert resp.status == HTTPStatus.OK
    assert await resp.json() == response_json


@pytest.mark.real_teams
async def test_get_real_teams_by_params(test_cli, add_real_team):
    response_json = {'name': 'Chelsea'}

    resp = await test_cli.get('/real-teams?fields=name&where=name:eq:Chelsea')
    assert resp.status == HTTPStatus.OK
    assert await resp.json() == response_json


@pytest.mark.real_teams
async def test_create_or_update_real_teams(test_cli, mock_parser_resp, tables):
    with mock.patch.object(BaseClientParser, 'parse_teams', return_value=mock_parser_resp):
        json = {'name': 'Chelsea'}
        resp = await test_cli.post('/real-teams', json=json)

        assert resp.status == HTTPStatus.OK
        assert await resp.json() == "OK"

        resp = await test_cli.post('/real-teams', json=json)

        assert resp.status == HTTPStatus.OK
        assert await resp.json() == "OK"
