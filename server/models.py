import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


class BettingData:
    metadata = sa.MetaData()

    def __init__(self):
        self.link = self.link()
        self.real_team = self.real_team()
        self.team = self.team()

    @classmethod
    def link(cls):
        tb_link = sa.Table(
            'tb_link', cls.metadata,
            sa.Column('link_id', sa.Integer, primary_key=True),
            sa.Column('site_name', sa.String(25), nullable=False),
            sa.Column('link', sa.String(100), nullable=False, unique=True),
            sa.Column('created_on', sa.DateTime(), nullable=False),
            sa.Column('attributes', sa.JSON, nullable=False))

        return tb_link

    @classmethod
    def real_team(cls):
        tb_real_team = sa.Table(
            'tb_real_team', cls.metadata,
            sa.Column('real_team_id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(80), nullable=False, unique=True),
            sa.Column('created_on', sa.DateTime(), nullable=False))

        return tb_real_team

    @classmethod
    def team(cls):
        tb_team = sa.Table(
            'tb_team', cls.metadata,
            sa.Column('team_id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(80), nullable=False),
            sa.Column('created_on', sa.DateTime(), nullable=False),
            sa.Column('site_name', sa.String(25), nullable=False),
            sa.Column('real_team_id', sa.Integer, sa.ForeignKey('tb_real_team.real_team_id')),
            sa.Column('link_id', sa.Integer, sa.ForeignKey('tb_link.link_id')),
            sa.Column('status', postgresql.ENUM('new', 'moderated', 'approved', name='status_team')),
            sa.Column('process_instance_id', sa.String(40)))

        return tb_team


_BettingData = BettingData()
