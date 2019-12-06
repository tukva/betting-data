import pytest
from unittest import mock

from common.utils.camunda import Camunda


@pytest.mark.change_status_team
async def test_change_status_team_in_moderated(test_cli, mock_camunda_resp, add_team, add_real_team):
    resp = await test_cli.patch('/change-status-team/1', json={"real_team_id": 1, "status": "approved"})

    assert resp.status == 422
    assert await resp.json() == "Current team status can not to approve"

    resp = await test_cli.patch('/change-status-team/1', json={"real_team_id": 1, "status": "wrong_value"})

    assert resp.status == 422
    assert await resp.json() == {'status': ["Must be one of: moderated, approved."]}

    resp = await test_cli.patch('/change-status-team/1', json={"real_team_id": 1, "wrong_key": "moderated"})

    assert resp.status == 422
    assert await resp.json() == {'wrong_key': ['Unknown field.']}

    resp = await test_cli.patch('/change-status-team/2', json={"real_team_id": 1, "status": "moderated"})

    assert resp.status == 404
    assert await resp.json() == "Not Found"

    resp = await test_cli.patch('/change-status-team/1')

    assert resp.status == 422
    assert await resp.json() == {'_schema': ['Invalid input type.']}

    with mock.patch.object(Camunda, 'task_complete', return_value=mock_camunda_resp):
        resp = await test_cli.patch('/change-status-team/1', json={"real_team_id": 1, "status": "moderated"})

        assert resp.status == 200


@pytest.mark.change_status_team
async def test_change_status_team_in_approved(test_cli, mock_camunda_resp, add_team_with_moderated_status, add_real_team):
    resp = await test_cli.patch('/change-status-team/1', json={"real_team_id": 1, "status": "moderated"})

    assert resp.status == 422
    assert await resp.json() == "Current team status can not to moderate"

    resp = await test_cli.patch('/change-status-team/2', json={"real_team_id": 1, "status": "approved"})

    assert resp.status == 404
    assert await resp.json() == "Not Found"

    resp = await test_cli.patch('/change-status-team/1')

    assert resp.status == 422
    assert await resp.json() == {'_schema': ['Invalid input type.']}

    with mock.patch.object(Camunda, 'task_complete', return_value=mock_camunda_resp):
        resp = await test_cli.patch('/change-status-team/1', json={"real_team_id": 1, "status": "approved"})

        assert resp.status == 200
