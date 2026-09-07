from odoo import http
from odoo.http import request


# Salary / Loan Request
class Dashboard(http.Controller):
    @http.route(['/dashboard'], type='http', auth="user", website=True)
    def dashboard(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        values = {
            'employee_info': employee_info,
        }

        return request.render("kyan_employee_portal.main_dashboard", values)
