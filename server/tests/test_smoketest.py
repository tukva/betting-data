import pytest

from engine import Connection, Engine
from tests.conftest import create_tables, drop_tables


@pytest.mark.smoke
async def test_acquire_connection():
    await Engine.init()
    async with Connection():
        assert True
    await Engine.close()


@pytest.mark.smoke
async def test_close_connection():
    await Engine.init()
    await Engine.close()
    try:
        async with Connection():
            assert False
    except RuntimeError:
        assert True


@pytest.mark.smoke
async def test_create_drop_tables(connection):
    await create_tables()
    assert True

    await drop_tables()
    assert True


@pytest.mark.smoke
async def test_server(test_cli):
    await test_cli.get('/real-team')
    assert True
