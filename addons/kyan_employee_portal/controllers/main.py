from odoo import http
from odoo.http import request
import json
import base64

from odoo.addons.portal.controllers.portal import CustomerPortal


# class CustomPortal(CustomerPortal):
#     @http.route(['/my', '/my/home'], type='http', auth="user", website=True)
#     def custom_home(self, **kw):
#         current_user = request.env.user
#         employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
#         leave_allocations = request.env['hr.leave.allocation'].sudo().search(
#             [('employee_id', '=', employee_info.id), ('state', '=', 'validate')])
#         total_leaves = request.env['hr.leave'].sudo().search(
#             [('employee_id', '=', employee_info.id), ('state', '=', 'validate')])
#
#         def parse_duration(duration):
#             if isinstance(duration, float):
#                 return duration
#             if isinstance(duration, str):
#                 try:
#                     if 'day' in duration:
#                         return float(duration.split()[0])
#                     elif ':' in duration:
#                         hours, minutes = map(int, duration.split(':'))
#                         return hours + minutes / 60
#                     else:
#                         return float(duration)
#                 except ValueError:
#                     return 0
#             return 0
#
#         total_allocated_duration = sum(parse_duration(allocation.duration_display) for allocation in leave_allocations)
#         total_leaves_duration = sum(parse_duration(leave.number_of_days_display) for leave in total_leaves)
#
#         remaining_leaves = total_allocated_duration - total_leaves_duration
#         total_expense = request.env['hr.expense'].sudo().search_count([('employee_id', '=', employee_info.id)])
#
#         total_salary = request.env['hr.loan'].sudo().search_count(
#             [('employee_id', '=', employee_info.id), ('types', '=', 'salary_advance')])
#
#         total_loan = request.env['hr.loan'].sudo().search_count([('employee_id', '=', employee_info.id), ('types', '=', 'loan')])
#
#         total_acc_inc = request.env['hr.accident'].sudo().search_count([('employee_id', '=', employee_info.id)])
#
#         values = {
#             'total_allocated_duration': total_allocated_duration,
#             'total_leaves_duration': total_leaves_duration,
#             'remaining_leaves': remaining_leaves,
#             'total_expense': total_expense,
#             'total_salary': total_salary,
#             'total_loan': total_loan,
#             'total_acc_inc': total_acc_inc,
#         }
#         return request.render("kyan_employee_portal.dashboard_main", values)

class CustomPortal(CustomerPortal):
    @http.route(['/my', '/my/home'], type='http', auth="user", website=True)
    def custom_home(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])

        # Check if the current user is an employee
        if current_user.is_customer:
            return request.render("portal.portal_my_home")
        else:
            leave_allocations = request.env['hr.leave.allocation'].sudo().search(
                [('employee_id', '=', employee_info.id), ('state', '=', 'validate')])
            total_leaves = request.env['hr.leave'].sudo().search(
                [('employee_id', '=', employee_info.id), ('state', '=', 'validate')])

            def parse_duration(duration):
                if isinstance(duration, float):
                    return duration
                if isinstance(duration, str):
                    try:
                        if 'day' in duration:
                            return float(duration.split()[0])
                        elif ':' in duration:
                            hours, minutes = map(int, duration.split(':'))
                            return hours + minutes / 60
                        else:
                            return float(duration)
                    except ValueError:
                        return 0
                return 0

            total_allocated_duration = sum(parse_duration(allocation.duration_display) for allocation in leave_allocations)
            total_leaves_duration = sum(parse_duration(leave.number_of_days_display) for leave in total_leaves)

            remaining_leaves = total_allocated_duration - total_leaves_duration
            total_expense = request.env['hr.expense'].sudo().search_count([('employee_id', '=', employee_info.id)])

            total_salary = request.env['hr.loan'].sudo().search_count(
                [('employee_id', '=', employee_info.id), ('types', '=', 'salary_advance')])

            total_loan = request.env['hr.loan'].sudo().search_count([('employee_id', '=', employee_info.id), ('types', '=', 'loan')])

            total_acc_inc = request.env['hr.accident'].sudo().search_count([('employee_id', '=', employee_info.id)])

            values = {
                'total_allocated_duration': total_allocated_duration,
                'total_leaves_duration': total_leaves_duration,
                'remaining_leaves': remaining_leaves,
                'total_expense': total_expense,
                'total_salary': total_salary,
                'total_loan': total_loan,
                'total_acc_inc': total_acc_inc,
            }
            return request.render("kyan_employee_portal.dashboard_main", values)


