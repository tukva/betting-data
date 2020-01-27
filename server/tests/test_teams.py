from http import HTTPStatus
from unittest import mock

import pytest

from common.utils.camunda import Camunda


@pytest.mark.teams
async def test_get_teams(test_cli, add_team):
    resp = await test_cli.get('/teams')

    response_json = {'created_on': '2019-11-07T14:13:44.041152', 'link_id': 1,
                     'team_id': 'd2c0778d-14b3-c6b1-5a72-232c9b64b680',
                     'name': 'Chelsea', 'real_team_id': None, 'site_name': 'bwin', 'status': 'New'}

    assert resp.status == HTTPStatus.OK
    assert await resp.json() == response_json


@pytest.mark.teams
async def test_get_teams_by_params(test_cli, add_team):
    response_json = {'name': 'Chelsea'}

    resp = await test_cli.get('/teams?fields=name&where=link_id:eq:1')

    assert resp.status == HTTPStatus.OK
    assert await resp.json() == response_json

    resp = await test_cli.get('/teams?where=link_id:eq:3')

    assert resp.status == HTTPStatus.OK
    assert await resp.json() == []


@pytest.mark.teams
async def test_create_or_update_teams(test_cli, mock_parser_resp, mock_camunda_resp, tables):
    with mock.patch.object(Camunda, 'get_process_definition_id', return_value=mock_camunda_resp):
        with mock.patch.object(Camunda, 'start_process', return_value=mock_camunda_resp):
            json = {"site_name": "bwin", "link_id": 1, "name": "Chelsea"}
            resp = await test_cli.post('/teams', json=json)

            assert resp.status == HTTPStatus.OK
            assert await resp.json() == "OK"

            resp = await test_cli.post('/teams', json=json)

            assert resp.status == HTTPStatus.OK
            assert await resp.json() == "OK"

            json = {"site_name": "bwin", "link_id": 3, "name": "Chelsea"}
            resp = await test_cli.post('/teams', json=json)

            assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
            assert await resp.json() == "link_id does not exist"
