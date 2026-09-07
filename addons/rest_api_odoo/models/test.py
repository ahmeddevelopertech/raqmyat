import json

import logging

from odoo import http

from odoo.http import request

from odoo import fields, models

import requests


# _logger = logging.getLogger(__name__)


class AttendanceSync(models.Model):
    _name = 'attendance.api'

    _description = "Motabaqah attendace API"

    name = fields.Char(string="API name")

    db_url = fields.Char(string="URL")

    db_port = fields.Integer(string="Port")

    db_name = fields.Char(string="Database Name")

    db_username = fields.Char(string="Database Username")

    db_password = fields.Char(string="Database Password")

    api_key = fields.Char(string="API Key")

    target_model = fields.Many2one('ir.model', string="Model",

                                   help="Select model which can be accessed by "

                                        "REST api requests.")

    call_method = fields.Selection([('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')])

    data = fields.Html('Data from Target')

    fields = fields.One2many()

    def odoo_connect(self):
        """This is the controller which initializes the api transaction by

        generating the api-key for specific user and database"""

        payload = {}

        headers2 = {

            'db': self.db_name,

            'login': self.db_username,

            'password': self.db_password,

            'api-key': self.api_key

        }

        url = f"{self.db_url}:{self.db_port}/odoo_connect"

        response_session_id = requests.request("GET", url, headers=headers2, data=payload)

        r_session_id = response_session_id.cookies["session_id"]

        print(response_session_id.text)

        print(r_session_id)

        headers = {

            'db': self.db_name,

            'login': self.db_username,

            'password': self.db_password,

            'api-key': self.api_key,

            'Cookie': f"session_id={r_session_id}"

        }

        response_auth = requests.request("GET", url, headers=headers, data=payload)

        session_id = response_auth.cookies["session_id"]

        print(response_auth.text)

        URL = self.db_url

        # URL = http://cybrosys:8016/odoo_connect

        connect_url = f"{self.db_url}:{self.db_port}/send_request?model={self.target_model.model}"

        print(connect_url)

        print(self.target_model.model)

        # print('%s:%s/odoo_connect' % (self.db_url, self.db_port))

        url = connect_url

        payload2 = json.dumps({

            "fields": [

                "id",

                "name",

                "mobile"

            ]

        })

        headers3 = {

            'login': self.db_username,

            'password': self.db_password,

            'api-key': self.api_key,

            'Content-Type': 'application/json',

            'Cookie': f"session_id={session_id}"

        }

        response = requests.request("GET", url, headers=headers3, data=payload2)

        print(response.text)

        # print(response.text)

        data = response.text

        print(session_id)

        self.data = response.text

        data_in_model = f"{self.target_model.model}"

        print('dfsdfsjdfkljslkfjsdkljfklsdjl')

        print(data_in_model)

        for record in data:
            print(record.get('name'))

            print(record.get('id'))

            self.env[data_in_model].sudo().create(data)

