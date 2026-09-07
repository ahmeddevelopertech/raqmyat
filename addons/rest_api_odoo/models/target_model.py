# -*- coding: utf-8 -*-
import json
import requests
from odoo import models, fields, api, _

class RestApiTargetModel(models.Model):
    _name = 'rest.api.target.model'
    _description = 'Rest API Target Model'

    name = fields.Char(string='Model Name', required=True, help="e.g. res.partner")
    selected_fields = fields.Char(string='Selected Fields', help='e.g. ["id", "name"]')
    method = fields.Selection([
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE')
    ], string='Method', required=True, default='GET')
    sync_interval = fields.Integer(string='Sync Interval') # Not sure how this is used yet, just adding field.
    connection_id = fields.Many2one('rest.api.connection', string='Connection', required=True)
    result = fields.Text(string='Result', readonly=True)

    rec_id = fields.Integer()
    # New fields for bidirectional support
    request_body = fields.Text(string='Request Payload (JSON)', default='{}', help='JSON body for POST/PUT requests (e.g. {"name": "New Partner"})')
    auto_sync = fields.Boolean(string='Sync/Save Received Data', help='If checked, data received from GET requests will be created locally.')
    unique_field = fields.Char(string='Unique Identifier Field', help="Field to check for duplicates (e.g. 'email' or 'ref'). If found, record will be updated instead of created.")

    def action_test_request(self):
        self.ensure_one()
        if not self.connection_id.api_key:
             self.result = "Error: Connection has no API Key. Please test connection first."
             return

        url = f"{self.connection_id.server_url}:{self.connection_id.server_port}/send_request"
        url_with_id = f"{self.connection_id.server_url}:{self.connection_id.server_port}/send_request/{self.rec_id}"
        headers = {
            'Content-Type': 'application/json',
            'api-key': self.connection_id.api_key,
            'login': self.connection_id.db_username,
            'password': self.connection_id.db_password,
        }

        params = {'model': self.name}
        data = {}
        
        # 1. Handle Fields Selection
        if self.selected_fields:
            try:
                fields_list = json.loads(self.selected_fields)
                data['fields'] = fields_list
            except:
                pass
        else:
             data['fields'] = []

        # 2. Handle Request Body (Payload)
        try:
            if self.request_body:
                body_json = json.loads(self.request_body)
                if 'values' not in body_json:
                    data['values'] = body_json
                else:
                    data.update(body_json)
        except Exception as e:
            self.result = f"Error parsing Request Payload: {str(e)}"
            return

        try:
            if self.method == 'GET':
                response = requests.get(url_with_id, headers=headers, params=params, json=data)
            elif self.method == 'POST':
                response = requests.post(url_with_id, headers=headers, params=params, json=data)
            elif self.method == 'PUT':
                 response = requests.put(url_with_id, headers=headers, params=params, json=data)
            elif self.method == 'DELETE':
                 response = requests.delete(url_with_id, headers=headers, params=params)

            if response.status_code == 200:
                self.result = "Request Successful:\n" + response.text
                
                # 3. Handle Auto Sync (Saving Data)
                try:
                    json_res = response.json()
                    self.result = "Request Successful:\n" + json.dumps(json_res, indent=4)
                    
                    if self.method == 'GET' and self.auto_sync:
                        if 'records' in json_res:
                            records = json_res['records']
                            created_count = 0
                            updated_count = 0
                            errors = []
                            
                            for rec in records:
                                # Clean system fields
                                clean_rec = {k: v for k, v in rec.items() if k not in ['id', 'create_uid', 'create_date', 'write_uid', 'write_date', '__last_update']}
                                
                                try:
                                    # Duplicate Prevention / Update Logic
                                    record_processed = False
                                    if self.unique_field and self.unique_field in clean_rec:
                                        unique_val = clean_rec[self.unique_field]
                                        # Search for existing record
                                        existing_rec = self.env[self.name].search([(self.unique_field, '=', unique_val)], limit=1)
                                        if existing_rec:
                                            existing_rec.write(clean_rec)
                                            updated_count += 1
                                            record_processed = True
                                    
                                    # If no unique field or record not found, Create
                                    if not record_processed:
                                        self.env[self.name].create(clean_rec)
                                        created_count += 1

                                except Exception as sync_err:
                                    errors.append(f"Failed to process record {rec.get('display_name', 'Unknown')}: {str(sync_err)}")
                            
                            self.result += f"\n\nSync Results:\nCreated: {created_count}\nUpdated: {updated_count}"
                            if errors:
                                self.result += "\nErrors:\n" + "\n".join(errors)

                except Exception as e:
                    self.result += f"\nWarning: Could not parse JSON or Sync data: {str(e)}"
            else:
                self.result = f"Request Failed (Status {response.status_code}):\n" + response.text

        except requests.exceptions.RequestException as e:
            self.result = f"Request Error:\n{str(e)}"
