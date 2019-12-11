from marshmallow import Schema, fields, validate


class TeamResponseSchema(Schema):
    team_id = fields.Int()
    name = fields.Str()
    created_on = fields.DateTime()
    site_name = fields.Str()
    real_team_id = fields.Int()
    link_id = fields.Int()
    status = fields.Str()


class ChangeStatusTeam(Schema):
    real_team_id = fields.Int()
    status = fields.Str(validate=validate.OneOf(["Moderated", "Approved"]), required=True)
