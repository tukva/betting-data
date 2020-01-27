import aiopg.sa

from config import url, DB_POOL_SIZE_MIN, DB_POOL_SIZE_MAX


class Engine:
    _engine = None

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    async def init(cls):
        cls._engine = await aiopg.sa.create_engine(url,
                                                   minsize=DB_POOL_SIZE_MIN,
                                                   maxsize=DB_POOL_SIZE_MAX)

    @classmethod
    async def acquire(cls):
        return await cls._engine.acquire()

    @classmethod
    async def close(cls):
        cls._engine.close()
        await cls._engine.wait_closed()

    @classmethod
    async def release(cls, connection):
        await  cls._engine.release(connection)


class Connection:
    __slots__ = ('_connection',)

    def __init__(self):
        self._connection = None

    async def __aenter__(self):
        self._connection = await Engine.acquire()
        return self

    async def __aexit__(self, typ, val, trb):
        await Engine.release(self._connection)

    async def execute(self, statement):
        return await self._connection.execute(statement)
