from odoo import fields, models
from odoo.exceptions import ValidationError

class LeaveWizard(models.TransientModel):
    _name = 'leave.wizard'

    holiday_status_id = fields.Many2one('hr.leave.type', string="Time Off Type")


    def action_create_leave(self):
        active_id = self.env.context.get('active_id')
        request_id = self.env['request.request'].browse(active_id)
        hr_leave_type_id = self.env['hr.leave.type'].browse(request_id.type_id.id)

        if self.holiday_status_id.requires_allocation == 'yes':
            hr_leave_allocation_id = self.env['hr.leave.allocation'].search([
                ('employee_id', '=', request_id.employee_id.id),
                ('holiday_status_id', '=', self.holiday_status_id.id),
                ('state', '=', 'validate')
            ])

            if not hr_leave_allocation_id:
                raise ValidationError("The selected employee does not have an allocated leave for this type.")

        vals = {
            'employee_id': request_id.employee_id.id,
            'holiday_status_id': self.holiday_status_id.id,
            'request_date_from': request_id.start_date,
            'request_date_to': request_id.end_date,
            'date_from': request_id.start_date,
            'date_to': request_id.end_date,
            'name': request_id.description,
            'request_id': request_id.id,
        }
        res = self.env['hr.leave'].create(vals)

        return res

