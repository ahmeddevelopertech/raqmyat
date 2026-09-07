# -*- coding: utf-8 -*-
{
    'name': "HR Request",
    'summary': """
                Employee request from portal can Manage in this Module in Backend, Request like
                Leave request portal
                Employee Expense 
                employee loan 
                employee advance salary portal
            """,
    'category': 'Generic Modules/Human Resources',
    'author': 'kyan systems ',
    'website': "https://kyansys.sa",
    'version': "17.0",
    'depends': ['web', 'hr_holidays', 'hr_expense'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/leave_wizard_views.xml',
        'wizard/expense_wizard_view.xml',
        'wizard/journal_entry.xml',
        'views/hr_request.xml',
        'views/inherited_view.xml',
        'views/hr_request_portal.xml',
        'views/hr_loan.xml',
        'views/hr_accident.xml',
        # 'views/website_menu.xml',
        'views/website_request_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'kyan_request_management/static/src/js/website_request.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 31.0,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
}
