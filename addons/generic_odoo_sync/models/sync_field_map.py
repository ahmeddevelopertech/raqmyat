# from odoo import models, fields
#
# class SyncFieldMap(models.Model):
#     _name = "sync.field.map"
#     _description = "Sync Field Mapping"
#     _order = "sequence,id"
#
#     config_id = fields.Many2one(
#         "sync.config",
#         ondelete="cascade",
#         required=True
#     )
#
#     field_id = fields.Many2one(
#         "ir.model.fields",
#         required=True,
#         domain="[('model_id','=', parent.model_id.id)]"
#     )
#
#     remote_field = fields.Char(
#         help="Remote field name (optional)"
#     )
#
#     sequence = fields.Integer(default=10)
#     active = fields.Boolean(default=True)


from odoo import models, fields

class SyncFieldMap(models.Model):
    _name = "sync.field.map"
    _description = "Sync Field Mapping"
    _order = "sequence,id"

    config_id = fields.Many2one(
        "sync.config",
        required=True,
        ondelete="cascade"
    )

    field_id = fields.Many2one(
        "ir.model.fields",
        required=True,
        ondelete="cascade",
        domain="[('model_id','=', parent.model_id)]"
    )

    remote_field = fields.Char(
        help="Remote field name (optional)"
    )

    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
