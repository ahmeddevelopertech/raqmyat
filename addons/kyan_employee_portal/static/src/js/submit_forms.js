import {
    validateContactNumber,
    validateCnic,
    validateEmail,
    validateAttachment,
    validateEmptyField,
    validateSelect,
    updateFileLabel, validateDate
} from './validation_rules.js';
import {Toast} from "./swatToast.js";
import {disablePage} from "./overlay.js";


//  CONTACT FORM SUBMISSION
const ContactForm = document.getElementById('contactForm');
const primary_mobile_no = document.getElementById('primary_mobile_no');
const secondary_mobile_no = document.getElementById('secondary_mobile_no');
const emergency_contact_number = document.getElementById('emergency_contact_number');
const personal_email = document.getElementById('personal_email');
const national_address_attachments = document.getElementById('national_address_attachments');
const rental_agreement_attachments = document.getElementById('rental_agreement_attachments');
const home_country_contact_number = document.getElementById('home_country_contact_number');
const home_country_address = document.getElementById('home_country_address');
const home_country_cnic = document.getElementById('home_country_cnic');
ContactForm.addEventListener('submit', e => {
    e.preventDefault();
    validateContactFormInputs();
});
//
const validateContactFormInputs = () => {
    const allValid = [
        validateContactNumber(primary_mobile_no),
        validateContactNumber(secondary_mobile_no),
        validateContactNumber(emergency_contact_number),
        validateContactNumber(home_country_contact_number),
        validateEmail(personal_email),
        validateCnic(home_country_cnic),
        validateAttachment(national_address_attachments),
        validateAttachment(rental_agreement_attachments),
        validateEmptyField(home_country_address),
    ].every(validationResult => validationResult);

    if (allValid) {
        let formData = new FormData();
        formData.append('employee_id', employee_id.value);
        formData.append('primary_mobile_no', primary_mobile_no.value);
        formData.append('secondary_mobile_no', secondary_mobile_no.value);
        formData.append('emergency_phone', emergency_contact_number.value);
        formData.append('home_country_contact_number', home_country_contact_number.value);
        formData.append('personal_email', personal_email.value);
        formData.append('home_country_cnic', home_country_cnic.value);
        formData.append('home_country_address', home_country_address.value);
        formData.append('national_address_attachments', national_address_attachments.files[0]);
        formData.append('rental_agreement_attachments', rental_agreement_attachments.files[0]);

        $.ajax({
            url: '/employee/contact_info',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response)
                window.location.reload();
                Toast.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Request submitted successfully"
                });
                disablePage();
                // console.log('Success:', response);
            },
            error: function (error) {
                Toast.fire({
                    position: "top-end",
                    icon: "error",
                    title: "An Error Occurred during submission try later "
                });
                // console.error('Error:', error);
            }
        });

    } else {
        Toast.fire({
            position: "top",
            icon: "error",
            title: "Please fill all required fields and retry"
        });
    }
};
primary_mobile_no.addEventListener('input', function () {
    validateContactNumber(primary_mobile_no);
});
secondary_mobile_no.addEventListener('input', function () {
    validateContactNumber(secondary_mobile_no);
});
emergency_contact_number.addEventListener('input', function () {
    validateContactNumber(emergency_contact_number);
});
home_country_contact_number.addEventListener('input', function () {
    validateContactNumber(home_country_contact_number);
});
personal_email.addEventListener('input', function () {
    validateEmail(personal_email);
});
home_country_cnic.addEventListener('input', function () {
    validateCnic(home_country_cnic);
});
home_country_address.addEventListener('input', function () {
    validateEmptyField(home_country_address);
});

national_address_attachments.addEventListener('change', () => {
    updateFileLabel(national_address_attachments);
    validateAttachment(national_address_attachments);
});
rental_agreement_attachments.addEventListener('change', () => {
    updateFileLabel(rental_agreement_attachments);
    validateAttachment(rental_agreement_attachments);
});


//  Qualification FORM SUBMISSION

const QualificationForm = document.getElementById('QualificationForm');
const qualification_degree = document.getElementById('qualification_degree');
const qualification_university = document.getElementById('qualification_university');
const qualification_year = document.getElementById('qualification_year');
const qualification_document_attachment = document.getElementById('qualification_document_attachment');

