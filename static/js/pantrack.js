"use strict";

// Pop up that confirms the user wants to cancel their appointment
$('#cancel-appt').on('click', () => {
    const cancel = confirm('Are you sure you want to cancel this appointment?');

    if (cancel) {
        alert("Your appointment has been cancelled")
        location.href = "/handle-cancel-appt"
    }
})

// Alert that tells admin their selected appointments have been deleted
$('#delete-appt-slot').on('click', () => {

    alert('The appointment slot(s) selected have been deleted');
})


// Collects name of person picking up for when yes is selected on household form
$(document).ready(function(){
    $('.picking-up').change(function(){
        alert('Radio button has changed');
    })
})