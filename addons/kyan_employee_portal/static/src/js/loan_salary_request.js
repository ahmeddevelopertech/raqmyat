import {
    validateEmptyField,
    validateSelect,
    validateDate,
    validateEmptyTextArea,
} from './validation_rules.js';
import { Toast } from "./swatToast.js";
import { disablePage } from "./overlay.js";

const loanSalaryRequestForm = document.getElementById('loanSalaryRequestForm');
const types = document.getElementById('types');
const loan_amount = document.getElementById('loan_amount');
const installment = document.getElementById('installment');
const details_notes = document.getElementById('details_notes');
const date = document.getElementById('date');

loanSalaryRequestForm.addEventListener('submit', e => {
    e.preventDefault();
    validateRequisitionInput();
});

const validateRequisitionInput = () => {
    const validations = [
        validateSelect(types),
        validateEmptyField(loan_amount),
        validateEmptyTextArea(details_notes),
        validateEmptyField(installment),
        validateDate(date), // Add this line
    ];
    const allValid = validations.every(validationResult => validationResult);
    if (allValid) {
        let formData = new FormData();
        formData.append('types', types.value);
        formData.append('loan_amount', loan_amount.value);
        formData.append('details_notes', details_notes.value);
        formData.append('installment', installment.value);
        formData.append('date', date.value);
        console.log(formData);
        $.ajax({
            url: '/portal_salary_loan_request_save',
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
types.addEventListener('change', () => validateSelect(types));
loan_amount.addEventListener('input', () => validateEmptyField(loan_amount));
installment.addEventListener('input', () => validateEmptyField(installment));
details_notes.addEventListener('input', () => validateEmptyTextArea(details_notes));
date.addEventListener('change', () => validateDate(date));