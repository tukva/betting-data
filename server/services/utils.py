from datetime import datetime

from sqlalchemy import and_
from common.rest_client.base_client_parser import BaseClientParser
from common.utils.camunda import Camunda

from models import tb_team, tb_real_team, tb_link
from engine import Connection
from settings import StatusTeam

client = BaseClientParser()


async def get_real_teams():
    async with Connection() as conn:
        select_real_teams = await conn.execute(tb_real_team.select())

        real_teams = await select_real_teams.fetchall()
        return real_teams


async def get_teams():
    async with Connection() as conn:
        select_teams = await conn.execute(tb_team.select())

        teams = await select_teams.fetchall()
        return teams


async def get_team_by_id(team_id):
    async with Connection() as conn:
        select_team = await conn.execute(tb_team.select().where(
            tb_team.c.team_id == team_id))

        team = await select_team.fetchone()
        return team


async def get_teams_by_link_id(link_id):
    async with Connection() as conn:
        select_teams = await conn.execute(tb_team.select().where(tb_team.c.link_id == link_id))
        teams = await select_teams.fetchall()
        return teams


async def get_links(type_link):
    async with Connection() as conn:
        select_tb_link = await conn.execute(tb_link.select().where(tb_link.c.type == type_link))
        link = await select_tb_link.fetchall()
        return link


async def get_link_by_id(link_id, type_link):
    async with Connection() as conn:
        select_tb_link = await conn.execute(tb_link.select().where(and_(tb_link.c.link_id == link_id,
                                                                        tb_link.c.type == type_link)))
        link = await select_tb_link.fetchone()
        return link


async def put_real_teams_by_link(conn, link):
    resp = await client.parse_teams(link.link, link.attributes["class"], link.attributes["elem"])
    teams = resp.json

    for team in teams:
        select_tb_team = await conn.execute(tb_real_team.select().where(
            tb_real_team.c.name == team
        ))

        if select_tb_team.rowcount:
            await conn.execute(tb_real_team.update().where(tb_real_team.c.name == team).values(
                created_on=datetime.utcnow())
            )
        else:
            await conn.execute(tb_real_team.insert().values(
                name=team, created_on=datetime.utcnow())
            )


async def put_teams_by_link(conn, link, process_definition_id):
    resp = await client.parse_teams(link.link, link.attributes["class"], link.attributes["elem"])
    teams = resp.json

    for team in teams:
        select_tb_team = await conn.execute(tb_team.select().where(and_(
            tb_team.c.name == team,
            tb_team.c.link_id == link.link_id
        )))

        if select_tb_team.rowcount:
            await conn.execute(tb_team.update().where(and_(
                tb_team.c.name == team, tb_team.c.link_id == link.link_id)).values(
                created_on=datetime.utcnow())
            )
        else:
            insert_tb_team = await conn.execute(tb_team.insert().values(
                name=team, site_name=link.site_name, created_on=datetime.utcnow(),
                link_id=link.link_id, status=StatusTeam.NEW)
            )
            insert_team = await insert_tb_team.fetchone()
            await Camunda.start_process(process_definition_id, insert_team.team_id)


async def moderate_team(team_id, real_team_id, status):
    async with Connection() as conn:
        await conn.execute(tb_team.update().values(
            real_team_id=real_team_id, status=status).where(
            tb_team.c.team_id == team_id))


async def approve_team(team_id, status):
    async with Connection() as conn:
        await conn.execute(tb_team.update().values(
            status=status).where(
            tb_team.c.team_id == team_id))
