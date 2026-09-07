import {
    validateEmptyField,
    validateSelect,
    validateDate,
    validateEmptyTextArea,
} from './validation_rules.js';
import { Toast } from "./swatToast.js";
import { disablePage } from "./overlay.js";

const accidentRequestForm = document.getElementById('accidentRequestForm');
const incident_type = document.getElementById('incident_type');
const type_of_inquiry = document.getElementById('type_of_inquiry');
const hospital = document.getElementById('hospital');
const occupation = document.getElementById('occupation');
const wiba = document.getElementById('wiba');
const sick = document.getElementById('sick');
const time_location = document.getElementById('time_location');
const witnesses = document.getElementById('witnesses');
const details_notes = document.getElementById('details_notes');
const date_of_accident = document.getElementById('date_of_accident');
const date_of_resumption = document.getElementById('date_of_resumption');
const date_of_reporting = document.getElementById('date_of_reporting');
const accident_document_attachment = document.getElementById('accident_document_attachment');

accidentRequestForm.addEventListener('submit', e => {
    e.preventDefault();
    validateRequisitionInput();
});

const validateRequisitionInput = () => {
    const validations = [
        validateSelect(incident_type),
        validateEmptyField(hospital),
        validateEmptyTextArea(details_notes),
        validateEmptyField(sick),
        validateEmptyField(time_location),
        validateDate(date_of_accident),
        validateDate(date_of_resumption),
        validateDate(date_of_reporting),
    ];
    const allValid = validations.every(validationResult => validationResult);
    if (allValid) {
        let formData = new FormData();
        formData.append('incident_type', incident_type.value);
        formData.append('type_of_inquiry', type_of_inquiry.value);
        formData.append('hospital', hospital.value);
        formData.append('details_notes', details_notes.value);
        formData.append('occupation', occupation.value);
        formData.append('wiba', wiba.value);
        formData.append('sick', sick.value);
        formData.append('time_location', time_location.value);
        formData.append('witnesses', witnesses.value);
        formData.append('date_of_accident', date_of_accident.value);
        formData.append('date_of_resumption', date_of_resumption.value);
        formData.append('date_of_reporting', date_of_reporting.value);
        formData.append('accident_document_attachment', accident_document_attachment.files[0]);
//        alert(formData)
        console.log(formData)
        $.ajax({
        url: '/portal_accident_request_save',
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
        },
        error: function (error) {
            Toast.fire({
                position: "top-end",
                icon: "error",
                title: "An Error Occurred during submission try later "
            });
        }
    });
    } else {
        Toast.fire({
            position: "top",
            icon: "error",
            title: "Please fill all required fields and retry"
        });
    }
}

// Add event listeners for real-time validation
incident_type.addEventListener('change', () => validateSelect(incident_type));
type_of_inquiry.addEventListener('change', () => validateSelect(type_of_inquiry));
hospital.addEventListener('input', () => validateEmptyField(hospital));
details_notes.addEventListener('input', () => validateEmptyTextArea(details_notes));
sick.addEventListener('input', () => validateEmptyField(sick));
time_location.addEventListener('input', () => validateEmptyField(time_location));
date_of_accident.addEventListener('change', () => validateDate(date_of_accident));
date_of_resumption.addEventListener('change', () => validateDate(date_of_resumption));
date_of_reporting.addEventListener('change', () => validateDate(date_of_reporting));
incident_type.addEventListener('input', function () {
    validateSelect(incident_type);
});