# class EmployeeManagement(http.Controller):
#     @http.route(['/my_profile', '/my/profile'], type='http', auth="user", website=True)
#     def custom_home(self, **kw):
#         current_user = request.env.user
#         employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
#         marital_status_options = employee_info._fields['marital'].selection
#         gender_options = employee_info._fields['gender'].selection
#         country_options = request.env['res.country'].sudo().search([])
#         employment_options = request.env['hr.contract.type'].sudo().search([])
#         base64_data = employee_info.image_1920.decode('utf-8')
#         values = {
#             'employee_info': employee_info,
#             'marital_status': marital_status_options,
#             'gender': gender_options,
#             'country_options': country_options,
#             'employment_options': employment_options,
#             'image_data': base64_data,
#         }
#         return request.render("kyan_employee_portal.portal_employee_management", values)

class EmployeeManagement(http.Controller):
    @http.route(['/my_profile', '/my/profile'], type='http', auth="user", website=True)
    def custom_home(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)

        # Check if employee_info exists
        if not employee_info:
            return request.render("kyan_employee_portal.portal_employee_management", {
                'no_employee_found': True,
            })

        marital_status_options = employee_info._fields['marital'].selection
        gender_options = employee_info._fields['gender'].selection
        country_options = request.env['res.country'].sudo().search([])
        employment_options = request.env['hr.contract.type'].sudo().search([])

        # Ensure image_1920 exists before decoding
        base64_data = employee_info.image_1920.decode('utf-8') if employee_info.image_1920 else None

        values = {
            'employee_info': employee_info,
            'marital_status': marital_status_options,
            'gender': gender_options,
            'country_options': country_options,
            'employment_options': employment_options,
            'image_data': base64_data,
        }
        return request.render("kyan_employee_portal.portal_employee_management", values)