QualificationForm.addEventListener('submit', e => {
    e.preventDefault();
    validateQualificationFormInputs();
});

const validateQualificationFormInputs = () => {
    const allValid = [
        validateEmptyField(qualification_degree),
        validateEmptyField(qualification_university),
        validateAttachment(qualification_document_attachment),
    ].every(validationResult => validationResult);

    if (allValid) {
        let formData = new FormData();
        formData.append('employee_id', employee_id.value);
        formData.append('degree', qualification_degree.value);
        formData.append('university', qualification_university.value);
        formData.append('year', qualification_year.value);
        formData.append('attachment', qualification_document_attachment.files[0]);
        console.log('FormData:', formData);

        $.ajax({
            url: '/employee/qualification',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                // console.log(response)
                // window.location.reload();
                Toast.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Request submitted successfully"
                });
                disablePage();
                // console.log('Success:', response);
            },
            error: function (error) {
                Toast.fire({
                    position: "top-end",
                    icon: "error",
                    title: "An Error Occurred during submission try later "
                });
                // console.error('Error:', error);
            }
        });

    } else {
        Toast.fire({
            position: "top",
            icon: "error",
            title: "Please fill all required fields and retry"
        });

    }
};
qualification_degree.addEventListener('input', function () {
    validateEmptyField(qualification_degree);
});
qualification_university.addEventListener('input', function () {
    validateEmptyField(qualification_university);
});

qualification_document_attachment.addEventListener('change', () => {
    updateFileLabel(qualification_document_attachment)
    validateAttachment(qualification_document_attachment);
});


//  BANK FORM SUBMISSION

const bankForm = document.getElementById('bankForm')
const bank_account_title = document.getElementById('bank_account_title')
const bank_account_name = document.getElementById('bank_account_name')
const bank_iban_no = document.getElementById('bank_iban_no')


bankForm.addEventListener('submit', e => {
    e.preventDefault();
    validateBankFormInputs();
});

const validateBankFormInputs = () => {
    const allValid = [
        validateEmptyField(bank_account_name),
        validateEmptyField(bank_account_title),
    ].every(validationResult => validationResult);

    if (allValid) {
        let formData = new FormData();


        formData.append('employee_id', employee_id.value);
        formData.append('bank_name', bank_account_name.value);
        formData.append('bank_account_title', bank_account_title.value);
        formData.append('iban_no', bank_iban_no.value);

        $.ajax({
            url: '/employee/bank_details',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                // console.log(response)
                // window.location.reload();
                Toast.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Record  Inserted successfully"
                });
                disablePage();
                // console.log('Success:', response);
            },
            error: function (error) {
                Toast.fire({
                    position: "top-end",
                    icon: "error",
                    title: "An Error Occurred during submission try later "
                });
                // console.error('Error:', error);
            }
        });

    } else {
        Toast.fire({
            position: "top",
            icon: "error",
            title: "Please fill all required fields and retry"
        });

    }
};
bank_account_name.addEventListener('input', function () {
    validateEmptyField(bank_account_name);
});
bank_account_title.addEventListener('input', function () {
    validateEmptyField(bank_account_title);
});


// Contract FORM SUBMISSION

const contractForm = document.getElementById('contractForm');
const contract_type = document.getElementById('contract_type');
const contract_start_date = document.getElementById('contract_start_date');
const contract_end_date = document.getElementById('contract_end_date');

contractForm.addEventListener('submit', e => {
    e.preventDefault();
    validateContractFormInputs();
});

const validateContractFormInputs = () => {
    const allValid = [
        validateSelect(contract_type),

    ].every(validationResult => validationResult);

    if (allValid) {
        let formData = new FormData();
        formData.append('employee_id', employee_id.value);
        formData.append('contract_type_id', contract_type.value);
        formData.append('contract_start_date', contract_start_date.value);
        formData.append('contract_end_date', contract_end_date.value);
        console.log('FormData:', formData);

        $.ajax({
            url: '/employee/contract_info',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                Toast.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Request submitted successfully"
                });
                disablePage();
                // console.log('Success:', response);
            },
            error: function (error) {
                Toast.fire({
                    position: "top-end",
                    icon: "error",
                    title: "An Error Occurred during submission try later "
                });
                // console.error('Error:', error);
            }
        });
    } else {
        Toast.fire({
            position: "top",
            icon: "error",
            title: "Please fill all required fields and retry"
        });

    }
};
contract_type.addEventListener('select', function () {
    validateSelect(contract_type);
});


