from odoo import http
from odoo.http import request
import base64


class AddEmployeeQualification(http.Controller):
    @http.route('/employee/qualification', type='http', auth="user", csrf=False, website=True)
    def _submit_request(self, **kw):
        attachment = kw.get('attachment')
        image = base64.b64encode(attachment.read())
        values = {
            'employee_id': kw.get('employee_id'),
            'degree': kw.get('degree'),
            'university': kw.get('university'),
            'year': kw.get('year'),
            'attachment': image,
        }

        response = http.request.env['hr.employee.qualification'].sudo().create(values)
        return 'Qualification created successfully!'


class AddEmployeeExperience(http.Controller):
    @http.route('/employee/experience', type='http', auth="user", csrf=False, website=True)
    def _submit_request(self, **kw):
        response = http.request.env['hr.employee.experience'].sudo().create(kw)
        print(response)
        return


class AddEmployeeContractDetails(http.Controller):
    @http.route('/employee/contract_info', type='http', auth="user", csrf=False, website=True)
    def _submit_request(self, **kw):
        current_user = request.env.user
        employee_id = int(kw.get('employee_id'))

        contract_id = request.env['hr.contract'].sudo().search([('employee_id', '=', employee_id)],
                                                               limit=1)

        employee_name = current_user.name.replace(' ', '_')
        contract_name = "%s_%s" % (employee_name, "contract")
        print(contract_name)
        if contract_id:
            values = {
                'contract_type_id': int(kw.get('contract_type_id')),
                'date_end': kw.get('contract_end_date'),
                'date_start': kw.get('contract_start_date'),
            }
            update_contract = contract_id.sudo().write(values)
            if update_contract:
                return 'success'
        else:
            values = {
                'employee_id': employee_id,
                'resource_calendar_id': current_user.employee_resource_calendar_id.id,
                'company_id': current_user.company_id.id,
                'job_id': current_user.employee_id.job_id.id,
                'department_id': current_user.department_id.id,
                'contract_type_id': int(kw.get('contract_type')),
                'date_end': kw.get('contract_end_date'),
                'date_start': kw.get('contract_start_date'),
                'name': contract_name,
                'wage': 0.0,
                'state': 'draft'

            }
            new_contract_id = request.env['hr.contract'].sudo().create(values)
            if new_contract_id:
                return 'success'


class AddEmployeeBankDetails(http.Controller):
    @http.route('/employee/bank_details', type='http', auth="user", csrf=False, website=True)
    def _submit_request(self, **kw):
        print(kw)
        current_user = request.env.user
        if current_user.bank_account_id:
            print("if")
            bank_account = current_user.bank_account_id
            bank_id = ''
            if bank_account.bank_id:
                update_bank_id = bank_account.bank_id.sudo().write({'name': kw.get('bank_name')})
                if update_bank_id:
                    bank_id = bank_account.bank_id.id
            else:
                new_bank_id = request.env['res.bank'].sudo().create({
                    'name': kw.get('bank_name')
                })
                if new_bank_id:
                    bank_id = new_bank_id.id

            update_bank_account = bank_account.sudo().write({
                'bank_id': bank_id,
                'acc_number': kw.get('iban_no'),
                'acc_holder_name': kw.get('bank_account_title')
            })
            if update_bank_account:
                return 'success'

        else:
            print("in else")
            new_bank_id = request.env['res.bank'].sudo().create({
                'name': kw.get('bank_name')
            })
            if new_bank_id:
                values = {
                    'partner_id': current_user.partner_id.id,
                    'acc_number': kw.get('iban_no'),
                    'bank_id': new_bank_id.id,
                    'acc_holder_name': kw.get('bank_account_title'),
                }
                new_account = request.env['res.partner.bank'].sudo().create(values)
                if new_account:
                    response = current_user.employee_id.sudo().write({'bank_account_id': new_account.id})
                    if response:
                        return 'success'


class AddEmployeeDependents(http.Controller):
    @http.route('/employee/dependents', type='http', auth="user", csrf=False, website=True)
    def _submit_request(self, **kw):
        response = http.request.env['hr.employee.dependent'].sudo().create(kw)
        # print(response)
        return


