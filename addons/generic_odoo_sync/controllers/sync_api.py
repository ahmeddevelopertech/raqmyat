from odoo import http
from odoo.http import request

class SyncAPI(http.Controller):

    @http.route("/api/sync/receive", type="json", auth="none", csrf=False)
    def receive(self, **payload):
        model = payload["model"]
        operation = payload["operation"]
        data = payload["data"]
        external_id = str(payload["external_id"])

        Model = request.env[model].sudo()

        mapping = request.env["sync.external.map"].sudo().search([
            ("model", "=", model),
            ("remote_id", "=", external_id)
        ], limit=1)

        if operation in ("create", "write"):
            if mapping:
                Model.browse(mapping.local_id).write(data)
            else:
                record = Model.create(data)
                request.env["sync.external.map"].sudo().create({
                    "model": model,
                    "local_id": record.id,
                    "remote_id": external_id,
                    "system": "remote"
                })

        elif operation == "delete" and mapping:
            Model.browse(mapping.local_id).unlink()

        request.env["sync.log"].sudo().create({
            "model": model,
            "record_id": external_id,
            "operation": operation,
            "direction": "in",
            "status": "success"
        })

        return {"status": "ok"}
