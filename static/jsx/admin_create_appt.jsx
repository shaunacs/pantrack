'use strict';

function PickingUpForAnother(props) {
    return (
        <div>
            <label class="form-label">Are they picking up for anyone else?</label>
            <input class="form-check-input" onClick={props.onTrueClick} type="radio" name="picking-up-for-another" value={props.pickup} defaultChecked></input>
            <label class="form-check-label">Yes</label>
            <input class="form-check-input" onClick={props.onFalseClick} type="radio" name="picking-up-for-another" value={props.pickup}></input>
            <label class="form-check-label">No</label><br></br>
            <label class="form-label">Who are they picking up for?</label>
            <input class="form-control" type="text" name="pickup-for" id="pickup-for"></input><br></br>
        </div>
    )
}

function NotPickingUpForAnother(props) {
    return (
        <div>
            <label class="form-label">Are they picking up for anyone else?</label>
            <input class="form-check-input" onClick={props.onTrueClick} type="radio" name="picking-up-for-another" value={props.pickup}></input>
            <label class="form-check-label">Yes</label>
            <input class="form-check-input" onClick={props.onFalseClick} type="radio" name="picking-up-for-another" value={props.pickup} defaultChecked></input>
            <label class="form-check-label">No</label><br></br>
        </div>
    )
}


function DisplayUserApptForm() {

    const [anotherPickup, handleAnotherPickup] = React.useState(false);

    function truePickup() {
        handleAnotherPickup(true);
    }

    function falsePickup() {
        handleAnotherPickup(false);
    }

    let pickupInput;
    if (anotherPickup) {
        pickupInput = <PickingUpForAnother onFalseClick={falsePickup} onClick={truePickup} pickup={anotherPickup} />;
    } else {
        pickupInput = <NotPickingUpForAnother onFalseClick={falsePickup} onTrueClick={truePickup} pickup={anotherPickup} />;
    }

    return (
        <div>
            <label class="form-label">First Name</label>
            <input class="form-control form-control-sm" type="text" name="fname" required></input><br></br>
            <label class="form-label">Last Name</label>
            <input class="form-control form-control-sm" type="text" name="lname" required></input><br></br>
            <label class="form-label">Phone Number</label>
            <input class="form-control form-control-sm" type="tel" id="phone-number" name="phone-number" pattern="[0-9]{10}"></input><br></br>
            <small>Format: 1234567890</small><br></br>
            <label class="form-label">Number of people in household</label>
            <input class="form-control" type="number" name="num-people" required></input><br></br>
            <label class="form-label">Do they want peanut butter?</label>
            <input class="form-check-input" type="radio" name="wants-peanut-butter"  value="True"></input>
            <label class="form-check-label">Yes</label>
            <input class="form-check-input" type="radio" name="wants-peanut-butter" value="False"></input>
            <label class="form-check-label">No</label><br></br>
            {pickupInput}
            <label class="form-label">Allergies?</label><br></br>
            <input class="form-control" type="text" name="allergies"></input><br></br>
            <label class="form-label">Any special requests?</label><br></br>
            <input class="form-control" type="text" name="special-requests"></input><br></br>
            <input class="btn btn-lg" type="submit" name="submit"></input>
        </div>
    )
}


ReactDOM.render(
    <DisplayUserApptForm />,
    document.querySelector('#user-appt')
)