// EXPERIENCE FORM SUBMISSION

const experienceForm = document.getElementById('experienceForm')
const experience_job_company = document.getElementById('experience_job_company')
const experience_job_position = document.getElementById('experience_job_position')
const experience_job_type = document.getElementById('experience_job_type')
const experience_job_country = document.getElementById('experience_job_country')
const experience_date_form = document.getElementById('experience_date_form')
const experience_date_to = document.getElementById('experience_date_to')

experienceForm.addEventListener('submit', e => {
    e.preventDefault();
    validateExperienceFormInputs();
});

const validateExperienceFormInputs = () => {
        const allValid = [
            validateEmptyField(experience_job_company),
            validateEmptyField(experience_job_position),
            validateSelect(experience_job_country),
            validateSelect(experience_job_type),
            validateDate(experience_date_form),
            validateDate(experience_date_to),

        ].every(validationResult => validationResult);

        if (allValid) {
            let formData = new FormData();
            formData.append('employee_id', employee_id.value);
            formData.append('company_name', experience_job_company.value);
            formData.append('job_position', experience_job_position.value);
            formData.append('job_type', experience_job_type.value);
            formData.append('country_id', experience_job_country.value);
            formData.append('date_from', experience_date_form.value);
            formData.append('date_to', experience_date_to.value);
            console.log('FormData:', formData);

            $.ajax({
                    url: '/employee/experience',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (response) {

                        Toast.fire({
                            position: "top-end",
                            icon: "success",
                            title: "Request submitted successfully"
                        });
                        disablePage();
                        // window.location.reload();


                        //     setTimeout(1000)
                        // window.location.reload();
                        // console.log('Success:', response);
                    },
                    error: function (error) {
                        Toast.fire({
                            position: "top-end",
                            icon: "error",
                            title: "An Error Occurred during submission try later "
                        });
                        // console.error('Error:', error);
                    }
                }
            )
            ;
        } else {
            Toast.fire({
                position: "top",
                icon: "error",
                title: "Please fill all required fields and retry"
            });

        }
    }
;
experience_job_company.addEventListener('input', function () {
    validateEmptyField(experience_job_company);
});
experience_job_position.addEventListener('input', function () {
    validateEmptyField(experience_job_position);
});
experience_job_country.addEventListener('input', function () {
    validateSelect(experience_job_country);
});
experience_job_type.addEventListener('input', function () {
    validateSelect(experience_job_type);
});

// PERSONAL DETAILS FORM SUBMISSION


const personalDetailForm = document.getElementById('personalDetailForm');
const employee_name_english = document.getElementById('employee_name_english');
const employee_name_arabic = document.getElementById('employee_name_arabic');
const employee_grade = document.getElementById('employee_grade');
const job_position_english = document.getElementById('job_position_english');
const job_position_arabic = document.getElementById('job_position_arabic');
const reporting_manager = document.getElementById('reporting_manager');
const department_english = document.getElementById('department_english');
const department_arabic = document.getElementById('department_arabic');
const block = document.getElementById('block');
const employee_id = document.getElementById('employee_id');
const employee_type = document.getElementById('employee_type');
const unit = document.getElementById('unit');
const joining_date = document.getElementById('joining_date');
const contract_expiry = document.getElementById('contract_expiry');
const nationality = document.getElementById('nationality');
const passport_no = document.getElementById('passport_no');
const passport_expiry = document.getElementById('passport_expiry');
const marital_status = document.getElementById('marital_status');
const work_phone = document.getElementById('work_phone');
const work_email = document.getElementById('work_email');
const gender = document.getElementById('gender');
const national_id = document.getElementById('national_id');
const religion = document.getElementById('religion');
const children = document.getElementById('children');
const blood_group = document.getElementById('blood_group');

