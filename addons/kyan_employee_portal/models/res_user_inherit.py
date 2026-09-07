from odoo import models,fields, api

class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    is_customer = fields.Boolean(string='Is Customer', default=False)


