import asyncio

import pytest
from sanic import Sanic
from sqlalchemy.schema import CreateTable, DropTable

from routes import add_routes
from engine import Connection, Engine
from models import tb_team, tb_real_team, tb_link


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "real_teams: real teams tests")
    config.addinivalue_line("markers", "teams: teams tests")
    config.addinivalue_line("markers", "change_status_team: change status team tests")


async def drop_tables():
    async with Connection() as conn:
        await conn.execute(DropTable(tb_team))
        await conn.execute(DropTable(tb_real_team))
        await conn.execute(DropTable(tb_link))
        await conn.execute("DROP TYPE status_team;")


async def create_tables():
    async with Connection() as conn:
        await conn.execute("CREATE TYPE status_team AS ENUM ('New', 'Moderated', 'Approved');")
        await conn.execute(CreateTable(tb_link))
        await conn.execute(CreateTable(tb_real_team))
        await conn.execute(CreateTable(tb_team))

        await conn.execute(tb_link.insert().values(site_name="bwin",
                                                   link="https://sports.bwin.com/en/sports",
                                                   created_on='2019-11-07T14:13:44.041152',
                                                   attributes={"elem": "a", "class": "js-mg-tooltip"},
                                                   type="team"))

        await conn.execute(tb_link.insert().values(site_name="UEFA",
                                                   link="https://en.competitions.uefa.com/"
                                                        "memberassociations/uefarankings/club"
                                                        "/libraries//years/2020/",
                                                   created_on='2019-11-07T14:13:44.041152',
                                                   attributes={"elem": "a",
                                                               "class": "team-name visible-md visible-lg"},
                                                   type="real_team"))


@pytest.fixture
def test_cli(loop, sanic_client):
    app = Sanic()
    add_routes(app)
    return loop.run_until_complete(sanic_client(app))


@pytest.fixture
async def tables(test_cli):
    await create_tables()

    yield

    await drop_tables()


@pytest.fixture
async def add_team(tables):
    async with Connection() as conn:
        await conn.execute(tb_team.insert().values(team_id="d2c0778d-14b3-c6b1-5a72-232c9b64b680", name="Chelsea",
                                                   created_on='2019-11-07T14:13:44.041152',
                                                   site_name="bwin", link_id=1, status="New"))


@pytest.fixture
async def add_team_with_moderated_status(tables):
    async with Connection() as conn:
        await conn.execute(tb_team.insert().values(team_id="d2c0778d-14b3-c6b1-5a72-232c9b64b680", name="Chelsea",
                                                   created_on='2019-11-07T14:13:44.041152',
                                                   site_name="bwin", link_id=1, status="Moderated"))


@pytest.fixture
async def add_real_team(tables):
    async with Connection() as conn:
        await conn.execute(tb_real_team.insert().values(name="Chelsea", created_on='2019-11-07T14:13:44.041152'))


@pytest.fixture
async def connection():
    await Engine.init()

    yield

    await Engine.close()


@pytest.fixture
async def mock_camunda_resp(test_cli):
    future = asyncio.Future()
    future.set_result(None)
    return future


@pytest.fixture
async def mock_parser_resp(test_cli):
    class Response:
        json = ["test_team_1", "test_team_2"]

    future = asyncio.Future()
    future.set_result(Response())

    return future
