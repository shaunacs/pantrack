"use strict";

// Pop up that confirms the user wants to cancel their appointment
$('#cancel-appt').on('click', () => {
   
    location.href = "/handle-cancel-appt"
    
})

$('#log-out-button').on('click', () => {
    location.href = "/logout"
})