from datetime import datetime

import psycopg2
from common.rest_client.base_client_parser import BaseClientParser
from common.utils.camunda import Camunda

from models import tb_team, tb_real_team
from engine import Connection

client = BaseClientParser()


async def get_data(filter_data):
    async with Connection() as conn:
        select = await conn.execute(filter_data)
        data = await select.fetchone() if select.rowcount == 1 else await select.fetchall()
        return data


async def create_real_team(data):
    async with Connection() as conn:
        await conn.execute(tb_real_team.insert().values(**data))


async def update_real_team(real_team_id):
    async with Connection() as conn:
        await conn.execute(tb_real_team.update().where(tb_real_team.c.real_team_id == real_team_id).values(
            created_on=datetime.utcnow())
        )


async def create_or_update_team(process_definition_id, data):
    async with Connection() as conn:
        try:
            insert_tb_team = await conn.execute(tb_team.insert().values(**data))
            insert_team = await insert_tb_team.fetchone()
            await Camunda.start_process(process_definition_id, str(insert_team.team_id))
        except psycopg2.IntegrityError:
            await conn.execute(tb_team.update().values(created_on=datetime.utcnow()).where(
                tb_team.c.name == data["name"], tb_team.c.link_id == data["link_id"]))


async def update_team(team_id, **kwargs):
    async with Connection() as conn:
        await conn.execute(tb_team.update().values(**kwargs, created_on=datetime.utcnow()).where(
            tb_team.c.team_id == team_id))


async def real_team_exists(real_team_id):
    flag = False

    async with Connection() as conn:
        select_real_team = await conn.execute(tb_real_team.select().where(
            tb_real_team.c.real_team_id == real_team_id))

    if select_real_team.rowcount:
        flag = True

    return flag
