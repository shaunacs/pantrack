'use strict';

function PickingUpForAnother(props) {
    return (
        <div>
            <label>Are they picking up for anyone else?</label>
            <input onClick={props.onTrueClick} type="radio" name="picking-up-for-another" value={props.pickup} defaultChecked></input>
            <label>Yes</label>
            <input onClick={props.onFalseClick} type="radio" name="picking-up-for-another" value={props.pickup}></input>
            <label>No</label><br></br>
            <label>Who are they picking up for?</label>
            <input type="text" name="pickup-for" id="pickup-for"></input><br></br>
        </div>
    )
}

function NotPickingUpForAnother(props) {
    return (
        <div>
            <label>Are they picking up for anyone else?</label>
            <input onClick={props.onTrueClick} type="radio" name="picking-up-for-another" value={props.pickup}></input>
            <label>Yes</label>
            <input onClick={props.onFalseClick} type="radio" name="picking-up-for-another" value={props.pickup} defaultChecked></input>
            <label>No</label><br></br>
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
            <label>First Name</label>
            <input type="text" name="fname"></input><br></br>
            <label>Last Name</label>
            <input type="text" name="lname"></input><br></br>
            <label>Number of people in household</label>
            <input type="number" name="num-people" required></input><br></br>
            <label>Do they want peanut butter?</label>
            <input type="radio" name="wants-peanut-butter"  value="True"></input>
            <label>Yes</label>
            <input type="radio" name="wants-peanut-butter" value="False"></input>
            <label>No</label><br></br>
            {pickupInput}
            <input type="text" name="allergies"></input>
            <label>Allergies</label><br></br>
            <input type="text" name="special-requests"></input>
            <label>Any special requests?</label><br></br>
            <input type="submit" name="submit"></input>
        </div>
    )
}


ReactDOM.render(
    <DisplayUserApptForm />,
    document.querySelector('#user-appt')
)