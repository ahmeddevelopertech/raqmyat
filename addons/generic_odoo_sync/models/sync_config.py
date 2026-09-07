# from odoo import models, fields
#
# class SyncConfig(models.Model):
#     _name = "sync.config"
#     _description = "Sync Configuration"
#
#     name = fields.Char(required=True)
#     active = fields.Boolean(default=True)
#
#     model_id = fields.Many2one(
#         "ir.model",
#         string="Model",
#         required=True,
#         ondelete="cascade"
#     )
#
#     sync_create = fields.Boolean(default=True)
#     sync_write = fields.Boolean(default=True)
#     sync_delete = fields.Boolean(default=False)
#
#     remote_url = fields.Char(required=True)
#     api_key = fields.Char(required=True)
#
#     field_map_ids = fields.One2many(
#         "sync.field.map",
#         "config_id",
#         string="Field Mapping"
#     )

from odoo import models, fields

class SyncConfig(models.Model):
    _name = "sync.config"
    _description = "Sync Configuration"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        ondelete="cascade"
    )

    sync_create = fields.Boolean(default=True)
    sync_write = fields.Boolean(default=True)
    sync_delete = fields.Boolean(default=False)

    remote_url = fields.Char(required=True)
    api_key = fields.Char(required=True)

    field_map_ids = fields.One2many(
        "sync.field.map",
        "config_id",
        string="Field Mapping"
    )
