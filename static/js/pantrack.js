"use strict";

$('#cancel-appt').on('click', () => {
    if (confirm('Are you sure you want to cancel this appointment?')) {
        const cancel = True;
    } else {
        const cancel = False;
    }

    if (cancel === True) {
        $.post('/handle-cancel-appt')
    } else {
        $.get('/')
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