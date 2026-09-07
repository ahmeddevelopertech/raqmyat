from odoo import models, fields

class SyncExternalMap(models.Model):
    _name = "sync.external.map"
    _description = "External Record Mapping"

    model = fields.Char(required=True)
    local_id = fields.Integer(required=True)
    remote_id = fields.Char(required=True)
    system = fields.Char(required=True)

    _sql_constraints = [
        ("uniq_map", "unique(model, system, local_id)", "Already mapped!")
    ]
