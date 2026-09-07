import {
    validateEmptyField,
    validateSelect,
    validateRadioField,
    getSelectedRadioValue,
    getSelectedCheckBoxes,
    validateCheckBoxField,
    validateAttachment,
    updateFileLabel,
    validateDate, validateSpecific
} from './validation_rules.js';
import {Toast} from "./swatToast.js";
import {disablePage} from "./overlay.js";

const requisitionRequestForm = document.getElementById('requisitionRequestForm');
const position_request = document.getElementsByName('position_request');
const position_type = document.getElementsByName('position_type');
const employment_status = document.getElementsByName('employment_status');
const no_of_positions = document.getElementById('no_of_positions');
const monthly_basic_salary = document.getElementById('monthly_basic_salary');
const line_manager = document.getElementById('line_manager');
const required_position = document.getElementById('required_position');
const grade = document.getElementById('grade');
const expected_joining_date = document.getElementById('expected_joining_date');
const contract_duration = document.getElementsByName('contract_duration');
const nationality = document.getElementsByName('nationality');
const gender = document.getElementsByName('gender');
const budgeted = document.getElementsByName('budgeted');
const external_funds_id = document.getElementById('external_funds_id');
const purpose_of_position = document.getElementById('purpose_of_position');
const main_accountability = document.getElementById('main_accountability');
const computer_knowledge = document.getElementsByName('computer_knowledge');
const other_computer_skills = document.getElementById('other_computer_skills');
const language = document.getElementsByName('language')
const education = document.getElementsByName('education')
const other_education = document.getElementById('other_education');
const other_languages = document.getElementById('other_languages');
const experience = document.getElementsByName('experience');
const certificate1 = document.getElementById('certificate1');
const competencies = document.getElementById('competencies');
const certificate2 = document.getElementById('certificate2');
const certificate3 = document.getElementById('certificate3');
const attachment = document.getElementById('attachment');
const office_space_available = document.getElementsByName('office_space_available');
const space_availability = document.getElementsByName('space_availability');
const room_no = document.getElementById('room_no');
const floor_no = document.getElementById('floor_no');
const building_name = document.getElementById('building_name');


requisitionRequestForm.addEventListener('submit', e => {
    e.preventDefault()
    console.log("in submit")
    validateRequisitionInput();
});

