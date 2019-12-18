from http import HTTPStatus

import pytest


@pytest.mark.real_teams
async def test_get_links(test_cli, tables):
    response_json = [{'link_id': 1, 'site_name': 'bwin', 'link': 'https://sports.bwin.com/en/sports',
                      'created_on': '2019-11-07T14:13:44.041152',
                      'attributes': {"elem": "a", "class": "js-mg-tooltip"}, 'type': 'team'},
                     {'link_id': 2, 'site_name': 'UEFA', 'link': 'https://en.competitions.uefa.com/'
                                                                 'memberassociations/uefarankings/'
                                                                 'club/libraries//years/2020/',
                      'created_on': '2019-11-07T14:13:44.041152',
                      'attributes': {"elem": "a", "class": "team-name visible-md visible-lg"}, 'type': 'real_team'}]

    resp = await test_cli.get('/links')
    assert resp.status == HTTPStatus.OK
    assert await resp.json() == response_json


@pytest.mark.real_teams
async def test_get_links_by_params(test_cli, tables):
    response_json = {'site_name': 'bwin'}

    resp = await test_cli.get('/links?fields=site_name&where=type:eq:team')
    assert resp.status == HTTPStatus.OK
    assert await resp.json() == response_json


@pytest.mark.real_teams
async def test_get_link_by_id(test_cli, tables):
    response_json = {'link_id': 2, 'site_name': 'UEFA', 'link': 'https://en.competitions.uefa.com/'
                                                                'memberassociations/uefarankings/'
                                                                'club/libraries//years/2020/',
                     'created_on': '2019-11-07T14:13:44.041152',
                     'attributes': {"elem": "a", "class": "team-name visible-md visible-lg"}, 'type': 'real_team'}

    resp = await test_cli.get('/links/2')
    assert resp.status == HTTPStatus.OK
    assert await resp.json() == response_json
