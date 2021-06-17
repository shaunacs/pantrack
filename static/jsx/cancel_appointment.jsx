'use strict';

function CancelAppointment() {
    function alertMessage() {
        alert('You just clicked a button');
    }

    return (
        <button onClick={alertMessage}>
            <i>Click to cancel appointment</i>
        </button>
    )
}