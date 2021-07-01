'use strict';

function PickingUpForAnother(props) {
    return (
        <div>
            <label class="form-label">Are you picking up for anyone else?</label>
            <input onClick={props.onTrueClick} type="radio" name="picking-up-for-another" value={props.pickup} defaultChecked></input>
            <label class="form-label">Yes</label>
            <input onClick={props.onFalseClick} type="radio" name="picking-up-for-another" value={props.pickup}></input>
            <label class="form-label">No</label><br></br>
            <label class="form-label">Who are you picking up for?</label>
            <input type="text" name="pickup-for" id="pickup-for"></input><br></br>
        </div>
    )
}

function NotPickingUpForAnother(props) {
    return (
        <div>
            <label class="form-label">Are you picking up for anyone else?</label>
            <input onClick={props.onTrueClick} type="radio" name="picking-up-for-another" value={props.pickup}></input>
            <label class="form-label">Yes</label>
            <input onClick={props.onFalseClick} type="radio" name="picking-up-for-another" value={props.pickup} defaultChecked></input>
            <label class="form-label">No</label><br></br>
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
            <div class="row">
                <div class="col-lg-5">
                    <label class="form-label">Number of people in household</label>
                </div>
                <div class="col-lg-3">
                    <input class="form-control" type="number" name="num-people" required></input>
                </div>
            </div>
            <label class="form-label">Would you like peanut butter?</label>
            <input type="radio" name="wants-peanut-butter"  value="True"></input>
            <label class="form-label">Yes</label>
            <input type="radio" name="wants-peanut-butter" value="False"></input>
            <label class="form-label">No</label><br></br>
            {pickupInput}
            <input type="text" name="allergies"></input>
            <label class="form-label">Allergies</label><br></br>
            <input type="text" name="special-requests"></input>
            <label class="form-label">Any special requests?</label><br></br>
            <input type="submit" name="submit"></input>
        </div>
    )
}


ReactDOM.render(
    <DisplayHouseholdForm />,
    document.querySelector('#household-info')
)