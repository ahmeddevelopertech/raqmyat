$(document).ready(function() {
    // For sending messages (already implemented)
    $('#message_form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var messageContent = $('#message_content').val().trim(); // Trim to remove leading/trailing spaces

        // Validate the message content before submitting
        if (messageContent === "") {
            $('#message_error').text('Message cannot be empty'); // Show inline error
            showToast('Message cannot be empty!', 'error');
            return; // Prevent form submission if validation fails
        } else {
            $('#message_error').text(''); // Clear the error message if validation passes
        }

        var url = form.attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function(response) {
                var result = JSON.parse(response);
                if (result.success) {
                    showToast('Message sent successfully!', 'success');
                    $('#message_content').val(''); // Clear the textarea
                    addMessageToList(messageContent); // Add the new message to the list
                } else {
                    showToast('Error sending message: ' + result.error, 'error');
                }
            },
            error: function() {
                showToast('Error sending message. Please try again.', 'error');
            }
        });
    });

    // For uploading attachments
    $('#attachment_form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var attachmentInput = $('#attachment')[0]; // Get the file input element

        // Validate if the file is selected
        if (!attachmentInput.files.length) {
            showToast('Please select a file to upload!', 'error');
            return; // Prevent form submission if no file is selected
        }

        var formData = new FormData(form[0]); // Use FormData for file uploads
        var url = form.attr('action');

        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            contentType: false, // Set to false for file uploads
            processData: false, // Set to false for file uploads
            success: function(response) {
                // Assuming the server response is in JSON
                var result = JSON.parse(response);
                if (result.success) {
                    showToast('Attachment uploaded successfully!', 'success');
                    $('#attachment').val(''); // Clear the file input
                    addAttachmentToList(result.attachment_name); // Add the attachment to the list (if needed)
                } else {
                    showToast('Error uploading attachment: ' + result.error, 'error');
                }
            },
            error: function() {
                showToast('Error uploading attachment. Please try again.', 'error');
            }
        });
    });

    // Function to show toast messages (already implemented)
    function showToast(message, type) {
        var toast = $('<div class="toast" role="alert" aria-live="assertive" aria-atomic="true">')
            .append($('<div class="toast-body">').text(message))
            .addClass(type === 'success' ? 'bg-success text-white' : 'bg-danger text-white');

        $('#toast-container').append(toast);
        toast.toast({ delay: 3000 }).toast('show');

        setTimeout(function() {
            toast.remove();
        }, 3000);
    }

    // Function to dynamically add the uploaded attachment to the list (if applicable)
    function addAttachmentToList(attachmentName) {
        var newAttachment = $('<div class="o_portal_chatter_message">')
            .append($('<div class="o_portal_chatter_message_title">').append($('<span class="font-weight-bold">').text('Attachment')))
            .append($('<div class="o_portal_chatter_message_info">').text('Just now'))
            .append($('<div class="o_portal_chatter_message_content mt-2">').text(attachmentName));

        $('.o_portal_chatter_messages').prepend(newAttachment);
    }

    // For adding messages to the list (already implemented)
    function addMessageToList(messageContent) {
        var currentDate = new Date();
        var formattedDate = currentDate.toLocaleString();
        var currentUser = $('body').data('user-name') || 'Current User'; // Make sure to set this data attribute in your template

        var newMessage = $('<div class="o_portal_chatter_message">')
            .append($('<div class="o_portal_chatter_message_title">').append($('<span class="font-weight-bold">').text(currentUser)))
            .append($('<div class="o_portal_chatter_message_info">').text(formattedDate))
            .append($('<div class="o_portal_chatter_message_content mt-2">').html(messageContent));

        $('.o_portal_chatter_messages').prepend(newMessage);
    }
});






//$(document).ready(function() {
//    $('#message_form').on('submit', function(e) {
//        e.preventDefault();
//        var form = $(this);
//        var messageContent = $('#message_content').val().trim(); // Trim to remove leading/trailing spaces
//
//        // Validate the message content before submitting
//        if (messageContent === "") {
//            $('#message_error').text('Message cannot be empty'); // Show inline error
//            showToast('Message cannot be empty!', 'error');
//            return; // Prevent form submission if validation fails
//        } else {
//            $('#message_error').text(''); // Clear the error message if validation passes
//        }
//
//        var url = form.attr('action');
//        $.ajax({
//            type: "POST",
//            url: url,
//            data: form.serialize(),
//            success: function(response) {
//                var result = JSON.parse(response);
//                if (result.success) {
//                    showToast('Message sent successfully!', 'success');
//                    $('#message_content').val(''); // Clear the textarea
//                    addMessageToList(messageContent); // Add the new message to the list
//                } else {
//                    showToast('Error sending message: ' + result.error, 'error');
//                }
//            },
//            error: function() {
//                showToast('Error sending message. Please try again.', 'error');
//            }
//        });
//    });
//
//    function showToast(message, type) {
//        var toast = $('<div class="toast" role="alert" aria-live="assertive" aria-atomic="true">')
//            .append($('<div class="toast-body">').text(message))
//            .addClass(type === 'success' ? 'bg-success text-white' : 'bg-danger text-white');
//
//        $('#toast-container').append(toast);
//        toast.toast({ delay: 3000 }).toast('show');
//
//        setTimeout(function() {
//            toast.remove();
//        }, 3000);
//    }
//
//    function addMessageToList(messageContent) {
//        var currentDate = new Date();
//        var formattedDate = currentDate.toLocaleString();
//        var currentUser = $('body').data('user-name') || 'Current User'; // Make sure to set this data attribute in your template
//
//        var newMessage = $('<div class="o_portal_chatter_message">')
//            .append($('<div class="o_portal_chatter_message_title">').append($('<span class="font-weight-bold">').text(currentUser)))
//            .append($('<div class="o_portal_chatter_message_info">').text(formattedDate))
//            .append($('<div class="o_portal_chatter_message_content mt-2">').html(messageContent));
//
//        $('.o_portal_chatter_messages').prepend(newMessage);
//    }
//});