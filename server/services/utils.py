from datetime import datetime

import psycopg2
from sqlalchemy import and_
from common.rest_client.base_client_parser import BaseClientParser
from common.utils.camunda import Camunda

from models import tb_team, tb_real_team, tb_link
from constants import StatusTeam
from engine import Connection

client = BaseClientParser()


async def get_data(filter_data):
    async with Connection() as conn:
        select = await conn.execute(filter_data)
        data = await select.fetchone() if select.rowcount == 1 else await select.fetchall()
        return data


async def create_or_update_real_team(data):
    async with Connection() as conn:
        try:
            await conn.execute(tb_real_team.insert().values(**data))
        except psycopg2.IntegrityError:
            await conn.execute(tb_real_team.update().where(tb_real_team.c.name == data["name"]).values(
                created_on=datetime.utcnow())
            )


async def create_or_update_team(process_definition_id, data):
    async with Connection() as conn:
        try:
            insert_team = await conn.execute(tb_team.insert().values(
                **data, status=StatusTeam.NEW).returning(tb_team.c.team_id))
            team_id = await insert_team.fetchone()
            await Camunda.start_process(process_definition_id, str(team_id[0]))
        except psycopg2.errors.UniqueViolation:
            await conn.execute(tb_team.update().values(created_on=datetime.utcnow()).where(and_(
                tb_team.c.name == data["name"], tb_team.c.link_id == data["link_id"])))


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


async def link_exists(link_id):
    flag = False

    async with Connection() as conn:
        select_link = await conn.execute(tb_link.select().where(
            tb_link.c.link_id == link_id))

    if select_link.rowcount:
        flag = True

    return flag
