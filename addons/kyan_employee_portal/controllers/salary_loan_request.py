import base64
import logging
from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)


class SalaryLoanDetails(http.Controller):
    @http.route(['/salary_loan_request/<int:salary_id>'], type='http', auth="user", website=True)
    def view_salary_advance(self, salary_id, **kw):
        salary_loan = request.env['hr.loan'].sudo().browse(salary_id)
        if not salary_loan.exists():
            return request.not_found()
        values = {
            'salary_loan': salary_loan,
        }
        return request.render("kyan_employee_portal.view_salary_loan_request", values)

    @http.route(['/salary/post_message/<int:salary_id>'], type='http', auth="user", website=True, methods=['POST'])
    def post_salary_message(self, salary_id, **post):
        message_content = post.get('message', '')
        salary = request.env['hr.loan'].sudo().browse(salary_id)

        # Ensure the loan record exists
        if not salary.exists():
            return json.dumps({'success': False, 'error': 'Salary Advance not found'})

        # Post the message on the salary record
        if message_content:
            salary.message_post(body=message_content, message_type="comment")
            return json.dumps({'success': True})
        else:
            return json.dumps({'success': False, 'error': 'Empty message'})

    # For Attachment
    @http.route(['/salary/upload_attachment/<int:salary_id>'], type='http', auth="user", website=True,
                methods=['POST'], csrf=True)
    def upload_salary_attachment(self, salary_id, **post):
        attachment = request.httprequest.files.get('attachment')

        if not attachment:
            return json.dumps({'success': False, 'error': 'No file uploaded'})

        salary = request.env['hr.loan'].sudo().browse(salary_id)
        if not salary.exists():
            return json.dumps({'success': False, 'error': 'Expense not found'})

        try:
            file_content = attachment.read()
            if file_content:
                new_attachment = request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'type': 'binary',
                    'datas': base64.b64encode(file_content),
                    'res_model': 'hr.loan',
                    'res_id': salary_id,
                    'mimetype': attachment.content_type,
                })
                salary.message_post(body=f'New attachment added: {attachment.filename}', message_type='comment')
                return json.dumps({'success': True, 'attachment_name': attachment.filename})
        except Exception as e:
            _logger.error("Error uploading attachment: %s", str(e))
            return json.dumps({'success': False, 'error': 'An error occurred during upload'})

    # This Controller For Loan
    @http.route(['/all_loan_request/<int:loan_id>'], type='http', auth="user", website=True)
    def view_salary_loan(self, loan_id, **kw):
        loan = request.env['hr.loan'].sudo().browse(loan_id)
        if not loan.exists():
            return request.not_found()
        values = {
            'salary_loan': loan,
        }
        return request.render("kyan_employee_portal.view_loan_details", values)

    @http.route(['/loan/post_message/<int:loan_id>'], type='http', auth="user", website=True, methods=['POST'])
    def post_loan_message(self, loan_id, **post):
        message_content = post.get('message', '')
        loan = request.env['hr.loan'].sudo().browse(loan_id)

        # Ensure the loan record exists
        if not loan.exists():
            return json.dumps({'success': False, 'error': 'Loan not found'})

        # Post the message on the loan record
        if message_content:
            loan.message_post(body=message_content, message_type="comment")
            return json.dumps({'success': True})
        else:
            return json.dumps({'success': False, 'error': 'Empty message'})

    # For Attachment
    @http.route(['/loan/upload_attachment/<int:loan_id>'], type='http', auth="user", website=True,
                methods=['POST'], csrf=True)
    def upload_loan_attachment(self, loan_id, **post):
        attachment = request.httprequest.files.get('attachment')

        if not attachment:
            return json.dumps({'success': False, 'error': 'No file uploaded'})

        loan = request.env['hr.loan'].sudo().browse(loan_id)
        if not loan.exists():
            return json.dumps({'success': False, 'error': 'Expense not found'})

        try:
            file_content = attachment.read()
            if file_content:
                new_attachment = request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'type': 'binary',
                    'datas': base64.b64encode(file_content),
                    'res_model': 'hr.loan',
                    'res_id': loan_id,
                    'mimetype': attachment.content_type,
                })
                loan.message_post(body=f'New attachment added: {attachment.filename}', message_type='comment')
                return json.dumps({'success': True, 'attachment_name': attachment.filename})
        except Exception as e:
            _logger.error("Error uploading attachment: %s", str(e))
            return json.dumps({'success': False, 'error': 'An error occurred during upload'})


class PortalLoanSalaryRequest(http.Controller):
    @http.route('/portal_loan_salary_request', type='http', auth="user", website=True)
    def portal_loan_salary_request(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
        values = {
            'employee_info': employee_info,
        }
        return request.render("kyan_employee_portal.portal_salary_advance_request", values)

    @http.route('/portal_salary_loan_request_save', type='http', auth="user", website=True, csrf=False)
    def portal_salary_loan_request_save(self, **kw):
        current_user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
        # if product:
        salary_loan_data = {
            'types': kw.get('types'),
            'date': kw.get('date'),
            'installment': kw.get('installment'),
            'loan_amount': kw.get('loan_amount'),
            'description': kw.get('details_notes'),
            'employee_id': employee.id,
            'department_id': employee.department_id.id,
            'job_position': employee.job_id.id,
        }
        accident_id = request.env['hr.loan'].sudo().create(salary_loan_data)

    # Controller For Loan Request
    @http.route('/portal_loan_request', type='http', auth="user", website=True)
    def portal_loan_request(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
        values = {
            'employee_info': employee_info,
        }
        return request.render("kyan_employee_portal.portal_loan_request", values)

    @http.route('/portal_loan_request_save', type='http', auth="user", website=True, csrf=False)
    def portal_loan_request_save(self, **kw):
        current_user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
        # if product:
        salary_loan_data = {
            'types': kw.get('types'),
            'date': kw.get('date'),
            'installment': kw.get('installment'),
            'loan_amount': kw.get('loan_amount'),
            'description': kw.get('details_notes'),
            'employee_id': employee.id,
            'department_id': employee.department_id.id,
            'job_position': employee.job_id.id,
        }
        loan_id = request.env['hr.loan'].sudo().create(salary_loan_data)
