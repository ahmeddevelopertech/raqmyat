from odoo import models

class SyncMixin(models.AbstractModel):
    _name = "sync.mixin"
    _description = "Generic Sync Mixin"

    # -----------------
    # CREATE
    # -----------------
    @classmethod
    def create(cls, vals_list):
        records = super().create(vals_list)

        # منع loop
        if cls.env.context.get("skip_sync"):
            return records

        for rec in records:
            rec.env["sync.engine"].sync_record(rec, "create")

        return records

    # -----------------
    # WRITE
    # -----------------
    def write(self, vals):
        res = super().write(vals)

        if self.env.context.get("skip_sync"):
            return res

        for rec in self:
            rec.env["sync.engine"].sync_record(rec, "write")

        return res

    # -----------------
    # DELETE
    # -----------------
    def unlink(self):
        if not self.env.context.get("skip_sync"):
            for rec in self:
                rec.env["sync.engine"].sync_record(rec, "delete")

        return super().unlink()
