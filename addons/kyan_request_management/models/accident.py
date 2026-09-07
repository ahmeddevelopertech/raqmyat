from odoo import models, fields, api, _


class HrAccident(models.Model):
    _name = "hr.accident"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hr Accident"
    _order = "id desc"

    # name = fields.Char(default='New', readonly=True, copy=False)
    name = fields.Char(default=lambda self: _('New'), copy=False, readonly=True, tracking=True)
    incident_type = fields.Selection([('incident', 'Incident'), ('accident', 'Accident')], default='incident')
    occupation = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    department_id = fields.Many2one('hr.department')
    job_id = fields.Many2one('hr.job')
    date_of_accident = fields.Date(string="Date of Accident")
    date_of_incident = fields.Date(string="Date of Incident")
    time_location = fields.Char(string="Time and Exact Location")
    date_of_reporting = fields.Date(string="Date of Reporting")
    witnesses = fields.Text()
    type_of_injury = fields.Selection([('fatal', 'FATAL'), ('non_fatal', 'NON FATAL')], string="Type of Injury", default='non_fatal')
    hospital = fields.Char()
    date_of_resumption = fields.Date(string="Date Of Resumption")
    sick = fields.Char(string="Sick of Leave")
    wiba = fields.Text(string="WIBA Compensation")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel'), ], default='draft')
    hr_lines = fields.One2many("medical.report", "accident_id", string="Medical Reports")
    attachment_ids = fields.Many2many("ir.attachment")
    your_details = fields.Char()
    request_id = fields.Many2one('request.request')

    def button_confirm(self):
        self.state = 'confirm'

    def button_set_to_draft(self):
        self.state = 'draft'

    def button_cancel(self):
        self.state = 'cancel'

    @api.onchange('employee_id')
    def _onChangeEmployee(self):
        if self.employee_id:
            self.department_id = self.employee_id.department_id and self.employee_id.department_id.id
            self.job_id = self.employee_id.job_id and self.employee_id.job_id.id

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.accident') or ('New')
        return super(HrAccident, self).create(vals)

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', 'New') == 'New':
    #         vals['name'] = self.env['ir.sequence'].next_by_code('hr.accident') or 'New'
    #     return super(HrAccident, self).create(vals)

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the student model """
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hr.accident')
        return super().create(vals_list)


class MedicalReport(models.Model):
    _name = "medical.report"

    name = fields.Char()
    file = fields.Binary()
    accident_id = fields.Many2one("hr.accident", string="Accident")
