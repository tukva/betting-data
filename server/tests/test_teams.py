import pytest
from unittest import mock

from common.rest_client.base_client_parser import BaseClientParser
from common.utils.camunda import Camunda


@pytest.mark.teams
async def test_get_teams_by_all_link(test_cli, add_team):
    resp = await test_cli.get('/teams')

    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'link_id': 1, 'team_id': 1,
                      'name': 'Chelsea', 'real_team_id': None, 'site_name': 'bwin', 'status': 'New'}]

    assert resp.status == 200
    assert await resp.json() == response_json


@pytest.mark.teams
async def test_get_teams_by_link(test_cli, add_team):
    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'link_id': 1, 'team_id': 1,
                      'name': 'Chelsea', 'real_team_id': None, 'site_name': 'bwin', 'status': 'New'}]

    resp = await test_cli.get('/teams?link_id=1')

    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await test_cli.get('/teams?link_id=3')

    assert resp.status == 200
    assert await resp.json() == []


@pytest.mark.teams
async def test_refresh_teams(test_cli, mock_parser_resp, mock_camunda_resp, tables):
    with mock.patch.object(BaseClientParser, 'parse_teams', return_value=mock_parser_resp):
        with mock.patch.object(Camunda, 'get_process_definition_id', return_value=mock_camunda_resp):
            with mock.patch.object(Camunda, 'start_process', return_value=mock_camunda_resp):
                resp = await test_cli.put('/teams')

                assert resp.status == 200
                assert await resp.json() == "OK"


@pytest.mark.teams
async def test_refresh_teams_by_link(test_cli, mock_parser_resp, mock_camunda_resp, tables):
    with mock.patch.object(BaseClientParser, 'parse_teams', return_value=mock_parser_resp):
        with mock.patch.object(Camunda, 'get_process_definition_id', return_value=mock_camunda_resp):
            with mock.patch.object(Camunda, 'start_process', return_value=mock_camunda_resp):
                resp = await test_cli.put('/teams?link_id=1')

                assert resp.status == 200
                assert await resp.json() == "OK"

                resp = await test_cli.put('/teams?link_id=3')

                assert resp.status == 422
                assert await resp.json() == "link_id does not exist"
