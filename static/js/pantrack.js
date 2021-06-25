"use strict";

// Pop up that confirms the user wants to cancel their appointment
$('#cancel-appt').on('click', () => {
   
    location.href = "/handle-cancel-appt"
    
})

// Alert that tells admin their selected appointments have been deleted
$('#delete-appt-slot').on('click', () => {

    alert('The appointment slot(s) selected have been deleted');
})
