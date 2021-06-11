"use strict";

$('#cancel-appt').on('click', () => {
    const cancel = confirm('Are you sure you want to cancel this appointment?');

    if (cancel) {
        alert("Your appointment has been cancelled")
        location.href = "/handle-cancel-appt"
    }
})


// $('#create-account').on('click', (evt) => {

//     const accountInfo = {
//         'fname': $('input[name="fname"]'),
//         'lname': $('input[name="lname"]'),
//         'email': $('input[name="email"]'),
//         'username': $('input[name="usernmae"]'),
//         'password': $('input[name="password"]'),
//         'phone_number': $('input[name="phone-number"]')
//     }
//     $.post('/handle-create-account', accountInfo, (res) => {
//         alert(res)
//     })
// })