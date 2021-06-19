'use strict';

// function AnotherPickup(props) {

// }


function PickingUpForAnother() {
    function promptMessage() {
        const pickupName = prompt('Who are you picking up for?');
        return pickupName
    }

    const [anotherPickup, handleAnotherPickup] = React.useState('False');
    const [isHidden, handleHiddenInput] = React.useState("True");

    function truePickup() {
        handleAnotherPickup('True');
        handleHiddenInput('False');
    }

    function falsePickup() {
        handleAnotherPickup('False');
    }


    return (
        <div>
            <input type="number" name="num-people" required></input>
            <label>Number of people in household</label><br></br>
            <label>Would you like peanut butter?</label>
            <input type="radio" name="wants-peanut-butter"  value="True"></input>
            <label>Yes</label>
            <input type="radio" name="wants-peanut-butter" value="False"></input>
            <label>No</label><br></br>
            <label>Are you picking up for anyone else?</label>
            <input onClick={truePickup} type="radio" name="picking-up-for-another" value={anotherPickup}></input>
            <label>Yes</label>
            <input onClick={falsePickup} type="radio" name="picking-up-for-another" value={anotherPickup}></input>
            <label>No</label><br></br>
            <input type="text" name="pickup-for" hidden={isHidden}></input>
            <input type="text" name="allergies"></input>
            <label>Allergies</label><br></br>
            <input type="text" name="special-requests"></input>
            <label>Any special requests?</label><br></br>
            <input type="submit" name="submit"></input>
        </div>
    );
}

ReactDOM.render(
    <PickingUpForAnother />,
    document.querySelector('#household-info')
)

