import base64
import logging
from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)


class AccidentDetailsRequest(http.Controller):
    @http.route(['/accident_requests/<int:accident_id>'], type='http', auth="user", website=True)
    def view_accident(self, accident_id, **kw):
        accident = request.env['hr.accident'].sudo().browse(accident_id)
        if not accident.exists():
            return request.not_found()
        values = {
            'accident': accident,
        }
        return request.render("kyan_employee_portal.portal_view_accident_request", values)

    @http.route(['/accident/post_message/<int:accident_id>'], type='http', auth="user", website=True, methods=['POST'])
    def post_accident_message(self, accident_id, **post):
        message_content = post.get('message', '')
        accident = request.env['hr.accident'].sudo().browse(accident_id)

        # Ensure the loan record exists
        if not accident.exists():
            return json.dumps({'success': False, 'error': 'Salary Advance not found'})

        # Post the message on the accident record
        if message_content:
            accident.message_post(body=message_content, message_type="comment")
            return json.dumps({'success': True})
        else:
            return json.dumps({'success': False, 'error': 'Empty message'})

    # For Attachment
    @http.route(['/accident/upload_attachment/<int:accident_id>'], type='http', auth="user", website=True,
                methods=['POST'], csrf=True)
    def upload_accident_attachment(self, accident_id, **post):
        attachment = request.httprequest.files.get('attachment')

        if not attachment:
            return json.dumps({'success': False, 'error': 'No file uploaded'})

        accident = request.env['hr.accident'].sudo().browse(accident_id)
        if not accident.exists():
            return json.dumps({'success': False, 'error': 'Expense not found'})

        try:
            file_content = attachment.read()
            if file_content:
                new_attachment = request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'type': 'binary',
                    'datas': base64.b64encode(file_content),
                    'res_model': 'hr.loan',
                    'res_id': accident_id,
                    'mimetype': attachment.content_type,
                })
                accident.message_post(body=f'New attachment added: {attachment.filename}', message_type='comment')
                return json.dumps({'success': True, 'attachment_name': attachment.filename})
        except Exception as e:
            _logger.error("Error uploading attachment: %s", str(e))
            return json.dumps({'success': False, 'error': 'An error occurred during upload'})


class PortalAccidentRequest(http.Controller):
    @http.route('/portal_accident_request', type='http', auth="user", website=True)
    def portal_accident_request(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
        values = {
            'employee_info': employee_info,
            # 'product': product,
        }
        return request.render("kyan_employee_portal.portal_accident_request", values)

    @http.route('/portal_accident_request_save', type='http', auth="user", website=True, csrf=False)
    def portal_accident_request_save(self, **kw):
        current_user = request.env.user
        print(kw)
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
        attachment = kw.get('accident_document_attachment')
        image = base64.b64encode(attachment.read())
        # if product:
        accident_data = {
            'incident_type': kw.get('incident_type'),
            'type_of_injury': kw.get('type_of_inquiry'),
            'hospital': kw.get('hospital'),
            'occupation': kw.get('occupation'),
            'wiba': kw.get('wiba'),
            'sick': kw.get('sick'),
            'time_location': kw.get('time_location'),
            'witnesses': kw.get('witnesses'),
            'date_of_accident': kw.get('date_of_accident'),
            'date_of_resumption': kw.get('date_of_resumption'),
            'date_of_reporting': kw.get('date_of_reporting'),
            'your_details': kw.get('details_notes'),
            'employee_id': employee.id,
        }
        accident_id = request.env['hr.accident'].sudo().create(accident_data)
        attachment = request.env['ir.attachment'].sudo().create({
            'name': accident_id.name,
            'type': 'binary',
            'datas': image,
            'res_model': 'hr.accident',
            'res_id': accident_id.id,
        })
