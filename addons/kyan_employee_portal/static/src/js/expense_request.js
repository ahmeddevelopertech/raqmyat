import {
    validateEmptyField,
    validateSelect,
    validateRadioField,
    getSelectedRadioValue,
    getSelectedCheckBoxes,
    validateCheckBoxField,
    updateFileLabel,
    validateSpecific
} from './validation_rules.js';
import { Toast } from "./swatToast.js";
import { disablePage } from "./overlay.js";

const expenseRequestForm = document.getElementById('expenseRequestForm');
const product = document.getElementById('product');
const quantity = document.getElementById('quantity');
const bill_reference = document.getElementById('bill_reference');
const unit_price = document.getElementById('unit_price');
const expense_date = document.getElementById('expense_date');
const leave_document_attachment = document.getElementById('leave_document_attachment');

expenseRequestForm.addEventListener('submit', e => {
    e.preventDefault();
    validateRequisitionInput();
});

const validateRequisitionInput = () => {
    const validations = [
        validateSelect(product),
        validateEmptyField(quantity),
        validateEmptyField(bill_reference),
        validateEmptyField(unit_price),
    ];
    const allValid = validations.every(validationResult => validationResult);
    if (allValid) {
        let formData = new FormData();
        formData.append('product', product.value); // Use .value for input fields
        formData.append('quantity', quantity.value); // Use .value for input fields
        formData.append('bill_reference', bill_reference.value); // Use .value for input fields
        formData.append('unit_price', unit_price.value); // Use .value for input fields
        formData.append('expense_date', expense_date.value); // Use .value for date input
        formData.append('leave_document_attachment', leave_document_attachment.files[0]);
//        alert(formData)
        console.log(formData)
        $.ajax({
        url: '/portal_expense_request_save',
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
product.addEventListener('change', () => validateSelect(product));
quantity.addEventListener('input', () => validateEmptyField(quantity));
bill_reference.addEventListener('input', () => validateEmptyField(bill_reference));
unit_price.addEventListener('input', () => validateEmptyField(unit_price));
//expense_date.addEventListener('input', () => validateDate(expense_date));
//attachment.addEventListener('change', () => {
//    updateFileLabel(attachment);
//    validateAttachment(attachment);
//});


