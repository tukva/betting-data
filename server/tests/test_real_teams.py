import pytest


@pytest.mark.real_teams
@pytest.mark.parser
async def test_get_real_teams(test_cli, add_real_team):
    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'real_team_id': 1, 'name': 'Chelsea', }]

    resp = await test_cli.get('/parse-links?parse_by=real_teams')
    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await test_cli.get('/parse-links/1?parse_by=real_teams')
    assert resp.status == 422
    assert await resp.json() == "Can not parse by link"


@pytest.mark.real_teams
@pytest.mark.parser
async def test_refresh_real_teams(test_cli, tables):
    resp = await test_cli.put('/parse-links?parse_by=real_teams')

    assert resp.status == 200
    assert await resp.json() == "Ok"

    resp = await test_cli.get('/parse-links/1?parse_by=real_teams')
    assert resp.status == 422
    assert await resp.json() == "Can not parse by link"
