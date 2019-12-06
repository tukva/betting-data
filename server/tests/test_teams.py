import pytest
from unittest import mock

from common.rest_client.base_client_parser import BaseClientParser
from common.utils.camunda import Camunda

from services.decorators import VALID_DATA


@pytest.mark.teams
async def test_get_teams_by_all_link(test_cli, add_team):
    resp = await test_cli.get('/links?data=teams')

    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'link_id': 1, 'team_id': 1,
                      'name': 'Chelsea', 'real_team_id': None, 'site_name': 'bwin', 'status': 'new',
                      'process_instance_id': None}]

    assert resp.status == 200
    assert await resp.json() == response_json


@pytest.mark.teams
async def test_get_teams_by_link(test_cli, add_team):
    resp = await test_cli.get('/links/1?data=teams')

    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'link_id': 1, 'team_id': 1,
                      'name': 'Chelsea', 'real_team_id': None, 'site_name': 'bwin',
                      'status': 'new', 'process_instance_id': None}]

    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await test_cli.get('/links/3?data=teams')

    assert resp.status == 404
    assert await resp.json() == "Not Found"


@pytest.mark.teams
async def test_refresh_teams_by_link(test_cli, mock_parser_resp, mock_camunda_init, tables):
    with mock.patch.object(BaseClientParser, 'parse_teams', return_value=mock_parser_resp):
        with mock.patch.object(Camunda, 'init', return_value=mock_camunda_init):
            resp = await test_cli.put('/links/1?data=teams')

            assert resp.status == 200
            assert await resp.json() == "Ok"

            resp = await test_cli.put('/links/3?data=teams')

            assert resp.status == 404
            assert await resp.json() == "Not Found"


@pytest.mark.teams
async def test_wrong_parameters_by(test_cli, add_team):
    resp = await test_cli.get('/links')

    assert resp.status == 200
    assert await resp.json() == "Type the data parameter if you want to get something"

    resp = await test_cli.get('/links?data=wrong_value')

    assert resp.status == 422
    assert await resp.json() == f"Тo such data 'wrong_value'. Valid data: " \
                                f"{[field.name for field in VALID_DATA]}"
