const setError = (element, message) => {
    // console.log(element);
    // console.log(message);
    const inputControl = element.parentElement;
    // console.log(inputControl);
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success')
}
const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};

const validateEmptyTextArea = (element) => {
    const elementParent = element.parentElement;
    const errorDisplay = elementParent.querySelector('.error');
    const message = "This field is required";
    if (element.value) {
        errorDisplay.innerText = '';
        element.classList.add('success');
        element.classList.remove('error-date');
        return true;
    } else {
        errorDisplay.innerText = message;
        element.classList.add('error-date');
        element.classList.remove('success');
        return false;
    }

}

const EmailRegex = email => {
//     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//
// const isValidEmail = (email) => {
//   return emailRegex.test(email);
// };
    const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return emailRegex.test(email);
}

const CnicRegex = cnic => {
    // Regular expression to match CNIC format: nnnnn-nnnnnnn-n
    const cnicRegex = /^[0-9]{5}-[0-9]{7}-[0-9]$/;

    return cnicRegex.test(cnic);
};

const validateEmail = (element) => {
    const value = element.value.trim();
    if (value === '') {
        setError(element, 'Email is Required');
        return false;
    } else if (!EmailRegex(value)) {
        setError(element, 'Provide a valid email address');
        return false;
    } else {
        setSuccess(element);
        return true;
    }
}

const validateCnic = (element) => {
    const value = element.value.trim();
    if (value === '') {
        setError(element, 'Cnic is Required');
        return false;
    } else if (!CnicRegex(value)) {
        setError(element, 'Provide a valid cnic number');
        return false;
    } else {
        setSuccess(element);
        return true;
    }
}
const ContactNumberRegix = contactNumber => {
    // Regular expression to allow digits, hyphens, and spaces
    const contactNumberRegex = /^[\d- ]+$/;

    return contactNumberRegex.test(contactNumber);
};
const validateContactNumber = (element) => {
    const value = element.value.trim();

    if (value === '') {
        // console.log("in secondary_mobile_no error")
        setError(element, 'Number is Required');
        return false;
    } else if (!ContactNumberRegix(value)) {

        setError(element, 'Provide a valid contact number');
        return false;
    } else {

        setSuccess(element);
        return true;
    }
}
const setErrorAttachment = (element, message) => {
    const inputControl = element.parentElement;
    const superParent = inputControl.parentElement;
    const errorDisplay = superParent.querySelector('.error');

    errorDisplay.innerText = message;
    superParent.classList.add('attachment-error');
    superParent.classList.remove('attachment-success');

}

const setSuccessAttachment = element => {
    const inputControl = element.parentElement;
    const superParent = inputControl.parentElement;
    const errorDisplay = superParent.querySelector('.error');

    errorDisplay.innerText = '';
    superParent.classList.add('attachment-success');
    superParent.classList.remove('attachment-error');
};
const validateAttachment = (element) => {

    const files = element.files;

    // Check if files are selected
    if (!files || files.length === 0) {
        // console.log("in 1!FILE")
        setErrorAttachment(element, 'Please select a file');
        return false;
        // alert('Please select a file.');
        // // return false;
    } else {
        setSuccessAttachment(element)
        return true;
    }


}
//const validateDate = (element) => {
//    const date = element.value;
//    // console.log("in date wala");
//
//    const parentElement = element.parentElement;
//    // console.log("parentElement", parentElement);
//    const Sibling = parentElement.nextElementSibling;
//    // console.log("Sibling", Sibling);
//
//    if (!date) {
//        Sibling.innerText = 'Please select a date';
//        element.classList.add('error-date');
//        return false;
//    }
//
//    let inputDate = new Date(date);
//    let today = new Date(); // Get today's date
//
//    today.setHours(0, 0, 0, 0);
//    inputDate.setHours(0, 0, 0, 0);
//
//    if (inputDate < today) {
//        Sibling.innerText = 'Date cannot be earlier than today';
//        element.classList.add('error-date');
//
//        return false;
//    } else {
//        // Clear the error message and return true
//        Sibling.innerText = '';
//        element.classList.remove('error-date');
//        return true;
//    }
//};
//
//const setDateError = (element, message) => {
//
//}
//const setDateSuccess = (element, message) => {
//
//}