const validateRequisitionInput = () => {

    const validations = [
        validateRadioField(position_request),
        validateRadioField(position_type),
        validateRadioField(employment_status),
        validateRadioField(contract_duration),
        validateRadioField(nationality),
        validateRadioField(gender),
        validateRadioField(budgeted),
        validateRadioField(experience),
        validateCheckBoxField('education', 'error_education'),
        validateCheckBoxField('language', 'error_language'),
        validateCheckBoxField('computer_knowledge', 'error_computer_knowledge'),
        validateEmptyField(no_of_positions),
        validateSelect(line_manager),
        validateSelect(grade),
        validateRadioField(office_space_available),
        validateEmptyField(monthly_basic_salary),
        validateEmptyField(required_position),
        validateEmptyField(purpose_of_position),
        validateEmptyField(main_accountability),
        validateAttachment(attachment),
        validateDate(expected_joining_date)
    ];
    if (getSelectedRadioValue(budgeted) === 'external_funds') {
        validations.push(validateEmptyField(external_funds_id));
    }

    if (getSelectedRadioValue(office_space_available) === 'yes') {
        const spaceAvailabilityValid = validateSpecific(space_availability);
        validations.push(spaceAvailabilityValid);

        if (spaceAvailabilityValid && getSelectedRadioValue(space_availability) !== 'n_a') {
            validations.push(
                validateEmptyField(room_no),
                validateEmptyField(floor_no),
                validateEmptyField(building_name)
            );
        }
    }

    const allValid = validations.every(validationResult => validationResult);
    if (allValid) {
        if (getSelectedRadioValue(budgeted) === 'external_funds') {
            validateEmptyField(external_funds_id)
        }
        let formData = new FormData();

        formData.append('position_request', getSelectedRadioValue(position_request));
        formData.append('position_type', getSelectedRadioValue(position_type));
        formData.append('employment_status', getSelectedRadioValue(employment_status));
        formData.append('no_of_positions', no_of_positions.value);
        formData.append('monthly_basic_salary', monthly_basic_salary.value);
        formData.append('manager_id', line_manager.value);
        formData.append('required_position', required_position.value);
        formData.append('grade', grade.value);
        formData.append('expected_joining_date', expected_joining_date.value);
        formData.append('contract_duration', getSelectedRadioValue(contract_duration));
        formData.append('nationality', getSelectedRadioValue(nationality));
        formData.append('gender', getSelectedRadioValue(gender));
        formData.append('budgeted', getSelectedRadioValue(budgeted));
        formData.append('external_funds_id', external_funds_id.value);
        formData.append('purpose_of_position', purpose_of_position.value);
        formData.append('main_accountability', main_accountability.value);
        formData.append('computer_knowledge_ids', getSelectedCheckBoxes(computer_knowledge).join(','));
        formData.append('language_ids', getSelectedCheckBoxes(language).join(','));
        formData.append('education_ids', getSelectedCheckBoxes(education).join(','));
        formData.append('other_education', other_education.value);
        formData.append('other_languages', other_languages.value);
        formData.append('other_computer_skills', other_computer_skills.value);
        formData.append('experience', getSelectedRadioValue(experience));
        formData.append('certificate1', certificate1.value);
        formData.append('certificate2', certificate2.value);
        formData.append('certificate3', certificate3.value);
        formData.append('office_space_available', getSelectedRadioValue(office_space_available));
        formData.append('space_availability', getSelectedRadioValue(space_availability));
        formData.append('room_no', room_no.value);
        formData.append('floor_no', floor_no.value);
        formData.append('building_name', building_name.value);
        formData.append('key_competencies', competencies.value);

        formData.append('attachment', attachment.files[0]);
        //  for (let [key, value] of formData.entries()) {
        //         console.log(`${key}: ${value}`);
        //     }
        $.ajax({
            url: '/submit/requisition/request',
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
        // showToast("This is a toast message!");
    }

}
attachment.addEventListener('change', () => {
    updateFileLabel(attachment);
    validateAttachment(attachment);
});

position_request.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateRadioField(position_request);
    });
});
position_type.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateRadioField(position_type);
    });
});
employment_status.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateRadioField(employment_status);
    });
});
contract_duration.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateRadioField(contract_duration);
    });
});
nationality.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateRadioField(nationality);
    });
});
gender.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateRadioField(gender);
    });
});
budgeted.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateRadioField(budgeted);
    });
});
experience.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateRadioField(experience);
    });
});
office_space_available.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateRadioField(office_space_available);
    });
});
space_availability.forEach(function (radio) {
    radio.addEventListener('change', function () {
        validateSpecific(space_availability);
    });
});

purpose_of_position.addEventListener('input', function () {
    validateEmptyField(purpose_of_position)
});
main_accountability.addEventListener('input', function () {
    validateEmptyField(main_accountability)
});
monthly_basic_salary.addEventListener('input', function () {
    validateEmptyField(monthly_basic_salary)
});
no_of_positions.addEventListener('input', function () {
    validateEmptyField(no_of_positions)
});
required_position.addEventListener('input', function () {
    validateEmptyField(required_position)
});
expected_joining_date.addEventListener('input', function () {
    validateDate(expected_joining_date)
});
grade.addEventListener('input', function () {
    validateSelect(grade);
});
line_manager.addEventListener('input', function () {
    validateSelect(line_manager);
});

document.querySelectorAll('input[name="language"]').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        validateCheckBoxField('language', 'error_language');
    });
});
document.querySelectorAll('input[name="education"]').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        validateCheckBoxField('education', 'error_education');
    });
});
document.querySelectorAll('input[name="computer_knowledge"]').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        validateCheckBoxField('computer_knowledge', 'error_computer_knowledge');
    });
});


$('#request_date').datepicker({
    format: 'yyyy-mm-dd'
});
$('#request_expiry_date').datepicker({
    format: 'yyyy-mm-dd'
});
$('#expected_joining_date').datepicker({
    format: 'yyyy-mm-dd'
});
$('#expected_joining_date').datepicker().on('changeDate', function (e) {
    validateDate(expected_joining_date)
});

document.addEventListener('DOMContentLoaded', function () {
    const today = new Date()
    const todayDate = new Date().toISOString().split('T')[0];

    // Set the value of the input field
    const dateInput = document.getElementById('request_date');
    if (!dateInput.value) {
        dateInput.value = todayDate;
    }

    const futureDate = new Date(today);
    futureDate.setMonth(today.getMonth() + 6);
    const futureDateStr = futureDate.toISOString().split('T')[0];

    const request_expiry_date = document.getElementById('request_expiry_date');
    if (!request_expiry_date.value) {
        request_expiry_date.value = futureDateStr;
    }
});