class AddEmployeePersonalInfo(http.Controller):
    @http.route('/employee/personal/info', type='http', auth="user", csrf=False, website=True)
    def _submit_request(self, **kw):
        print(kw)
        # response = http.request.env['hr.employee.dependent'].sudo().create(kw)
        # print(response)
        # return


class AddEmployeeContactInfo(http.Controller):
    @http.route('/employee/contact_info', type='http', auth="user", csrf=False, website=True)
    def _submit_request(self, **kw):
        national_address_attachments = kw.get('national_address_attachments')
        national_address = base64.b64encode(national_address_attachments.read())
        rental_agreement_attachments = kw.get('rental_agreement_attachments')
        rental_agreement = base64.b64encode(rental_agreement_attachments.read())
        employee_id = kw.get('employee_id')
        values = {
            'primary_phone_no': kw.get('primary_mobile_no'),
            'secondary_phone_no': kw.get('secondary_mobile_no'),
            'emergency_phone': kw.get('emergency_phone'),
            'home_country_contact_number': kw.get('home_country_contact_number'),
            'private_email': kw.get('personal_email'),
            'home_country_cnic': kw.get('home_country_cnic'),
            'home_country_address': kw.get('home_country_address'),
            'national_address': national_address,
            'rental_agreement': rental_agreement,
        }
        employee_record = request.env['hr.employee'].sudo().search([('id', '=', employee_id)], limit=1)
        print("employee_record", employee_record)
        employee_record.sudo().write(values)
        # http.request.env['hr.employee'].sudo().create(values).record_id('record_id')
        return 'Record added successfully!'


class SubmitRequisitionRequest(http.Controller):
    @http.route('/submit/requisition/request', type='http', auth="user", csrf=False, website=True)
    def submit_requisition_request(self, **kw):
        print("KW", kw)
        current_user = request.env.user
        employee_info = request.env['hr.employee'].sudo().search([('user_id', '=', current_user.id)])
        computer_knowledge_ids = [int(x) for x in kw.get('computer_knowledge_ids', '').split(',') if x]
        language_ids = [int(x) for x in kw.get('language_ids', '').split(',') if x]
        education_ids = [int(x) for x in kw.get('education_ids', '').split(',') if x]
        attachment = kw.get('attachment')
        image = base64.b64encode(attachment.read())
        data = {
            'employee_id': employee_info.id,
            'position_request': kw.get('position_request'),
            'position_type': kw.get('position_type'),
            'employment_status': kw.get('employment_status'),
            'no_of_positions': kw.get('no_of_positions'),
            'monthly_basic_salary': kw.get('monthly_basic_salary'),
            'manager_id': kw.get('manager_id'),
            'required_position': kw.get('required_position'),
            'grade': kw.get('grade'),
            'expected_joining_date': kw.get('expected_joining_date'),
            'contract_duration': kw.get('contract_duration'),
            'nationality': kw.get('nationality'),
            'gender': kw.get('gender'),
            'budgeted': kw.get('budgeted'),
            'external_funds': kw.get('external_funds_id'),
            'purpose_of_position': kw.get('purpose_of_position'),
            'main_accountability': kw.get('main_accountability'),
            'computer_knowledge_ids': [(6, 0, computer_knowledge_ids)],
            'language_ids': [(6, 0, language_ids)],
            'education_ids': [(6, 0, education_ids)],
            'other_education': kw.get('other_education'),
            'other_languages': kw.get('other_languages'),
            'other_computer_skills': kw.get('other_computer_skills'),
            'experience': kw.get('experience'),
            'certificate1': kw.get('certificate1'),
            'certificate2': kw.get('certificate2'),
            'certificate3': kw.get('certificate3'),
            'office_space_available': kw.get('office_space_available'),
            'key_competencies': kw.get('key_competencies'),
            'attachment': image,
            'position_state': 'draft'

        }
        if not kw.get('space_availability'):
            data['space_availability'] = kw.get('space_availability')
            data['room_no'] = kw.get('room_no')
            data['building_name'] = kw.get('building_name')
            data['floor_no'] = kw.get('floor_no')
        request_id = http.request.env['job.request'].sudo().create(data)
        print("request_id", request_id)
        return
