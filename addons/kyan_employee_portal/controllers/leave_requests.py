import base64
import logging
from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError


class AddEmployeeQualification(http.Controller):
    @http.route(['/leave_requests/<int:leave_id>'], type='http', auth="user", website=True)
    def view_leave(self, leave_id, **kw):
        leave = request.env['hr.leave'].sudo().browse(leave_id)
        if not leave.exists():
            return request.not_found()
        values = {
            'leave': leave,
        }
        return request.render("kyan_employee_portal.view_leave_request", values)

    @http.route(['/leave/post_message/<int:leave_id>'], type='http', auth="user", website=True, methods=['POST'])
    def post_leave_message(self, leave_id, **post):
        message_content = post.get('message', '')
        leave = request.env['hr.leave'].sudo().browse(leave_id)

        # Ensure the expense record exists
        if not leave.exists():
            return json.dumps({'success': False, 'error': 'Expense not found'})

        # Post the message on the expense record
        if message_content:
            leave.message_post(body=message_content, message_type="comment")
            return json.dumps({'success': True})
        else:
            return json.dumps({'success': False, 'error': 'Empty message'})

    # For Attachment
    @http.route(['/leave/upload_attachment/<int:leave_id>'], type='http', auth="user", website=True,
                methods=['POST'], csrf=True)
    def upload_leave_attachment(self, leave_id, **post):
        attachment = request.httprequest.files.get('attachment')

        if not attachment:
            return json.dumps({'success': False, 'error': 'No file uploaded'})

        leave = request.env['hr.leave'].sudo().browse(leave_id)
        if not leave.exists():
            return json.dumps({'success': False, 'error': 'Expense not found'})

        try:
            file_content = attachment.read()
            if file_content:
                new_attachment = request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'type': 'binary',
                    'datas': base64.b64encode(file_content),
                    'res_model': 'hr.leave',
                    'res_id': leave_id,
                    'mimetype': attachment.content_type,
                })
                leave.message_post(body=f'New attachment added: {attachment.filename}', message_type='comment')
                return json.dumps({'success': True, 'attachment_name': attachment.filename})
        except Exception as e:
            _logger.error("Error uploading attachment: %s", str(e))
            return json.dumps({'success': False, 'error': 'An error occurred during upload'})

    @http.route('/employee/leave_request/save', type='http', csrf=False, auth="user", website=True)
    def _submit_request(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        request_date_from = kw.get('leave_date_form')
        request_date_to = kw.get('leave_date_to')
        leave_type = int(kw.get('leave_type'))

        # Check for overlapping leaves
        overlapping_leaves = request.env['hr.leave'].sudo().search([
            ('employee_id', '=', employee_info.id),
            ('state', 'in', ['confirm', 'validate']),
            '|',
            '&', ('request_date_from', '<=', request_date_to), ('request_date_to', '>=', request_date_from),
            '&', ('request_date_from', '<=', request_date_to), ('request_date_to', '>=', request_date_from)
        ])

        if overlapping_leaves:
            overlap_message = f"An employee already booked time off which overlaps with this period: {employee_info.name} - from {overlapping_leaves[0].request_date_from} to {overlapping_leaves[0].request_date_to} - {overlapping_leaves[0].state.title()}"
            return http.Response(overlap_message, status=400)

        # Process the leave request if no overlap is found
        attachment = kw.get('leave_document_attachment')
        image = base64.b64encode(attachment.read())
        values = {
            'employee_id': employee_info.id,
            'holiday_status_id': leave_type,
            'request_date_from': request_date_from,
            'request_date_to': request_date_to,
            'name': kw.get('leave_description'),
            'state': 'confirm',
            'department_id': employee_info.department_id.id,
            'company_id': employee_info.company_id.id,
            'employee_company_id': current_user.company_id.id,
            'resource_calendar_id': 1,
        }

        leave_id = request.env['hr.leave'].sudo().create(values)
        request.env['ir.attachment'].sudo().create({
            'name': leave_id.name,
            'type': 'binary',
            'datas': image,
            'res_model': 'hr.leave',
            'res_id': leave_id.id,
        })

        return http.Response("Request submitted successfully", status=200)
