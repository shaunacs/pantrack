'use strict';

function PickingUpForAnother(props) {
    return (
        <div>
            <label class="form-label">Are you picking up for anyone else?</label>
            <input class="form-check-input" onClick={props.onTrueClick} type="radio" name="picking-up-for-another" value={props.pickup} defaultChecked></input>
            <label class="form-check-label">Yes</label>
            <input class="form-check-input" onClick={props.onFalseClick} type="radio" name="picking-up-for-another" value={props.pickup}></input>
            <label class="form-check-label">No</label><br></br>
            <label class="form-label">Who are you picking up for?</label>
            <input class="form-control" type="text" name="pickup-for" id="pickup-for"></input><br></br>
        </div>
    )
}

function NotPickingUpForAnother(props) {
    return (
        <div>
            <label class="form-label">Are you picking up for anyone else?</label>
            <input class="form-check-input" onClick={props.onTrueClick} type="radio" name="picking-up-for-another" value={props.pickup}></input>
            <label class="form-check-label">Yes</label>
            <input class="form-check-input" onClick={props.onFalseClick} type="radio" name="picking-up-for-another" value={props.pickup} defaultChecked></input>
            <label class="form-check-label">No</label><br></br>
        </div>
    )
}

function DisplayHouseholdForm() {

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
            <label class="form-label">Number of people in household</label><br></br>
            <input class="form-control" type="number" name="num-people" required></input>
            <label class="form-label">Would you like peanut butter?</label>
            <input class="form-check-input" type="radio" name="wants-peanut-butter"  value="True"></input>
            <label class="form-check-label">Yes</label>
            <input class="form-check-input" type="radio" name="wants-peanut-butter" value="False"></input>
            <label class="form-check-label">No</label><br></br>
            {pickupInput}
            <label class="form-label">Allergies</label><br></br>
            <input class="form-control" type="text" name="allergies"></input><br></br>
            <label class="form-label">Any special requests?</label><br></br>
            <input class="form-control" type="text" name="special-requests"></input><br></br>
            <input type="submit" name="submit"></input>
        </div>
    )
}


ReactDOM.render(
    <DisplayHouseholdForm />,
    document.querySelector('#household-info')
)