function updateFileLabel(inputElement) {
    const fileLabel = inputElement.nextElementSibling;
    const files = inputElement.files;
    if (files.length > 0) {
        fileLabel.textContent = files[0].name;
    } else {
        fileLabel.textContent = 'Choose file ...';
    }
}

const validateEmptyField = element => {
    // console.log(element)
    const value = element.value.trim();
    // console.log(value)
    if (value === '') {
        setError(element, 'This field is required');
        return false;
    } else {
        setSuccess(element);
        return true;
    }
}

const setErrorSelect = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('errorSelect');
    inputControl.classList.remove('successSelect')
}
const setSuccessSelect = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('successSelect');
    inputControl.classList.remove('errorSelect');
};
const validateSelect = element => {
    const value = element.value.trim();

    if (value === '') {
        setErrorSelect(element, 'Please select a value');
        return false;
    } else {
        setSuccessSelect(element);
        return true;
    }
}


const validateRadioField = element => {
    const firstElement = element[0];
    // console.log(firstElement.value)
    const parentElement = firstElement.parentElement;
    const superParent = parentElement.parentElement;
    console.log("superParent", superParent)
    // console.log(superParent);
    const errorDisplay = superParent.querySelector('.error');
    console.log("errorDisplay", errorDisplay)
    let message = "Please select one of these options"
    // errorDisplay.innerText = message;
    let hasValue;

    for (let radioButton of element) {
        if (radioButton.checked) {
            // console.log(radioButton.value);
            errorDisplay.innerText = '';
            hasValue = radioButton.value;
            break;
        }

    }
    if (hasValue) {
        return true
    } else {
        errorDisplay.innerText = message;
        return false
    }
}


const getSelectedRadioValue = (element) => {
    // var experienceOptions = document.getElementsByName('experience');

    for (var i = 0; i < element.length; i++) {
        if (element[i].checked) {
            // console.log("getSelectedCheckBoxValue", element[i].value)
            return element[i].value;
        }
    }

    return null;
}


const getSelectedCheckBoxes = (element) => {
    let selectedValues = [];


    for (var i = 0; i < element.length; i++) {
        if (element[i].checked) {
            selectedValues.push(element[i].value)
        }
    }
    // console.log("getSelectedCheckBoxes", selectedValues)
    return selectedValues;
}

const validateSpecific = (element) => {
    // const superParent = parentElement.parentElement
    const errorDisplay = document.querySelector('.error_space_availability');
    const message = "Please select at least one option";
    let hasValue;

    for (let radioButton of element) {
        if (radioButton.checked) {
            errorDisplay.innerText = '';
            hasValue = radioButton.value;
            break;
        }

    }
    if (hasValue) {
        return true
    } else {
        errorDisplay.innerText = message;
        return false
    }


}

const validateCheckBoxField = (fieldName, errorClass) => {
    const errorDisplay = document.querySelector(`.${errorClass}`);
    // console.log(errorDisplay)

    const message = "Please select at least one option";
    const checkboxes = document.querySelectorAll(`input[name="${fieldName}"]:checked`);


    if (checkboxes.length > 0) {
        errorDisplay.innerText = '';
        return true;
    } else {
        errorDisplay.innerText = message;
        return false;
    }
}

const validateDate = (element) => {
    const value = element.value.trim();
    const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format

    if (value === '') {
        setError(element, 'Date is required');
        return false;
    } else if (value < today) {
        setError(element, 'Date cannot be in the past');
        return false;
    } else {
        setSuccess(element);
        return true;
    }
};


export {
    validateContactNumber,
    validateCnic,
    validateEmail,
    validateAttachment,
    validateEmptyField,
    validateSelect,
    validateRadioField,
    getSelectedRadioValue,
    getSelectedCheckBoxes,
    validateSpecific,
    validateCheckBoxField,
    updateFileLabel,
    validateDate,
    validateEmptyTextArea,
    setError,setSuccess
}