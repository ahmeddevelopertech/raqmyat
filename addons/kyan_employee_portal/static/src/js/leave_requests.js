import {
    validateEmptyTextArea,
    validateSelect,
    validateAttachment,
    validateDate,
    updateFileLabel,
    setError,
    setSuccess
} from './validation_rules.js';
import {Toast} from "./swatToast.js";
import {disablePage} from "./overlay.js";

const leaveRequestForm = document.getElementById('leaveRequestForm');
const leave_type = document.getElementById('leave_type');
const leave_document_attachment = document.getElementById('leave_document_attachment');
const leave_date_form = document.getElementById('leave_date_form');
const leave_date_to = document.getElementById('leave_date_to');
const leave_description = document.getElementById('leave_description');
leaveRequestForm.addEventListener('submit', e => {
    e.preventDefault()

    validateLeaveRequestInputs();
});


const validateLeaveRequestInputs = () => {
    const allValid = [
        validateSelect(leave_type),
        validateDate(leave_date_form),
        validateDate(leave_date_to),
        validateAttachment(leave_document_attachment),
        validateEmptyTextArea(leave_description),
    ].every(validationResult => validationResult);

    if (allValid) {
        let formData = new FormData();
        formData.append('leave_type', leave_type.value);
        formData.append('leave_date_form', leave_date_form.value);
        formData.append('leave_date_to', leave_date_to.value);
        formData.append('leave_document_attachment', leave_document_attachment.files[0]);
        formData.append('leave_description', leave_description.value);

        $.ajax({
            url: '/employee/leave_request/save',
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
            error: function (xhr) {
                if (xhr.status === 400) {
                    // Display overlapping leave message
                    Toast.fire({
                        position: "top-end",
                        icon: "error",
                        title: xhr.responseText
                    });
                } else {
                    // Generic error message
                    Toast.fire({
                        position: "top-end",
                        icon: "error",
                        title: "An Error Occurred during submission, try again later"
                    });
                }
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

leave_document_attachment.addEventListener('change', () => {
    updateFileLabel(leave_document_attachment);
    validateAttachment(leave_document_attachment);
});
leave_description.addEventListener('input', () => validateEmptyTextArea(leave_description));
leave_date_form.addEventListener('change', () => validateDate(leave_date_form));
leave_date_to.addEventListener('change', () => validateDate(leave_date_to));


