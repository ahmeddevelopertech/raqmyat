# -*- coding: utf-8 -*-
import json
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class RestApiConnection(models.Model):
    _name = 'rest.api.connection'
    _description = 'Rest API Connection'

    name = fields.Char(string='Connection Name', required=True)
    server_url = fields.Char(string='Server URL', required=True, help="e.g. http://localhost")
    server_port = fields.Char(string='Server Port', default='8069')
    db_name = fields.Char(string='Database Name', required=True)
    db_username = fields.Char(string='Database Username', required=True)
    db_password = fields.Char(string='Database Password', required=True)  # Note: Will use password=True in view
    api_key = fields.Char(string='API Key', readonly=True)
    result = fields.Text(string='Result', readonly=True)

    def action_test_connection(self):
        self.ensure_one()
        url = f"{self.server_url}:{self.server_port}/odoo_connect"
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'db': self.db_name,
            'login': self.db_username,
            'password': self.db_password,
        }

        try:
            # Using POST as we are sending sensitive data in body and potentially creating a session/key resource
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                try:
                    data = response.json()
                    # The example response:
                    # {
                    # "Status": "auth successful",
                    # "User": "Administrator",
                    # "api-key": "..."
                    # }
                    if 'api-key' in data:
                        self.api_key = data['api-key']
                        self.result = "Connection Successful:\n" + json.dumps(data, indent=4)
                    else:
                        self.result = "Connection Failed (No API Key in response):\n" + response.text
                except ValueError:
                    self.result = "Connection Failed (Invalid JSON):\n" + response.text
            else:
                self.result = f"Connection Failed (Status {response.status_code}):\n" + response.text

        except requests.exceptions.RequestException as e:
            self.result = f"Connection Error:\n{str(e)}"

    # def action_test_connection(self):
    #     self.ensure_one()
    #
    #     url = f"{self.server_url}:{self.server_port}/odoo_connect"
    #
    #     payload = {
    #         'db': self.db_name,
    #         'login': self.db_username,
    #         'password': self.db_password,
    #     }
    #
    #     headers = {
    #         'Content-Type': 'application/json',
    #     }
    #
    #     try:
    #         response = requests.post(
    #             url,
    #             json={
    #                 "jsonrpc": "2.0",
    #                 "method": "call",
    #                 "params": {
    #                     "db": self.db_name,
    #                     "login": self.db_username,
    #                     "password": self.db_password,
    #                 }
    #             },
    #             headers={"Content-Type": "application/json"}
    #         )
    #
    #         if response.status_code == 200:
    #             data = response.json()
    #
    #             if data.get('status') == 'success' and data.get('api_key'):
    #                 self.api_key = data['api_key']
    #                 self.result = "Connection Successful:\n" + json.dumps(data, indent=4)
    #             else:
    #                 self.result = "Connection Failed:\n" + json.dumps(data, indent=4)
    #
    #         else:
    #             self.result = f"Connection Failed (Status {response.status_code}):\n{response.text}"
    #
    #     except requests.exceptions.RequestException as e:
    #         self.result = f"Connection Error:\n{str(e)}"
