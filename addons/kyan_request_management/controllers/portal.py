import binascii
import json

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request

from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
import operator
from odoo.tools import float_compare, float_round
import pytz

class CustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        employee_id = request.env.user.employee_id
        if 'request_count' in counters:
            request_count = request.env['request.request'].sudo().search_count([('employee_id', '=', employee_id.id)]) \
                if request.env['request.request'].check_access_rights('read', raise_exception=False) else 0
            values['request_count'] = request_count
        return values

    def get_request_types(self):
        return request.env['hr.request.type'].sudo().search([])

    @http.route('/add/request', type='json', auth='public')
    def create_request(self, data):
        request_selection, request_date, description_request, amount = operator.itemgetter('request_selection', 'request_date', 'description_request', 'amount')({f['sequence_name']: f['value'] for f in data})
        employee_id = request.env.user.employee_id
        if not request_selection:
            return {'title': _('Send info'), 'msg': "Please select request type"}
        if not request_date:
            return {'title': _('Send info'), 'msg': "Please select request date"}
        if not description_request:
            return {'title': _('Send info'), 'msg': "Please enter request description"}
        request_date = fields.Date.from_string(request_date)
        employee_id = employee_id.id if employee_id else False
        vals = {
                'employee_id' : employee_id, 
                'reqest_date' : request_date, 
                'type_id' : int(request_selection), 
                'state' : 'draft', 
                'description' : description_request, 
                'amount' : amount}
        try:
            request_id = request.env['request.request'].sudo().create(vals)
        except ValidationError as e:
            request.env.cr.rollback()
            data = {'title': _('Send info'), 'msg': e.args[0]}
            return data
        return True

    @http.route(['/my/request', '/my/request/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_request(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        employee_id = request.env.user.employee_id
        request_obj = request.env['request.request']
        domain = [
            ('employee_id', '=', employee_id.id if employee_id else False)
        ]
        searchbar_sortings = {
            'state': {'label': _('state'), 'order': 'state desc'},
           
        }
        # default sortby order
        if not sortby:
            sortby = 'state'
        sort_order = searchbar_sortings[sortby]['order']
        
        # count for pager
        request_ids = request_obj.sudo().search(domain)

        request_count = request_ids.sudo().search_count(domain)
        #picking_ids = order_ids.mapped('picking_ids')
        # pager
        pager = portal_pager(
            url="/my/request",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=len(request_ids),
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        requests = request_obj.sudo().search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_request_history'] = request_ids.ids[:100]
        values.update({
            'date': date_begin,
            'requests_ids': request_ids.sudo(),
            'page_name': 'request',
            'pager': pager,
            'default_url': '/my/request',
            'searchbar_sortings': searchbar_sortings,
            'create_request' : True,
            'requests_type_ids' : self.get_request_types(),
            'sortby': sortby,
        })
        return request.render("kyan_request_management.portal_my_request", values)