personalDetailForm.addEventListener('submit', e => {
    e.preventDefault();
    validatePersonalDetailsFormInputs();
});
const validatePersonalDetailsFormInputs = () => {
    const allValid = [
        validateEmptyField(employee_name_english),
        validateEmptyField(employee_name_arabic),
        validateEmptyField(employee_grade),
        validateEmptyField(job_position_english),
        validateEmptyField(job_position_arabic),
        validateEmptyField(reporting_manager),
        validateEmptyField(department_english),
        validateEmptyField(department_arabic),
        validateEmptyField(block),
        validateEmptyField(employee_id),
        validateEmptyField(employee_type),
        validateSelect(unit),
        validateEmptyField(joining_date),
        validateSelect(nationality),
        validateSelect(marital_status),
        validateSelect(gender),
        validateEmptyField(passport_no),
        validateEmptyField(passport_expiry),
        validateEmptyField(contract_expiry),
        validateContactNumber(work_phone),
        validateEmail(work_email),
        validateEmptyField(national_id),
        validateEmptyField(religion),
        validateEmptyField(children),
        validateEmptyField(blood_group)
    ].every(validationResult => validationResult);

    if (allValid) {
        console.log("All validations are done successfully!");

    } else {
        console.log("Please address any validation errors before submission.");

    }
};
employee_name_english.addEventListener('input', function () {
    validateEmptyField(employee_name_english);
});
employee_name_arabic.addEventListener('input', function () {
    validateEmptyField(employee_name_arabic);
});
employee_grade.addEventListener('input', function () {
    validateEmptyField(employee_grade);
});
job_position_english.addEventListener('input', function () {
    validateEmptyField(job_position_english);
});
job_position_arabic.addEventListener('input', function () {
    validateEmptyField(job_position_arabic);
});
reporting_manager.addEventListener('input', function () {
    validateEmptyField(reporting_manager);
});
department_english.addEventListener('input', function () {
    validateEmptyField(department_english);
});
department_arabic.addEventListener('input', function () {
    validateEmptyField(department_arabic);
});
block.addEventListener('input', function () {
    validateEmptyField(block);
});
employee_id.addEventListener('input', function () {
    validateEmptyField(employee_id);
});
employee_type.addEventListener('input', function () {
    validateEmptyField(employee_type);
});
// unit.addEventListener('input', function () {
//     validateSelect(unit);
// });
joining_date.addEventListener('input', function () {
    validateEmptyField(joining_date);
});
passport_no.addEventListener('input', function () {
    validateEmptyField(passport_no);
});
passport_expiry.addEventListener('input', function () {
    validateEmptyField(passport_expiry);
});
contract_expiry.addEventListener('input', function () {
    validateEmptyField(contract_expiry);
});
national_id.addEventListener('input', function () {
    validateEmptyField(national_id);
});
religion.addEventListener('input', function () {
    validateEmptyField(religion);
});
children.addEventListener('input', function () {
    validateEmptyField(children);
});
blood_group.addEventListener('input', function () {
    validateEmptyField(blood_group);
});
nationality.addEventListener('input', function () {
    validateSelect(nationality);
});
marital_status.addEventListener('input', function () {
    validateSelect(marital_status);
});
gender.addEventListener('input', function () {
    validateSelect(gender);
});

work_phone.addEventListener('input', function () {
    validateContactNumber(work_phone);
});
work_email.addEventListener('input', function () {
    validateEmail(work_email);
});

// DEPENDENT DETAILS SUBMISSION

const DependentsForm = document.getElementById('DependentsForm');
const dependent_name = document.getElementById('dependent_name');
const dependent_dob = document.getElementById('dependent_dob');
const dependent_relation = document.getElementById('dependent_relation');
const dependent_nationality = document.getElementById('dependent_nationality');
const dependent_passport = document.getElementById('dependent_passport');
const dependent_passport_expiry_date = document.getElementById('dependent_passport_expiry_date');
const dependent_ssn = document.getElementById('dependent_ssn');

DependentsForm.addEventListener('submit', e => {
    e.preventDefault();
    validateDependentFormInputs();
});

