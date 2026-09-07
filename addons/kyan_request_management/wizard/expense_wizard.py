from odoo import fields, models

class ExpenseWizard(models.TransientModel):
    _name = 'expense.wizard'

    product_id = fields.Many2one('product.product', required=True, domain="[('can_be_expensed', '=', True)]")
    name = fields.Char(related="product_id.name", required=True,)
    expense_date = fields.Date(string="Expense Date")
    payment_mode = fields.Selection([('own_account','Employee'),('company_account','Company')])
    unit_amount = fields.Float()
    expense_quantity = fields.Float()
    total_amount = fields.Monetary("Total In Currency", currency_field='currency_id')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company, ondelete='cascade')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')

    def create_expense(self):
        active_id = self.env.context.get('active_id')
        request_id = self.env['request.request'].browse(active_id)
        vals = {
            'employee_id' : request_id.employee_id.id or False, 
            'product_id' : self.product_id.id or False, 
            'date' : self.expense_date,
            'payment_mode' : self.payment_mode,
            'quantity' : self.expense_quantity or 1,
            'state' : 'draft',
            'name': self.name,
            'total_amount': self.total_amount,
            'currency_id': self.currency_id.id,
            'company_id': self.company_id.id,
            'request_id': request_id.id,
        }

        if self.expense_quantity != 0:
            vals['total_amount_currency'] = self.total_amount / self.expense_quantity
        else:
            vals['total_amount_currency'] = 0

        res = self.env['hr.expense'].search([]).create(vals)
        return res
