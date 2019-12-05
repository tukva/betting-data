from datetime import datetime
import asyncio

import pytest
from sanic import Sanic
from sqlalchemy.schema import CreateTable, DropTable

from routes import add_routes
from engine import Connection, Engine
from models import _Parser as Parser


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "parser: parser tests")
    config.addinivalue_line("markers", "real_teams: real teams tests")
    config.addinivalue_line("markers", "parse_links: parse links tests")
    config.addinivalue_line("markers", "change_status_team: change status team tests")


async def drop_tables():
    async with Connection() as conn:
        await conn.execute(DropTable(Parser.team))
        await conn.execute(DropTable(Parser.real_team))
        await conn.execute(DropTable(Parser.link))
        await conn.execute("DROP TYPE status_team;")


async def create_tables():
    async with Connection() as conn:
        await conn.execute("CREATE TYPE status_team AS ENUM ('new', 'moderated', 'approved');")
        await conn.execute(CreateTable(Parser.link))
        await conn.execute(CreateTable(Parser.real_team))
        await conn.execute(CreateTable(Parser.team))

        await conn.execute(Parser.link.insert().values(site_name="bwin",
                                                       link="https://sports.bwin.com/en/sports",
                                                       created_on=datetime.utcnow(),
                                                       attributes={"elem": "a", "cls": "js-mg-tooltip"}))

        await conn.execute(Parser.link.insert().values(site_name="UEFA",
                                                       link="https://en.competitions.uefa.com/"
                                                            "memberassociations/uefarankings/club"
                                                            "/libraries//years/2020/",
                                                       created_on=datetime.utcnow(),
                                                       attributes={"elem": "a",
                                                                   "cls": "team-name visible-md visible-lg"}))


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
        await conn.execute(Parser.team.insert().values(name="Chelsea", created_on='2019-11-07T14:13:44.041152',
                                                       site_name="bwin", link_id=1, status="new"))


@pytest.fixture
async def add_team_with_moderated_status(tables):
    async with Connection() as conn:
        await conn.execute(Parser.team.insert().values(name="Chelsea", created_on='2019-11-07T14:13:44.041152',
                                                       site_name="bwin", link_id=1, status="moderated"))


@pytest.fixture
async def add_real_team(tables):
    async with Connection() as conn:
        await conn.execute(Parser.real_team.insert().values(name="Chelsea", created_on='2019-11-07T14:13:44.041152'))


@pytest.fixture
async def connection():
    await Engine.init()

    yield

    await Engine.close()


@pytest.fixture
async def mock_resp(test_cli):
    future = asyncio.Future()
    future.set_result(None)
    return future
