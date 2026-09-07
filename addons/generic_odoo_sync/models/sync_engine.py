import requests
from odoo import models, api

class SyncEngine(models.AbstractModel):
    _name = "sync.engine"
    _description = "Generic Sync Engine"

    @api.model
    def _prepare_payload(self, record, config):
        data = {}
        for fmap in config.field_map_ids.filtered("active"):
            local = fmap.field_id.name
            remote = fmap.remote_field or local
            data[remote] = record[local]
        return data

    @api.model
    def sync_record(self, record, operation):
        configs = self.env["sync.config"].search([
            ("model_id.model", "=", record._name),
            ("active", "=", True)
        ])

        for config in configs:
            if not getattr(config, f"sync_{operation}"):
                continue

            payload = {
                "model": record._name,
                "operation": operation,
                "external_id": record.id,
                "data": self._prepare_payload(record, config)
            }

            try:
                r = requests.post(
                    f"{config.remote_url}/api/sync/receive",
                    json=payload,
                    headers={"api-key": config.api_key},
                    timeout=20
                )
                r.raise_for_status()

                self.env["sync.log"].create({
                    "model": record._name,
                    "record_id": record.id,
                    "operation": operation,
                    "direction": "out",
                    "status": "success"
                })

            except Exception as e:
                self.env["sync.log"].create({
                    "model": record._name,
                    "record_id": record.id,
                    "operation": operation,
                    "direction": "out",
                    "status": "failed",
                    "message": str(e)
                })
