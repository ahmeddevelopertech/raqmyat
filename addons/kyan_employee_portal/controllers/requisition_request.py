from odoo import http
from odoo.http import request


class JobRequisitionRequest(http.Controller):
    @http.route('/requisition_request/<string:id>', type='http', auth="user", website=True)
    def custom_home(self, id=None, **kw):
        # < int: id >
        if id and id.isdigit():
            print(" is ====", id)
            id = int(id)
            current_user = request.env.user
            employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
            job_request = request.env['job.request'].sudo().search([('id', '=', id)])
            position_request_options = job_request._fields['position_request'].selection
            position_type_options = job_request._fields['position_type'].selection
            employment_status_options = job_request._fields['employment_status'].selection
            contract_duration_options = job_request._fields['contract_duration'].selection
            nationality_options = job_request._fields['nationality'].selection
            gender_options = job_request._fields['gender'].selection
            budgeted_options = job_request._fields['budgeted'].selection
            experience_options = job_request._fields['experience'].selection
            office_space_options = job_request._fields['office_space_available'].selection
            space_availability_options = job_request._fields['space_availability'].selection
            grade_options = request.env['position.grade'].sudo().search([])
            education_options = request.env['required.education'].sudo().search([])
            employee_ids = request.env['hr.employee'].sudo().search([])
            language_options = request.env['required.language'].sudo().search([])
            grade_id = request.env['position.grade'].sudo().search([])

            computer_knowledge_options = request.env['computer.knowledge'].sudo().search([])
            # print("employee_ids", employee_ids)
            if employee_info:
                for employee in grade_id:
                    employee_data = employee.read()[0]
                    print("Employee Data:")
                    for field_name, field_value in employee_data.items():
                        print(f"{field_name}: {field_value}")
            # else:
            #     print("No employee found for the current user.")
            # employee_info = request.env['hr.employee'].sudo().search_read(
            #     [('user_id', '=', current_user.id)],
            #     fields=['job_id', 'department_id', 'name','id']
            # )
            # if employee_info:
            #     job_id = employee_info[0].get('job_id')
            #
            #     if job_id:
            #         job_name = job_id[1]
            #         print(job_name)
            #     else:
            #         print("Job ID not found or empty.")
            # else:
            #     print("Employee information not found or empty.")
            # print(employee_info[0]['job_id']['name'])

            values = {
                'employee_info': employee_info,
                'job_request': job_request,
                'position_request': position_request_options,
                'position_type': position_type_options,
                'employment_status': employment_status_options,
                'grade': grade_options,
                'contract_duration': contract_duration_options,
                'nationality': nationality_options,
                'gender': gender_options,
                'budgeted': budgeted_options,
                'education': education_options,
                'language': language_options,
                'computer_knowledge': computer_knowledge_options,
                'experience': experience_options,
                'office_space_available': office_space_options,
                'space_availability': space_availability_options,
                'manager_id': employee_ids,
                'grade_id': grade_id,
            }
            return request.render("kyan_employee_portal.portal_job_requisition_request", values)
        else:
            print(" is ==== None")
            return request.render("kyan_employee_portal.portal_job_requisition_request", {})
        # print("in employee")
