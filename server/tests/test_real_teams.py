import pytest
from unittest import mock

from common.rest_client.base_client_parser import BaseClientParser


@pytest.mark.real_teams
async def test_get_real_teams(test_cli, add_real_team):
    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'real_team_id': 1, 'name': 'Chelsea', }]

    resp = await test_cli.get('/links?data=real_teams')
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await test_cli.get('/links/1?data=real_teams')
    assert resp.status == 422
    assert await resp.json() == "Can not to use link"


@pytest.mark.real_teams
async def test_refresh_real_teams(test_cli, mock_parser_resp, tables):
    with mock.patch.object(BaseClientParser, 'parse_teams', return_value=mock_parser_resp):
        resp = await test_cli.put('/links?data=real_teams')

        assert resp.status == 200
        assert await resp.json() == "Ok"

        resp = await test_cli.put('/links/1?data=real_teams')
        assert resp.status == 422
        assert await resp.json() == "Can not to use link"