const validateDependentFormInputs = () => {
    const allValid = [
        validateEmptyField(dependent_name),
        // validateEmptyField(dependent_dob),
        validateEmptyField(dependent_relation),
        validateEmptyField(dependent_passport),
        // validateEmptyField(dependent_passport_expiry_date),
        validateEmptyField(dependent_ssn),
        validateSelect(dependent_nationality),
    ].every(validationResult => validationResult);

    if (allValid) {
        let formData = new FormData();
        formData.append('employee_id', employee_id.value);
        formData.append('name', dependent_name.value);
        formData.append('dob', dependent_dob.value);
        formData.append('relation', dependent_relation.value);
        formData.append('nationality', dependent_nationality.value);
        formData.append('passport_no', dependent_passport.value);
        formData.append('passport_expiry_date', dependent_passport_expiry_date.value);
        formData.append('ssn', dependent_ssn.value);
        console.log('FormData:', formData);

        $.ajax({
            url: '/employee/dependents',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response)
                Toast.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Request submitted successfully"
                });
                disablePage();
                // console.log('Success:', response);
            },
            error: function (error) {
                Toast.fire({
                    position: "top-end",
                    icon: "error",
                    title: "An Error Occurred during submission try later "
                });
                // console.error('Error:', error);
            }
        });

    } else {
        Toast.fire({
            position: "top",
            icon: "error",
            title: "Please fill all required fields and retry"
        });

    }
};

// for TAb NAV toggle

// document.querySelectorAll('.nav-link').forEach(function (link) {
//     link.addEventListener('click', function (event) {
//       var target = document.querySelector(this.getAttribute('href'));
//       var tabContent = target.closest('.tab-content');
//
//       tabContent.querySelectorAll('.tab-pane').forEach(function (pane) {
//         pane.classList.remove('show', 'active');
//       });
//
//       target.classList.add('show', 'active');
//
//       tabContent.previousElementSibling.querySelectorAll('.nav-link').forEach(function (nav) {
//         nav.classList.remove('active');
//       });
//
//       this.classList.add('active');
//     });
//   });


document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.scrollable-nav .nav-link');
    const tabContents = document.querySelectorAll('.tab-content .tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent default anchor behavior

            // Remove 'active' class from all tabs and tab content
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(tc => tc.classList.remove('active'));

            // Add 'active' class to the clicked tab
            tab.classList.add('show', 'active');

            // Show the associated content section
            const targetId = tab.getAttribute('href').substring(1);
            const targetContent = document.getElementById(targetId);

            if (targetContent) {
                targetContent.classList.add('show', 'active');

                // Scroll the navigation container to ensure the clicked tab is visible
                const navWrapper = document.querySelector('.scrollable-nav-wrapper');
                const tabRect = tab.getBoundingClientRect();
                const navWrapperRect = navWrapper.getBoundingClientRect();

                // Adjust the scroll position to keep the clicked tab centered
                const offset = tabRect.left - navWrapperRect.left - (navWrapperRect.width / 2) + (tabRect.width / 2);
                navWrapper.scrollLeft += offset;
            }
        });
    });

    // Optionally handle initial hash from URL
    const initialHash = window.location.hash;
    if (initialHash) {
        const initialTab = document.querySelector(`.scrollable-nav .nav-link[href="${initialHash}"]`);
        if (initialTab) {
            initialTab.click();
        }
    }
});


$(document).ready(function () {
    $('#joining_date').datepicker({
        format: 'yyyy-mm-dd'
    });
    $('#contract_expiry').datepicker({
        format: 'yyyy-mm-dd'
    });
    $('#passport_expiry').datepicker({
        format: 'yyyy-mm-dd'
    });
    // $('#experience_date_form').datepicker({format: 'yyyy-mm-dd'})
    $('#experience_date_form').datepicker({format: 'yyyy-mm-dd'})
        .on('changeDate', function (e) {
        validateDate(experience_date_form)
    });

    $('#experience_date_to').datepicker({format: 'yyyy-mm-dd'}).on('changeDate', function (e) {
        validateDate(experience_date_to)
    });
    $('#year').datepicker({
        format: 'yyyy-mm-dd'
    });
    $('#dependent_passport_expiry_date').datepicker({
        format: 'yyyy-mm-dd'
    });
    $('#qualification_year').datepicker({
        format: 'yyyy-mm-dd'
    });
    $('#dependent_dob').datepicker({
        format: 'yyyy-mm-dd'
    });
    $('#contract_start_date').datepicker({
        format: 'yyyy-mm-dd'
    });
    $('#contract_end_date').datepicker({
        format: 'yyyy-mm-dd'
    });

});

