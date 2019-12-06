from datetime import datetime
from abc import ABC, abstractmethod

from sanic.log import logger
from sanic.response import json
from psycopg2 import DatabaseError
from sqlalchemy import and_
from common.rest_client.base_client_parser import BaseClientParser
from common.utils.camunda import Camunda, CamundaException

from models import _BettingData as Data
from services.forms import TeamResponseSchema

client = BaseClientParser()


class ByLink(ABC):

    @staticmethod
    @abstractmethod
    async def get(conn, link_id):
        pass

    @staticmethod
    @abstractmethod
    async def put(conn, link_id):
        pass


class ByAllLinks(ABC):

    @staticmethod
    @abstractmethod
    async def get(conn):
        pass

    @staticmethod
    @abstractmethod
    async def put(conn):
        pass


class TeamsByLink(ByLink):

    @staticmethod
    async def get(conn, link_id):
        teams = await conn.execute(Data.team.select().where(Data.team.c.link_id == link_id))
        result = await teams.fetchall()
        if not result:
            return json("Not Found", 404)
        res = TeamResponseSchema().dump(result, many=True)
        return json(res, 200)

    @staticmethod
    async def put(conn, link_id):
        select_tb_link = await conn.execute(Data.link.select().where(Data.link.c.link_id == link_id))
        link = await select_tb_link.fetchone()
        if not link or link.site_name == "UEFA":
            return json("Not Found", 404)

        resp = await client.parse_teams(link.link, link.attributes["cls"], link.attributes["elem"])
        teams = resp.json[0]

        for team in teams:
            select_tb_team = await conn.execute(Data.team.select().where(and_(
                Data.team.c.name == team,
                Data.team.c.link_id == link_id
            )))

            if select_tb_team.rowcount:
                await conn.execute(Data.team.update().where(and_(
                    Data.team.c.name == team, Data.team.c.link_id == link_id)).values(created_on=datetime.utcnow())
                )
            else:
                try:
                    await conn.execute(Data.team.insert().values(
                        name=team, site_name=link.site_name, created_on=datetime.utcnow(),
                        link_id=link_id, status="new", process_instance_id=await Camunda.init("BetAggr"))
                    )
                except CamundaException as e:
                    return json(e.args, 422)
        return json("Ok", 200)

    @staticmethod
    async def delete(conn, link_id):
        select_tb_link = await conn.execute(Data.link.select().where(Data.link.c.link_id == link_id))
        link = await select_tb_link.fetchone()
        if not link:
            return json("Not Found", 404)
        await conn.execute(Data.team.delete().where(Data.team.c.link_id == link_id))
        return json("Ok", 200)


class TeamsByAllLinks(ByAllLinks):

    @staticmethod
    async def get(conn):
        teams = await conn.execute(Data.team.select())
        res = TeamResponseSchema().dump(await teams.fetchall(), many=True)
        return json(res, 200)

    @staticmethod
    async def put(conn):
        select_tb_link = await conn.execute(Data.link.select())
        all_links = await select_tb_link.fetchall()
        for link in all_links:
            if not link or link.site_name == "UEFA":
                continue

            resp = await client.parse_teams(link.link, link.attributes["cls"], link.attributes["elem"])
            teams = resp.json[0]

            for team in teams:
                select_tb_team = await conn.execute(Data.team.select().where(and_(
                    Data.team.c.name == team,
                    Data.team.c.link_id == link.link_id
                )))

                if select_tb_team.rowcount:
                    await conn.execute(Data.team.update().where(and_(
                        Data.team.c.name == team, Data.team.c.link_id == link.link_id)).values(
                        created_on=datetime.utcnow())
                    )
                else:
                    try:
                        await conn.execute(Data.team.insert().values(
                            name=team, site_name=link.site_name, created_on=datetime.utcnow(),
                            link_id=link.link_id, status="new", process_instance_id=await Camunda.init("BetAggr"))
                        )
                    except CamundaException as e:
                        return json(e.args, 422)
        return json("Ok", 200)


class RealTeamsByAllLinks(ByAllLinks):

    @staticmethod
    async def get(conn):
        teams = await conn.execute(Data.real_team.select())
        res = TeamResponseSchema().dump(await teams.fetchall(), many=True)
        return json(res, 200)

    @staticmethod
    async def put(conn):
        select_tb_link = await conn.execute(Data.link.select().where(Data.link.c.site_name == 'UEFA'))
        link = await select_tb_link.fetchone()

        resp = await client.parse_teams(link.link, link.attributes["cls"], link.attributes["elem"])
        teams = resp.json[0]

        for team in teams:
            select_tb_team = await conn.execute(Data.real_team.select().where(
                Data.real_team.c.name == team
            ))

            if select_tb_team.rowcount:
                await conn.execute(Data.real_team.update().where(Data.real_team.c.name == team).values(
                    created_on=datetime.utcnow())
                )
            else:
                await conn.execute(Data.real_team.insert().values(
                    name=team, created_on=datetime.utcnow())
                )
        return json("Ok", 200)


async def set_real_team(conn, team_id, data):
    select_team = await conn.execute(Data.team.select().where(
        Data.team.c.team_id == team_id))

    if not select_team.rowcount:
        return json("Not Found", 404)

    team = await select_team.fetchone()
    if data["status"] == "moderated":
        if team.status != "new":
            return json("Current team status can not to moderate", 422)
        try:
            await Camunda.task_complete(team.process_instance_id, "New", True)
        except CamundaException as e:
            return json(e, 422)
        try:
            await conn.execute(Data.team.update().values(
                real_team_id=data["real_team_id"], status=data["status"]).where(
                Data.team.c.team_id == team_id))
        except DatabaseError as e:
            logger.error(f"DB Update error: {e}")
            return json("Bad request", 400)
    else:
        if team.status != "moderated":
            return json("Current team status can not to approve", 422)
        try:
            await Camunda.task_complete(team.process_instance_id, "Moderated", True)
        except CamundaException as e:
            return json(e, 422)
        await conn.execute(Data.team.update().values(status=data["status"]).where(
            Data.team.c.team_id == team_id))
    return json("Ok", 200)
