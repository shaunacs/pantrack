'use strict';

function PickingUpForAnother() {
    function alertMessage() {
        alert('Radio button has changed');
    }

    return (
        <div>
            <i>Are you picking up for anyone else?</i>
            <input onClick={alertMessage} type="radio" name="picking-up-for-another" value="True"></input>
            <label>Yes</label>
            <input type="radio" name="picking-up-for-another" value="False"></input>
            <label>No</label>
        </div>
    );
}

ReactDOM.render(
    <PickingUpForAnother />,
    document.querySelector('#pickup')
)

