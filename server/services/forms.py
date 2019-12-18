from marshmallow import Schema, fields, validate


class TeamResponseSchema(Schema):
    team_id = fields.UUID()
    name = fields.Str()
    created_on = fields.DateTime()
    site_name = fields.Str()
    real_team_id = fields.Int()
    link_id = fields.Int()
    status = fields.Str()


class LinkResponseSchema(Schema):
    link_id = fields.Int()
    site_name = fields.Str()
    link = fields.Str()
    created_on = fields.DateTime()
    attributes = fields.Dict()
    type = fields.Str()


class CreateTeamSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=80), required=True, nullable=False)
    site_name = fields.Str(validate=validate.Length(min=2, max=25), required=True, nullable=False)
    link_id = fields.Int(required=True, nullable=False)


class CreateRealTeamSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=80), required=True, nullable=False)


class ChangeStatusTeam(Schema):
    real_team_id = fields.Int()
    status = fields.Str(validate=validate.OneOf(["Moderated", "Approved"]), required=True)
