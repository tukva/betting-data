from engine import Engine


async def acquire_con(app, loop):
    await Engine.init()


async def close_con(app, loop):
    await Engine.close()
