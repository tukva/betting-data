from listeners import acquire_con, close_con
from services.views.link import LinkView, AllLinksView
from services.views.change_status_team import change_status_team


def add_routes(app):
    app.register_listener(acquire_con, "before_server_start")
    app.register_listener(close_con, "after_server_stop")

    app.add_route(AllLinksView.as_view(), '/links')
    app.add_route(LinkView.as_view(), '/links/<link_id:int>')

    app.add_route(change_status_team, '/change-status-team/<team_id:int>', methods=["PATCH"])
