from odoo import http
from odoo.http import request
import base64
import operator
from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError


class RequestController(http.Controller):
    
    @http.route(['/request',], type='http', auth="user", website=True)
    def request_get_data(self, message=None, **kwargs):
        request_id = request.env['request.request'].sudo().search([('create_uid', '=', request.env.user.id)])
        request_type_id = request.env['hr.request.type'].sudo().search([])
        employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        values = {  'requests_ids': request_id,
                    'requests_type_id' : request_type_id,
                    'employee_id' : employee_id }
        return request.render("kyan_request_management.request_website_page",values)

    @http.route('/new/request_type', type='json', auth='public')
    def create_request_by_page(self, data):
        request_selection, request_date, description_request, amount, start_date, end_date, your_details, employe_id = operator.itemgetter('request_selection', 'request_date', 'description_request', 'amount', 'start_date', 'end_date', 'your_details', 'employe_id')({f['name']: f['value'] for f in data})
        if request_selection:
            request_type = request.env['hr.request.type'].sudo().search([('id','=', request_selection)])
        if not request_selection:
            return {'title': _('Send info'), 'msg': "Please Enter Request Type"}
        if not request_date:
            return {'title': _('Send info'), 'msg': "Please Enter Request Date"}
        if not description_request:
            return {'title': _('Send info'), 'msg': "Please Enter Description"}
        if not your_details:
            return {'title': _('Send info'), 'msg': "Please Enter Your Details"}
        if request_type.types == 'loan' or request_type.types == 'advance_salary':
            if not amount:
                return {'title': _('Send info'), 'msg': "Please Enter Amount"}
        if request_type.types == 'leave':
            if not start_date:
                return {'title': _('Send info'), 'msg': "Please Enter Start Date"}
        if request_type.types == 'leave':
            if not end_date:
                return {'title': _('Send info'), 'msg': "Please Enter End Date"}

        request_date = fields.Date.from_string(request_date)
        start_date = fields.Date.from_string(start_date)
        end_date = fields.Date.from_string(end_date)

        if not employe_id:
            employee_id = request.env.user.employee_id
            employe_id = employee_id.id
            department = employee_id.department_id.id if employee_id.department_id else False
            job = employee_id.job_id.id if employee_id.job_id else False
        else:
            employee_id = int(employe_id)
            employee = request.env['hr.employee'].sudo().browse(employee_id)
            department = employee.department_id.id if employee.department_id else False
            job = employee.job_id.id if employee.job_id else False

        vals = {
                'employee_id' : employe_id,
                'department_id' : department,
                'job_id' : job,
                'reqest_date' : request_date, 
                'type_id' : int(request_selection), 
                'state' : 'draft', 
                'description' : description_request, 
                'start_date' : start_date, 
                'end_date' : end_date, 
                'amount' : amount,
                'your_details': your_details}
        try:
            request_id = request.env['request.request'].sudo().create(vals)
        except ValidationError as e:
            request.env.cr.rollback()
            data = {'title': _('Send info'), 'msg': e.args[0]}
            return data
        return True


    @http.route(['/refrence2/product/'], type='json', auth="public", website=True)
    def check_products_onchange(self, product, **kw):
        response = request.env['hr.request.type'].sudo().search([('id', '=', product)])
        return response.types