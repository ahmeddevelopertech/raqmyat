from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError, UserError

class HrRequest(models.Model):
    _name = "request.request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hr Accident"
    _order = "id desc"
    _rec_name = "sequence_name"

    sequence_name = fields.Char(default='New', readonly=True,copy=False)
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'), ('approve','Approve'), ('cancel','Cancel')], default='draft')
    employee_id = fields.Many2one('hr.employee')
    department_id = fields.Many2one('hr.department')
    job_id = fields.Many2one('hr.job')
    reqest_date = fields.Date(string="Request Date", default=date.today())
    description = fields.Text(string="Description")
    type_id = fields.Many2one('hr.request.type', string="Request Type")
    amount = fields.Float()
    types = fields.Selection(related='type_id.types')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    
    leave_count = fields.Integer(compute='_compute_leave')
    loan_count = fields.Integer(compute='_compute_loan')
    advnc_slry_count = fields.Integer(compute='_compute_advnc_slry')
    expense_count = fields.Integer(compute='_compute_expense')
    accident_count = fields.Integer(compute='_compute_accident')
    incident_count = fields.Integer(compute='_compute_incident')
    your_details = fields.Char()

# ===== state button =====

    def action_leave(self):
        self.ensure_one()
        return {
            'name': 'Leaves',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.leave',
            'domain': [('request_id', '=', self.id)],
        }

    def action_loan(self):
        self.ensure_one()
        return {
            'name': 'Loan',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.loan',
            'domain': [('request_id', '=', self.id), ('types', '=', 'loan')],
        }

    def action_advance_slry(self):
        self.ensure_one()
        return {
            'name': 'Advance Salary',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.loan',
            'domain': [('request_id', '=', self.id), ('types', '=', 'salary_advance')],
        }

    def action_expense(self):
        self.ensure_one()
        return {
            'name': 'Expenses',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.expense',
            'domain': [('request_id', '=', self.id)],
        }

    def action_accident(self):
        self.ensure_one()
        return {
            'name': 'Accident',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.accident',
            'domain': [('request_id', '=', self.id)],
        }

    def action_incident(self):
        self.ensure_one()
        return {
            'name': 'Incident',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.accident',
            'domain': [('request_id', '=', self.id)],
        }

# ===== compute count =====

    @api.depends('employee_id')
    def _compute_leave(self):
        self.leave_count = self.env['hr.leave'].search_count([('request_id','=',self.id)])

    @api.depends('employee_id')
    def _compute_expense(self):
        self.expense_count = self.env['hr.expense'].search_count([('request_id','=',self.id)])

    @api.depends('employee_id')
    def _compute_accident(self):
        self.accident_count = self.env['hr.accident'].search_count([('request_id','=',self.id)])

    @api.depends('employee_id')
    def _compute_incident(self):
        self.incident_count = self.env['hr.accident'].search_count([('request_id','=',self.id)])

    @api.depends('employee_id')
    def _compute_loan(self):
        self.loan_count = self.env['hr.loan'].search_count([('request_id','=',self.id)])

    @api.depends('employee_id')
    def _compute_advnc_slry(self):
        self.advnc_slry_count = self.env['hr.loan'].search_count([('request_id','=',self.id)])

# ===== header button =====

    def button_confirm(self):
        if self.types == 'loan' or self.types == 'advance_salary':
            if self.amount == 0 and self.amount == 0.00:
                raise ValidationError(_("The amount is zero. Please enter amount. "))
        self.state = 'confirm'

    def button_approve(self):
        self.state = 'approve'

    def button_cancel(self):
        self.state = 'cancel'

    def button_draft(self):
        self.state = 'draft'

    def button_req_loan(self):
        vals = {
            'employee_id': self.employee_id.id,
            'loan_amount': self.amount,
            'types': 'loan',
            'request_id': self.id,
        }
        res = self.env['hr.loan'].search([]).create(vals)
        return res

    def button_advnc_slry(self):
        vals = {
            'employee_id': self.employee_id.id,
            'loan_amount': self.amount,
            'types': 'salary_advance',
            'request_id': self.id,
        }
        res = self.env['hr.loan'].search([]).create(vals)
        return res

    def button_expense(self):
        vals = {
                'name': 'Expens Wizard',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'expense.wizard',
                'target': 'new',
            }
        return vals

    def button_accident(self):
        accident_model = self.env['hr.accident']
        accident_data = {
            'employee_id': self.employee_id.id,
            'department_id': self.department_id.id,
            'job_id': self.job_id.id,
            'request_id': self.id,
            'your_details': self.your_details or False,
            'incident_type':'accident',
        }
        new_accident = accident_model.create(accident_data)
        return {
            'name': 'Accident',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.accident',
            'res_id': new_accident.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def button_incident(self):
        accident_model = self.env['hr.accident']
        accident_data = {
            'employee_id': self.employee_id.id,
            'department_id': self.department_id.id,
            'job_id': self.job_id.id,
            'request_id': self.id,
            'your_details': self.your_details or False,
            'incident_type':'incident',
        }
        new_accident = accident_model.create(accident_data)
        return {
            'name': 'Incident',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.accident',
            'res_id': new_accident.id,
            'view_mode': 'form',
            'target': 'new',
        }
        

    def button_leave(self):
        holiday_status_id = self.env['hr.leave.type'].search([('request_type_id', '=', self.type_id.id)], limit=1)
        if self.types == "leave" and holiday_status_id:
            wizard = self.env['leave.wizard'].create({'holiday_status_id': holiday_status_id.id})
            return {
                'name': 'Leave Wizard',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_id': wizard.id,
                'res_model': 'leave.wizard',
                'target': 'new',
            }
        else:
            return {
                'name': 'Leave Wizard',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_id': False,
                'res_model': 'leave.wizard',
                'target': 'new',
            }

# ===== other method =====

    @api.onchange('employee_id')
    def _onChangeEmployee(self):
        if self.employee_id:
            self.department_id = self.employee_id.department_id and self.employee_id.department_id.id   
            self.job_id = self.employee_id.job_id and self.employee_id.job_id.id        

    @api.model
    def create(self, vals):
        if vals.get('sequence_name', 'New') == 'New':
            vals['sequence_name'] = self.env['ir.sequence'].next_by_code('request.request') or ('New')
        return super(HrRequest, self).create(vals)

class RequestType(models.Model):
    _name = "hr.request.type"

    name = fields.Char()
    code = fields.Char()
    types = fields.Selection([('incident','Incident'), ('accident','Accident'), ('expense','Expense'), ('loan','Loan'),('advance_salary','Advance Salary'), ('request','Request'), ('leave','Leave')], default='request')

class LeaveLeave(models.Model):
    _inherit = 'hr.leave'

    request_id = fields.Many2one('request.request')

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    request_type_id = fields.Many2one('hr.request.type')

class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    request_id = fields.Many2one('request.request')

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    request_id = fields.Many2one('request.request')