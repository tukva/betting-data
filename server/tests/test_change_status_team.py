from http import HTTPStatus
from unittest import mock

import pytest

from common.utils.camunda import Camunda


@pytest.mark.change_status_team
async def test_change_status_team_in_moderated(test_cli, mock_camunda_resp, add_team, add_real_team):
    with mock.patch.object(Camunda, 'task_complete', return_value=mock_camunda_resp):
        resp = await test_cli.patch('/teams/d2c0778d-14b3-c6b1-5a72-232c9b64b680',
                                    json={"real_team_id": 3, "status": "Moderated"})

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert await resp.json() == "real_id does not exist"

        resp = await test_cli.patch('/teams/d2c0778d-14b3-c6b1-5a72-232c9b64b680',
                                    json={"real_team_id": 1, "status": "wrong_value"})

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert await resp.json() == {'status': ["Must be one of: Moderated, Approved."]}

        resp = await test_cli.patch('/teams/d2c0778d-14b3-c6b1-5a72-232c9b64b680',
                                    json={"real_team_id": 1, "wrong_key": "Moderated"})

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert await resp.json() == {'status': ['Missing data for required field.'], 'wrong_key': ['Unknown field.']}

        resp = await test_cli.patch('/teams/d2c0778d-14b3-c6b1-5a72-232c9b64b680')

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert await resp.json() == {'_schema': ['Invalid input type.']}

        resp = await test_cli.patch('/teams/d2c0778d-14b3-c6b1-5a72-232c9b64b680',
                                    json={"real_team_id": 1, "status": "Moderated"})

        assert resp.status == HTTPStatus.OK


@pytest.mark.change_status_team
async def test_change_status_team_in_approved(test_cli, mock_camunda_resp,
                                              add_team_with_moderated_status,
                                              add_real_team):
    with mock.patch.object(Camunda, 'task_complete', return_value=mock_camunda_resp):
        resp = await test_cli.patch('/teams/d2c0778d-14b3-c6b1-5a72-232c9b64b680')

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert await resp.json() == {'_schema': ['Invalid input type.']}

        resp = await test_cli.patch('/teams/d2c0778d-14b3-c6b1-5a72-232c9b64b680', json={"status": "Approved"})

        assert resp.status == HTTPStatus.OK
