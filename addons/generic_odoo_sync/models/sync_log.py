from odoo import models, fields

class SyncLog(models.Model):
    _name = "sync.log"
    _description = "Sync Log"
    _order = "create_date desc"

    model = fields.Char()
    record_id = fields.Integer()
    operation = fields.Selection([
        ("create", "Create"),
        ("write", "Write"),
        ("delete", "Delete")
    ])
    direction = fields.Selection([
        ("out", "Outgoing"),
        ("in", "Incoming")
    ])
    status = fields.Selection([
        ("success", "Success"),
        ("failed", "Failed")
    ])
    message = fields.Text()
    retry_count = fields.Integer(default=0)
