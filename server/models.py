import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


metadata = sa.MetaData()


tb_link = sa.Table(
    'tb_link', metadata,
    sa.Column('link_id', sa.Integer, primary_key=True),
    sa.Column('site_name', sa.String(25), nullable=False),
    sa.Column('link', sa.String(100), nullable=False, unique=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('attributes', sa.JSON, nullable=False),
    sa.Column('type', sa.String(20), nullable=False))


tb_real_team = sa.Table(
    'tb_real_team', metadata,
    sa.Column('real_team_id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(80), nullable=False, unique=True),
    sa.Column('created_on', sa.DateTime(), nullable=False))


tb_team = sa.Table(
    'tb_team', metadata,
    sa.Column('team_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=True),
    sa.Column('name', sa.String(80), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('site_name', sa.String(25), nullable=False),
    sa.Column('real_team_id', sa.Integer, sa.ForeignKey('tb_real_team.real_team_id')),
    sa.Column('link_id', sa.Integer, sa.ForeignKey('tb_link.link_id')),
    sa.Column('status', postgresql.ENUM('New', 'Moderated', 'Approved', name='status_team')),
    sa.UniqueConstraint('name', 'link_id', name='uq_team_link'))
