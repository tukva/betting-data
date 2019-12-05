import pytest

from services.decorators import VALID_PARSER_BY_FIELDS


@pytest.mark.parse_links
@pytest.mark.parser
async def test_get_teams_by_all_link(test_cli, add_team):
    resp = await test_cli.get('/parse-links?parse_by=teams')

    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'link_id': 1, 'team_id': 1,
                      'name': 'Chelsea', 'real_team_id': None, 'site_name': 'bwin', 'status': 'new',
                      'process_instance_id': None}]

    assert resp.status == 200
    assert await resp.json() == response_json


@pytest.mark.parse_links
@pytest.mark.parser
async def test_get_teams_by_link(test_cli, add_team):
    resp = await test_cli.get('/parse-links/1?parse_by=teams')

    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'link_id': 1, 'team_id': 1,
                      'name': 'Chelsea', 'real_team_id': None, 'site_name': 'bwin',
                      'status': 'new', 'process_instance_id': None}]

    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await test_cli.get('/parse-links/3?parse_by=teams')

    assert resp.status == 404
    assert await resp.json() == "Not Found"


@pytest.mark.parse_links
@pytest.mark.parser
async def test_refresh_teams_by_link(test_cli, tables):
    resp = await test_cli.put('/parse-links/1?parse_by=teams')

    assert resp.status == 200
    assert await resp.json() == "Ok"

    resp = await test_cli.put('/parse-links/3?parse_by=teams')

    assert resp.status == 404
    assert await resp.json() == "Not Found"


@pytest.mark.parse_links
@pytest.mark.parser
async def test_delete_teams_by_link(test_cli, add_team):
    resp = await test_cli.put('/parse-links/1?parse_by=teams')

    assert resp.status == 200
    assert await resp.json() == "Ok"

    resp = await test_cli.put('/parse-links/3?parse_by=teams')

    assert resp.status == 404
    assert await resp.json() == "Not Found"


async def test_wrong_parameters_by(test_cli, add_team):
    resp = await test_cli.get('/parse-links')

    assert resp.status == 200
    assert await resp.json() == "Type the parse_by parameter if you want to parse something"

    resp = await test_cli.get('/parse-links?parse_by=wrong_value')

    assert resp.status == 422
    assert await resp.json() == f"Can not parse by 'wrong_value'. Valid values: " \
                                f"{[field.name for field in VALID_PARSER_BY_FIELDS]}"