class AllJobRequests(http.Controller):
    @http.route(['/job_requests'], type='http', auth="user", website=True)
    def all_jobs(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        job_request = request.env['job.request'].sudo().search([('employee_id', '=', employee_info.id)])

        # print(job_request)
        if job_request:
            for employee in job_request:
                employee_data = employee.read()[0]
                print("Employee Data:")
                for field_name, field_value in employee_data.items():
                    print(f"{field_name}: {field_value}")
        else:
            print("No employee found for the current user.")
        print(job_request)
        values = {
            'data': job_request,
        }

        return request.render("kyan_employee_portal.portal_all_job_requests", values)


class LeaveRequests(http.Controller):
    @http.route(['/leave_requests_details'], type='http', auth="user", website=True)
    def all_leave_requests(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        leave_details = request.env['hr.leave'].sudo().search([('employee_id', '=', employee_info.id)])
        values = {
            'data': leave_details,
        }

        return request.render("kyan_employee_portal.all_leave_requests", values)

    @http.route(['/leave_requests'], type='http', auth="public", website=True)
    def custom_home(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
        leave_allocations = request.env['hr.leave.allocation'].sudo().search(
            [('employee_id', '=', employee_info.id), ('state', '=', 'validate')])
        print(leave_allocations)
        total_leaves = request.env['hr.leave'].sudo().search(
            [('employee_id', '=', employee_info.id), ('state', '=', 'validate')])

        def parse_duration(duration):
            if isinstance(duration, float):
                return duration
            if isinstance(duration, str):
                try:
                    if 'day' in duration:
                        return float(duration.split()[0])
                    elif ':' in duration:
                        hours, minutes = map(int, duration.split(':'))
                        return hours + minutes / 60
                    else:
                        return float(duration)
                except ValueError:
                    return 0
            return 0

        total_allocated_duration = sum(parse_duration(allocation.duration_display) for allocation in leave_allocations)
        total_leaves_duration = sum(parse_duration(leave.number_of_days_display) for leave in total_leaves)

        remaining_leaves = total_allocated_duration - total_leaves_duration

        allocated_leave_type_ids = leave_allocations.mapped('holiday_status_id.id')
        print(allocated_leave_type_ids)

        leave_types = request.env['hr.leave.type'].sudo().search([
            '|',
            ('id', 'in', allocated_leave_type_ids),  # Leave types from allocations
            ('unpaid', '=', True)  # Unpaid leave types
        ])
        print(leave_types)
        values = {
            'employee_info': employee_info,
            'total_leaves_duration': total_leaves_duration,
            'remaining_leaves': remaining_leaves,
            'leave_types': leave_types,
        }

        # current_user = request.env.user
        # employee_leaves = request.env['hr.leave'].sudo().search([('user_id', '=', current_user.id), ('state', '=', 'validate')])
        # leave_allocations = request.env['hr.leave.allocation'].sudo().search(
        #     [('employee_id', '=', current_user.employee_id.id),
        #      ('state', '=', 'validate')])
        #
        # available_leaves = 0
        # allocation_leave_ids = set()
        # for allocation in leave_allocations:
        #     allocation_leave_ids.add(allocation.holiday_status_id.id)
        #     available_leaves = available_leaves + allocation['number_of_days_display']
        #
        # print("total no of days = ", available_leaves)
        # print("allocation_leave_ids", allocation_leave_ids)
        #
        # leave_consumed = 0
        # for leaves in employee_leaves:
        #     leave_consumed = leave_consumed + leaves['number_of_days']
        #
        # remaining_leaves = available_leaves - leave_consumed
        #
        # leave_types = request.env['hr.leave.type'].sudo().search([
        #     '|',
        #     ('id', 'in', list(allocation_leave_ids)),  # Allocated leave types
        #     ('unpaid', '=', True)  # Unpaid leave types
        # ])
        # values = {
        #     'employee_info': current_user,
        #     'remaining_leaves': int(remaining_leaves),
        #     'leave_types': leave_types,
        # }
        return request.render("kyan_employee_portal.portal_leave_request", values)


# Expense Request
class ExpenseRequest(http.Controller):
    @http.route(['/expense_requests'], type='http', auth="user", website=True)
    def all_expense(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        expense_request = request.env['hr.expense'].sudo().search([('employee_id', '=', employee_info.id)])
        if expense_request:
            for employee in expense_request:
                employee_data = employee.read()[0]
                print("Employee Data:")
                for field_name, field_value in employee_data.items():
                    print(f"{field_name}: {field_value}")
        values = {
            'data': expense_request,
        }

        return request.render("kyan_employee_portal.portal_all_expense_requests", values)


# Accident Incident Request
class AccidentRequest(http.Controller):
    @http.route(['/accident_requests'], type='http', auth="user", website=True)
    def all_accident_incident(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        accident_request = request.env['hr.accident'].sudo().search([('employee_id', '=', employee_info.id)])
        values = {
            'data': accident_request,
        }

        return request.render("kyan_employee_portal.portal_all_accident_requests", values)


# Salary / Loan Request
class SalaryLoanRequest(http.Controller):
    @http.route(['/salary_loan_request'], type='http', auth="user", website=True)
    def salary_loan_request(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        salary_loan_request = request.env['hr.loan'].sudo().search(
            [('employee_id', '=', employee_info.id), ('types', '=', 'salary_advance')])
        values = {
            'data': salary_loan_request,
        }

        return request.render("kyan_employee_portal.salary_advance_loan_request", values)

    @http.route(['/all_loan_request'], type='http', auth="user", website=True)
    def all_loan_request(self, **kw):
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)], limit=1)
        loan_request = request.env['hr.loan'].sudo().search([('employee_id', '=', employee_info.id), ('types', '=', 'loan')])
        values = {
            'data': loan_request,
        }

        return request.render("kyan_employee_portal.loan_all_request", values)
