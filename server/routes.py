from listeners import acquire_con, close_con
from services.views.team import TeamDetailsView, TeamsView
from services.views.real_team import RealTeamsView


def add_routes(app):
    app.register_listener(acquire_con, "before_server_start")
    app.register_listener(close_con, "after_server_stop")

    app.add_route(RealTeamsView.as_view(), '/real-teams')

    app.add_route(TeamsView.as_view(), '/teams')
    app.add_route(TeamDetailsView.as_view(), '/teams/<team_id:int>')
