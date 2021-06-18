'use strict';

// function AnotherPickup(props) {

// }


function PickingUpForAnother(props) {
    function promptMessage() {
        const pickupName = prompt('Who are you picking up for?');
        console.log(props.anotherPickup)
        return pickupName
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
            <input onClick={promptMessage} type="radio" name="picking-up-for-another" value="True"></input>
            <label>Yes</label>
            <input type="radio" name="picking-up-for-another" value="False"></input>
            <label>No</label><br></br>
            <input type="text" name="allergies"></input>
            <label>Allergies</label><br></br>
            <input type="text" name="special-requests"></input>
            <label>Any special requests?</label><br></br>
            <input type="submit" name="submit"></input>
        </div>
    );
}

ReactDOM.render(
    <PickingUpForAnother anotherPickup="False"/>,
    document.querySelector('#household-info')
)

