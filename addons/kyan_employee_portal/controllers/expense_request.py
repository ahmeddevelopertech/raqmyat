import base64
import logging
from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)


class EmployeeExpenseRequest(http.Controller):

    @http.route(['/expense_request/<int:expense_id>'], type='http', auth="user", website=True)
    def view_expense(self, expense_id, **kw):
        expense = request.env['hr.expense'].sudo().browse(expense_id)
        if not expense.exists():
            return request.not_found()
        values = {
            'expense': expense,
        }
        return request.render("kyan_employee_portal.portal_view_expense_request", values)

    @http.route(['/expense/post_message/<int:expense_id>'], type='http', auth="user", website=True, methods=['POST'])
    def post_expense_message(self, expense_id, **post):
        message_content = post.get('message', '')
        expense = request.env['hr.expense'].sudo().browse(expense_id)
        print("Ddddddddddddddddddd")

        # Ensure the expense record exists
        if not expense.exists():
            return json.dumps({'success': False, 'error': 'Expense not found'})

        # Post the message on the expense record
        if message_content:
            expense.message_post(body=message_content, message_type="comment")
            return json.dumps({'success': True})
        else:
            return json.dumps({'success': False, 'error': 'Empty message'})

    # For Attachment
    @http.route(['/expense/upload_attachment/<int:expense_id>'], type='http', auth="user", website=True,
                methods=['POST'], csrf=True)
    def upload_expense_attachment(self, expense_id, **post):
        attachment = request.httprequest.files.get('attachment')

        if not attachment:
            return json.dumps({'success': False, 'error': 'No file uploaded'})

        expense = request.env['hr.expense'].sudo().browse(expense_id)
        if not expense.exists():
            return json.dumps({'success': False, 'error': 'Expense not found'})

        try:
            file_content = attachment.read()
            if file_content:
                new_attachment = request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'type': 'binary',
                    'datas': base64.b64encode(file_content),
                    'res_model': 'hr.expense',
                    'res_id': expense_id,
                    'mimetype': attachment.content_type,
                })
                expense.message_post(body=f'New attachment added: {attachment.filename}', message_type='comment')
                return json.dumps({'success': True, 'attachment_name': attachment.filename})
        except Exception as e:
            _logger.error("Error uploading attachment: %s", str(e))
            return json.dumps({'success': False, 'error': 'An error occurred during upload'})


class ExpenseRequestSave(http.Controller):
    @http.route('/portal_expense_request', type='http', auth="user", website=True)
    def portal_expense_request(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        product = request.env['product.product'].sudo().search(
            [('can_be_expensed', '=', True), ('company_id', '=', current_user.company_id.id)])
        print(len(product))
        values = {
            'employee_info': employee_info,
            'product': product,
        }
        return request.render("kyan_employee_portal.portal_expense_request", values)

    @http.route('/portal_expense_request_save', type='http', auth="user", website=True, csrf=False)
    def portal_expense_request_save(self, **kw):
        current_user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)

        product_id = int(kw.get('product'))
        product = request.env['product.product'].sudo().search([('id', '=', product_id)], limit=1)
        attachment = kw.get('leave_document_attachment')

        # Make sure the file was uploaded
        if attachment:
            # The attachment is sent as an InMemoryUploadedFile object, not as a string
            file_content = attachment.read()  # Read the content of the file
            image = base64.b64encode(file_content)  # Encode it in base64

            if product:
                expense_data = {
                    'name': product.name,
                    'product_id': product.id,
                    'total_amount_currency': kw.get('unit_price'),
                    'quantity': kw.get('quantity'),
                    'date': kw.get('expense_date'),
                    'employee_id': employee.id,
                }
                expense_id = request.env['hr.expense'].sudo().create(expense_data)
                expense_id.action_submit_expenses()

                # Attach the file to the expense record
                request.env['ir.attachment'].sudo().create({
                    'name': expense_id.name,
                    'type': 'binary',
                    'datas': image,
                    'res_model': 'hr.expense',
                    'res_id': expense_id.id,
                    'mimetype': attachment.content_type,  # Store the mimetype for reference
                })
