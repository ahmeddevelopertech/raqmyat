{
    'name': 'Employee Portal',
    'version': '17.0',
    'author': 'kyan systems ',
    'website': 'https://kyansys.sa',
    'summary': """In this Module employee can request from portal like leave expense loan advance salary incident and accident.
                Employee Dashboard
                Employee Profile
                Employee Request management
                Employee service management
                Leave request portal
                Employee Expense 
                employee loan 
                employee advance salary portal
                Employee portal management
                Communication History Against Each Record like Leave, Expense, Loan, Salary and Accident
            """,
    'description': """
                   """,
    'depends': ['base', 'hr', 'mail', 'hr_expense', 'kyan_request_management', 'portal', 'hr_holidays', 'hr_contract'],
    'static': {
        'web.assets_backend': [
            '/employee_portal/static/src/js/*.js',
        ],
        'web.assets_frontend': [
            'employee_portal/static/src/css/*.js',
        ],
    },
    'data': [
        'security/security_groups.xml',
        'views/backend_views/res_users_inherit.xml',
        'views/portal/base_navigation/portal_navigation.xml',
        'views/portal/employee_details/portal_employee_management.xml',
        'views/portal/job_requests/portal_job_requisition_request.xml',
        'views/portal/portal_dashboard.xml',
        'views/portal/job_requests/portal_all_job_requests.xml',
        'views/portal/leave_requests/view_leave_details.xml',
        'views/portal/leave_requests/leave_all_requests.xml',
        'views/portal/leave_requests/portal_leave_request.xml',
        'views/portal/expense_request/expense_all_job_requests.xml',
        'views/portal/expense_request/view_expense_details.xml',
        'views/portal/expense_request/portal_expense_request.xml',
        'views/portal/accident_request/accident_all_requests.xml',
        'views/portal/accident_request/view_accident_details.xml',
        'views/portal/accident_request/portal_accident_request.xml',
        'views/portal/salary_advance_request/salary_advance_requests.xml',
        'views/portal/salary_advance_request/view_salary_advance_details.xml',
        'views/portal/salary_advance_request/portal_salary_advance_request.xml',
        'views/portal/salary_advance_request/loan_requests.xml',
        'views/portal/salary_advance_request/view_loan_details.xml',
        'views/portal/salary_advance_request/portal_loan_request.xml',
    ],
    'sequence': -101,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'installable': True

}
